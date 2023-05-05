import math
import random

from cleaning_robot_model import CleaningRobotModel

from helper_functions import *


class RoombaModel(CleaningRobotModel):

    def __init__(self, settings, *args, **kwargs):
        super(RoombaModel,self).__init__(*args, **kwargs)
        self.mode_time_limit = settings["mode_time_limit"]
        self.turn_size_on_wall_follow = settings["turn_size_on_wall_follow"]
        self.max_turn_steps  = settings["max_turn_steps"]
        self.spiral_angle_init = settings["spiral_angle_init"]
        self.spiral_angle_ratio = settings["spiral_angle_ratio"]
        self.use_random_direction_mode = settings["use_random_direction_mode"]
        self.in_random_direction_mode = False
        self.looking_for_wall = False
        self.spiral_mode = True
        self.spiral_angle = self.spiral_angle_init
        self.time_in_mode = 0


    def left_hand_tracking(self):
        found_wall = False
        for i in range(self.max_turn_steps):
            self.turn(-self.turn_size_on_wall_follow)
            if self.check_move():
                found_wall = True
                break
        if not found_wall:
            self.looking_for_wall = True
        self.turn(self.turn_size_on_wall_follow)

    def spiral_step(self):
        self.turn(self.spiral_angle)
        self.spiral_angle = self.spiral_angle * self.spiral_angle_ratio

    def step(self):
        if not self.in_random_direction_mode and not self.looking_for_wall:
            self.left_hand_tracking()
        if self.spiral_mode:
            self.spiral_step()
        collided = self.move()
        self.time_in_mode += 1
        if collided:
            self.looking_for_wall = False
            self.spiral_mode = False
            if self.in_random_direction_mode:
                self.turn(random.randint(0,360)*math.pi/180.)
            else:
                while self.check_move():
                    self.turn(self.turn_size_on_wall_follow)
        if self.use_random_direction_mode:
            if not self.spiral_mode and self.time_in_mode > self.mode_time_limit[self.in_random_direction_mode]:
                self.in_random_direction_mode = not self.in_random_direction_mode
                self.time_in_mode = 0
                print("Switched to mode", self.in_random_direction_mode)

