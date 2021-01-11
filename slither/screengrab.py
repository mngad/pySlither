from PIL import ImageGrab
import cv2
import numpy as np


class ScreenGrab:
    def __init__(self, bbox=None):
        """Class contains the grabbing the image and most of the image
        manipulation. Calls self.extent() and self.get_scr() on init"""

        self.extent = bbox
        self.img = None





    def get_scr(self):
        """Grabs the image based on the extent function. Returns the image as
        an RGB (cv2 defaults to BGR)"""

        img = ImageGrab.grab(bbox=self.extent)

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # This makes the colours "normal" but costs ~1 fps
        self.img = img
        return img


    def toGray(self):
        """Takes self.img and returns a grayscale image"""

        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        #img_gray = cv2.GaussianBlur(img_gray, (7, 7), 0)

        return img_gray


    def to_col(self):
        """Takes a grayscale image and returns and colour image - useful for
        drawing colour on a gray image"""

        img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
        return img

    def colour_threshold(self):
        """Takes the self.img and applied two inrange filters (the second one
        is for the colour orange...) and combines them, returns the combined
        image. Used for the contour detection"""

        # colour order is blue, green, red
        #img = cv2.GaussianBlur(img, (7, 7), 0)
        lower_color_bounds = (10, 10, 40)
        upper_color_bounds = (230, 230, 230)
        mask = cv2.inRange(self.img, lower_color_bounds, upper_color_bounds)
        lower_color_bounds2 = (0, 0, 120)
        upper_color_bounds2 = (50, 100, 255)
        mask2 = cv2.inRange(self.img, lower_color_bounds2, upper_color_bounds2)
        maskf = cv2.addWeighted(mask, 1, mask2, 1, 0)
        return maskf
