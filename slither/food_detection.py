from PIL import ImageGrab
import cv2
import numpy as np
import helper as hlp


class FoodDetection:
    def __init__(self, needle_img, haystack_img):
        self.needle_img = needle_img
        self.haystack_img = haystack_img

    def dist_from(self, x, y):
        centrex = 475
        centrey = 462
        return (((x - centrex)*(x-centrex)) + ((y-centrey)*(y-centrey)))



    def find(self, threshold=0.5, debug_mode=None,
            method=cv2.TM_CCOEFF_NORMED):
        needle_w = self.needle_img.shape[1]
        needle_h = self.needle_img.shape[0]
        # run the OpenCV algorithm
        result = cv2.matchTemplate(self.haystack_img, self.needle_img, method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)

        # Stolen from: https://github.com/learncodebygaming/opencv_tutorials/tree/master/005_real_time
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv2.groupRectangles(
            rectangles, groupThreshold=1, eps=0.5)

        haystack_img = self.haystack_img
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
                    haystack_img = cv2.rectangle(haystack_img, top_left, bottom_right, color=line_color,
                                  lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    haystack_img = cv2.drawMarker(haystack_img, (center_x, center_y),
                                   color=marker_color, markerType=marker_type,
                                   markerSize=40, thickness=2)

        # if debug_mode:
            #cv2.imshow('Matches', haystack_img)
            # cv.waitKey()
            #cv.imwrite('result_click_point.jpg', haystack_img)
        self.points = points
        self.food_vis_img = haystack_img




    def get_closest_point(self, sm=100000, cp=200):

        cl_p = (0, 0)
        for point in self.points:
            #point = np.round(point).astype("int")
            p = self.dist_from(point[0], point[1])
            if p < sm and p > cp:
                sm = p
                cl_p = (point[0], point[1])
                # print(p)
        self.closest_points = cl_p


