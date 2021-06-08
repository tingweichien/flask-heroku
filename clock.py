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

#\ The schedule to wake the herok, since for the free dyno, it'll begin to sleep if idling for 30 minutes
# @sched.scheduled_job('cron', **index.HOURAlarm)
# def scheduled_job():
#     conn = requests.get(index.ServerURL)

#     for key, value in conn.getheaders():
#         print(key, value)



#\ testing
@sched.scheduled_job('cron', minute="*/10")
def testing():
    print(f"[INFO] scheduled_job: {datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}")


#\ Set the timer to update the datebase
#\ this will be trigger every
@sched.scheduled_job('cron', hour=0, minute=0, second=0)
def SetTimer2Update_job():
    #index.DAYAlarm["hour"] #\ we set the hour at 0 and let the minute and second to be random

    #\ Start from 1 min is because this function will be triggerred at 00:00:00, avoid conflict with this function with UpdateDataBase_job()
    #\ The reason to set the minutes boundary to 30 is due to the heroku free dyno will sleep every 30 minutes idling.
    index.DAYAlarm["minute"] = random.randint(1, 30)
    index.DAYAlarm["second"] = random.randint(0, 60)
    # cache.set("DAYAlarm", index.HOURAlarm)
    sched.reschedule_job("UpdateDataBase_job_ID", trigger='cron', **index.HOURAlarm)
    print(f"[INFO] In SetTimer2Update_job() set the timer to update : {cache.get('DAYAlarm')}")


#\ This is to update the database's TodayID eveyday midnight
# @sched.scheduled_job('cron', **cache.get("DAYAlarm"))
@sched.scheduled_job('cron', id="UpdateDataBase_job_ID", **index.DAYAlarm)
def UpdateDataBase_job():
    print(f"[INFO] In UpdateDataBase_job() Update the database latest ID at {datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}")
    retry = 0
    while retry < index.re_try_limit:
        [session, _, Login_state] = DragonflyData.Login_Web(LineBotClass.CreateWebSession(None))

        #\ if fail then retry
        if Login_state is False:
            retry += 1

    #\ Get the latest ID
    Max_ID_num = DragonflyData.GetMaxID(session)

    #\ write back to the database
    Update_Data = (index.VarLatestDataID, Max_ID_num)
    Database.InsertDB(Database.CreateDBConection(),
                      Database.Update_varaible_query,
                      Update_Data
                      )


#\ use this function to start the alarm
def StartAlarm():
    sched.start()



#\ start the clock
# StartAlarm()