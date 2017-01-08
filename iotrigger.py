#!/usr/bin/env python
#coding:utf-8

import os
import RPi.GPIO as GPIO #
from time import sleep #
from twython import Twython

#Twitter API 
CONSUMER_KEY =''
CONSUMER_SECRET =''
ACCESS_KEY =''
ACCESS_SECRET =''
api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)



def on_positive_edge(channel):
    #time stamp
    timestamp = 'date +%F_%H:%M:%S'
    current_time=os.popen(timestamp).readline().strip()


    # get CPU temperature
    cmd = '/opt/vc/bin/vcgencmd measure_temp'
    line = os.popen(cmd).readline().strip()
    temp = line.split('=')[1].split("'")[0]

    global ledstate
    if channel == 21:
        ledstate = not ledstate
        GPIO.output(25, ledstate)
        api.send_direct_message(text='CPU:'+temp+'deg @'+current_time+'  : by Python script',screen_name='mqttand')



GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(21, GPIO.RISING, callback=on_positive_edge, bouncetime=1000)

ledstate = GPIO.LOW

try:
    while True:
        sleep(0.01)

except KeyboardInterrupt: #
    pass

GPIO.cleanup() #
