from random import choice
from math import sin, cos, radians
import pygame
pygame.init()


# find the locations of planets and the angles of their moons from a .txt file
# the .txt file should be formatted like this:
#
# planet    1,2     90      120
#
# the first word is a keyword as to what type of object to load
# for planets, the second value is the coordinates
# planets must have at least one angle in degrees after the coords to show the angle of its moons
# each value must be separated by a tab character
def load_map(map_directory):
    planet_coords = []          # will contain the coordinates of all planets
    planet_moon_angles = []     # will contain lists of moons for each planet

    # begin reading the .txt file
    map_1 = open(map_directory, "r")
    for line in map_1.readlines():      # iterate through every line
        line_list = line.split("\t")    # generate a list of values separated by tab characters

        # if the first value is the keyword "planet" generate a planet's location and the angles of its moons
        if line_list[0] == "planet":
            # get the coordinates from the second string in the line
            x, y = line_list[1].split(",")
            x = int(x)
            y = int(y)
            planet_coords.append((x, y))

            # every string past the planet coordinates is the angle of a moon
            # extract those angles and store them in a list of lists
            # (each index in the first list corresponds to all moons of one planet)
            moon_angles = []
            for angle in line_list[2:]:
                moon_angles.append(int(angle))
            planet_moon_angles.append(moon_angles)

    map_1.close()

    return planet_coords, planet_moon_angles


def load_planets(coords, images,  size):
    planet_surfaces = []
    planet_rects = []

    for x, y in coords:
        planet_rects.append(pygame.Rect(x, y, size, size))

        img = pygame.transform.scale(choice(images).copy(), (size, size))
        planet_surfaces.append(img)

    return planet_rects, planet_surfaces


def load_moons(planet_rects, angles, images, size, distance):
    moon_rects = []
    moon_surfaces = []
    moon_indices = []

    for i in range(len(planet_rects)):
        indices = []

        for angle in angles[i]:
            new_rect = pygame.Rect(0, 0, size, size)

            relative_x = int(distance * cos(radians(angle)))
            relative_y = int(distance * sin(radians(angle)))

            new_rect.centerx = planet_rects[i].centerx + relative_x
            new_rect.centery = planet_rects[i].centery + relative_y

            moon_rects.append(new_rect)
            indices.append(len(moon_rects) - 1)

            img = pygame.transform.scale(choice(images).copy(), (size, size))
            moon_surfaces.append(img)

        moon_indices.append(indices)

    return moon_rects, moon_surfaces, moon_indices
