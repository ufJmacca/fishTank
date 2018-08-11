import time, serial, datetime,sqlite3, sqlalchemy, pandas as pd

eng = sqlalchemy.create_engine('sqlite:////home/fish/tank.db')

metadata = sqlalchemy.MetaData()
metadata.reflect(bind=eng)

conn = eng.connect()

next_change = pd.read_sql_query('select * from suncycle limit 1', eng)

#print(datetime.datetime.now(), datetime.datetime.strptime(next_change.iloc[0]['dt'], '%Y-%m-%d %H:%M:%S.000000'))
try:
    if datetime.datetime.strptime(next_change.iloc[0]['dt'], '%Y-%m-%d %H:%M:%S.000000') <= datetime.datetime.now():
        ser = serial.Serial(
                            port='/dev/ttyACM0',
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=1
                           )
        time.sleep(5)
        if next_change.iloc[0]['instruction'] == 'night on':
            counter = '1'
            ser.write(counter.encode())
            ser.close()
        elif next_change.iloc[0]['instruction'] == 'day on':
            counter = '2'
            ser.write(counter.encode())
            ser.close()
        elif next_change.iloc[0]['instruction'] == 'day off':
            counter = '1'
            ser.write(counter.encode())
            ser.close()
        elif next_change.iloc[0]['instruction'] == 'night off':
            counter = '4'
            ser.write(counter.encode())
            ser.close()

        tankConn = sqlite3.connect('/home/fish/tank.db')
        tankConn.cursor().execute("""delete from suncycle where id = '""" + str(next_change.iloc[0]['id']) + """';""")
        tankConn.commit()
        tankConn.commit()

except:
    pass
