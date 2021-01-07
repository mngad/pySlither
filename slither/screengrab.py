from PIL import ImageGrab
import cv2
import numpy as np

class ScreenGrab:
    def __init__(self):
        self.extent = self.open_conf()
        self.img = self.get_scr() 
        
    def open_conf(self):
        f = open("../capture_size.conf","r")
        bbox = f.readline()
        f.close()
        bbox = tuple(map(int, bbox.split(', ')))
        return (bbox)

    def get_scr(self):

        img = ImageGrab.grab(bbox=self.extent)
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


    def toGray(self):
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        #img_gray = cv2.GaussianBlur(img_gray, (7, 7), 0)

        return img_gray


    def to_col(self):
        img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
        return img

    def colour_threshold(self):
        # colour order is blue, green, red
        #img = cv2.GaussianBlur(img, (7, 7), 0)
        lower_color_bounds = (10, 10, 30)
        upper_color_bounds = (200, 200, 200)
        mask = cv2.inRange(self.img, lower_color_bounds, upper_color_bounds)
        return mask

