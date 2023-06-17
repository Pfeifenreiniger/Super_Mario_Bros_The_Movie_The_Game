
import pygame as pg
import math

def check_distance_between_rects(rect1 :pg.Rect, rect2 :pg.Rect, max_distance :int) -> bool:
    """function to pass to any graphical objects except the player.
    It will calculate the distance between said objects and the player's current position in pixels.
    The object's rectangle has to be passed to the parameter 'rect='.
    If the distance between the player's rectangle center position and those of the passed object's rectangle
    center position exceeds the set maximum (parameter 'max_distance=') a boolean false will be returned,
    otherwise true."""

    if math.dist(rect1.center, rect2.center) < max_distance:
        return True
    else:
        return False