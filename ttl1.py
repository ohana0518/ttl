#!/usr/bin/env python3
import socket
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import http.client as http
import urllib
import json
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.IN)

deviceId = "DTFEZNR2"
deviceKey = "RAq0F2o0UF00uFo3" 

def post_to_mcs(payload): 
        headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
        not_connected = 1 
        while (not_connected):
                try:
                        conn = http.HTTPConnection("api.mediatek.com:80")
                        conn.connect() 
                        not_connected = 0 
                except (http.HTTPException, socket.error) as ex: 
                        print ("Error: %s" % ex)
                       
			 
        conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
        response = conn.getresponse() 
        print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
        data = response.read() 
        conn.close() 
try:
    while True:
        
        SwitchStatus = GPIO.input(4)
        if( SwitchStatus == 0):
            print('Button is OFF')
        else:
            print('Button is ON')
        payload = {"datapoints":[{"dataChnId":"Switch","values":{"value":SwitchStatus}}]}	
        post_to_mcs(payload)
        time.sleep(5)
except KeyboardInterrupt:
    print('關閉程式')

