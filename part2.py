import cv2
import numpy as np
from scipy.optimize import minimize

btn_down = False

'''
0 placing circle center
3
4
'''
state = 0
click_start = (0,0)
circle_center = (0,0)
clicked_arr = []
generate = False

def clicked_circe(centers,click,radius):
    for center in centers:
        if dist(center,click)<=radius:
            return center
    return None


def circle_intersects(centers,radius,drawn_center,drawn_radius):
    intersects = []
    for center in centers:
        d = dist(center,drawn_center)
        if(d <= radius+drawn_radius and d>= drawn_radius-radius):
            intersects.append(center)
    return intersects

def error_fun(args):
    global clicked_arr
    global c_radius
    x,y,radius = int(args[0]),int(args[1]),int(args[2])
    n = len(circle_intersects(clicked_arr,c_radius,(x,y),radius))
    return (len(clicked_arr)-n)

def get_centroid(centers):
    if(len(centers) == 0):
        return None
    x=0
    y=0
    for center in centers:
        x+=center[0]
        y+=center[1]
    x /= len(centers)
    y /= len(centers)
    return (int(x),int(y))

def avg_distance(centers,point):
    d = 0
    for center in centers:
        d+=dist(center,point)
    d/=len(centers)
    return int(d)

def dist(a,b):
    return np.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

def mouse_handler(event, x, y, flags, data):
    global btn_down
    global state
    global background
    global circle_centers
    global c_radius
    global clicked_arr
    global generate
    global image

    if event == cv2.EVENT_LBUTTONUP and btn_down:
        btn_down = False

        if(x>720 and y>780):
            centroid = get_centroid(clicked_arr)
            if(centroid is None):
                return

            generate = True
            avg_dist = avg_distance(clicked_arr,centroid)
            guess = (centroid[0],centroid[1],avg_dist)
            cv2.circle(image, centroid, avg_dist, (0, 0, 255), 1)
            m = minimize(error_fun,guess,method="Nelder-Mead").x
            cv2.circle(image, (int(m[0]),int(m[1])), int(m[2]), (255, 0, 0), 1)
            cv2.imshow("Part 2", image)

        clicked = clicked_circe(circle_centers,(x,y),c_radius)
        if clicked:
            clicked_arr.append(clicked)
            cv2.circle(image, clicked, c_radius, (255, 0, 0), -1)
            cv2.imshow("Part 2", image)

    elif event == cv2.EVENT_LBUTTONDOWN:
        btn_down = True
        if generate:
            image = background.copy()
            generate = False
            clicked_arr = []
            cv2.imshow("Part 2", background)



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

cv2.rectangle(background, (720,780), (800,800), (0,255,0),-1)
image =background.copy()

cv2.imshow("Part 2", image)
cv2.setMouseCallback("Part 2", mouse_handler, image)
cv2.waitKey(0)
