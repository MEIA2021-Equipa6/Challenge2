from __future__ import print_function
import numpy as np
import math
import matplotlib.pyplot as plt
import pprint

class MazeUI():

    def __init__(self, x_spacing, y_spacing, theta, colormapval=(0, 8)):
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.theta = theta
        self.colormapval = colormapval
        

    def create_initial_maze(self, maze):
        viz_map=maze
        fig = plt.figure(figsize=(12,12))
        ax = fig.add_subplot(111)
        ax.set_title('Factory Floor Grid')
        plt.xticks(visible=False)
        plt.yticks(visible=False)
        plt.imshow(viz_map, origin='upper', interpolation='none', clim=self.colormapval)
        ax.set_aspect('equal')
        plt.pause(0.2)
        return viz_map


    def show_initial_and_goal_target(self, viz_map, startX, startY, goalY, goalX, color_modifier=0):
        viz_map[startY][startX] = 5 - color_modifier
        viz_map[goalY][goalX] = 6 - color_modifier
        plt.imshow(viz_map, origin='upper', interpolation='none', clim=self.colormapval)
        plt.pause(0.2)


    def transfrom_coords_to_draw(self, pos):
        posX = int(math.ceil((pos[0] / self.x_spacing) - 0.5))  # startingx
        posY = int(math.ceil((pos[1] / self.y_spacing) - 0.5))  # startingy

        return (posX, posY)


    def goal_found(self, viz_map):
        plt.text(2, 10, s="Goal found!", fontsize=18, style='oblique', ha='center', va='top')
        plt.imshow(viz_map, origin='upper', interpolation='none', clim=self.colormapval)
        plt.pause(0.2)


    def highligh_explored_node(self, viz_map, x_cord, y_cord, color_modifier=0):
        viz_map[y_cord][x_cord] = 3 - color_modifier
        plt.imshow(viz_map, origin='upper', interpolation='none', clim=self.colormapval)
        plt.pause(.001)


    def highlight_node(self, viz_map, posY, posX, color_modifier=0):
        viz_map[posY][posX] = 7 - color_modifier
        plt.imshow(viz_map, origin='upper', interpolation='none', clim=self.colormapval)
        plt.pause(.001)


    def show_full_route(self, viz_map, route, goalX, goalY, color_modifier=0):
        for i in range(0, len(route)):
            self.highlight_node(viz_map, posY=route[i][2], posX=route[i][1], color_modifier=color_modifier)
            plt.imshow(viz_map, origin='upper', interpolation='none', clim=self.colormapval)
            plt.pause(.001)

        viz_map[goalY][goalX] = 7 - color_modifier
        plt.imshow(viz_map, origin='upper', interpolation='none', clim=self.colormapval)
        plt.pause(0.5)


    def no_path_found(self, viz_map):
        plt.text(2, 10, s="No path found...", fontsize=18, style='oblique', ha='center', va='top')
        plt.imshow(viz_map, origin='upper', interpolation='none', clim=self.colormapval)
        plt.pause(1)


    def coordinates_into_np_array(self, x, y):
        start_item0 = (x + 0.5) * self.x_spacing
        start_item1 = (y + 0.5) * self.y_spacing
        return np.array([[start_item0], [start_item1], [self.theta]])