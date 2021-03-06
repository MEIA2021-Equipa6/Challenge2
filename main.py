from re import M
from signal import valid_signals
from dijkstra import Dijkstra
from random import randrange
from maze_ui import MazeUI
import time
import math
import random
import time
from a_star import PathPlanner

X_DIM = 14
Y_DIM = 14

mazeUI = MazeUI(x_spacing=0.13, y_spacing = 0.2, theta=0)

def empty_position(maze, position):
    return not maze[position[1]][position[0]] == 1     


def generate_packages_robot(maze, number_of_packages=10):
    robot_orders = []
    for i in range(number_of_packages):
        if i==0:
            start, end = generate_random_package(maze)
        else:
            # ensure that the next package starts at the end of previous package
            start, end = generate_random_package(maze=maze, start=robot_orders[i-1][1])
        robot_orders.append([start, end])
    return robot_orders


def test_dataset_rl (orders_robot, maze):
    print("\n\n###############################################")
    print("Generation of Test Dataset for Reinforced Learning")
    dijkstra = Dijkstra()
    test_dataset = []
    for order in orders_robot:
        start, end = order        
        shortest_path_dijkstra = dijkstra.exec(maze=maze, start=start, end=end)
        if not shortest_path_dijkstra:
            continue
        best_solution_cost = len(shortest_path_dijkstra)
        test_dataset.append([start, end, best_solution_cost])
    
    print(f"Generated {len(orders_robot)} testcases")
    print(f"Test Dataset:\n {test_dataset}")
    print("\n###############################################")
    return test_dataset


def generate_random_package(maze, start=None):
    start = find_empty_space(maze) if not start else start
    goal = find_empty_space(maze)
    return start, goal


def find_empty_space(maze):
    x_value = randrange(X_DIM)
    y_value = randrange(Y_DIM)
 
    while True:
        if empty_position(maze, [x_value, y_value]):
            break
        else:
            x_value = randrange(X_DIM)
            y_value = randrange(Y_DIM)
    return [x_value, y_value]


def handle_with_possible_colision(current_maze, rb_moving_to_pos, current_pos):
    moves_to_remove = []
    possible_moves = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, 1], [-1, -1], [1, -1]]
    if rb_moving_to_pos[0] >= len(current_maze[0]):
        moves_to_remove.append([[1, 0], [1, 1], [1, -1]])
    if rb_moving_to_pos[0] < 0:
        moves_to_remove.append([[-1, 0], [-1, 1], [-1, -1]])
    if rb_moving_to_pos[1] >= len(current_maze):
        moves_to_remove.append([[0, 1], [1, 1], [-1, 1]])
    if rb_moving_to_pos[1] < 0:
        moves_to_remove.append([[0, -1], [-1, -1], [1, -1]])
    possible_moves = [possible_move for possible_move in possible_moves if possible_move not in moves_to_remove]

    for move in possible_moves:
        suggested_move_pos = [y + x for x, y in zip(move, current_pos)]
        if not empty_position(maze=current_maze, position=suggested_move_pos):
            possible_moves.remove(move)

    if not possible_moves:
        return current_pos
    else:
        move = random.choice(possible_moves)	
        inverse_move = [element * -1 for element in move]
        return [y + x for x, y in zip(move, current_pos)], inverse_move


def find_next_order_path(orders_rb, test_planner):
    start_rb = orders_rb[0][0]
    end_rb = orders_rb[0][1]
    shortest_path_rb = test_planner.a_star(start_rb, end_rb)
    return shortest_path_rb


def execute_robot_movement(orders_rb, missing_path_rb, current_maze, test_planner, rb_current_pos, viz_map, color_modifier=0):
    # if the robot has somewhere to go, move
    if len(missing_path_rb) > 0:
        # initial assumption that the robot will move the next best position
        rb_moving_to_pos = missing_path_rb[1]
        if not empty_position(current_maze, rb_moving_to_pos):
            rb_moving_to_pos, inverse_move = handle_with_possible_colision(current_maze=current_maze, rb_moving_to_pos=rb_moving_to_pos, current_pos=rb_current_pos)
            missing_path_rb.insert(0, inverse_move)
        
        current_maze[rb_moving_to_pos[1]][rb_moving_to_pos[0]] = 1
        missing_path_rb.pop(0)
        draw_moving_to_pos(rb_moving_to_pos=rb_moving_to_pos, viz_map=viz_map, color_modifier=color_modifier)
        return missing_path_rb


