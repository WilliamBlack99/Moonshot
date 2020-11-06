if __name__ == "__main__":
    # initialize modules
    from os.path import join, dirname, realpath
    import pygame
    pygame.init()
    from pygame.locals import *
    import setup

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
    military_power_color = (0, 0, 255)  # blue
    military_power_font = pygame.font.SysFont(None, 40, True)
    #military_power = [None for i in range(len(planet_rects))]
    military_power = [10]   # for testing

    # game loop
    game_running = True
    while game_running:
        # fill the background
        window.fill((0, 0, 0))
        game_screen.fill((50, 50, 50))

        # display the planets
        for i in range(len(planet_rects)):
            game_screen.blit(planet_surfaces[i], planet_rects[i])

        # display the moons
        for i in range(len(moon_rects)):
            game_screen.blit(moon_surfaces[i], moon_rects[i])

        # display the military power of planets
        for i in range(len(military_power)):
            if military_power[i]:
                text_surface = military_power_font.render(str(military_power[i]), True, military_power_color)
                text_rect = pygame.Rect(0, 0, text_surface.get_width(), text_surface.get_height())
                text_rect.center = planet_rects[i].center
                game_screen.blit(text_surface, text_rect)

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
