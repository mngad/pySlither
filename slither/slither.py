import pyautogui
import time
import cv2
import sys
import getopt
from PIL import ImageGrab
import numpy as np
import imutils
from screengrab import ScreenGrab
from opponent_detection import Opponent
from food_detection import FoodDetection
import helper as hlp

def read_args(args):
    bbox = None
    if args:
        if args[0] == "-c":
            bbox = hlp.get_screen_bounds()
            hlp.write_conf(bbox)
    else: bbox = hlp.open_conf()
    return bbox




def main(argv):
    try:

        # try:
        #     opts = getopt.getopt(argv,"h:conf:")
        # except getopt.GetoptError:
        #     print('test.py -conf')
        #     sys.exit(2)
        # for opt, arg in opts:
        #     if opt == '-h':
        #         print 'test.py -conf'
        #         sys.exit()
        #     elif opt in ("--conf", "-c"):
        bbox = read_args(argv)
        screen_grab = ScreenGrab(bbox)

        print(bbox)

        width = int(screen_grab.get_scr().shape[1])
        height = int(screen_grab.get_scr().shape[0])
        midwidth = int(screen_grab.get_scr().shape[1]/2)
        midheight = int(screen_grab.get_scr().shape[0]/2)
        captEdgeDistX = bbox[0]  # for mouse movements
        captEdgeDistY = bbox[1]  # for mouse movements
        marker_color = (255, 0, 255)
        marker_type = cv2.MARKER_CROSS
        loop_time = time.time()

        # an array of the possible template matches, tanks performance when
        # more than on is used and also increases changes of false positives
        needle = [cv2.imread("../blob.png", cv2.IMREAD_UNCHANGED)]
                #cv2.imread("../big_blob.png", cv2.IMREAD_UNCHANGED)]

        while True:
            ogimg = ScreenGrab(bbox)
            og_img = ogimg.get_scr()
            opponent = Opponent(midwidth,
                                midheight,
                                og_img,
                                ogimg.colour_threshold())
            opponent.findSnakeContours()

            food = FoodDetection(needle, og_img, midwidth, midheight)
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


if __name__ == "__main__":
    main(sys.argv[1:])
