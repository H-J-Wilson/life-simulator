import random

class CondensedMilk:
    def __init__(self):
        x = random.randint(0, 1500)  # Random x position
        y = random.randint(0, 900)  # Random y position
        self.position = (x, y)  # Set the position of the condensed milk

    def write_to_world(self, world):
        world["condensed_milk"].append([self])  # Add condensed milk to the world