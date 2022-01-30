#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import math
import matplotlib.pyplot as plt
import pprint
from maze_ui import MazeUI

class Dijkstra():

    def __init__(self):
        self.mazeUI = MazeUI(x_spacing=0.13, y_spacing = 0.2, theta=0)

    def dijkstras(self, occupancy_map, x_spacing, y_spacing, start, goal, debug=False, visual=False):
        """
        Implements Dijkstra's shortest path algorithm
        Input:
        occupancy_map - an N by M numpy array of boolean values (represented
            as integers 0 and 1) that represents the locations of the obstacles
            in the world
        x_spacing - parameter representing spacing between adjacent columns
        y_spacing - parameter representing spacing between adjacent rows
        start - a 3 by 1 numpy array of (x,y,theta) for the starting position 
        goal - a 3 by 1 numpy array of (x,y,theta) for the finishing position 
        Output: 
        path: list of the indices of the nodes on the shortest path found
            starting with "start" and ending with "end" (each node is in
            metric coordinates)
        """
        colormapval = (0, 8)
        goal_found = False

        # Setup Map Visualizations:
        if visual == True:
            self.viz_map = self.mazeUI.create_initial_maze(maze=occupancy_map)

        # We will use this delta function to search surrounding nodes.
        delta = [[-1, 0],  # go up
                [0, -1],  # go left
                [1, 0],  # go down
                [0, 1]]  # go right

        # Each node on the map "costs" 1 step to reach.
        cost = 1

        # Convert numpy array of map to list of map, makes it easier to search.
        occ_map = occupancy_map.tolist()
        if debug == True:
            print("occ_map: ")
            pprint.pprint(occ_map)

        # Converge start and goal positions to map indices.
        startX = int(math.ceil((start.item(0) / x_spacing) - 0.5))  # startingx
        startY = int(math.ceil((start.item(1) / y_spacing) - 0.5))  # startingy
        goalX = int(math.ceil((goal.item(0) / x_spacing) - 0.5))
        goalY = int(math.ceil((goal.item(1) / y_spacing) - 0.5))
        print("Start Pose: ", startX, startY)
        print("Goal Pose: ", goalX, goalY)

        # Make a map to keep track of all the nodes and their cost distance values.
        possible_nodes = [[0 for row in range(len(occ_map[0]))] for col in range(len(occ_map))]
        row = startY
        col = startX

        # Show the starting node and goal node.
        # 5 looks similar to S and 6 looks similar to G.
        possible_nodes[row][col] = 5

        if visual == True:
            self.mazeUI.show_initial_and_goal_target(viz_map=self.viz_map, startX=row, startY=col, goalX=goalX, goalY=goalY)


        if debug == True:
            print("Possible Nodes: ")
            pprint.pprint(possible_nodes)

        # The g_value will count the number of steps each node is from the start.
        # Since we are at the start node, the total cost is 0.
        g_value = 0
        frontier_nodes = [(g_value, col, row)] # dist, x, y
        searched_nodes = []
        parent_node = {}  # Dictionary that Maps {child node : parent node}
        loopcount = 0

        while len(frontier_nodes) != 0:
            if debug == True:
                "\n>>>>>>>>>>>>LOOP COUNT: ", loopcount, "\n"
            frontier_nodes.sort(reverse=True) #sort from shortest distance to farthest
            current_node = frontier_nodes.pop()
            if debug == True:
                print("current_node: ", current_node)
                print("frontier nodes: ", searched_nodes)

            if current_node[1] == goalX and current_node[2] == goalY:
                goal_found = True
                if visual == True:
                    self.mazeUI.goal_found(viz_map=self.viz_map)
                break
            g_value, col, row = current_node

            # Check surrounding neighbors.
            for i in delta:
                possible_expansion_x = col + i[0]
                possible_expansion_y = row + i[1]
                valid_expansion = 0 <= possible_expansion_y < len(occupancy_map[0]) and 0 <= possible_expansion_x < len(occ_map)
                if debug == True:
                    print("Current expansion Node: ", possible_expansion_x, possible_expansion_y)

                if valid_expansion:
                    try:
                        unsearched_node = possible_nodes[possible_expansion_y][possible_expansion_x] == 0
                        open_node = occ_map[possible_expansion_y][possible_expansion_x] == 0
                        if debug == True:
                            print("Check Open or Wall: ", occ_map[possible_expansion_y][possible_expansion_x])
                    except:
                        unsearched_node = False
                        open_node = False
                    if unsearched_node and open_node:
                        # Using  instead of 1 to make it easier to read This node has been searched.
                        # searched_row = possible_expansion_y
                        # searched_col = possible_expansion_x
                        possible_nodes[possible_expansion_y][possible_expansion_x] = 3
                        possible_node = (g_value + cost, possible_expansion_x, possible_expansion_y)
                        frontier_nodes.append(possible_node)
                        if debug == True:
                            print("frontier_nodes:", frontier_nodes)
                        if visual == True:
                            self.mazeUI.highligh_explored_node(viz_map=self.viz_map,x_cord=possible_expansion_x, y_cord=possible_expansion_y)

                        # This now builds parent/child relationship
                        parent_node[possible_node] = current_node
                        if debug == True:
                            print("Parent Node: \n", parent_node)
                            print("While Possible Nodes: ")
                            pprint.pprint(possible_nodes)
            loopcount = loopcount+1

        if goal_found == True:

            print("Generating path...")

            route = []
            child_node = current_node
            while child_node in parent_node:
                route.append(parent_node[child_node])
                child_node = parent_node[child_node]
                route.sort()

            #  route back to metric units:
            if debug == True:
                print("Route: ", route)
            if visual == True:
                self.mazeUI.show_full_route(viz_map=self.viz_map, route=route, goalX=goalX, goalY=goalY)

            path = []
            position = [startX, startY]  # Starting point passed in by function
            #path.append(position)  # Add it to the list for the path

            for i in range(0, len(route)):
                position = [route[i][1], route[i][2]]
                path.append(position)

            # Add the goal state:
            position = [goalX, goalY]
            path.append(position)
      
            return path

        else:
            if visual == True:
                self.mazeUI.no_path_found(viz_map=self.viz_map)
            return False


    def coordinates_into_np_array(self, x, y, x_spacing, y_spacing, theta):
        """
            Duplicate function in maze_ui.py
        """

        start_item0 = (x + 0.5) * x_spacing
        start_item1 = (y + 0.5) * y_spacing
        return np.array([[start_item0], [start_item1], [theta]])


    def exec(self, maze, start, end, debug=False, visual=False):
        """
        Function that provides a few examples of maps and their solution paths
        """
        test_map1 = np.array(maze)
        x_spacing1 = 0.13
        y_spacing1 = 0.2
        
        x_start = start[0]
        y_start = start[1]
        x_goal = end[0]
        y_goal = end[1]

        start1 = self.coordinates_into_np_array(x=x_start, y=y_start, x_spacing=x_spacing1, y_spacing=y_spacing1, theta=0)
        goal1 = self.coordinates_into_np_array(x=x_goal,y=y_goal, x_spacing=x_spacing1, y_spacing=y_spacing1, theta=0)

        path1 = self.dijkstras(
            occupancy_map=test_map1, 
            x_spacing=x_spacing1,
            y_spacing=y_spacing1,
            start=start1,
            goal=goal1,
            debug=debug,
            visual=visual
        )

        return path1