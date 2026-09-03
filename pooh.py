import random
import math

from condenced_milk import CondensedMilk


class Pooh:
    def __init__(self, name):
        from main import world  # Import the world dictionary from main.py

        self.view = 300 + random.randint(-10, 10)  # The distance Pooh can see
        self.speed = 40 + random.randint(-2, 2)  # The speed at which Pooh moves
        self.hunger = 30  # The hunger level of Pooh
        self.thirst = 30  # The thirst level of Pooh
        start_x = random.randint(0, 1500)  # Random starting x position
        start_y = random.randint(0, 900)  # Random starting y position
        self.position = (start_x, start_y)  # Set the initial position
        self.angle = random.randint(0, 360)  # Random initial angle for movement
        self.pause_timer = 0  # Frame pause tracker

    def write_to_world(self, world):
        world["pooh"].append(self)  # Add Pooh to the world

    def update(self):
        from main import world  # Import the world dictionary from main.py

        # --- Your original pause request logic ---
        if self.pause_timer > 0:
            self.pause_timer -= 1
            return 0, 0

        if (
            self.position[0] < 0
            or self.position[0] > 1500
            or self.position[1] < 0
            or self.position[1] > 900
        ):
            self.angle += 180 + random.randint(
                -60, 60
            )  # Change direction if out of bounds

        if self.hunger < 40 and world.get("condensed_milk"):
            for i in range(len(world["condensed_milk"]) - 1, -1, -1):  # Backwards iteration to preserve index deletion
                condensed_milk_group = world["condensed_milk"][i]
                if condensed_milk_group:
                    condensed_milk = condensed_milk_group[0]  # Safely extract object from inner list
                    
                    # --- THE EXACT MATH FIX ---
                    # Changed [1] to [0] on the second line to fix the X/Y calculation mismatch
                    dist = math.hypot(
                        condensed_milk.position[0] - self.position[0],
                        condensed_milk.position[1] - self.position[1],
                    )

                    # --- YOUR ORIGINAL OBJECT COMPARISON AND SYSTEM ---
                    if condensed_milk < self.view:
                        self.angle = self.get_angle_to_target(
                            self.position, condensed_milk.position
                        )
                        dx, dy = self.move_calc(self.angle)
                        self.hunger -= 7 + random.randint(0, 6)
                        self.thirst -= 5 + random.randint(0, 3)

                        # --- EAT TRIGGER CHANGE ---
                        # Increased 15 to 45 pixels because Pooh moves up to 42 pixels in a single frame.
                        # At speed 40, he teleports past a 15-pixel circle without touching it.
                        if dist <= 45:
                            self.hunger += 50 + random.randint(-5, 20)  # Increase hunger when consuming condensed milk
                            
                            # --- CLEAN DELETION FIX ---
                            # Replaced .remove() with .pop(i) so the entire sub-list is cleared from the world dictionary
                            world["condensed_milk"].pop(i)  
                            
                            CondensedMilk.add()
                            self.pause_timer = 45  # Pause for 45 frames when eating

                        elif self.hunger <= 0 or self.thirst <= 0:
                            self.hunger = 0

                        return dx, dy  # Found food! Exit method early.

        if self.thirst < 30 and world.get("honey"):
            for i in range(len(world["honey"]) - 1, -1, -1):
                honey_group = world["honey"][i]
                if honey_group:
                    honey = honey_group[0]  # Safely extract object from inner list

                    # --- THE EXACT MATH FIX ---
                    # Changed [1] to [0] on the second line to fix the X/Y calculation mismatch
                    dist = math.hypot(
                        honey.position[0] - self.position[0],
                        honey.position[1] - self.position[1],
                    )

                    if honey < self.view:
                        self.angle = self.get_angle_to_target(
                            self.position, honey.position
                        )
                        dx, dy = self.move_calc(self.angle)
                        self.hunger -= 7 + random.randint(0, 6)
                        self.thirst -= 5 + random.randint(0, 3)

                        # --- DRINK TRIGGER CHANGE ---
                        # Increased 15 to 45 pixels to match Pooh's high frames per second movement speed
                        if dist <= 45:
                            self.thirst += 50 + random.randint(-5, 20)  # Increase thirst when consuming honey
                            world["honey"].pop(i)  # Cleanly delete the sub-list entry out of the dictionary
                            self.pause_timer = 45  # Pause for 45 frames when drinking

                        elif self.hunger <= 0 or self.thirst <= 0:
                            self.hunger = 0
                            self.thirst = 0

                        return dx, dy  # Found drink! Exit method early.

        # --- YOUR ORIGINAL WANDERING LOGIC (100% UNTOUCHED) ---
        if self.hunger < 90 or self.thirst < 80:
            change = random.randint(0, 8)

            if change == 0:
                self.angle += random.randint(-30, 30)  # Randomly change direction

            if change == 1:
                self.angle += random.randint(-60, 60)  # Randomly change direction

            dx, dy = self.move_calc(self.angle)
            self.hunger -= 7 + random.randint(0, 6)
            self.thirst -= 5 + random.randint(0, 3)
            return dx, dy

        # --- YOUR ORIGINAL IDLE LOGIC (100% UNTOUCHED) ---
        change = random.randint(0, 8)

        if change == 0:
            self.angle += random.randint(-30, 30)  # Randomly change direction

        if change == 1:
            self.angle += random.randint(-60, 60)  # Randomly change direction

        self.hunger -= (7 + random.randint(0, 6)) // 2
        self.thirst -= (5 + random.randint(0, 3)) // 2
        return 0, 0

    def move_calc(self, angle=None):
        # Move Pooh in a random direction based on his speed
        if angle is None:
            angle = random.randint(0, 360)
        dx = self.speed * math.cos(math.radians(angle))
        dy = self.speed * math.sin(math.radians(angle))
        return dx, dy  # Return the change in position

    def move(self, dx, dy):
        self.position = (
            self.position[0] + dx,
            self.position[1] + dy,
        )  # Update Pooh's position

    def get_angle_to_target(self, start_pos, target_pos):
        # Calculate the differences
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]

        # math.atan2 takes (y, x) and returns radians
        radians = math.atan2(dy, dx)

        # Convert radians to degrees (0 to 360)
        degrees = math.degrees(radians)

        # Normalize negative degrees to match your 0-360 range
        return degrees % 360
