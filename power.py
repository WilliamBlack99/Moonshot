from random import randint
import pygame
pygame.init()


def fight(human_power, alien_power, planet_index):
    human_strength = human_power[planet_index]
    alien_strength = alien_power[planet_index]

    if human_strength == alien_strength:
        if randint(0, 1):
            human_strength -= 1
        else:
            alien_strength -= 1

    human_power[planet_index] -= alien_strength
    alien_power[planet_index] -= human_strength

    if human_power[planet_index] < 0:
        human_power[planet_index] = 0

    if alien_power[planet_index] < 0:
        alien_power[planet_index] = 0

    return human_power, alien_power


def update_power_lists(power, old_power, power_rects, power_surfaces, power_background_surfaces, power_font, power_font_color):
    for i in range(len(power)):
        power_surfaces[i] = power_font.render(str(power[i]), True, power_font_color)
        power_rects[i] = pygame.Rect(0, 0, power_surfaces[i].get_width(), power_surfaces[i].get_height())
        power_background_surfaces[i] = pygame.transform.scale(power_background_surfaces[i], power_rects[i].size)

        old_power = power
