import pyautogui
import time
import cv2
from PIL import ImageGrab
import numpy as np
import imutils
from screengrab import ScreenGrab
from opponent_detection import Opponent
from food_detection import FoodDetection
import helper as hlp
from multiprocessing import Process


if __name__ == "__main__":
    try:
        screen_grab = ScreenGrab()
        bbox = screen_grab.extent

        width = int(screen_grab.img.shape[1])
        height = int(screen_grab.img.shape[0])
        midwidth = int(screen_grab.img.shape[1]/2)
        midheight = int(screen_grab.img.shape[0]/2)
        captEdgeDistX = bbox[0]  # for mouse movements
        captEdgeDistY = bbox[1]  # for mouse movements
        marker_color = (255, 0, 255)
        marker_type = cv2.MARKER_CROSS
        loop_time = time.time()

        # an array of the possible template matches, tanks performance when
        # more than on is used and also increases changes of false positives
        needle = [cv2.imread("../blob.png", cv2.IMREAD_UNCHANGED),
                cv2.imread("../big_blob.png", cv2.IMREAD_UNCHANGED)]

        while True:
            ogimg = ScreenGrab()
            opponent = Opponent(midwidth,
                                midheight,
                                ogimg.img,
                                ogimg.colour_threshold())

            opponent.findSnakeContours()

            food = FoodDetection(needle, ogimg.img, midwidth, midheight)
            food.find(threshold=0.65, debug_mode='rectangles')
            food.get_closest_point(sm=90000, cp=400)
            img = food.food_vis_img
            clp = food.closest_points
            
            # opponent.draw and opponent.avoid have two varients for point or
            # center of enemy detection, point is more accurate but costs 2 to
            # 4 fps
            img, contimg = opponent.draw_enemy_pos(mode='point')
            opponent.avoid_snake(mode='point')
            avoid_positions = opponent.move_direction
            test = False
            if avoid_positions is None and test == False:

                if (clp != (0, 0)):
                    # _pause defaults to true, creates large slowdown
                    pyautogui.moveTo(clp[0]+captEdgeDistX,
                                     clp[1]+captEdgeDistY,
                                     _pause=False)

                    cv2.drawMarker(img,
                                   (clp[0], clp[1]),
                                   color=marker_color,
                                   markerType=marker_type,
                                   markerSize=40,
                                   thickness=2)
                else:
                    pyautogui.moveTo(midwidth + captEdgeDistX,
                                     midheight + captEdgeDistY,
                                     _pause=False)
                    # _pause defaults to true, creates large slowdown

            elif test == False:
                cv2.drawMarker(img,
                               (int(avoid_positions[0]),
                                int(avoid_positions[1])),
                               color=(0, 100, 255),
                               markerType=marker_type,
                               markerSize=40,
                               thickness=20)

                pyautogui.moveTo(avoid_positions[0] + captEdgeDistX,
                                 avoid_positions[1] + captEdgeDistY,
                                 _pause=False)
            # centre marker
            cv2.drawMarker(img,
                           (midwidth, midheight),
                           color=(55, 255, 255),
                           markerType=marker_type,
                           markerSize=40,
                           thickness=1)

            print('FPS {}'.format(1 / (time.time() - loop_time)))
            loop_time = time.time()

            hlp.output_img("norm", img, (980, 0), (600, 500))
            hlp.output_img("cont",contimg, (980, 600), (400, 300))

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
    except KeyboardInterrupt:
        print('done')
