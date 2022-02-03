#\ This is the file to set the routine to wake the Heroku up since in the free version, it'll sleep if there is no action occcurred
#\ also put the daily update for the dragonfly info here in set schedule
#\ ref: https://ithelp.ithome.com.tw/articles/10218874
from apscheduler.schedulers.blocking import BlockingScheduler
import index
import datetime
from VarIndex import cache
import random
import DragonflyData
import LineBotClass
import Database
import pytz
import gSheetAPI


sched = BlockingScheduler()


#\ testing
@sched.scheduled_job('cron', minute="*/29")
def testing():
    print(f"[INFO] scheduled_job: {datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}")


#\ Set the timer to update the datebase
#\ this will be trigger every
@sched.scheduled_job('cron', hour=0, minute=0, second=0)
def SetTimer2Update_job():
    global sched
    print(f"[INFO] SetTimer2Update_job start: {datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}")
    # index.DAYAlarm["hour"] = 2 #\ we set the hour at 0 and let the minute and second to be random

    #\ Start from 1 min is because this function will be triggerred at 00:00:00, avoid conflict with this function with UpdateDataBase_job()
    #\ The reason to set the minutes boundary to 30 is due to the heroku free dyno will sleep every 30 minutes idling.
    index.DAYAlarm["minute"] = random.randint(1, 30)
    index.DAYAlarm["second"] = random.randint(0, 60)
    # cache.set("DAYAlarm", index.HOURAlarm)
    sched.reschedule_job("UpdateDataBase_job_ID", trigger='cron', **index.DAYAlarm)
    print(f"[INFO] In SetTimer2Update_job() set the timer to update : {index.DAYAlarm}")


#\ Update database to the google sheets
def update_gSheets_daily():
    #\ Update the database to the google sheets
    # [status, gSheetResult] = gSheetAPI.GetDragonflyDataGoogleSheets()
    None



#\ This is to update the database's TodayID eveyday midnight
def UpdateDataBase_job(session, conn, time_zone):

    #\ Get the latest ID
    Max_ID_num = DragonflyData.GetMaxID(session)
    # print(f"[INFO] Max_ID_num : {Max_ID_num}")

    #\ write back to the database
    Update_Data = [(str(Max_ID_num), index.VarLatestDataID),
                   (datetime.datetime.now(time_zone).strftime('%Y-%m-%d'), index.VarLatestDataIDDate)
                   ]
    print(f"[INFO] Update_Data : {Update_Data}")
    Database.InsertManyDB(conn,
                        Database.Update_varaible_query,
                        Update_Data,
                        False
                        )

    #\ Update database to the google sheets
    # update_gSheets_daily()




#\ Send the hourly summary of the update for the dragonfly data
def Send_Hourly_Summary(session, Conn, DB_Variable_Data:dict):
    #\ Get the user id from the database
    userid_list = Database.ReadFromDB(Conn ,
                                      Database.Read_all_row_for_col_query("userid"),
                                      True,
                                      False
                                      )

    #\ Get the filter to the filter object : [user_list, species_list, keep_or_filter ]
    _, Species_filter_list_name = DragonflyData.GetSpeciesRecordingNumberRank(session)
    index.Hourly_Summary_default_data_filter[1] = Species_filter_list_name[index.HSDDFilter_start_index:]
    # print(f"[INFO] The Filter is {index.Hourly_Summary_default_data_filter}")

    #\ Send to all the user
    for user_id in userid_list:
        print(f"[INFO] >>> Looping with the User ID : {user_id}\n{'-'*60}")
        LineBotClass.GetTodayDataSend2LINEBot(user_id,
                                              AllDayData=False,
                                              filter=index.Hourly_Summary_default_data_filter,
                                              conn=Conn,
                                              DragonflyData_session=session
                                              )





#\ The main function to run the clock.py function every heroku dependency defined schedule time.
def RunClockFunctionbyHeroku():
    #\ Get the date time
    time_zone = pytz.timezone("Asia/Taipei")
    print(f"[INFO] In UpdateDataBase_job() Update the database latest ID at {datetime.datetime.now(time_zone).strftime('%Y-%m-%d, %H:%M:%S')}")

    #\ Create the web session and conn
    #\ DB_User_Data will be list of tuple or just list
    session, conn = LineBotClass.CreateWebSession(None, False)

    #\ Read variable data
    DB_Variable_Data = dict((Database.ReadFromDB(conn,
                                                Database.Read_all_query(index.VariableTableName),
                                                False,
                                                False)
                            ))

    #\ Update the database everyday
    if datetime.datetime.now(time_zone).hour == 0:
        UpdateDataBase_job(session, conn, time_zone)
        print("[INFO][Clock] Update the date and the latest ID to the database")

    #\ Send the data to the Line bot for all the user evey x hour
    if datetime.datetime.now(time_zone).hour % int(index.Send_Hour_Summary_timeInterval) == 0:
        Send_Hourly_Summary(session, conn, DB_Variable_Data)
        print("[INFO][Clock]Send the data to the user for hourly summary")

    #\ for testing (remove when pushing to heroku master)
    # Send_Hourly_Summary(session, conn, DB_Variable_Data)







################################################################################################

#\ ----------------------------------------------------------------
#\ Run the clock by the schedul of apscheduler
if index.ClockStandAloneVer:
    #\ Add the job
    sched.add_job(UpdateDataBase_job, "cron", id="UpdateDataBase_job_ID", hour=0, minute=1, second=0)

    #\ start the clock
    sched.start()

#\ Run the clock by the schedule of the Heroku add-on
#\ The heroku schedule set to run every hour
elif index.ClockHerokuDependancyVer:

    #\ Main function for the clock
    RunClockFunctionbyHeroku()
