import random
import math

class CondensedMilk:
    def __init__(self, name):
            from main import world
            x = random.randint(50, 1450)
            y = random.randint(50,850)
            self.position = (x,y)

    def add_to_world(self, world):

        chance = random.randint(0,4)
        amount_one = random.randint(1,3)
        amount_two = random.randint(4,6)

        if chance == 0:
          amount = amount_two

        else:
          amount = amount_one  

        
          for i in range (amount):
            world["condensed_milk"].append([self])

