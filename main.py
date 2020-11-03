if __name__ == "__main__":
    # initialize modules
    from os.path import join, dirname, realpath
    import pygame
    pygame.init()
    from pygame.locals import *

    # create game window
    # window and game_screen are different for future fullscreen support with working resolution
    resolution = (800, 600)
    window = pygame.display.set_mode(resolution)
    game_screen = pygame.surface.Surface(resolution)

    # image loading
    home_dir = dirname(realpath(__file__))
    planet_img_1 = pygame.image.load(join(home_dir, "images/planet_1.png"))
    planet_img_1.convert()

    # create visible game object surfaces
    planet_size = (50, 50)
    planet_1 = planet_img_1.copy()
    planet_1 = pygame.transform.scale(planet_1, planet_size)

    # game loop
    game_running = True
    while game_running:
        window.fill((0, 0, 0))
        game_screen.fill((50, 50, 50))

        game_screen.blit(planet_1, (0, 0))

        # reflect changes on the window
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
