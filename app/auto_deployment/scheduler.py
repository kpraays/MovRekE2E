# run in background: `nohup python3 scheduler.py &`
import subprocess
import schedule
import time
from datetime import datetime

def job(t):
    print(t)
    subprocess.run(["python3", "auto_deploy.py"])
    return

schedule.every().day.at("20:00").do(job,'Periodic training and deployment scheduled successfully at ',datetime.now())

while True:
    # Run pending tasks
    schedule.run_pending()
    # Sleep for 1 minute
    time.sleep(60)