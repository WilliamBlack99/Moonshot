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


# generate a list of rects and a list of surfaces where each index corresponds to a planet
def load_planets(coords, images,  size):
    planet_surfaces = []
    planet_rects = []

    for x, y in coords:
        planet_rects.append(pygame.Rect(x, y, size, size))  # create a rect for the planet

        # copy and scale a random planet image to be the planet surface
        img = pygame.transform.scale(choice(images).copy(), (size, size))
        planet_surfaces.append(img)

    return planet_rects, planet_surfaces


# generate a list of rects and a list of surfaces where each index corresponds to a planet
# also generate a list of lists of where each sublist is a list of moon indices orbiting the corresponding planet
def load_moons(planet_rects, angles, images, size, distance):
    moon_rects = []
    moon_surfaces = []
    moon_indices = []

    for i in range(len(planet_rects)):
        indices = []

        for angle in angles[i]:
            # calculate the moon's position using its planet's position, the distance from the planet, and the angle from the planet
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


def load_power_lists(planet_count, font_size, alpha=255):
    power_font = pygame.font.SysFont(None, font_size, True)

    power = [15 for i in range(planet_count)]
    power_rects = [pygame.Rect(0, 0, 0, 0) for i in range(planet_count)]
    power_surfaces = [pygame.Surface((0, 0)) for i in range(planet_count)]
    power_background_surfaces = [pygame.Surface((0, 0)) for i in range(planet_count)]
    for surface in power_background_surfaces:
        surface.fill((255, 255, 255))
        surface.set_alpha(alpha)

    return power, power_font, power_rects, power_surfaces, power_background_surfaces
