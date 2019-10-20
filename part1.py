import cv2
import numpy as np

btn_down = False

'''
0 placing circle center
3
4
'''
state = 0
click_start = (0,0)
circle_center = (0,0)

def smallest_radius(intersects,radius,drawn_center,drawn_radius):
    r = drawn_radius
    new_intersects = intersects[:]
    while(len(intersects) == len(new_intersects)):
        r-=1 
        new_intersects = circle_intersects(intersects,radius,drawn_center,r)
    return r+1

def biggest_radius(intersects,radius,drawn_center,drawn_radius):
    r = drawn_radius
    new_intersects = intersects[:]
    while(len(intersects) == len(new_intersects)):
        r+=1
        new_intersects = circle_intersects(intersects,radius,drawn_center,r)
    return r-1

def circle_intersects(centers,radius,drawn_center,drawn_radius):
    intersects = []
    for center in centers:
        d = dist(center,drawn_center)
        if(d <= radius+drawn_radius and d>= drawn_radius-radius):
            intersects.append(center)
    return intersects

def dist(a,b):
    return np.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

def mouse_handler(event, x, y, flags, data):
    global btn_down
    global state
    global background
    global click_start
    global circle_center
    global circle_centers
    global c_radius

    if event == cv2.EVENT_LBUTTONUP and btn_down:
        btn_down = False
        image = data.copy()
        if (state == 0):
            state=1
            r = int(dist(circle_center,(x,y)))
            overlapped = circle_intersects(circle_centers,c_radius,circle_center,r)
            if len(overlapped) == 0:
                cv2.imshow("Image", image)
                return
            for circle in overlapped:
                cv2.circle(image, circle, c_radius, (255, 0, 0), -1)
            sr = smallest_radius(overlapped,c_radius,circle_center,r)
            br = biggest_radius(overlapped,c_radius,circle_center,r)
            cv2.circle(image, circle_center, r, (255, 0, 0), 2)
            cv2.circle(image, circle_center, sr, (0, 0, 255), 1)
            cv2.circle(image, circle_center, br, (0, 0, 255), 1)
            cv2.imshow("Image", image)

    elif event == cv2.EVENT_MOUSEMOVE and btn_down:
        image = data.copy()
        if state == 0:
            r = int(dist(circle_center,(x,y)))
            overlapped = circle_intersects(circle_centers,c_radius,circle_center,r)
            for circle in overlapped:
                cv2.circle(image, circle, c_radius, (255, 0, 0), -1)
            cv2.line(image, circle_center, (x, y), (0,0,0), 1)
            cv2.circle(image, circle_center, int(dist(circle_center,(x,y))), (255, 0, 0), 2)
            cv2.imshow("Image", image)

    elif event == cv2.EVENT_LBUTTONDOWN:
        btn_down = True
        if(state ==1):
            cv2.imshow("Image", data)
            state=0
        if(state == 0):
            circle_center = (x,y)


image_height = 800
image_width = 800

n_dots_h = 20
n_dots_v = 20

background = 255 * np.ones((image_height,image_width,3), np.uint8)


c_radius = 10
h_offset = int(image_height/(n_dots_h+1))
v_offset = int(image_width/(n_dots_v+1))

circle_centers = []

for i in range(1,n_dots_h+1):
    for j in range(1,n_dots_v+1):
        circle_centers.append((i*h_offset, j*v_offset))
        cv2.circle(background, (i*h_offset, j*v_offset), c_radius, (100, 100, 100), -1)

cv2.imshow("Image", background)
cv2.setMouseCallback("Image", mouse_handler, background.copy())
cv2.waitKey(0)
