#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys
import math


def initGPIO():
    # pin 21 = blue, pin 20 = green, pin 16 = red
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    # Dont print out the warnings that may occur
    GPIO.setwarnings(False)
    return


def cleanup():
    GPIO.cleanup()
    return


#LED to flash the red LED
def flashRed(numFlash):
    count = 0
    # While less than the amount of flashes
    while (count < numFlash):
        #output the red for half a second
        GPIO.output(16, GPIO.HIGH)
        time.sleep(.7)
        #sleep for a tenth of a second
        GPIO.output(16, GPIO.LOW)
        time.sleep(.3)
        #increment
        count += 1
    return


def flashGreen(numFlash):
    count = 0
    # While less than the amount of flashes
    while (count < numFlash):
        #output the green for half a second
        GPIO.output(20, GPIO.HIGH)
        time.sleep(.7)
        #sleep for a tenth of a second
        GPIO.output(20, GPIO.LOW)
        time.sleep(.3)
        #increment
        count += 1
    return


def flashBlue(numFlash):
    count = 0
    # While less than the amount of flashes
    while (count < numFlash):
        #output the blue for half a second
        GPIO.output(21, GPIO.HIGH)
        time.sleep(.7)
        #sleep for a tenth of a second
        GPIO.output(21, GPIO.LOW)
        time.sleep(.3)
        #increment
        count += 1
    return


def lightLED(messCount):
    print("Message count:", messCount)
    # if there are less than 100 messages        
    if(messCount > 99):
        # find the digit in the hundreds place
        hundreds = messCount // 100
        # update message count
        messCount = messCount - (hundreds * 100)
        # call the red flash function
        flashRed(hundreds)

    # if there are less than 10 messages
    # in the updated message count
    if(messCount > 9):
        # find the tens digit
        tenths = messCount // 10
        #update message count
        messCount = messCount - (tenths * 10)
        # flash green
        flashGreen(tenths)

    # flash blue with the rest
    flashBlue(messCount)
    return
