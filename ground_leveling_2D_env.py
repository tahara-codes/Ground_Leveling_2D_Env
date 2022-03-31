import numpy as np
from scipy import ndimage

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from action_generator import ActionGenerator


class Ground_Leveling_2D_Env:
    def __init__(self):
        map_size = 15
        self.map = self.create_map(
            map_size=map_size, void=int(map_size / 4), max_val=4, min_val=1
        )
        self.goalset = self.plan(self.map)

        self.robot_state = RobotState()
        self.action_generator = ActionGenerator()

    def create_map(self, map_size, void, min_val, max_val):
        map = np.zeros((map_size, map_size))
        for i in zip(np.arange(void, map_size - void, 1)):
            for j in zip(np.arange(void, map_size - void, 1)):
                map[i, j] = np.random.randint(min_val, max_val)
        return map

    def get_map(self):
        return self.map

    def plan(self, map):
        goalset = np.zeros((0, 2))
        for i in range(map.shape[0] - 2):
            for j in range(map.shape[1] - 2):
                goalset = np.concatenate([goalset, [[j + 1, i + 1]]], 0)
            for j in range(map.shape[1] - 3):
                goalset = np.concatenate([goalset, [[map.shape[1] - j - 3, i + 1]]], 0)
        goalset = np.delete(goalset, 0, 0)
        return goalset

    # Lendering takes long time
    def visualize(self, robot_state, goal_index, goalset):
        plt.clf()
        sns.heatmap(
            self.map,
            linewidth=2,
            linecolor="white",
            annot=True,
            cmap="Oranges",
            cbar=False,
        )
        self.imscatter(
            y=robot_state["robot_pos"][0] + 0.5,
            x=robot_state["robot_pos"][1] + 0.5,
            angle=robot_state["robot_pos"][2],
            image="./robot.png",
            zoom=0.03,
        )
        plt.text(
            0, -0.5, s="SPEED : " + str(robot_state["speed"]), fontsize="xx-large",
        )
        plt.text(
            5,
            -0.5,
            s="GOAL " + str(goal_index) + "/" + str(len(goalset)),
            fontsize="xx-large",
        )
        for i in range(len(goalset) - 1):
            plt.quiver(
                goalset[i][1] + 0.5,
                goalset[i][0] + 0.5,
                goalset[i + 1][1] - goalset[i][1],
                goalset[i + 1][0] - goalset[i][0],
                angles="xy",
                scale_units="xy",
                width=0.005,
            )
        plt.draw()
        plt.pause(0.001)

    def imscatter(self, x, y, angle=0, image=None, ax=None, zoom=1):
        ax = plt.gca()
        image = plt.imread(image)
        image = (image * 255).astype(np.uint8)
        image = ndimage.rotate(image, angle)
        im = OffsetImage(image, zoom=zoom)
        x, y = np.atleast_1d(x, y)
        for x0, y0 in zip(x, y):
            ab = AnnotationBbox(im, (x0, y0), xycoords="data", frameon=False)
            ax.add_artist(ab)  # Draw Image

    def step(self, action, goal_index, visualize=False):
        self.robot_state.move(action)
        state = self.robot_state.get_state()
        if visualize is True:
            self.visualize(state, goal_index, self.goalset)
        self.map = self.robot_state.check_collision(self.map)
        if visualize is True:
            self.visualize(state, goal_index, self.goalset)
        self.robot_state.set_cell_cost(self.map, self.goalset[goal_index])
        state = self.robot_state.get_state()
        return state


class RobotState:
    def __init__(self):
        self.state = {
            "robot_pos": [1, 1, 0],
            "prev_robot_pos": [1, 1, 0],
            "speed": 0,
            "neighbor_cost": np.zeros((3, 3)),
            "front_cost": 0,
            "goal_cost": 0,
        }

    def get_state(self):
        return self.state

    def set_cell_cost(self, map, goal):
        x = self.state["robot_pos"][0]
        y = self.state["robot_pos"][1]
        self.state["front_cost"] = map[x + 1, y]
        self.state["goal_cost"] = map[int(goal[0]), int(goal[1])]
        self.state["neighbor_cost"][0][0] = map[x - 1, y - 1]
        self.state["neighbor_cost"][0][1] = map[x - 1, y]
        self.state["neighbor_cost"][0][2] = map[x - 1, y + 1]
        self.state["neighbor_cost"][1][0] = map[x, y - 1]
        self.state["neighbor_cost"][1][1] = map[x, y]
        self.state["neighbor_cost"][1][2] = map[x, y + 1]
        self.state["neighbor_cost"][2][0] = map[x + 1, y - 1]
        self.state["neighbor_cost"][2][1] = map[x + 1, y]
        self.state["neighbor_cost"][2][2] = map[x + 1, y + 1]

    def move(self, action):
        if action == 1:
            self.state["robot_pos"][0] -= 1
            self.state["robot_pos"][2] = 1
        elif action == 2:
            self.state["robot_pos"][0] += 1
            self.state["robot_pos"][2] = 0
        elif action == 3:
            self.state["robot_pos"][1] -= 1
            self.state["robot_pos"][2] = -90
        elif action == 4:
            self.state["robot_pos"][1] += 1
            self.state["robot_pos"][2] = 90

    def check_collision(self, map):
        x = self.state["robot_pos"][0]
        y = self.state["robot_pos"][1]

        # Limit
        if x == 0 or x == map.shape[0] - 1 or y == 0 or y == map.shape[1] - 1:
            self.state["robot_pos"] = self.state["prev_robot_pos"].copy()
            self.state["speed"] = 0

        # Move on cost cell
        if map[x, y] > 0.0:
            # Enough speed
            if self.state["speed"] >= map[x, y]:
                map[x, y] = 0
                self.state["speed"] = 0
            else:
                self.state["robot_pos"] = self.state["prev_robot_pos"].copy()
                self.state["speed"] = 0
        # Move on free cost cell
        else:
            if self.state["robot_pos"] != self.state["prev_robot_pos"]:
                if self.state["robot_pos"][2] != self.state["prev_robot_pos"][2]:
                    self.state["speed"] = 1
                else:
                    self.state["speed"] += 1
        # Prev pos update
        self.state["prev_robot_pos"] = self.state["robot_pos"].copy()
        return map


def Test(self):
    step = 0
    goal_index = 0

    state = env.robot_state.get_state()
    env.visualize(state, goal_index, self.goalset)

    while True:

        state = env.robot_state.get_state()
        action = env.action_generator.get_joy_action()
        state = env.step(action, goal_index, visualize=True)

        step += 1
        print(" step: ", step)


if __name__ == "__main__":
    env = Ground_Leveling_2D_Env()
    Test(env)
