from control_joy import JoyController


class ActionGenerator:
    def __init__(self):
        self.joy = JoyController(0)
        self.deadzone = 0.5
        self.back_count = 0

    def get_joy_action(self):
        while True:
            self.joy.get_controller_value()
            action_x = self.joy.cross_key[1]
            action_y = -self.joy.cross_key[0]
            action = 0
            if action_x > self.deadzone:
                action = 1
                break
            elif action_x < -self.deadzone:
                action = 2
                break
            elif action_y > self.deadzone:
                action = 3
                break
            elif action_y < -self.deadzone:
                action = 4
                break
        return action

    def get_expert_action(self, map, goal, state):
        if map[state["robot_pos"][0] + 1, state["robot_pos"][1]] > state["speed"]:
            self.back_count = map[state["robot_pos"][0] + 1, state["robot_pos"][1]]
        while self.back_count > 0:
            action = 1
            self.back_count -= 1
            return action

        action_x = state["robot_pos"][0] - goal[0]
        action_y = state["robot_pos"][1] - goal[1]
        action = 0
        if action_x > self.deadzone:
            action = 1
        elif action_x < -self.deadzone:
            action = 2
        elif action_y > self.deadzone:
            action = 3
        elif action_y < -self.deadzone:
            action = 4
        return action
