import pyautogui
import time
import cv2
from PIL import ImageGrab
import numpy as np
import imutils


def circle(mult):
    while True:
        pyautogui.moveRel(mult*1, mult*-1, duration=dur)
        pyautogui.moveRel(mult*1, 0, duration=dur)
        pyautogui.moveRel(mult*1, mult*1, duration=dur)
        pyautogui.moveRel(0, mult*1, duration=dur)
        pyautogui.moveRel(mult*-1, mult*1, duration=dur)
        pyautogui.moveRel(mult*-1, 0, duration=dur)
        pyautogui.moveRel(mult*-1, mult*-1, duration=dur)
        pyautogui.moveRel(0, mult*-1, duration=dur)


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
            dist = distFrom(x, y)

            if(dist < 20000 and dist > 10000):
                pyautogui.moveTo(x+50, y+100, duration=0)
                #drawCirc(x, y, r)


def distFrom(x, y):
    centrex = 475
    centrey = 462
    return (((x - centrex)*(x-centrex)) + ((y-centrey)*(y-centrey)))


def drawCirc(x, y, r):
    cv2.circle(img, (x, y), r, (0, 255, 255), 4)
    cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    # show the output image
    cv2.imshow("output", img)
    cv2.waitKey(1)


def find(needle_img, haystack_img, threshold=0.5, debug_mode=None,
         method=cv2.TM_CCOEFF_NORMED):
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    # run the OpenCV algorithm
    result = cv2.matchTemplate(haystack_img, needle_img, method)

    # Get the all the positions from the match result that exceed our threshold
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    # print(locations)

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        # Add every box to the list twice in order to retain single (non-overlapping) boxes
        rectangles.append(rect)
        rectangles.append(rect)

    # Stolen from: https://github.com/learncodebygaming/opencv_tutorials/tree/master/005_real_time
    # Apply group rectangles.
    # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
    # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
    # in the result. I've set eps to 0.5, which is:
    # "Relative difference between sides of the rectangles to merge them into a group."
    rectangles, weights = cv2.groupRectangles(
        rectangles, groupThreshold=1, eps=0.5)

    points = []
    if len(rectangles):
        #print('Found needle.')

        line_color = (0, 255, 0)
        line_type = cv2.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv2.MARKER_CROSS

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:

            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                # Determine the box position
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                cv2.rectangle(haystack_img, top_left, bottom_right, color=line_color,
                              lineType=line_type, thickness=2)
            elif debug_mode == 'points':
                cv2.drawMarker(haystack_img, (center_x, center_y),
                               color=marker_color, markerType=marker_type,
                               markerSize=40, thickness=2)

    # if debug_mode:
        #cv2.imshow('Matches', haystack_img)
        # cv.waitKey()
        #cv.imwrite('result_click_point.jpg', haystack_img)

    return haystack_img, points


def getScr():
    f = open("capture_size.conf","r")
    bbox = f.readline()
    f.close()
    bbox = tuple(map(int, bbox.split(', '))) 
    #print(bbox)
    img = ImageGrab.grab(bbox=bbox)
    # 910x 800
    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
    img = np.ascontiguousarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # This makes the colours "normal" but costs ~1 fps

    return img


