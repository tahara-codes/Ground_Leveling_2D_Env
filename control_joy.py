import pygame
from pygame.locals import *
import time


class JoyController:
    def __init__(self, id):
        pygame.init()
        pygame.joystick.init()

        self.weight_coff = 1.0

        self.l_hand_x = 0.0
        self.l_hand_y = 0.0
        self.r_hand_x = 0.0
        self.r_hand_y = 0.0
        self.button_A = False
        self.button_B = False
        self.button_X = False
        self.button_Y = False
        self.button_UD = False
        self.button_RL = False
        self.button_R1 = False
        self.button_R2 = False
        self.button_L1 = False
        self.button_L2 = False
        self.button_BACK = False
        self.button_START = False
        self.cross_key = [0, 0]

        self.__initialize_controller(id)

    def __initialize_controller(self, id):
        self.joys = pygame.joystick.Joystick(id)
        self.joys.init()

    def get_controller_value(self):
        for eventlist in pygame.event.get():

            # Read stick
            if eventlist.type == JOYAXISMOTION:
                self.l_hand_x = round(
                    -self.joys.get_axis(0) * self.weight_coff, 2
                )  # joy_left(left_hand [L<->R])
                self.l_hand_y = round(
                    -self.joys.get_axis(1) * self.weight_coff, 2
                )  # joy_left(left_hand [U<->D])
                self.r_hand_x = round(
                    -self.joys.get_axis(2) * self.weight_coff, 2
                )  # joy_right(left_hand [L<->R])
                self.r_hand_y = round(
                    -self.joys.get_axis(3) * self.weight_coff, 2
                )  # joy_right(left_hand [U<->D])

            # Read button
            self.button_A = self.joys.get_button(0)
            self.button_B = self.joys.get_button(1)
            self.button_X = self.joys.get_button(2)
            self.button_Y = self.joys.get_button(3)
            self.button_L1 = self.joys.get_button(4)
            self.button_R1 = self.joys.get_button(5)
            self.button_BACK = self.joys.get_button(6)
            self.button_START = self.joys.get_button(7)

            # Read hat
            if eventlist.type == JOYHATMOTION:
                self.cross_key = self.joys.get_hat(0)

            # print(
            #     self.joys.get_button(0),
            #     self.joys.get_button(1),
            #     self.joys.get_button(2),
            #     self.joys.get_button(3),
            #     self.joys.get_button(4),
            #     self.joys.get_button(5),
            #     self.joys.get_button(6),
            #     self.joys.get_button(7),
            #     self.joys.get_button(8),
            #     self.joys.get_button(9),
            # )
