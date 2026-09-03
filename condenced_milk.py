import random
import math

class CondensedMilk:
    def __init__(self):
        start_x = random.randint(100, 1400)
        start_y = random.randint(100, 800)
        self.position = (start_x, start_y)
        self.shown = True

    def write_to_world(self, world):
        world["condensed_milk"].append([self])  # Add condensed milk to the world

    @staticmethod
    def add():
        from main import world
        
        # LOGARITHMIC SPAWN QUANTITY SELECTION
        u = random.random()
        if u == 0: u = 0.0001 # Boundary guard against log(0) exceptions
        
        # Scale distribution density heavily towards low numbers
        milk_count = 1 + int(-2.5 * math.log(u))
        milk_count = max(1, min(milk_count, 7))  # Enforces bounds strictly from 1 to 7
        
        for _ in range(milk_count):
            new_milk = CondensedMilk()
            # Maintains matching nested world structural requirements [[obj], [obj]]
            world["condensed_milk"].append([new_milk])