def toGray(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #img_gray = cv2.GaussianBlur(img_gray, (7, 7), 0)

    return img_gray


def toCol(img):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return img


def closestPoint(points, sm=100000, cp=200):

    smolPoint = sm
    clP = (0, 0)
    for point in points:
        #point = np.round(point).astype("int")
        p = distFrom(point[0], point[1])
        if p < smolPoint and p > cp:
            smolPoint = p
            clP = (point[0], point[1])
            # print(p)
    return clP


def colourThreshold(img):
    # colour order is blue, green, red
    #img = cv2.GaussianBlur(img, (7, 7), 0)

    lower_color_bounds = (10, 10, 30)
    upper_color_bounds = (200, 200, 200)
    mask = cv2.inRange(img, lower_color_bounds, upper_color_bounds)
    return mask


def findSnakeContours(thresholdedimg, ogimg, midw, midh):
    img = thresholdedimg
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    kernel = np.ones((10, 10), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    img = cv2.rectangle(img, (0, 0), (midw*2, (midh-1)*2), (0, 0, 0), 20)

    img = cv2.rectangle(img, (700, 0), (midw*2, (300-1)), (0, 0, 0), -1)

    #img = cv2.Canny(toGray(ogimg), threshold, threshold*2)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_NONE)
    largecont = []
    numcont = 0
    rectarr = []
    centers = []
    for c in contours:
        if(cv2.contourArea(c) > 3000):
            x, y, w, h = cv2.boundingRect(c)
            cent = (x+w/2, y+h/2)
            dist = ((cent[0]-midw)**2 + (cent[1]-midh)**2)

            result = cv2.pointPolygonTest(c, (midw, midh), False)
            # incredibly cool function to check if the contour we found is us
            # or not

            if(result >= 0):
                continue

            # print(dist)
#            if dist < 70000:
            largecont.append(c)
            numcont += 1

            # centers.append((x+((w-x)/2),y+((h-y)/2)))
            centers.append(cent)
            #img = cv2.rectangle(ogimg,(x,y),(x+w,y+h),(0,255,0),2)
    # print(centers)
    # print(numcont)
    img = cv2.drawContours(toCol(img), largecont, -1, (200, 100, 0), 3)
    return img, centers


def avoidSnake(centers, midw, midh):

    curr_closest_dist = 80000
    curr_closest_center = []
    for center in centers:
        dist = ((center[0]-midw)**2 + (center[1]-midh)**2)
        if dist < curr_closest_dist:
            curr_closest = dist
            curr_closest_center = center

    # move_direction
    if curr_closest_center:
        diffx = curr_closest_center[0] - midw
        diffy = curr_closest_center[1] - midh
        move_direction = (midw - diffx, midh-diffy)
        return move_direction
    else:
        return None


if __name__ == "__main__":
    try:

        f = open("capture_size.conf","r")
        bbox = f.readline()
        f.close()
        bbox = tuple(map(int, bbox.split(', ')))

        width = int(getScr().shape[1])
        height = int(getScr().shape[0])
        midwidth = int(getScr().shape[1]/2)
        midheight = int((getScr().shape[0]+115)/2)
        # 115 to account for cutting the bottom off to remove minimap
        captEdgeDistX = bbox[0]  # for mouse movements
        captEdgeDistY = bbox[1]  # for mouse movements
        marker_color = (255, 0, 255)
        marker_type = cv2.MARKER_CROSS
        #pyautogui.moveTo(460, 510, duration=0.25)
        # circle(mult=100)
        loop_time = time.time()
        offset = (midheight - 200, midwidth - 200)
        needle = cv2.imread("blob.png", cv2.IMREAD_UNCHANGED)

        while True:
            ogimg = getScr()
            contimg, cent = findSnakeContours(colourThreshold(ogimg), ogimg, midwidth,
                                              midheight)
            img, points = find(needle, (ogimg), 0.65, debug_mode='rectangles')
            clp = closestPoint(points, sm=50000, cp=400)

            for c in cent:
                cv2.drawMarker(img, (int(c[0]), int(c[1])),
                               color=(0, 0, 255), markerType=marker_type,
                               markerSize=40, thickness=20)

            avoid_positions = avoidSnake(cent, midwidth, midheight)

            # print(avoid_positions)
            if avoid_positions is None:

                if (clp != (0, 0)):
                    # _pause defaults to true, creates large slowdown
                    pyautogui.moveTo(clp[0]+captEdgeDistX,
                                     clp[1]+captEdgeDistY, _pause=False)

                    cv2.drawMarker(img, (clp[0], clp[1]),
                                   color=marker_color, markerType=marker_type,
                                   markerSize=40, thickness=2)
                else:
                    pyautogui.moveTo(midwidth + captEdgeDistX,
                                     midheight + captEdgeDistY, _pause=False)
                    # _pause defaults to true, creates large slowdown

            else:
                cv2.drawMarker(img, (int(avoid_positions[0]), int(avoid_positions[1])),
                               color=(0, 100, 255), markerType=marker_type,
                               markerSize=40, thickness=20)

                pyautogui.moveTo(avoid_positions[0] + captEdgeDistX,
                                 avoid_positions[1] + captEdgeDistY, _pause=False)
            # centre marker
            cv2.drawMarker(img, (midwidth,
                                 midheight), color=(55, 255, 255), markerType=marker_type,
                           markerSize=40, thickness=1)

            print('FPS {}'.format(1 / (time.time() - loop_time)))
            loop_time = time.time()
            img = cv2.resize(img, (600, 500))
            cv2.imshow("out", img)
            cv2.moveWindow("out", 980, 20)
            contimg = cv2.resize(contimg, (400, 300))
            cv2.imshow("out2", contimg)
            cv2.moveWindow("out2", 980, 600)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
    except KeyboardInterrupt:
        print('done')
