from PIL import ImageGrab
import cv2
import numpy as np
import helper as hlp


class FoodDetection:
    def __init__(self, needle_img_ar, haystack_img, midw, midh):
        """Class for all of the food detection and nearest food identification.
        Takes an list of needles to be identified and the haystack image to
        find the needle in.

        Parameters:
            midw (int): mid width
            midh (int): mid height
            needle_img_ar ([numpy.ndarray]): list of the needles
            haystack_img (numpy.ndarray): the haystack or normal img
        """
        self.needle_img_ar = needle_img_ar
        self.haystack_img = haystack_img
        self.midw = midw
        self.midh = midh

    def dist_from(self, x, y):
        """Finds the distance from the point x, y to the center, returns the
        distance/ hypotenuse
            
            x (int): x position
            y (int): y position

        """
        return ((x - self.midw)**2 + ((y-self.midh)**2))



    def find(self, threshold=0.5, debug_mode=None,method=cv2.TM_CCOEFF_NORMED):
        """Finds the food. Takes a theshhold, sensible value above 0.5, below
        0.2 causes it to hang. Debug mode gives choice of rectangle or point
        for food identification. Method can be changed, but TM_CCOEFF_NORMED
        was the most reliable. Updates points list of food, and haystack image
        for vis.

        Parameters:
            threshold (float): threshold for matching
            debug_mode (str): None, rectangle or point for type of drawing
            method (cv2 / (int)): method used for matching
        """

        points = []
        haystack_img = self.haystack_img
        count = 0
        for needle_img in self.needle_img_ar:
            needle_w = needle_img.shape[1]
            needle_h = needle_img.shape[0]
            # run the OpenCV algorithm
            result = cv2.matchTemplate(self.haystack_img, needle_img, method)

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

            if len(rectangles):
                #print('Found needle.')

                line_color = (count*155, 255, 0)
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

            count += 1

        self.points = points
        self.food_vis_img = haystack_img




    def get_closest_point(self, sm=100000, cp=200):
        """Finds the closest item of food. Takes the point list from find(), sm
        is the initial furthest it should look and cp is the closest it should
        search. Sets self.closest_points for mouse movement in main().
        
        sm (int)
        cp (int)

        """

        cl_p = (0, 0)
        for point in self.points:
            #point = np.round(point).astype("int")
            p = self.dist_from(point[0], point[1])
            if p < sm and p > cp:
                sm = p
                cl_p = (point[0], point[1])
                # print(p)
        self.closest_points = cl_p


