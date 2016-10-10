# Import required Python libraries
import RPi.GPIO as GPIO
import os
import time
import socketInit

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Define GPIO to use on Pi
# GPIO_LED = 4
GPIO_PIR = 7

print "PIR Module Test (CTRL-C to exit)"

# Set pin as input
# GPIO.setup(GPIO_LED,GPIO.OUT)
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo
Current_State = 0
Previous_State = 0


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
      #If Motion detected, light up the LED
      # for i in range(10):
      #   GPIO.output(4,1)
      #   time.sleep(0.2)
      #   GPIO.output(4,0)
      #   time.sleep(0.2)

      socketInit.pushUsingIn()
      os.system("python Trans_DHT.py 11 17")
      #mySql_Con()

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




