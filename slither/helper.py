import cv2

def to_col(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

def output_img(name,img, pos, size):
    img = cv2.resize(img, size)
    cv2.imshow(name, img)
    cv2.moveWindow(name, pos[0], pos[1])

    
