"""
Robert Kuramshin
robert.kuramshin@gatech.edu

Part 2 of digitized circles problem 
"""

import cv2
import numpy as np
from scipy.optimize import minimize


def clicked_circe(centers, click, radius):
    """return center of the clicked circle

    Arguments:
        centers {tuple array} -- grid circle centers (x,y) array
        click {tuple} -- coordinates (x,y) of the click
        radius {integer} -- radius of grid circles

    Returns:
        typle -- coordinates of clicked circle (x,y)
    """

    # iterate through all circles until we find within a radius distance of click
    for center in centers:
        if dist(center, click) <= radius:
            return center
    return None


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


def error_fun(args):
    """Error function to be minimized

    Arguments:
        args {tuple} -- argument list (x,y,radius) describing circle

    Returns:
        integer -- error
    """
    global clicked_arr
    global c_radius

    # unpack argument
    x, y, radius = int(args[0]), int(args[1]), int(args[2])

    # determine the number of intersected circles
    n = len(circle_intersects(clicked_arr, c_radius, (x, y), radius))

    # return number of circles selected but not intersected
    return (len(clicked_arr)-n)


def get_centroid(centers):
    """Compute centroid of an list of circle centers

    Arguments:
        centers {tuple array} -- list of circles to be used

    Returns:
        tuple -- coordinates (x,y) of centroid
    """

    # return None if centers array is empty
    if(len(centers) == 0):
        return None

    x = 0  # total x coordinates
    y = 0  # total y coordinates

    # iterate over circle centers and compute total
    for center in centers:
        x += center[0]
        y += center[1]

    # divide by number of samples
    x /= len(centers)
    y /= len(centers)

    return (int(x), int(y))


def avg_distance(centers, point):
    """Find average distance from a point to a list of circle centers

    Arguments:
        centers {tuple array} -- list of circles to be used
        point {tuple} -- coordinate (x,y) of point to reference

    Returns:
        integer -- average distance
    """

    d = 0  # total distance

    # compute and total distance from every circle center to point
    for center in centers:
        d += dist(center, point)  # use euclidean distance

    # divide by number of samples
    d /= len(centers)

    return int(d)


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
    global btn_down
    global background
    global grid_circle_centers
    global c_radius
    global clicked_arr
    global generate
    global image

    # mouse button release
    if event == cv2.EVENT_LBUTTONUP and btn_down:
        btn_down = False

        # if pressed inside generate button
        if(x > generate_x and y > generate_y):
            # compute centroid of selected grid circles
            centroid = get_centroid(clicked_arr)

            # return if no circles selected
            if(centroid is None):
                return

            generate = True  # used to reset image once new circles are selected

            # average distance to all points used as radius guess
            avg_dist = avg_distance(clicked_arr, centroid)

            # use centroid and avg_dist as initial guesses for minimization function
            guess = (centroid[0], centroid[1], avg_dist)

            cv2.circle(image, centroid, avg_dist, (0, 0, 255), 1)  # draw guess

            m = minimize(error_fun, guess, method="Nelder-Mead").x  # minimize

            # draw minimized circle and show
            cv2.circle(image, (int(m[0]), int(m[1])),
                       int(m[2]), (255, 0, 0), 1)
            cv2.imshow("Part 2", image)

        # find clicked circle if any
        clicked = clicked_circe(grid_circle_centers, (x, y), c_radius)

        if clicked:
            # add clicked circle to list of selected circles
            clicked_arr.append(clicked)
            # change color of selected circle and draw
            cv2.circle(image, clicked, c_radius, (255, 0, 0), -1)
            cv2.imshow("Part 2", image)

    # mouse button pressed
    elif event == cv2.EVENT_LBUTTONDOWN:
        btn_down = True

        # circle has been generate and new points are selected
        if generate:
            image = background.copy()  # reset background
            generate = False
            clicked_arr = []  # reset list of selcted points
            cv2.imshow("Part 2", background)  # draw


btn_down = False  # mouse clicked
generate = False  # circle has been generated
clicked_arr = []  # array of selected grid circles

# generate button location
generate_x = 720
generate_y = 780

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

# Draw generate button
cv2.rectangle(background, (generate_x, generate_y),
              (800, 800), (0, 255, 0), -1)

# Keep global copy of background for resetting the screen
image = background.copy()

# draw and start callback
cv2.imshow("Part 2", image)
cv2.setMouseCallback("Part 2", mouse_handler, image)
cv2.waitKey(0)
