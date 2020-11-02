if __name__ == "__main__":
    # initialize modules
    from os.path import join, dirname, realpath
    import pygame
    pygame.init()
    from pygame.locals import *

    # create game window
    resolution = (800, 600)
    window = pygame.display.set_mode(resolution)

    home_dir = dirname(realpath(__file__))
    planet_1 = pygame.image.load(join(home_dir, "images/planet_1.png"))
    planet_1.convert()

    # game loop
    game_running = True
    while game_running:
        window.fill((50, 50, 50))

        window.blit(planet_1, (0, 0))

        # reflect changes on the window
        pygame.display.update()

        # event handling
        for event in pygame.event.get():

            # quit if x button clicked
            if event.type == QUIT:
                game_running = False
                break
