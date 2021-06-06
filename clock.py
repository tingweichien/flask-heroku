#\ This is the file to set the routine to wake the Heroku up since in the free version, it'll sleep if there is no action occcurred
#\ also put the daily update for the dragonfly info here in set schedule
#\ ref: https://ithelp.ithome.com.tw/articles/10218874
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import index


sched = BlockingScheduler()

@sched.scheduled_job('cron', **index.HOUR)
def scheduled_job():
    conn = requests.get(index.ServerURL )

    for key, value in conn.getheaders():
        print(key, value)


#\ use this function to start the alarm
def StartAlarm():
    sched.start()