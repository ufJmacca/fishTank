import urllib.request as Request
import json, time
from datetime import datetime, timedelta

print((datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') )

request = Request.urlopen('https://api.sunrise-sunset.org/json?lat=-33.7317363&lng=151.1242504&date=' + datetime.now().strftime('%Y-%m-%d')  + '&formatted=0')
timestring = json.loads(request.read().decode('utf-8'))
#timestring = request.read()

def to_local(utc):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return datetime.strptime(utc, '%Y-%m-%dT%H:%M:%S+00:00') + offset

print(str(to_local(timestring['results']['sunset'])))
print()
print(timestring)

assert timestring['status'] == 'OK'

from sqlalchemy import create_engine, MetaData

eng = create_engine('sqlite:////home/fish/tank.db')

metadata = MetaData()
metadata.reflect(bind=eng)

conn = eng.connect()

conn.execute(metadata.tables['suncycle'].insert().values(dt = to_local(timestring['results']['astronomical_twilight_begin']),
                                                         instruction = "night on"))

conn.execute(metadata.tables['suncycle'].insert().values(dt = to_local(timestring['results']['sunrise']) + timedelta(hours=1),
                                                         instruction = "day on"))

conn.execute(metadata.tables['suncycle'].insert().values(dt = to_local(timestring['results']['sunset']) - timedelta(hours=1),
                                                         instruction = "day off"))

conn.execute(metadata.tables['suncycle'].insert().values(dt = to_local(timestring['results']['astronomical_twilight_end']),
                                                         instruction = "night off"))





