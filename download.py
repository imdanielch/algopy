from datetime import datetime, date, timedelta
import requests
from config import url, year, month, day

def isWeekday(d):
    if d.weekday() > 4:
        return False
    else:
        return True

today = date.today()
last_date = date(year, month, day)
delta = today - last_date
print(delta.days)

# days -1 so it doesn't get today in case it hasn't finished
for i in range(0, delta.days - 1):
    i+= 1
    date = last_date + timedelta(days=i)
    if isWeekday(date):
        filename = "Daily_{y}_{m}_{d}.zip".format(y=date.year,m=f"{date:%m}",d=f"{date:%d}")
        dl_url = url + filename
        print(dl_url)
        r = requests.get(dl_url, allow_redirects=True)
        with open(filename, 'wb') as f:
            print("saving ", filename)
            f.write(r.content)
    else:
        print("---")
