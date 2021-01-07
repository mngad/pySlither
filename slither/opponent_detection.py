from PIL import ImageGrab
import cv2
import numpy as np
import helper as hlp

class Opponent:
    def __init__(self, midw, midh, img, thresh_img):
        self.midw = midw
        self.midh = midh
        self.img = img
        self.thresh_img = thresh_img
        self.marker_type = cv2.MARKER_CROSS



    def findSnakeContours(self):
        img = self.thresh_img

        kernel = np.ones((3, 3), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        kernel = np.ones((10, 10), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

        img = cv2.rectangle(img, (0, 0), (self.midw*2, (self.midh-1)*2), (0, 0, 0), 20)
        # surrounding black box to help with contour detection of partial
        # shapes

        img = cv2.rectangle(img, (700, 0), (self.midw*2, (300-1)), (0, 0, 0), -1)
        # covers the leader board
        
        img = cv2.rectangle(img, 
                            ((self.midw *2)-100, (self.midh *2)-100),
                            (self.midw*2, self.midh*2),
                            (0, 0, 0),
                            -1)
        # covers the minimap

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
                dist = ((cent[0]-self.midw)**2 + (cent[1]-self.midh)**2)

                result = cv2.pointPolygonTest(c, (self.midw, self.midh), False)
                # incredibly cool function to check if the contour we found is us
                # or not

                if(result >= 0):
                    continue

                largecont.append(c)
                numcont += 1
                centers.append(cent)


        img = cv2.drawContours(hlp.to_col(img), largecont, -1, (200, 100, 0), 3)

        self.contoured_image = img
        self.centers = centers


    def avoid_snake(self):
        centers = self.centers
        curr_closest_dist = 80000
        curr_closest_center = []
        for center in centers:
            dist = ((center[0]-self.midw)**2 + (center[1]-self.midh)**2)
            if dist < curr_closest_dist:
                curr_closest = dist
                curr_closest_center = center

        # move_direction
        if curr_closest_center:
            diffx = curr_closest_center[0] - self.midw
            diffy = curr_closest_center[1] - self.midh
            move_direction = (self.midw - diffx, self.midh-diffy)
            self.move_direction = move_direction
        else:
            self.move_direction = None

    def draw_enemy_pos(self):

        if self.centers:
            for c in self.centers:
                contimg = cv2.drawMarker(self.contoured_image, (int(c[0]), int(c[1])),
                           color=(0, 0, 255), markerType=self.marker_type,
                           markerSize=40, thickness=20)
                normimg = cv2.drawMarker(self.img, (int(c[0]), int(c[1])),
                           color=(0, 0, 255), markerType=self.marker_type,
                           markerSize=40, thickness=20)
            return normimg, contimg
        else: return self.img, self.contoured_image


