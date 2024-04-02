import datetime
import time

import dht11
import requests
import RPi.GPIO as GPIO

import config

SW_GPIO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

instance = dht11.DHT11(pin=14)

last_status = False

url = config.URL
token = config.TOKEN
headers = {"Authorization" : "Bearer " + token}


try:
    while True:
        result = instance.read()
        if result.is_valid():
            switch_status = GPIO.input(SW.GPIO)

            if last_status != switch_status:

                if switch_status == 1:
                    dt_now = datetime.datetime.now()
                    print("時刻: " + dt_now.strftime("%-H:%-M"))
                    print("温度: %d℃" % result.temperature)
                    print("湿度: %d%%" % result.humidity)
                    message =  "温度: %d℃" % result.temperature + " 湿度: %d%%" % result.humidity
                    payload = {"message" :  message}
                    r = requests.post(url, headers = headers, params=payload)

            last_status = switch_status


except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()





