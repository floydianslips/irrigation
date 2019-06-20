
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

#Assign channels to variables to keep track of them easier (these BCM pin numbers were listed in part 1 of the tutorial)
s1 = 13
s2 = 16
s3 = 19
s4 = 20
s5 = 26
s6 = 21

#Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)

#Set digital pin 24 to an input
GPIO.setup(24, GPIO.IN)

#Set solenoid driver pins to outputs:
GPIO.setup(s1, GPIO.OUT) #set Solenoid 1 output
GPIO.setup(s2, GPIO.OUT) #set Solenoid 2 output
GPIO.setup(s3, GPIO.OUT) #set Solenoid 3 output
GPIO.setup(s4, GPIO.OUT) #set Solenoid 4 output
GPIO.setup(s5, GPIO.OUT) #set Solenoid 5 output
GPIO.setup(s6, GPIO.OUT) #set Solenoid 6 output


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

    #Test Solenoids by turning each on for a half second
    GPIO.output(s1, GPIO.HIGH) #turn solenoid 1 on
    time.sleep(0.5) #Wait for a half second
    GPIO.output(s1, GPIO.LOW) #turn solenoid 1 off
    time.sleep(0.5)

    GPIO.output(s2, GPIO.HIGH) #turn solenoid 2 on
    time.sleep(0.5) #Wait for a half second
    GPIO.output(s2, GPIO.LOW) #turn solenoid 2 off
    time.sleep(0.5)

    GPIO.output(s3, GPIO.HIGH) #turn solenoid 3 on
    time.sleep(0.5) #Wait for a half second
    GPIO.output(s3, GPIO.LOW) #turn solenoid 3 off
    time.sleep(0.5)

    GPIO.output(s4, GPIO.HIGH) #turn solenoid 4 on
    time.sleep(0.5) #Wait for a half second
    GPIO.output(s4, GPIO.LOW) #turn solenoid 4 off
    time.sleep(0.5)

    GPIO.output(s5, GPIO.HIGH) #turn solenoid 5 on
    time.sleep(0.5) #Wait for a half second
    GPIO.output(s5, GPIO.LOW) #turn solenoid 5 off
    time.sleep(0.5)

    GPIO.output(s6, GPIO.HIGH) #turn solenoid 6 on
    time.sleep(0.5) #Wait for a half second
    GPIO.output(s6, GPIO.LOW) #turn solenoid 6 off
    time.sleep(0.5)

    #Print the results
    print( 'Temperature: ' , temperature)
    print( 'Soil Moisture: ' , val)
    print( 'Flow Rate: ' , waterFlow)
    print( ' ')
