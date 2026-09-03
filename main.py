import sys

import pygame
import random
import math
from datetime import datetime

# Importing modules


def main():
    """Main function where graphic display is proceded"""
    print("\nIf you are reading this it is not ready")
    print(datetime.now().strftime("%A %d %B %Y, %X\n"))

    pygame.init()  # initialize pygame
    desktop_size = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN
    )  # get desktop size

    screen_width, screen_height = desktop_size.get_width(), desktop_size.get_height()

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN) # sets window size
    pygame.display.set_caption("Life Simulator")  # sets window title
    clock = pygame.time.Clock()  # sets clock for framerate
    color_bg = (24, 29, 42)  # sets background color
    running = True  # running variable to keep the game loop running

    while running:
        screen.fill(color_bg)  # fill the screen with background color
        pygame.display.flip()  # update the display

        for event in pygame.event.get():  # iterate through events
            if event.type == pygame.QUIT:  # check if the event is a quit event
                running = False  # set running to False to exit the game loop

            elif event.type == pygame.KEYDOWN:
              if event.key == pygame.K_ESCAPE:  # Press ESC to exit safely
                running = False


            clock.tick(60)  # limit the framerate to 60 frames per second

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
