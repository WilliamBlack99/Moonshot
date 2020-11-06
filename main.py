if __name__ == "__main__":
    # initialize modules
    from os.path import join, dirname, realpath
    import pygame
    pygame.init()
    from pygame.locals import *
    import setup
    import power
    import animation

    # create game window
    # window and game_screen are different for future fullscreen support with working resolution
    resolution = (800, 600)
    window = pygame.display.set_mode(resolution)
    game_screen = pygame.surface.Surface(resolution)

    # create game clock
    clock = pygame.time.Clock()
    fps = 60

    # image loading
    home_dir = dirname(realpath(__file__))
 
    # load map
    planet_coords, moon_angles = setup.load_map(join(home_dir, "maps/map_1.txt"))

    # load the planets
    planet_size = 50
    planet_rects = setup.load_planets(planet_coords, planet_size)
    planet_animation_types = ["tundra_planet" for i in range(len(planet_rects))]
    planet_current_frames = [0 for i in range(len(planet_rects))]
    planet_surfaces = [pygame.Surface((0, 0)) for i in range(len(planet_rects))]

    # load the moons
    moon_size = 20
    moon_distance = 50
    moon_rects, moon_indices = setup.load_moons(planet_rects, moon_angles, moon_size, moon_distance)
    moon_animation_types = ["plain_moon" for i in range(len(moon_rects))]
    moon_current_frames = [0 for i in range(len(moon_rects))]
    moon_surfaces = [pygame.Surface((0, 0)) for i in range(len(moon_rects))]

    # load the animations
    animations = {}     # contains tuples of images for each animation
    frames = {}         # contains tuples of integers corresponding to the duration in frames of the animation in animations
    animations["tundra_planet"], frames["tundra_planet"] = animation.load_animation(join(home_dir, "images/planets/tundra_planet"), "tundra", (1,))
    animations["plain_moon"], frames["plain_moon"] = animation.load_animation(join(home_dir, "images/moons/plain_moon"), "moon", (1,))

    # load military power counters
    human_power_font_color = (49, 126, 204)    # blue
    alien_power_font_color = (255, 0, 0)    # red
    old_human_power = []
    old_alien_power = []
    font_size = 35
    alpha = 150
    human_power, human_power_font, human_power_rects, human_power_surfaces, human_power_background_surfaces = setup.load_power_lists(len(planet_rects), font_size, alpha)
    alien_power, alien_power_font, alien_power_rects, alien_power_surfaces, alien_power_background_surfaces = setup.load_power_lists(len(planet_rects), font_size, alpha)

    # game loop
    game_running = True
    while game_running:

        # update animations
        for i in range(len(planet_rects)):
            planet_surfaces[i], planet_current_frames[i] = animation.get_surface(animations[planet_animation_types[i]], frames[planet_animation_types[i]], planet_rects[i], planet_current_frames[i])
        for i in range(len(moon_rects)):
            moon_surfaces[i], moon_current_frames[i] = animation.get_surface(animations[moon_animation_types[i]], frames[moon_animation_types[i]], moon_rects[i], moon_current_frames[i])

        # fill the background
        window.fill((0, 0, 0))
        game_screen.fill((0, 0, 0))

        # display the planets
        for i in range(len(planet_rects)):
            game_screen.blit(planet_surfaces[i], planet_rects[i])

        # display the moons
        for i in range(len(moon_rects)):
            game_screen.blit(moon_surfaces[i], moon_rects[i])

        # update the surfaces, rects, lists for power counters
        if human_power != old_human_power:
            power.update_power_lists(human_power, old_human_power, human_power_rects, human_power_surfaces, human_power_background_surfaces, human_power_font, human_power_font_color)
        if alien_power != old_alien_power:
            power.update_power_lists(alien_power, old_alien_power, alien_power_rects, alien_power_surfaces, alien_power_background_surfaces, alien_power_font, alien_power_font_color)

        #  set the locations for the power counters
        for i in range(len(planet_rects)):
            if human_power[i] and alien_power[i]:
                human_power_rects[i].right = planet_rects[i].centerx
                human_power_rects[i].centery = planet_rects[i].centery
                alien_power_rects[i].left = planet_rects[i].centerx
                alien_power_rects[i].centery = planet_rects[i].centery
            elif human_power[i]:
                human_power_rects[i].center = planet_rects[i].center
            elif alien_power[i]:
                alien_power_rects[i].center = planet_rects[i].center
            else:
                continue

            # display the power counters and their backgrounds
            if human_power[i]:
                game_screen.blit(human_power_background_surfaces[i], human_power_rects[i])
                game_screen.blit(human_power_surfaces[i], human_power_rects[i])
            if alien_power[i]:
                game_screen.blit(alien_power_background_surfaces[i], alien_power_rects[i])
                game_screen.blit(alien_power_surfaces[i], alien_power_rects[i])

        # reflect changes on the window
        clock.tick(fps)
        window.blit(game_screen, (0, 0))
        pygame.display.update()

        # event handling
        for event in pygame.event.get():

            # quit if X button clicked
            if event.type == QUIT:
                game_running = False
                break
            elif event.type == KEYDOWN:

                # quit if ESCAPE is pressed
                if event.key == K_ESCAPE:
                    game_running = False
                    break
