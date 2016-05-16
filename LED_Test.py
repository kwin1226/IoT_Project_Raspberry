mport RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)

user = input("-------Choose one mode--------\n 1.Light up 2.Light down 3.Keep blinking 4.exit\n")


if(user == 1):
        GPIO.output(4,1)
elif(user == 2):
        GPIO.output(4,0)
elif(user == 3):
        count = 0
        while count<4:
                #light up led "4"
                GPIO.output(4,1)
                time.sleep(1)
                #light down led "4"
                GPIO.output(4,0)
                time.sleep(1)

                count = count +1

elif(user == 4):
        exit()
else:
	    print("Please input a number 1~4!")

