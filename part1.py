btn_down = False

def get_points(im):
    data = {}
    data['im'] = im.copy()
    data['lines'] = []

    cv2.imshow("Image", im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)

    points = np.uint16(data['lines'])

    return points, data['im']

def mouse_handler(event, x, y, flags, data):
    global btn_down

    if event == cv2.EVENT_LBUTTONUP and btn_down:
        btn_down = False
        data['lines'][0].append((x, y)) 
        cv2.circle(data['im'], (x, y), 3, (0, 0, 255),5)
        cv2.line(data['im'], data['lines'][0][0], data['lines'][0][1], (0,0,255), 2)
        cv2.imshow("Image", data['im'])

    elif event == cv2.EVENT_MOUSEMOVE and btn_down:
        image = data['im'].copy()
        cv2.line(image, data['lines'][0][0], (x, y), (0,0,0), 1)
        cv2.imshow("Image", image)

    elif event == cv2.EVENT_LBUTTONDOWN and len(data['lines']) < 2:
        btn_down = True
        data['lines'].insert(0,[(x, y)])
        cv2.circle(data['im'], (x, y), 3, (0, 0, 255), 5, 16)
        cv2.imshow("Image", data['im'])


import cv2
import numpy as np
img = 255 * np.ones((400,400,3), np.uint8)
pts, final_image = get_points(img)
cv2.imshow('Image', final_image)
print (pts)
cv2.waitKey(0)