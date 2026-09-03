import random
import math


class Pooh:
    def __init__(self, name):
        from main import world  # Import the world dictionary from main.py

        self.view = 100 + random.randint(-10, 10)  # The distance Pooh can see
        self.speed = 5 + random.randint(-2, 2)  # The speed at which Pooh moves
        self.hunger = 100  # The hunger level of Pooh
        self.thirst = 100  # The thirst level of Pooh
        start_x = random.randint(0, 1500)  # Random starting x position
        start_y = random.randint(0, 900)  # Random starting y position
        self.position = (start_x, start_y)  # Set the initial position

    def write_to_world(self, world):
        world["pooh"].append(self)  # Add Pooh to the world

    def update(self, hunger, thirst):
        from main import world  # Import the world dictionary from main.py

        moved = False

        if hunger < 30:
            for i in range(len(world["condensed_milk"])):
                condensed_milk = world["condensed_milk"][i]
                if condensed_milk < self.view:
                    dx, dy = self.move()
                    moved = True
                    return dx, dy  # Return the change in position
            if condensed_milk < self.view:
                dx, dy = self.move()
                moved = True

    def move(self, angle=None):
        # Move Pooh in a random direction based on his speed
        if angle is None:
            angle = random.randint(0, 360)
        dx = self.speed * math.cos(math.radians(angle))
        dy = self.speed * math.sin(math.radians(angle))
        return dx, dy  # Return the change in position