def draw_moving_to_pos(rb_moving_to_pos, viz_map, color_modifier=0):
    #coords_to_draw = mazeUI.coordinates_into_np_array(x=rb_moving_to_pos[0], y=rb_moving_to_pos[1])
    mazeUI.highlight_node(viz_map=viz_map, posX=rb_moving_to_pos[1], posY=rb_moving_to_pos[0], color_modifier=color_modifier)


def performance_check(maze, orders):
    print("\n\n###############################################")
    print("Performance Analysis")
    execution_time_astar = 0
    execution_time_dijkstra = 0

    solution_cost_astar = 0
    solution_cost_dijkstra = 0

    dijkstra = Dijkstra()
    test_planner = PathPlanner(grid=maze)

    for order in orders:
        tmp_time_astar = 0
        tmp_time_dijkstra = 0
        
        tmp_cost_astar = 0
        tmp_cost_dijkstra = 0

        start_point = order[0]
        end_point = order[1]
 
        # ==== A* Performance Tests ====
        start_time_astar = time.time()
        shortest_path_astar = test_planner.a_star(start_cart=start_point, goal_cart=end_point)
    
        tmp_time_astar = time.time() - start_time_astar
        execution_time_astar += tmp_time_astar
        
        tmp_cost_astar = len(shortest_path_astar)
        solution_cost_astar += tmp_cost_astar
        
        print(f"\nA* time: {tmp_time_astar}")
        print(f"Cost: {tmp_cost_astar}\n")

        # ==== Dijkstra Performance Tests ====
        start_time_dijkstra = time.time()
        shortest_path_dijkstra = dijkstra.exec(maze=maze, start=start_point, end=end_point)
        
        tmp_time_dijkstra = time.time() - start_time_dijkstra
        execution_time_dijkstra += tmp_time_dijkstra
        
        tmp_cost_dijkstra = len(shortest_path_dijkstra)
        solution_cost_dijkstra += tmp_cost_dijkstra
        
        print(f"\nDijkstra time : {tmp_time_dijkstra}")
        print(f"Cost: {tmp_cost_dijkstra}\n")

    print(f"Total Dijkstra time : {execution_time_dijkstra}")
    print(f"Total A* time : {execution_time_astar}")
    print(f"\nTotal Dijkstra Cost: {solution_cost_dijkstra}")
    print(f"Total A* Cost: {solution_cost_astar}\n")

    print("\n###############################################")


def store_test_dataset(test_dataset):
    import csv
    import os
    current_time = time.time()
    dir_name = "test_datasets/"
    # Create target Directory if don't exist
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("Directory " , dir_name ,  " Created ")
    else:    
        print("Directory " , dir_name ,  " already exists")

    filename = f"{dir_name}/{current_time}.csv"
    header = ['origin_point', 'destination_point', 'cost']
    # open the file in the write mode
    with open(filename, 'w', encoding='UTF8')as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write multiple rows
        writer.writerows(test_dataset)
        

def main():
    # x       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14    # y
    maze = [[0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # 0
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # 1
            [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0],   # 2
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],   # 3
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],   # 4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # 5
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],   # 6
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # 7
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # 8
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],   # 9
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],   # 10
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],   # 11
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],   # 12
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # 13
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]   # 14   

    start = (0, 0)
    end = (7, 8)

    # Dijkstra
    start_time_creation_of_dijktra = time.time()
    dijkstra = Dijkstra()

    print(f"\n\n **** Time to generate dijkstra matrix =  {time.time()-start_time_creation_of_dijktra}")

    shortest_path_dijkstra = dijkstra.exec(maze=maze, start=start, end=end, visual=False)
    print("\n\n=== Dijkstra ===")
    print(f"Shortest Path: {shortest_path_dijkstra}")
    print(f"\nShortest Path Cost: {len(shortest_path_dijkstra)}")

    # A*
    # Create an instance of the PathPlanner class:
    print("\n\n=== A* ===")
    test_planner = PathPlanner(grid=maze, visual=True)
    # Plan a path.
    shortest_path_astar = test_planner.a_star(start, end)
    print(f"Shortest Path: {shortest_path_astar}")
    print(f"\nShortest Path Cost: {len(shortest_path_astar)}")


