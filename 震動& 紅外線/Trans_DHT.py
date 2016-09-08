#!/usr/bin/python
# encoding: utf-8
# Function: 
#           1.upload sensors data through web api
#           2.detect accident
#           3.when a person leave, the transmission will end
#
# Author: Andrew Shen

import os
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from datetime import datetime
import urllib
import urllib2, base64
import MySQLdb
import getRules

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

def GetRules():
  print "Get rules data..."
  u = "testuser"
  p = "testpassword"
  eid = "Rasp03"
  geturl = "http://140.138.77.152:5000/v1.0/demand/getjoin"
  method = "GET"
  jsonRules = getRules.main(u, p, eid, geturl, method)
  return jsonRules

def loadData(temperature, humidity, vibe_flag):

  t2 = time.strftime("%Y-%m-%d %H:%M:%S")
  print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
  tdelta = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
  print('Total time:' + str(tdelta))
  uploadHis(temperature, humidity, vibe_flag ,t2,tdelta)
  vibe_flag = 0
  time.sleep(5)

def uploadHis(temperature, humidity, vibeState,curTime,useTime):
  url_con ="http://140.138.77.152:5000/v1.0/history"
  data = {
    "eid":"Rasp01",
    "eveid":"2", #default
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
GPIO_LED = 4
GPIO_PIR = 7
GPIO_Sounds = 22
GPIO_Vibe = 27
LED_flg = False
GPIO.setup(GPIO_PIR,GPIO.IN)
GPIO.setup(GPIO_LED,GPIO.OUT)
GPIO.setup(GPIO_Sounds, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_Vibe,GPIO.IN)      # Echo
Cur_vibe_State = 0
Cur_Sounds_State = 0 
Pre_vibe_State = 0
Cur_Pir_State = 0
vibe_flag = 0
FMT = '%Y-%m-%d %H:%M:%S'


try:
  print "Waiting for PIR to settle ..."
    # Loop until PIR、Vibe output is 0(not detected), Sound output is 1(not detected) 
  while GPIO.input(GPIO_PIR)==1 and GPIO.input(GPIO_Vibe)==1 and GPIO.input(GPIO_Vibe) == 0:
    Cur_Pir_State  = 0
    Cur_vibe_State  = 0
    Cur_Sounds_State = 1
    print "  Ready"

  while True:
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
      Cur_Pir_State = GPIO.input(GPIO_PIR)
      Cur_vibe_State = GPIO.input(GPIO_Vibe)
      Cur_Sounds_State = GPIO.input(GPIO_Sounds)

      if humidity is not None and temperature is not None and Cur_vibe_State==0 and Cur_Sounds_State==1: #pir,vibe not detected
      
          loadData(temperature, humidity, vibe_flag)

      elif humidity is not None and temperature is not None and Cur_vibe_State==1 and Cur_Sounds_State==0: #vibe detected

          # PIR is triggered
          print "  Fall down detected!"
          LED_flg = not LED_flg
          GPIO.output(GPIO_LED, LED_flg)
          vibe_flag = 1
          Cur_vibe_State = 0
          Cur_Sounds_State = 1

          loadData(temperature, humidity, vibe_flag)

      elif humidity is not None and temperature is not None and Cur_vibe_State==1 and Cur_Sounds_State==1: #vibe not detected
          print "  vibe>y \nSound>n"
          # PIR is triggered
          vibe_flag = 0
          Cur_vibe_State = 0
          Cur_Sounds_State = 1

          loadData(temperature, humidity, vibe_flag)

      elif humidity is not None and temperature is not None and Cur_vibe_State==0 and Cur_Sounds_State==0: #vibe not detected
          print "  vibe>n \nSound>y"
          # PIR is triggered
          vibe_flag = 0
          Cur_vibe_State = 0
          Cur_Sounds_State = 1

          loadData(temperature, humidity, vibe_flag)

      elif Cur_Pir_State ==1:   #pir detected
          print('Someone leave!')
          t2 = time.strftime("%Y-%m-%d %H:%M:%S")
          tdelta = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
          print('Total time:' + str(tdelta))
          # sys.exit(1)
      else:
          print('Failed to get reading. Try again!')
          sys.exit(1)

except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()
