import time
import picamera
from picamera.array import PiRGBArray
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import numpy as np
from datetime import datetime
import threading
from fractions import Fraction

pulses_per_kwh = 500

key = "KEY GOES HERE"
endpoint = "https://ap-southeast-2.aws.data.mongodb-api.com/app/data-zhdjq/endpoint/data/v1/action/insertOne"

s = requests.Session()
retries = Retry(total=25,
                    status_forcelist=[429, 500, 502, 503, 504])

s.mount('https://', HTTPAdapter(max_retries=retries))

def send_usage(time, kwh):
    response = s.post(endpoint,
        headers = {
            "apikey": key,
            "content-type": "application/ejson"
        },
        json = {
            "dataSource": "energy",
            "database": "meter",
            "collection": "meter",
            "document": {
                "date": { "$date": { "$numberLong": str(int(time.timestamp() * 1000)) } },
                "kwh": kwh
            }
        })
    print(response.text)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Boot Time =", current_time)

threading.Thread(target=send_usage, args=(now, -1)).start()

camera = picamera.PiCamera()
camera.resolution = (32, 32)
camera.framerate = 2 # Fraction(1,6)
# Set ISO to the desired value
camera.iso = 100
camera.led = False
time.sleep(2)
# Now fix the values
# camera.shutter_speed = camera.exposure_speed
camera.shutter_speed = 500000
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
time.sleep(2)

rawCapture = PiRGBArray(camera, size=(32, 32))
stream = camera.capture_continuous(rawCapture, 'rgb', use_video_port=True)
frame = None
stopped = False

def update():
    global frame, rawCapture, stream, camera, stopped
    for f in stream:
        frame = f.array
        rawCapture.truncate(0)

        if stopped:
            stream.close()
            rawCapture.close()
            camera.close()

threading.Thread(target=update).start()

blink = False
last_pulse = None

try:
    while True:
        if frame is None:
            continue
        
        avg = np.average(frame)
        if avg > 2:
            # avg0 = np.average(frame[0])
            # avg1 = np.average(frame[1])
            # avg2 = np.average(frame[2])

            if blink is False:
                print(avg)
                blink = True
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                
                if last_pulse is not None:
                    delta_s = (now-last_pulse).total_seconds()
                    # wh = 3600/delta_s
                    est_kwh = (1000/pulses_per_kwh) * 3600 / delta_s
                    print("Pulse at {}, {}s ago, est kWh = {}".format(current_time, delta_s, est_kwh))
                    threading.Thread(target=send_usage, args=(now, est_kwh)).start()
                else:
                    print("Pulse at {}".format(current_time))
                last_pulse = now
        else:
            if blink is True:
                print(avg)
            blink = False
except KeyboardInterrupt:
    print('interrupted!')
    stopped = True
