import sys
import pygame
import random
from datetime import datetime
from pooh import Pooh
from piglet import Piglet
from tiger import Tiger
from condenced_milk import CondensedMilk  # Import the CondensedMilk class
from honey import Honey  # Import the Honey class

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

    for i in range(10 + random.randint(-4, 10)):
        condensed_milk = CondensedMilk()  # Create a CondensedMilk instance
        condensed_milk.write_to_world(world)  # Add condensed milk to the world

    for i in range(5 + random.randint(-1, 5)):
            honey = Honey()  # Create a Honey instance
            honey.write_to_world(world)  # Add honey to the world
    for i in range(2 + random.randint(-1, 1)):
      pooh = Pooh("Pooh")  # Create a Pooh instance
      pooh.write_to_world(world)  # Add Pooh to the world

    print("\nIf you are reading this it is not ready")
    print(datetime.now().strftime("%A %d %B %Y, %X\n"))

    pygame.init()  # initialize pygame

    screen = pygame.display.set_mode((1500, 900), pygame.FULLSCREEN)  # sets window size
    pygame.display.set_caption("Life Simulator")  # sets window title
    clock = pygame.time.Clock()  # sets clock for framerate
    color_bg = (6, 71, 3)  # sets background color

    player_img_original = pygame.image.load("pooh_img.png").convert_alpha()
    player_img = pygame.transform.smoothscale(player_img_original, (250, 250))

    milk_img_original = pygame.image.load("c_milk_img.png").convert_alpha()
    milk_img = pygame.transform.smoothscale(milk_img_original, (80, 80))

    honey_img_original = pygame.image.load("honey_img.png").convert_alpha()
    honey_img = pygame.transform.smoothscale(honey_img_original, (80, 80))

    running = True  # running variable to keep the game loop running

    print("Available keys in world:", world.keys())
    print("Content of world:", world)

    while running:
        screen.fill(color_bg)  # Fill the screen with background color

        # 1. EVENT INTERFACES (Cleaned up: No entity updates here)
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    running = False

        # 2. GAME STATE MODIFICATIONS (Un-indented so it runs autonomously!)
        for pooh in world["pooh"]:
            moves = pooh.update()  
            pooh.move(moves[0], moves[1])  

        # 3. RENDER ALL ENTITIES
        

        milk_groups = world.get("condensed_milk", [])
        for milk_list in milk_groups:
            for milk in milk_list:
                if milk.shown and hasattr(milk, "position"):
                    current_milk_rect = milk_img.get_rect()
                    current_milk_rect.center = milk.position
                    screen.blit(milk_img, current_milk_rect)

        honey_groups = world.get("honey", [])
        for honey_list in honey_groups:
            for honey in honey_list:
                if honey.shown and hasattr(honey, "position"):
                    current_honey_rect = honey_img.get_rect()
                    current_honey_rect.center = honey.position
                    screen.blit(honey_img, current_honey_rect)

        pooh_list = world.get("pooh", [])
        for pooh in pooh_list:
            if pooh.shown and hasattr(pooh, "position"):
                current_player_rect = player_img.get_rect()
                current_player_rect.center = pooh.position
                screen.blit(player_img, current_player_rect)

        pygame.display.flip()  # Update the display
        clock.tick(60)         # Keep the cycle capped at 60 FPS

    


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
