import random

class CondensedMilk:
    def __init__(self):
        x = random.randint(0, 1500)  # Random x position
        y = random.randint(0, 900)  # Random y position
        self.position = (x, y)  # Set the position of the condensed milk
        

    def write_to_world(self, world):
        world["condensed_milk"].append([self])  # Add condensed milk to the world

    @staticmethod
    def add():
        from main import world  # Import the world dictionary from main.py
        condensed_milk = CondensedMilk()  # Create a new instance of CondensedMilk
        condensed_milk.write_to_world(world)  # Add the new condensed milk to the world