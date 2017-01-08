#!/usr/bin/env python
#coding:utf-8

import os
import RPi.GPIO as GPIO #
import json
from time import sleep #
from twython import Twython

f=open("tw_config.json",'r')
config=json.load(f)
f.close()

CONSUMER_KEY =config['consumer_key']
CONSUMER_SECRET =config['consumer_secret']
ACCESS_TOKEN =config['access_token']
ACCESS_SECRET =config['access_secret']

dist=config['dist']

def on_positive_edge(channel):
    #time stamp
    timestamp = 'date +%F_%H:%M:%S'
    current_time=os.popen(timestamp).readline().strip()


    # get CPU temperature
    cmd = '/opt/vc/bin/vcgencmd measure_temp'
    line = os.popen(cmd).readline().strip()
    temp = line.split('=')[1].split("'")[0]

    direct_message='CPU:'+temp+'deg @'+current_time+'  : by Python script'


    global ledstate
    if channel == trigger_input:
        ledstate = not ledstate
        GPIO.output(25, ledstate)

        api.send_direct_message(text=direct_message ,screen_name=dist)

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET)

trigger_input=21

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(trigger_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(trigger_input, GPIO.RISING, callback=on_positive_edge, bouncetime=1000)

ledstate = GPIO.LOW

try:
    while True:
        sleep(0.01)

except KeyboardInterrupt: #
    pass

GPIO.cleanup() #
