from datetime import datetime, date, timedelta
import holidays
import requests
from config import url, year, month, day
import os

def isWeekday(d):
    if d.weekday() > 4:
        return False
    else:
        return True

today = date.today()
last_date = date(year, month, day)
delta = today - last_date
print(f"days since last download: {delta.days}")
tw_holidays = holidays.CountryHoliday("TW")

# days -1 so it doesn't get today in case it hasn't finished
for i in range(0, delta.days - 1):
    i+= 1
    date = last_date + timedelta(days=i)
    download = True 
    if not isWeekday(date):
        print("---weekend---")
        download = False
    if date in tw_holidays:
        print("---holiday---")
        download = False
    if download:
        filename = "Daily_{y}_{m}_{d}.zip".format(y=date.year,m=f"{date:%m}",d=f"{date:%d}")
        dl_url = url + filename
        file_path = os.path.join("./download", filename)
        if not os.path.exists(file_path):
            print(f"downloading {dl_url}")
            r = requests.get(dl_url, allow_redirects=True)
            if len(r.content) > 1000:
                with open(filename, 'wb') as f:
                    print(f"saving {filename}")
                    f.write(r.content)
            else:
                print(f"no data: {filename} - {len(r.content)}")
        else:
            print(f"{filename} exists, skipping.")

