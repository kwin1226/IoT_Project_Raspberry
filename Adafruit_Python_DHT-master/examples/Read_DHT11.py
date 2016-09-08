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
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import MySQLdb

def mySql_Con(temperature, humidity, vibeState):
  db = MySQLdb.connect(host="140.138.77.98", user="bigdata_team04", passwd="284gj4rm42l3xjp4", db="2016_bigdata_team04")
  cursor = db.cursor()
  # excute SQL 
  _Table = "DataCollection"
  Data_time = time.strftime("%Y-%m-%d %H:%M:%S")
  Data_humidity = humidity
  Data_centigrade = temperature
  Data_vibration = vibeState
  data_form =[{'Rasp_ID': 'Pi3' ,'Data_time':Data_time, 'Data_humidity' : Data_humidity, 'Data_centigrade':Data_centigrade, 'Data_vibration':Data_vibration }]
  insert_stmt = "INSERT INTO " + _Table + " (Rasp_ID, Data_time, Data_humidity, Data_centigrade, Data_vibration) VALUES (%(Rasp_ID)s, %(Data_time)s, %(Data_humidity)s, %(Data_centigrade)s, %(Data_vibration)s)"
  cursor.executemany(insert_stmt, data_form)
  select_stmt ="SELECT * FROM " + _Table
  cursor.execute(select_stmt)
  result = cursor.fetchall()
  # output result
  for record in result:
      print (record)
  cursor.close()
  db.close()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIR = 7
print "PIR Module Test (CTRL-C to exit)"

GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo
Current_State = 0
Previous_State = 0

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

try:
 
  print "Waiting for PIR to settle ..."
 
  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0
 
  print "  Ready"
 
  # Loop until users quits with CTRL-C
  while True :
 
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
 
    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      print "  Motion detected!"
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

      if humidity is not None and temperature is not None:
          print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
          mySql_Con(temperature, humidity, Current_State)
      else:
          print('Failed to get reading. Try again!')
      #If Motion detected, light up the LED
      # for i in range(10):
      #   GPIO.output(4,1)
      #   time.sleep(0.2)
      #   GPIO.output(4,0)
      #   time.sleep(0.2)
      # mySql_Con()
      # Record previous state
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      print "  Ready"
      Previous_State=0
 
    # Wait for 10 milliseconds
    time.sleep(0.01)
 
except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()