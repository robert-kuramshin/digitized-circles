"""
Robert Kuramshin
robert.kuramshin@gatech.edu

Part 1 of digitized circles problem 
"""

import cv2
import numpy as np


def smallest_radius(intersects, radius, drawn_center, drawn_radius):
    """This function finds the smallest circle radius given intersected points and started properties of the circle

    Arguments:
        intersects {tuple array} -- list of circle centers (x,y) that the circle should intersect
        radius {integer} -- radius of the intersected circles
        drawn_center {tuple} -- center coordinates (x,y) for the drawn circle
        drawn_radius {integer} -- starting radius of the drawn circle

    Returns:
        integer -- radius of the smallest circle that interesects the provided points, None on argument error
    """
    r = drawn_radius  # radius to iterate over
    new_intersects = intersects[:]  # list of intersected points for comparison

    # reduce circle radius until we no longer intersect one of the points
    while(len(intersects) == len(new_intersects)):
        r -= 1
        new_intersects = circle_intersects(intersects, radius, drawn_center, r)
    return r+1  # we passed the smallest circle, so increment radius by 1


def biggest_radius(intersects, radius, drawn_center, drawn_radius):
    """This function finds the biggest circle radius given intersected points and started properties of the circle

    Arguments:
        intersects {tuple array} -- list of circle centers (x,y) that the circle should intersect
        radius {integer} -- radius of the intersected circles
        drawn_center {tuple} -- center coordinates (x,y) for the drawn circle
        drawn_radius {integer} -- starting radius of the drawn circle

    Returns:
        integer -- radius of the biggest circle that interesects the provided points, None on argument error
    """
    r = drawn_radius  # radius to iterate over
    new_intersects = intersects[:]  # list of intersected points for comparison

    # increase circle radius until we no longer intersect one of the points
    while(len(intersects) == len(new_intersects)):
        r += 1
        new_intersects = circle_intersects(intersects, radius, drawn_center, r)
    return r-1  # we passed the biggest circle, so increment radius by 1


def circle_intersects(centers, radius, drawn_center, drawn_radius):
    """Find the centers of circles that are intersected by given circle

    Arguments:
        centers {tuple array} -- list of centers (x,y) for points to be checked
        radius {integer} -- radius of the given circles
        drawn_center {tuple} -- center coordinates (x,y) of given circle
        drawn_radius {integer} -- radius of the given circle

    Returns:
        tuple array -- center coordinates (x,y) of from centers array that intersect the given circle
    """
    intersects = []  # list of intersected circle centers

    # iterate through circle center array and compare distance to given circle
    for center in centers:
        d = dist(center, drawn_center)  # euclidean distance

        # if the edge of drawn circle falls inside the grid circle
        if(d <= radius+drawn_radius and d >= drawn_radius-radius):
            intersects.append(center)
    return intersects


def dist(a, b):
    """Compute euclidean distance between two coordinate pairs

    Arguments:
        a {tuple} -- (x,y) coordinates of point one
        b {tuple} -- (x,y) coordinates of point two

    Returns:
        float -- distance between two points
    """
    return np.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)


def mouse_handler(event, x, y, flags, data):
    """Mouse event handler

    Arguments:
        x {integer} -- x coordinate component of event location
        y {integer} -- y coordinate component of event location
        data {numpy array} -- cv2 image passed to handler
    """
    global button_down
    global state
    global circle_center
    global grid_circle_centers
    global c_radius

    # mouse button release
    if event == cv2.EVENT_LBUTTONUP and button_down:
        button_down = False
        image = data.copy()  # create copy of image so that we do not modify the original directly

        if (state == 0):
            state = 1

            # find radius of circle by computing distance from center to current coordinates
            r = int(dist(circle_center, (x, y)))

            # find all overlapped grid circles
            overlapped = circle_intersects(
                grid_circle_centers, c_radius, circle_center, r)

            # if no circles overlapped then return
            if len(overlapped) == 0:
                cv2.imshow("Part 1", image)
                return

            # color overlapped circles blue
            for circle in overlapped:
                cv2.circle(image, circle, c_radius, (255, 0, 0), -1)

            # find smallest and biggest circles given overlapped points
            sr = smallest_radius(overlapped, c_radius, circle_center, r)
            br = biggest_radius(overlapped, c_radius, circle_center, r)

            # draw and show all circles
            cv2.circle(image, circle_center, r, (255, 0, 0), 2)
            cv2.circle(image, circle_center, sr, (0, 0, 255), 1)
            cv2.circle(image, circle_center, br, (0, 0, 255), 1)
            cv2.imshow("Part 1", image)

    # mouse dragging
    elif event == cv2.EVENT_MOUSEMOVE and button_down:
        image = data.copy()  # create copy of image so that we do not modify the original directly

        if state == 0:
            # find radius of the circle so far
            r = int(dist(circle_center, (x, y)))

            # find overlapped circles so far
            overlapped = circle_intersects(
                grid_circle_centers, c_radius, circle_center, r)

            # color overlapped circles blue
            for circle in overlapped:
                cv2.circle(image, circle, c_radius, (255, 0, 0), -1)

            # draw in progress redius line and circle
            cv2.line(image, circle_center, (x, y), (0, 0, 0), 1)
            cv2.circle(image, circle_center, int(
                dist(circle_center, (x, y))), (255, 0, 0), 2)
            cv2.imshow("Part 1", image)

    # mouse button pressed
    elif event == cv2.EVENT_LBUTTONDOWN:
        button_down = True

        if(state == 1):
            # just clear image and continue
            cv2.imshow("Part 1", data)
            state = 0
        if(state == 0):
            # set circle center
            circle_center = (x, y)


state = 0  # state machine variable, state=0 waiting for center of circle to be selected, state=1 center of circle selected
button_down = False  # mouse clicked
circle_center = (0, 0)  # center of selected circle

# image dimensions
image_height = 800
image_width = 800

# grid parameters
n_dots_h = 20
n_dots_v = 20

# grid circle size
c_radius = 10

# create white image
background = 255 * np.ones((image_height, image_width, 3), np.uint8)

# calculate horizontal and vertical distances between grid circles
h_offset = int(image_height/(n_dots_h+1))
v_offset = int(image_width/(n_dots_v+1))

# array of grid circle centers
grid_circle_centers = []

# iteratively draw grid circles and populate grid_circle_centers
for i in range(1, n_dots_h+1):
    for j in range(1, n_dots_v+1):
        grid_circle_centers.append((i*h_offset, j*v_offset))
        cv2.circle(background, (i*h_offset, j*v_offset),
                   c_radius, (100, 100, 100), -1)

# draw and start callback
cv2.imshow("Part 1", background)
cv2.setMouseCallback("Part 1", mouse_handler, background.copy())
cv2.waitKey(0)
