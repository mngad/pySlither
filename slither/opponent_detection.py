from PIL import ImageGrab
import cv2
import numpy as np
import helper as hlp

class Opponent:
    def __init__(self, midw, midh, img, thresh_img):
        """Class for the detection of enemy snakes. Sets middle of image, the
        image itself and the thresholded image on init

        Parameters:
            midw (int): mid width
            midh (int): mid height
            img (numpy.ndarray): the image
            thresh_img (numpy.ndarray): thresholded image
        """
        self.midw = midw
        self.midh = midh
        self.img = img
        self.thresh_img = thresh_img
        self.marker_type = cv2.MARKER_CROSS



    def findSnakeContours(self):
        """Finds the enemy snake contours from the thresholded image. Takes the
        thresholded image, performs dilate, open and close morpho filters.
        Draws the contours, sets the contour points and rect centers

        """
        img = self.thresh_img

        kernel = np.ones((3, 3), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        kernel = np.ones((10, 10), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

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
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        largecont = []
        numcont = 0
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
        self.contour_points = largecont


    def avoid_snake(self, mode='point'):
        """
        Function to decide the nearest enemy and the "escape vectore"
        
        Parameters:
            mode (str): either 'point' or 'center', which decides the type of
            snake avoidance - center of enemy or edge - point is better but
            with a performance hit.

        Returns:
            self.move_direction (tuple): sets the escape dir

        """

        

        if mode == 'center':
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

        if mode == 'point':
            curr_closest_dist = 80000
            curr_closest_center = []
            for cc in self.contour_points:
                for c in cc:

                    dist = ((c[0][0]-self.midw)**2 + (c[0][1]-self.midh)**2)
                    if dist < curr_closest_dist:
                        curr_closest = dist
                        curr_closest_center = c[0]

            # move_direction
            try:
                diffx = curr_closest_center[0] - self.midw
                diffy = curr_closest_center[1] - self.midh
                move_direction = (self.midw - diffx, self.midh-diffy)
                self.move_direction = move_direction
            except:
                self.move_direction = None

    

    def draw_enemy_pos(self, mode='point'):
        """Draws the enemy position

        Parameters:
            mode (str): either 'point' or 'center', which decides the type of
            snake avoidance - center of enemy or edge - point is better but
            with a performance hit.

        Returns:
            normimg (numpy.ndarray): the normal image with enemies drawn on
            contimg (numpy.ndarray): the contour image with enemies drawn on

            or

            self.img (numpy.ndarray): the normal image
            self.contoured_image (numpy.ndarray): the contour image

        """
        if mode == 'center':

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

        if mode == 'point':

            if self.contour_points:
                for cc in self.contour_points:
                    for c in cc:

                        #print(c[0])
                        contimg = cv2.drawMarker(self.contoured_image,
                                (int(c[0][0]), int(c[0][1])),
                                   color=(0, 0, 255), markerType=self.marker_type,
                                   markerSize=40, thickness=20)
                        normimg = cv2.drawMarker(self.img, (int(c[0][0]), int(c[0][1])),
                                   color=(0, 0, 255), markerType=self.marker_type,
                                   markerSize=40, thickness=20)
                return normimg, contimg
            else: return self.img, self.contoured_image


