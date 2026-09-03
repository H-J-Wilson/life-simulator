import random

class Honey:
    def __init__(self):
        x = random.randint(0, 1500)  # Random x position
        y = random.randint(0, 900)  # Random y position
        self.position = (x, y)  # Set the position of the honey
        self.shown = True  # Mark the honey as visible

    def write_to_world(self, world):
        world["honey"].append([self])  # Add honey to the world
