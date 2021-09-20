# https://py3.codeskulptor.org/#user306_a7oUKpYTVC_7.py
"""
COMP 614
Homework 1: Circles
"""

import math
import comp614_module1 as circles


def distance(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the 
    distance between them.
    """
    
    # Compute the distance 
    # between two points
    # using the distance formula.
    
    dist = math.sqrt((point0x - point1x) ** 2 + (point0y - point1y) ** 2)
    
    return dist


def midpoint(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the
    midpoint of the line segment between them.
    """
    
    # Compute the x-coordinate 
    # of the midpoint
    # using the midpoint formula
    
    x_m = point0x + ((point1x - point0x)/2)
    
    # Compute the y-coordinate 
    # of the midpoint
    # using the midpoint formula
    
    y_m = point0y + ((point1y - point0y)/2)
    
    return x_m, y_m


def slope(point0x, point0y, point1x, point1y):
    """
    Given the x- and y-coordinates of two points, computes and returns the
    slope of the line segment from (point0x, point0y) to (point1x, point1y).
    """
    
    # Compute the slope 
    # of two points
    # using the slope formula
    
    slope_points = (point1y - point0y)/(point1x - point0x)
    
    return slope_points


def perp(lineslope):
    """
    Given the slope of a line, computes and returns the slope of a line 
    perpendicular to the input slope.
    """
    
    # Compute the slope
    # of the line that is perpendicular
    # to the line of the input slope. 
    
    perpendicular_slope = -1/lineslope
    
    return perpendicular_slope


def intersect(slope0, point0x, point0y, slope1, point1x, point1y):
    """
    Given two lines, where each is represented by its slope and a point
    that it passes through, computes and returns the intersection point
    of the two lines. 
    """
    
    # Compute the x-coordinate 
    # of the intersection point
    # from the two input lines
    # using the formula.
    
    x_i = ((slope0 * point0x) - (slope1 * point1x) + (point1y - point0y))/(slope0 - slope1)
    
    # Compute the y-coordinate 
    # of the intersection point
    # from the two input lines
    # using the formula.
    
    y_i = slope0 * (x_i - point0x) + point0y
    
    return x_i, y_i


def make_circle(point0x, point0y, point1x, point1y, point2x, point2y):
    """
    Given the x- and y-coordinates of three points, computes and returns
    three real numbers: the x- and y-coordinates of the center of the circle
    that passes through all three input points, and the radius of that circle.
    """
    
    # 1. Connect a pair of points with a line.
    
    # Find the slopes of two lines
    # using the slope helper function.
    
    slope_1 = slope(point0x, point0y, point1x, point1y)
    slope_2 = slope(point1x, point1y, point2x, point2y)
    
    # 2. Find the midpoint of that line
    
    # Find the midpoint of the two lines 
    # using the midpoint helper function.
    mid_0_1_x, mid_0_1_y = midpoint(point0x, point0y, point1x, point1y)
    mid_1_2_x, mid_1_2_y = midpoint(point1x, point1y, point2x, point2y)
    
    # Find the two perpendicular line slopes.
    p_slope1 = perp(slope_1)
    p_slope2 = perp(slope_2)
    
    # Find the center of the circle.
    
    # Find the intersect of the two lines 
    # that is perpendicular to the two original lines
    # and passes through the midpoints of the two original lines.
    
    center_x, center_y = intersect(p_slope1, mid_0_1_x, mid_0_1_y, p_slope2, mid_1_2_x, mid_1_2_y)
    
    # Find the radius of the circle.
    # Compute the distance between the center of the circle
    # and one of the input points.
    
    radius = distance(point0x, point0y, center_x, center_y)
    
    return center_x, center_y, radius


# Run GUI - uncomment the line below after you have
#           implemented make_circle
#circles.start(make_circle)