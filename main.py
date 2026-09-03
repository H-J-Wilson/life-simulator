import sys
import pygame
from datetime import datetime
from pooh import Pooh
from piglet import Piglet
from tiger import Tiger
from condenced_milk import CondensedMilk  # Import the CondensedMilk class

# Importing modules

world = {
    "pooh": [],
    "piglet": [],
    "tigger": [],
    "honey": [],
    "condensed_milk": [],
}  # sets up empty world lists


def main():
    """Main function where graphic display is proceded"""

    for i in range(5):
        condensed_milk = CondensedMilk()  # Create a CondensedMilk instance
        condensed_milk.write_to_world(world)  # Add condensed milk to the world

    pooh = Pooh("Pooh")  # Create a Pooh instance
    pooh.write_to_world(world)  # Add Pooh to the world

    print("\nIf you are reading this it is not ready")
    print(datetime.now().strftime("%A %d %B %Y, %X\n"))

    pygame.init()  # initialize pygame

    screen = pygame.display.set_mode((1500, 900), pygame.FULLSCREEN)  # sets window size
    pygame.display.set_caption("Life Simulator")  # sets window title
    clock = pygame.time.Clock()  # sets clock for framerate
    color_bg = (24, 29, 42)  # sets background color

    player_img_original = pygame.image.load("pooh_img.png").convert_alpha()
    player_img = pygame.transform.smoothscale(player_img_original, (250, 250))
    player_rect = player_img.get_rect()
    milk_img_original = pygame.image.load("c_milk_img.png").convert_alpha()
    milk_img = pygame.transform.smoothscale(milk_img_original, (80, 80))
    milk_rect = milk_img.get_rect()

    running = True  # running variable to keep the game loop running

    print("Available keys in world:", world.keys())
    print("Content of world:", world)

    while running:
        screen.fill(color_bg)  # fill the screen with background color

        for event in pygame.event.get():  # iterate through events
            if event.type == pygame.QUIT:  # check if the event is a quit event
                running = False  # set running to False to exit the game loop

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to exit safely
                    running = False


        pooh_list = world.get("pooh", [])
        for pooh in pooh_list:
            if hasattr(pooh, "position"):
                player_rect.center = pooh.position
                screen.blit(player_img, player_rect)

        milk_groups = world.get("condensed_milk", [])
        for milk_list in milk_groups:
          for milk in milk_list:
              if hasattr(milk, "position"):
                  # Create a brand new rect copy or a fresh rect for this specific milk
                  current_milk_rect = milk_img.get_rect() 
                  current_milk_rect.center = milk.position
                  
                  # Blit using the individual rectangle
                  screen.blit(milk_img, current_milk_rect)

        pygame.display.flip()  # update the display
        clock.tick(60)  # limit the framerate to 60 frames per second

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
