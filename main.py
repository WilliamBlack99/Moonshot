if __name__ == "__main__":
    # initialize modules
    from os.path import join, dirname, realpath
    import pygame
    pygame.init()
    from pygame.locals import *
    import setup
    import power

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
    planet_img_1 = pygame.image.load(join(home_dir, "images/planets/planet_1.png"))
    planet_img_1.convert()
    moon_img_1 = pygame.image.load(join(home_dir, "images/moons/moon_1.png"))
    moon_img_1.convert_alpha()

    # load map
    planet_coords, moon_angles = setup.load_map(join(home_dir, "maps/map_1.txt"))

    # load the planets
    planet_size = 50
    planet_rects, planet_surfaces = setup.load_planets(planet_coords, (planet_img_1,), planet_size)

    # load the moons
    moon_size = 20
    moon_distance = 50
    moon_rects, moon_surfaces, moon_indices = setup.load_moons(planet_rects, moon_angles, (moon_img_1,), moon_size, moon_distance)

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
