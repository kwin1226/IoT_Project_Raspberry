#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from datetime import datetime
import urllib
import urllib2, base64
import MySQLdb
import socketInit
# import getRules

t1 = time.strftime("%Y-%m-%d %H:%M:%S") # for example

# def mySql_Con(temperature, humidity, vibeState):
#   db = MySQLdb.connect(host="140.138.77.98", user="bigdata_team04", passwd="284gj4rm42l3xjp4", db="2016_bigdata_team04", connect_timeout=28800)
#   cursor = db.cursor()
#   # excute SQL 
#   _Table = "HISTORY"
#   H_Time = time.strftime("%Y-%m-%d %H:%M:%S")
#   H_Hum = humidity
#   H_Tem = temperature
#   H_Accident = vibeState
#   data_form =[{'E_ID': 'Rasp02' ,'U_ID': "1",'H_Time':H_Time, 'H_Hum' : H_Hum, 'H_Tem':H_Tem, 'H_Accident':H_Accident }]
#   insert_stmt = "INSERT INTO " + _Table + " (E_ID, U_ID, H_Time, H_Hum, H_Tem, H_Accident) VALUES (%(E_ID)s,%(U_ID)s ,%(H_Time)s, %(H_Hum)s, %(H_Tem)s, %(H_Accident)s)"
#   cursor.executemany(insert_stmt, data_form)
#   select_stmt ="SELECT * FROM " + _Table + " ORDER BY H_ID DESC LIMIT 1"
#   cursor.execute(select_stmt)
#   result = cursor.fetchall()
#   # output result
#   for record in result:
#       print (record)
#   cursor.close()
#   db.close()

# def GetRules():
#   print "Get rules data..."
#   u = "testuser"
#   p = "testpassword"
#   eid = "Rasp01"
#   geturl = "http://140.138.77.152:5000/v1.0/demand/getjoin"
#   method = "GET"
#   jsonRules = getRules.main(u, p, eid, geturl, method)
#   return jsonRules

def uploadHis(temperature, humidity, vibeState,curTime,useTime):
  url_con ="http://140.138.77.152:5000/v1.0/history"
  data = {
    "eid":"Rasp01",
    "eveid":"1", #default
    "historyTem":temperature,
    "historyHum":humidity,
    "historyAccident":vibeState,
    "historyTime":curTime,
    "historyUTime":useTime
  }
  username = "testuser"
  password = "testpassword"
  data = urllib.urlencode(data)
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  req = urllib2.Request(url_con, data)

  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  req.add_header('Authorization', "Basic %s" % base64string) #handling Authorization Encoding
  req.get_method = lambda: "POST"
  url = opener.open(req)
  JSONResult = url.read()
  JSONResult_decode = JSONResult.decode('utf-8')
  print (JSONResult_decode)

  # Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
    print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
# jsonRules = GetRules()
# print(jsonRules)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIR = 7
GPIO.setup(GPIO_PIR,GPIO.IN)
Current_State = 0
FMT = '%Y-%m-%d %H:%M:%S'

print "Waiting for PIR to settle ..."
try:
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0
    print "  Ready"

  while True:
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
      Current_State = GPIO.input(GPIO_PIR)
      if humidity is not None and temperature is not None and Current_State==0 :
          t2 = time.strftime("%Y-%m-%d %H:%M:%S")
          print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
          # mySql_Con(temperature, humidity, 1)
          tdelta = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
          print('Total time:' + str(tdelta))
          uploadHis(temperature, humidity, 0 ,t2,tdelta)

          time.sleep(5)
      elif Current_State ==1:
          print('Someone leave!')
          socketInit.pushUsingOut()
          t2 = time.strftime("%Y-%m-%d %H:%M:%S")
          tdelta = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
          print('Total time:' + str(tdelta))
          sys.exit(1)
      else:
          print('Failed to get reading. Try again!')
          sys.exit(1)

except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()


