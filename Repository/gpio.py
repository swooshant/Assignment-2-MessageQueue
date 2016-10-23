#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys


def initGPIO():
    # pin 21 = blue, pin 20 = green, pin 16 = red
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setwarnings(False)
    return


def cleanup():
    GPIO.cleanup()
    return


def flashRed(numFlash):
    count = 0
    while (count < numFlash):
        GPIO.output(16, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(16, GPIO.LOW)
        time.sleep(1)
        count += 1
    return


def flashGreen(numFlash):
    count = 0
    while (count < numFlash):
        GPIO.output(20, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(20, GPIO.LOW)
        time.sleep(1)
        count += 1
    return


def flashBlue(numFlash):
    count = 0
    while (count < numFlash):
        GPIO.output(21, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(21, GPIO.LOW)
        time.sleep(1)
        count += 1
    return


def lightLED(messCount):
    #numFlash = 0

    hundreds = messCount / 100
    messCount = messCount - (hundreds * 100)
    flashRed(hundreds)

    tenths = messCount / 10
    messCount = messCount - (tenths * 10)
    flashGreen(tenths)
    flashBlue(messCount)
    return

#### main ####
