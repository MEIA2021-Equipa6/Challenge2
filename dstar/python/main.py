from random import randrange
from gui import Animation
from d_star_lite import DStarLite
from grid import OccupancyGridMap, SLAM
import time

BUFFERZONE = 128
BUFFERZONE1 = 129
OBSTACLE = 255
UNOCCUPIED = 0
starttime = time.time()

if __name__ == '__main__':

    """
    set initial values for the map occupancy grid
    |----------> y, column
    |           (x=0,y=2)
    |
    V (x=2, y=0)
    x, row
    """
    x_dim = 100
    y_dim = 80
    start = (randrange(x_dim), randrange(y_dim))
    goal = (randrange(x_dim), randrange(y_dim))
    start1 = (randrange(x_dim), randrange(y_dim))
    goal1 = (randrange(x_dim), randrange(y_dim))
    view_range = 5

    """"
    Path with forced colision
    start = (1, 1)
    goal = (98, 78)
    start1 = (98, 0)
    goal1 = (1, 78)
    
    Side by side path correction
    start = (2, 1)
    goal = (99, 1)
    start1 = (99, 2)
    goal1 = (1, 2)
    """""

    gui = Animation(title="D* Lite Path Planning",
                    width=10,
                    height=10,
                    margin=0,
                    x_dim=x_dim,
                    y_dim=y_dim,
                    start=start,
                    goal=goal,
                    start1=start1,
                    goal1=goal1,
                    viewing_range=view_range)

    new_map = gui.world
    old_map = new_map
    new_position = start
    last_position = start
    new_position1 = start1
    last_position1 = start1

    # new_observation = None
    # type = OBSTACLE

    # D* Lite (optimized)
    dstar = DStarLite(map=new_map,
                      s_start=start,
                      s_goal=goal)

    # D* Lite (optimized)
    dstar1 = DStarLite(map=new_map,
                       s_start=start1,
                       s_goal=goal1)

    # SLAM to detect vertices
    slam = SLAM(map=new_map,
                view_range=view_range,
                robot=1)
    slam1 = SLAM(map=new_map,
                 view_range=view_range,
                 robot=2)

    # move and compute path
    path, g, rhs = dstar.move_and_replan(robot_position=new_position)
    # move and compute path
    path1, g1, rhs1 = dstar1.move_and_replan(robot_position=new_position1)

    len_path = len(path)
    len_path1 = len(path1)

    while not gui.done:
        if len(path) == 1 and len(path1) == 1:
            gui.set_done()
        # update the map
        # print(path)
        # drive gui
        gui.run_game(path=path, path1=path1)

        new_position = gui.current
        new_position1 = gui.current1
        new_observation = gui.observation
        new_observation1 = gui.observation1
        new_map = gui.world

        """
        if new_observation is not None:
            if new_observation["type"] == OBSTACLE:
                dstar.global_map.set_obstacle(pos=new_observation["pos"])
            if new_observation["pos"] == UNOCCUPIED:
                dstar.global_map.remove_obstacle(pos=new_observation["pos"])
        """

        if new_observation is not None:
            old_map = new_map
            slam.set_ground_truth_map(gt_map=new_map)

        if new_position != last_position:
            last_position = new_position

            # slam
            new_edges_and_old_costs, slam_map = slam.rescan(global_position=new_position)

            dstar.new_edges_and_old_costs = new_edges_and_old_costs
            dstar.sensed_map = slam_map

            # d star
            path, g, rhs = dstar.move_and_replan(robot_position=new_position)
        else:
            last_position = new_position

        if new_observation1 is not None:
            old_map = new_map
            slam.set_ground_truth_map(gt_map=new_map)
            slam1.set_ground_truth_map(gt_map=new_map)

        if new_position1 != last_position1:
            last_position1 = new_position1

            # slam
            new_edges_and_old_costs, slam_map1 = slam1.rescan(global_position=new_position1)

            dstar1.new_edges_and_old_costs = new_edges_and_old_costs
            dstar1.sensed_map = slam_map1

            # d star
            path1, g1, rhs = dstar1.move_and_replan(robot_position=new_position1)
        else:
            last_position1 = new_position1

    endtime = time.time() - starttime
    if len_path > len_path1:
        print("Biggest Path was Robot 1 with " + str(len_path) + " steps.")
        print("Shortest Path was Robot 2 with " + str(len_path1) + " steps.")
    else:
        print("Biggest Path was Robot 2 with " + str(len_path1) + " steps.")
        print("Shortest Path was Robot 1 with " + str(len_path) + " steps.")
    average_time_robot1 = endtime/len_path
    average_time_robot2 = endtime/len_path1
    print("Average execution time per steps for Robot 1 was " + str(average_time_robot1) + "s.")
    print("Average execution time per steps for Robot 2 was " + str(average_time_robot2) + "s.")
    print("Execution time: " + str(endtime) + "s.")

