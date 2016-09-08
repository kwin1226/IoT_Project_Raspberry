#!/usr/bin/env python
# encoding: utf-8

import RPi.GPIO 
import time

# LED GPIO port
GPIO_LED = 4

# Sensors OUT GPIO port
GPIO_Sounds = 22

# LED turn on & off flag
flg = False

RPi.GPIO.setmode(RPi.GPIO.BCM)

# 指定GPIO4（聲音感應器的OUT口連接的GPIO口）的模式為輸入模式
# 默認拉高到高電平，低電平表示OUT口有輸出
RPi.GPIO.setup(GPIO_Sounds, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

#指定GPIO17（LED長針連接的GPIO針腳）的模式為輸出模式
RPi.GPIO.setup(GPIO_LED, RPi.GPIO.OUT)

try : 
	print "Waiting for Sounds to settle ..."
	while  True :
		#檢測聲音感應器是否輸出低電平，若是低電平，表示聲音被檢測到，點亮或關閉LED燈
		if (RPi.GPIO.input(GPIO_Sounds) == 0 ): 
			flg = not flg 
			print "Sounds Detected!"
			RPi.GPIO .output(GPIO_LED, flg)
			#稍微延時一會，避免剛點亮就熄滅，或者剛熄滅就點亮。
			time.sleep( 0.5 )
			print " Ready!"

except KeyboardInterrupt: 
	pass

RPi.GPIO.cleanup()