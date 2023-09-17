import sys
import os
import argparse
import time
import datetime
import cv2
import numpy as np
from enum import Enum
from threading import Timer
import pyautogui

from eye_tracker2 import EyeTracker




class Mode(Enum):
    AWAITING = 0
    READING = 1
    ANSWERING = 2
    BEGINNING = 3
    COMPLETED = 4

RES_SCREEN = pyautogui.size() # RES_SCREEN[0] -> width
                              # RES_SCREEN[1] -> heigth

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 360

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

TIME_READING = 5
TIME_ANSWERING = 5

mode = Mode.BEGINNING



def nothing(val):
    pass


def main():
    global mode

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    eye_tracker = EyeTracker()




    quiz = None
    cv2.namedWindow("frame")


##    os.makedirs("./images", exist_ok=True)

    while True:
        print(mode)

        _, frame = camera.read()

        start = time.time()
        eye_tracker.update(frame)
        end = time.time()

        print("TIME: {:.3f} ms".format(end*1000 - start*1000))

        dec_frame = eye_tracker.decorate_frame()
        dec_frame = cv2.resize(dec_frame,(int(FRAME_WIDTH / 1.5), int(FRAME_HEIGHT / 1.5)))

        cv2.namedWindow("frame")
        cv2.moveWindow("frame", int(RES_SCREEN[0] / 2 - FRAME_WIDTH / 3), 1 + 75)
        cv2.imshow('frame', dec_frame)


        direction = eye_tracker.get_looking_direction()
        print("DIRECTION: {}".format(direction))




        k = cv2.waitKey(1) & 0xff




    camera.release()
    cv2.destroyAllWindows()
    os._exit(0)

if __name__ == '__main__':
    main()