#!/usr/bin/python
#util.py

'''File with function that makes accessible functions to be used by other
modules. Currently only calculates the distance between two given coordinates.'''

__author__ = "Beth Fineberg"
__version__ = "1.0"

import math

def get_distance_between_coords(lat1, lon1, lat2, lon2):
    """calculates the distance between two coordinates specified by user
    
    :param: lat1: the latitude of the first coordinate
    :param: lon1: the longitude of the first coordinate
    :param: lat2: the latitude of the second coordinate
    :param: lon2: the longitude of the second coordinate
    
    :return: distance: the distance between the two coordinates
    """
    #used stack overflow to help with this, I wasn't sure what equationt to use
    pi = 0.017453292519943295 #Pi/180 to convert to radians
    
    #Don't think I've learned the math yet to understand fully, but it works...
    a = 0.5 - math.cos((lat2 - lat1) * pi)/2 + math.cos(lat1 * pi)\
        * math.cos(lat2 * pi) * (1 - math.cos((lon2 - lon1) * pi)) / 2
    distance = 2 * 3959 * math.asin(math.sqrt(a)) #radius of earth * 2 * a sin...
    
    return distance
    
    
    