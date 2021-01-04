import pyautogui
import time
import cv2

import numpy as np
import imutils

dur=0.01


def circle(mult):
    while True:
        pyautogui.moveRel(mult*1, mult*-1, duration=dur)
        pyautogui.moveRel(mult*1, 0, duration=dur)
        pyautogui.moveRel(mult*1, mult*1, duration=dur)
        pyautogui.moveReal(0, mult*1,duration=dur)
        pyautogui.moveRel(mult*-1, mult*1,duration=dur)
        pyautogui.moveRel(mult*-1, 0,duration=dur)
        pyautogui.moveRel(mult*-1, mult*-1,duration=dur)
        pyautogui.moveRel(0, mult*-1,duration=dur)

def hough(img):
        #resized = imutils.resize(img, width=1000)
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_gray = cv2.GaussianBlur(img_gray, (7, 7), 0)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1.1, minDist=15,
                     param1=50, param2=18, minRadius=1, maxRadius=22)

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(img, (x, y), r, (0, 255, 255), 4)
            cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            # show the output image
    cv2.imshow("output", img)
    cv2.waitKey(0)

try:
    #pyautogui.moveTo(460, 510, duration=0.25)
    #circle(mult=100) 
    for i in range(100):
        img = pyautogui.screenshot(region=(50, 100,960,900))
        img = np.array(img)
        hough(img)
        time.sleep(1)
except KeyboardInterrupt:
    print('done')
