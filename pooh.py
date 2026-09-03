import random
import math

from condenced_milk import CondensedMilk


class Pooh:
    import random
import math

from condenced_milk import CondensedMilk


class Pooh:
    def __init__(self, name):
        from main import world  # Import the world dictionary from main.py

        self.view = 300 + random.randint(-30, 30)  # The distance Pooh can see
        self.speed = 10 + random.randint(-2, 2)  # The speed at which Pooh moves
        self.hunger = 30  # The hunger level of Pooh
        self.thirst = 30  # The thirst level of Pooh
        start_x = random.randint(0, 1500)  # Random starting x position
        start_y = random.randint(0, 900)  # Random starting y position
        self.position = (start_x, start_y)  # Set the initial position
        self.angle = random.randint(0, 360)  # Random initial angle for movement
        self.pause_timer = 0  # Added to support the pause feature you requested

    def write_to_world(self, world):
        world["pooh"].append(self)  # Add Pooh to the world

    def update(self):
        from main import world  # Import the world dictionary from main.py

        # Optional: Keeps Pooh still if he is pausing
        if self.pause_timer > 0:
            self.pause_timer -= 1
            return 0, 0

        # 1. SCREEN BOUNDARY CHECK
        if (
            self.position[0] < 0
            or self.position[0] > 1500
            or self.position[1] < 0
            or self.position[1] > 900
        ):
            self.angle += 180 + random.randint(-60, 60)
            self.angle %= 360

        # 2. HUNGER SYSTEM (Condensed Milk)
        if self.hunger < 40 and world.get("condensed_milk"):
            for i in range(len(world["condensed_milk"]) - 1, -1, -1):
                condensed_milk_group = world["condensed_milk"][i]

                if condensed_milk_group:  
                    condensed_milk = condensed_milk_group[0]

                    # YOUR ORIGINAL MATH: Formatted cleanly to fix the X/Y mixup
                    dist = math.hypot(
                        condensed_milk.position[0] - self.position[0],
                        condensed_milk.position[1] - self.position[1],
                    )

                    # FIXED: Checking the real 'dist' variable instead of the object '<' operator
                    if dist < self.view:
                        self.angle = self.get_angle_to_target(
                            self.position, condensed_milk.position
                        )
                        dx, dy = self.move_calc(self.angle)
                        
                        # YOUR ORIGINAL STAT DEGRADATION
                        self.hunger -= 7 + random.randint(0, 6)
                        self.thirst -= 5 + random.randint(0, 3)

                        # YOUR ORIGINAL HITBOX RADIUS (Increased slightly to 25 to catch his speed)
                        if dist <= 25:
                            self.hunger += 50 + random.randint(-5, 20)
                            if self.hunger > 100:
                                self.hunger = 100  

                            # SUCCESSFUL DELETION: Wipes the food from the world array
                            world["condensed_milk"].pop(i)
                            
                            # Sets a small pause (e.g., 30 frames = 0.5 seconds)
                            self.pause_timer = 30 

                        if self.hunger < 0 or self.thirst < 0:
                            if self in world["pooh"]:
                                world["pooh"].remove(self)
                        return dx, dy

        # 3. THIRST SYSTEM (Honey)
        if self.thirst < 30 and world.get("honey"):
            for i in range(len(world["honey"]) - 1, -1, -1):
                honey_group = world["honey"][i]

                if honey_group:
                    honey = honey_group[0]
                    dist = math.hypot(
                        honey.position[0] - self.position[0],
                        honey.position[1] - self.position[1],
                    )

                    if dist < self.view:
                        self.angle = self.get_angle_to_target(
                            self.position, honey.position
                        )
                        dx, dy = self.move_calc(self.angle)
                        self.hunger -= 7 + random.randint(0, 6)
                        self.thirst -= 5 + random.randint(0, 3)

                        if dist <= 25:
                            self.thirst += 50 + random.randint(-5, 20)
                            if self.thirst > 100:
                                self.thirst = 100
                            
                            world["honey"].pop(i)
                            self.pause_timer = 30

                        if self.hunger < 0 or self.thirst < 0:
                            if self in world["pooh"]:
                                world["pooh"].remove(self)
                        return dx, dy

        # 4. STANDARD WANDERING (YOUR ORIGINAL LOGIC)
        if self.hunger < 90 or self.thirst < 80:
            change = random.randint(0, 8)
            if change == 0:
                self.angle += random.randint(-30, 30)
            elif change == 1:
                self.angle += random.randint(-45, 45)

            dx, dy = self.move_calc(self.angle)
            self.hunger -= 7 + random.randint(0, 6)
            self.thirst -= 5 + random.randint(0, 3)

            if self.hunger < 0: self.hunger = 0
            if self.thirst < 0: self.thirst = 0
            return dx, dy

        # 5. IDLE STATE (YOUR ORIGINAL LOGIC)
        change = random.randint(0, 8)
        if change == 0:
            self.angle += random.randint(-30, 30)
        elif change == 1:
            self.angle += random.randint(-45, 45)

        self.hunger -= (7 + random.randint(0, 6)) // 2
        self.thirst -= (5 + random.randint(0, 3)) // 2

        if self.hunger < 0 or self.thirst < 0:
            if self in world["pooh"]:
                world["pooh"].remove(self)
        return 0, 0

    def move_calc(self, angle):
        rad_angle = math.radians(angle)
        dx = self.speed * math.cos(rad_angle)
        dy = self.speed * math.sin(rad_angle)
        return dx, dy

    def move(self, dx, dy):
        self.position = (
            self.position[0] + dx,
            self.position[1] + dy,
        )

    def get_angle_to_target(self, start_pos, target_pos):
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        radians = math.atan2(dy, dx)
        degrees = math.degrees(radians)
        return degrees % 360
