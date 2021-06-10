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


sched = BlockingScheduler()


#\ testing
@sched.scheduled_job('cron', hour="*/1")
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


#\ This is to update the database's TodayID eveyday midnight
def UpdateDataBase_job():
    print(f"[INFO] In UpdateDataBase_job() Update the database latest ID at {datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}")

    #\ Create the web session and conn
    session, conn = LineBotClass.CreateWebSession(None, False)

    #\ Get the latest ID
    Max_ID_num = DragonflyData.GetMaxID(session)
    # print(f"[INFO] Max_ID_num : {Max_ID_num}")

    #\ write back to the database
    Update_Data = (str(Max_ID_num), index.VarLatestDataID)
    print(f"[INFO] Update_Data : {Update_Data}")
    Database.InsertDB(conn,
                      Database.Update_varaible_query(index.VariableTableName),
                      Update_Data
                      )





################################################################################################

#\ Add the job
sched.add_job(UpdateDataBase_job, "cron", id="UpdateDataBase_job_ID", hour=0, minute=1, second=0)

#\ start the clock
sched.start()