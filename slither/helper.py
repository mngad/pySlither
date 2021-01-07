import cv2

def to_col(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

def output_img(img, pos, size):
    img = cv2.resize(img, size)
    cv2.imshow("out", img)
    cv2.moveWindow("out", pos[0], pos[1])

    
