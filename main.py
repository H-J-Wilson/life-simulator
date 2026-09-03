import sys
import pygame
import random
from datetime import datetime

from pooh import Pooh
from piglet import Piglet
from tiger import Tiger
from honey import Honey
from condensed_milk import CondensedMilk

world = {"pooh": [],
         "piglet": [],
         "tiger": [],
         "honey": [],
         "condensed_milk": []}


def main(world):

    for i in range(5):
        CondensedMilk.add_to_world

    pygame.init()
    bg_clour = (20, 70, 20)
    screen = pygame.display.set_mode((1500, 900))
    pygame.display.set_caption('Evolution Simulator')
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        img_character = pygame.image.load("pooh.png")

        screen.fill(bg_clour)
        pygame.display.flip()

        milk_list = world.get("condensed_milk")
        for milk in milk_list:


        clock.tick(60)  # limits FPS to 60

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(world)