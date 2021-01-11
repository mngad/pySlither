import cv2
import pyautogui, time

def to_col(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

def output_img(name,img, pos, size):
    img = cv2.resize(img, size)
    cv2.imshow(name, img)
    cv2.moveWindow(name, pos[0], pos[1])

def write_conf(bbox):
    """writes to the config file to set the capture dimensions. """

    f = open("../capture_size.conf","w")
    f.writelines(str(bbox[0])+', '+str(bbox[1])+', '+str(bbox[2])+', '+str(bbox[3]))
    f.close()

def open_conf():
    """Opens the config file to read the capture dimensions. Returns
    a tuple containing the four corners of the capture area"""
    try:
        with open("../capture_size.conf","r") as f:
            bbox = f.readline()
            f.close()
            bbox = tuple(map(int, bbox.split(', ')))


            return (bbox)
    except IOError:
        print("Run `python slither.py -c` first or create the config file `../capture_size.conf`")
        exit()

def get_screen_bounds():
    """
    Gets the screen bounds if the init argument is passed on start.
    Sets the conf file.
    """

    print("Mouse cursor to top left of the slither.io area \n")
    for i in range(5,0,-1):
        print(i)
        time.sleep(1)
    tl = pyautogui.position()
    print('Saved position ' + str(tl))

    print("Mouse cursor to bottom right of the slither.io area \n")
    for i in range(5,0,-1):
        print(i)
        time.sleep(1)
    br = pyautogui.position()
    print('Saved position ' + str(br))
    bbox = (tl[0], tl[1], br[0], br[1])
    print('Capture area = ' + str(bbox))
    return bbox
