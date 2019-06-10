#BC Robotics Irrigation Tutorial https://www.bc-robotics.com/tutorials/raspberry-pi-irrigation-control-part-1-2/

import time
from w1thermsensor import W1ThermSensor

import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import RPi.GPIO as GPIO

ds18b20 = W1ThermSensor()

ads = ADS.ADS1015(i2c)
ads.gain = 1

interval = 5  #How long we want to wait between loops (seconds)
waterTick = 0   #Used to count the number of times the flow input is triggered

#Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)

#Set digital pin 24 to an input
GPIO.setup(24, GPIO.IN)

#Event to detect flow (1 tick per revolution)
GPIO.add_event_detect(24, GPIO.FALLING)
def flowtrig(self):
    global waterTick
    waterTick += 1

GPIO.add_event_callback(24, flowtrig)

while True:

    time.sleep(interval)

    #Pull Temperature from DS18B20
    temperature = ds18b20.get_temperature()

    #Measure Analog Input 0
    chan = AnalogIn(ads, ADS.P0) #ADS.P1 , P2, P3 for channels 1, 2, 3
    val = chan.value #Pull the raw ADC data from Channel 0

    waterFlow = waterTick * 2.25
    waterTick = 0

    #Print the results
    print( 'Temperature: ' , temperature)
    print( 'Soil Moisture: ' , val)
    print( 'Flow Rate: ' , waterFlow)
    print( ' ')