#######################################################################################################

    # Start iterating different robots
    current_maze = maze

    orders_r1 = generate_packages_robot(maze=maze, number_of_packages=10)
    #orders_r1 = [[[5, 6], [11, 4]], [[11, 4], [1, 11]], [[1, 11], [14, 10]]]
    print(f"Orders R1: {orders_r1}")

    orders_r2 = generate_packages_robot(maze=maze, number_of_packages=10)
    #orders_r2 = [[[12, 9], [11, 1]], [[11, 1], [1, 5]], [[1, 5], [7, 7]]]
    print(f"\nOrders R2: {orders_r2}")
    
    # Position flags of robots
    r1_current_pos = orders_r1[0][0]
    r2_current_pos = orders_r2[0][0]

    # Path Planned for robots to deliver packages
    missing_path_r1 = []
    missing_path_r2 = []

    # Performance Check
    performance_check(maze=current_maze, orders=orders_r1)

    # Dataset creation to be used in RL
    orders_test_dataset = generate_packages_robot(maze=maze, number_of_packages=5)
    test_dataset = test_dataset_rl(orders_robot=orders_test_dataset, maze=current_maze)
    store_test_dataset(test_dataset)

    execution_flag = False
    if execution_flag:
        viz_map = mazeUI.create_initial_maze(maze=current_maze)
        while(len(orders_r2) > 0 or len(orders_r1) > 0):
            # if we have more orders 'waiting', let's assign them to the robot if he doesn't have anything to do
            if len(orders_r1) > 0 and not missing_path_r1:
                start_r1 = orders_r1[0][0]
                end_r1 = orders_r1[0][1]
                shortest_path_r1 = test_planner.a_star(start_r1, end_r1)
                missing_path_r1 = shortest_path_r1
                mazeUI.show_initial_and_goal_target(
                    viz_map=viz_map,
                    startX=start_r1[0],
                    startY=start_r1[1],
                    goalX=end_r1[0],
                    goalY=end_r1[1],
                    color_modifier=2
                )
            
            if len(orders_r2) > 0 and not missing_path_r2:
                start_r2 = orders_r2[0][0]
                end_r2 = orders_r2[0][1]
                shortest_path_r2 = test_planner.a_star(start_r2, end_r2)
                missing_path_r2 = shortest_path_r2
                mazeUI.show_initial_and_goal_target(
                    viz_map=viz_map,
                    startX=start_r2[0],
                    startY=start_r2[1],
                    goalX=end_r2[0],
                    goalY=end_r2[1]
                )

            # if the robot has somewhere to go, move
            if len(missing_path_r1) > 0: 
                missing_path_r1 = execute_robot_movement(orders_rb=orders_r1, 
                    missing_path_rb=missing_path_r1, 
                    current_maze=current_maze,
                    test_planner=test_planner,
                    rb_current_pos=r1_current_pos,
                    viz_map=viz_map,
                    color_modifier=2)

                if len(missing_path_r1) == 0:
                    print("R1: Goal Achieved, dropping package")
                    orders_r1.pop(0)


            if len(missing_path_r2) > 0: 
                missing_path_r2 = execute_robot_movement(orders_rb=orders_r2,
                    missing_path_rb=missing_path_r2, 
                    current_maze=current_maze,
                    test_planner=test_planner,
                    rb_current_pos=r2_current_pos,
                    viz_map=viz_map)
                
                if len(missing_path_r2) == 0:
                    print("R2: Goal Achieved, dropping package")
                    orders_r2.pop(0)

            time.sleep(0.5)  

if __name__ == '__main__':
    main()
