#!/usr/bin/python
import sys
import smbus
import math
import time
import MySQLdb
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def mySql_Con(gyro_xout, gyro_yout, gyro_zout, accel_xout, accel_yout, accel_zout):
  db = MySQLdb.connect(host="140.138.77.98", user="bigdata_team04", passwd="284gj4rm42l3xjp4", db="2016_bigdata_team04")
  cursor = db.cursor()
  # excute SQL 
  _Table = "VibeData"
  vibe_time = time.strftime("%Y-%m-%d %H:%M:%S")
  data_form =[{'Rasp_ID': 'Pi3' ,'vibe_time':vibe_time, 'vibe_gyro_x' : gyro_xout, 'vibe_gyro_y':gyro_yout, 'vibe_gyro_z':gyro_zout, 'vibe_accel_x':accel_xout, 'vibe_accel_y':accel_yout, 'vibe_accel_z':accel_zout}]
  insert_stmt = "INSERT INTO " + _Table + " (Rasp_ID, vibe_time, vibe_gyro_x, vibe_gyro_y, vibe_gyro_z, vibe_accel_x, vibe_accel_y, vibe_accel_z) VALUES (%(Rasp_ID)s, %(vibe_time)s, %(vibe_gyro_x)s, %(vibe_gyro_y)s, %(vibe_gyro_z)s, %(vibe_accel_x)s, %(vibe_accel_y)s, %(vibe_accel_z)s)"
  cursor.executemany(insert_stmt, data_form)
  select_stmt ="SELECT * FROM " + _Table
  cursor.execute(select_stmt)
  result = cursor.fetchall()
  # output result
  for record in result:
      print (record)
  cursor.close()
  db.close()

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

print "gyro data"
print "---------"

gyro_xout = read_word_2c(0x43)
gyro_yout = read_word_2c(0x45)
gyro_zout = read_word_2c(0x47)

print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

print
print "accelerometer data"
print "------------------"

accel_xout = read_word_2c(0x3b)
accel_yout = read_word_2c(0x3d)
accel_zout = read_word_2c(0x3f)

accel_xout_scaled = accel_xout / 16384.0
accel_yout_scaled = accel_yout / 16384.0
accel_zout_scaled = accel_zout / 16384.0

print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

mySql_Con(gyro_xout, gyro_yout, gyro_zout, accel_xout, accel_yout, accel_zout)