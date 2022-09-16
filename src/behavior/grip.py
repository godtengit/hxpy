import os
import sys
from multiprocessing import Process
from HX711 import AdvancedHX711, Rate
from pynput import keyboard
from utils.prompts import *
from utils.dframe import *

data = []
max01 = 0
max02 = 0

test = "grip"
experiment = ""
group = ""
boxes = ""
mice = ""
trials = ""
initials = ""

def onPress(key, data, f1, f2, exp, grp, box, mice, trs, inits, test):
    if key == keyboard.KEY.esc: 
        return False
        sys.exit(os.EX_USAGE)
    try:
        k = key.char
    except:
        k = key.name
    if k in ['m']:
        showData(f1,f2)
    if k in ['space']:
        pinData(data, f1, f2)
        resetForce(f1, f2)
    if k in ['z']:
        resetForce(f1, f2)
    if k in ['enter']:
        cleanExit(data, experiment, group, boxes, mice, trials, initials, test)


def pinData(data, f1, f2):
    data.append(f1)
    data.append(f2)
    print("Test #: ", int(len(data)/2))
    print("Peak 01 (g): {:.3f} - recorded".format(f1))
    print("Peak 02 (g): {:.3f} - recorded".format(f2))


def showData(f1, f2):
    print("Peak 01 (g): {:.3f}".format(f1))
    print("Peak 02 (g): {:.3f}".format(f2))


def getForce01():
    # Right Hand
    with AdvancedHX711(24, 23, 3045, 157432, Rate.HZ_80) as hx
        while True:
            max01 = max(max01, hx.weight(1))
            return max01


def getForce02():
    # Left Hand
    with AdvancedHX711(27, 17, -3082, 115338, Rate.HZ_80) as hx
        while True:
            max02 = max(max02, hx.weight(1))
            return max02


def resetForce(max01, max02):
    max01 = 0
    max02 = 0
    print("Force Reset: {}, {}".format(max01, max02))
    return max01, max02


if __name__ == "__main__":

    getInfo(experiment, group, boxes, mice, trials, initials)

    listener = keyboard.Listener(onPress = 
        lambda event:onPress(
            event, data, max01, max02, 
            experiment, group, boxes, 
            mice, trials, initials, test))
    listener.start()

    p1 = Process(target=getForce01())
    p2 = Process(target=getForce02())
    p1.start()
    p2.start()
    