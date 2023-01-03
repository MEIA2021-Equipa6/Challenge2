# Self Driving Car

# Importing the libraries
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import time

# Importing the Kivy packages
from kivy.app import App
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

# Importing the Dqn object from our AI in ai.py
from ai import Dqn

# Adding this line if we don't want the right click to put a red point
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '1200')

# Introducing last_x and last_y, used to keep the last point in memory when we draw the sand on the map
last_x = 0
last_y = 0
n_points = 0
length = 0

# Getting our AI, which we call "brain", and that contains our neural network that represents our Q-function
brain = Dqn(5,3,0.9)
action2rotation = [0,20,-20]
last_reward = 0
scores = []
goals = [[1400, 900], [100, 350], [1200, 650], [800, 1100]]

# Initializing the map
first_update = True
def init():
    global sand
    global goal_x
    global goal_y
    global first_update
    global cleared_goals
    cleared_goals = 0
    sand = np.zeros((longueur,largeur))

    # Rectangulo 1
    for x in range(200, 300):
        for y in range(200, 600):
            sand[x, y] = 1

    # Rectangulo 2
    for x in range(500, 700):
        for y in range(100, 150):
            sand[x, y] = 1

    # Rectangulo 3
    for x in range(1200, 1250):
        for y in range(800, 1100):
            sand[x, y] = 1

    # Rectangulo 4
    for x in range(500, 700):
        for y in range(500, 700):
            sand[x, y] = 1

    # Rectangulo 5
    for x in range(200, 250):
        for y in range(800, 1100):
            sand[x, y] = 1

    # Rectangulo 6
    for x in range(600, 1000):
        for y in range(800, 900):
            sand[x, y] = 1

    # Rectangulo 7
    for x in range(600, 700):
        for y in range(300, 400):
            sand[x, y] = 1

    # Rectangulo 8
    for x in range(900, 1300):
        for y in range(200, 300):
            sand[x, y] = 1

    # Rectangulo 9
    for x in range(1000, 1200):
        for y in range(500, 600):
            sand[x, y] = 1

    # Rectangulo 10
    for x in range(400, 750):
        for y in range(1100, 1150):
            sand[x, y] = 1

    # Rectangulo 11
    for x in range(1500, 1550):
        for y in range(500, 1000):
            sand[x, y] = 1

    goal_x = goals[cleared_goals][0]
    goal_y = goals[cleared_goals][1]

    first_update = False

# Initializing the last distance
last_distance = 0

# Creating the car class

class Car(Widget):
    
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        self.sensor2 = Vector(30, 0).rotate((self.angle+30)%360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle-30)%360) + self.pos
        self.signal1 = int(np.sum(sand[int(self.sensor1_x)-10:int(self.sensor1_x)+10, int(self.sensor1_y)-10:int(self.sensor1_y)+10]))/400.
        self.signal2 = int(np.sum(sand[int(self.sensor2_x)-10:int(self.sensor2_x)+10, int(self.sensor2_y)-10:int(self.sensor2_y)+10]))/400.
        self.signal3 = int(np.sum(sand[int(self.sensor3_x)-10:int(self.sensor3_x)+10, int(self.sensor3_y)-10:int(self.sensor3_y)+10]))/400.
        if self.sensor1_x>longueur-10 or self.sensor1_x<10 or self.sensor1_y>largeur-10 or self.sensor1_y<10:
            self.signal1 = 1.
        if self.sensor2_x>longueur-10 or self.sensor2_x<10 or self.sensor2_y>largeur-10 or self.sensor2_y<10:
            self.signal2 = 1.
        if self.sensor3_x>longueur-10 or self.sensor3_x<10 or self.sensor3_y>largeur-10 or self.sensor3_y<10:
            self.signal3 = 1.

class Ball1(Widget):
    pass
class Ball2(Widget):
    pass
class Ball3(Widget):
    pass
class Rectangle1(Widget):
    pass
class Rectangle2(Widget):
    pass
class Rectangle3(Widget):
    pass
class Rectangle4(Widget):
    pass
class Rectangle5(Widget):
    pass
class Rectangle6(Widget):
    pass
class Rectangle7(Widget):
    pass
class Rectangle8(Widget):
    pass
class Rectangle9(Widget):
    pass
class Rectangle10(Widget):
    pass
class Rectangle11(Widget):
    pass
class Goal1(Widget):
    pass
class Goal2(Widget):
    pass
class Goal3(Widget):
    pass
class Goal4(Widget):
    pass

# Creating the game class

class Game(Widget):

    car = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)
    rectangle1 = ObjectProperty(None)
    rectangle2 = ObjectProperty(None)
    rectangle3 = ObjectProperty(None)
    rectangle4 = ObjectProperty(None)
    rectangle5 = ObjectProperty(None)
    rectangle6 = ObjectProperty(None)
    rectangle7 = ObjectProperty(None)
    rectangle8 = ObjectProperty(None)
    rectangle9 = ObjectProperty(None)
    rectangle10 = ObjectProperty(None)
    rectangle11 = ObjectProperty(None)
    goal1 = ObjectProperty(None)
    goal2 = ObjectProperty(None)
    goal3 = ObjectProperty(None)
    goal4 = ObjectProperty(None)

    def serve_car(self):
        self.car.center = self.center
        self.car.velocity = Vector(0, 0)
        global longueur
        global largeur
        longueur = 1600
        largeur = 1200
        if first_update:
            init()

    def set_goal(self):
        global goal_x
        global goal_y
        print("Enter X coord: ")
        goal_x = int(input())
        print("Enter Y coord: ")
        goal_y = int(input())
        is_sand = self.verify_if_sand(goal_x, goal_y)
        if is_sand:
            print("Input coordinates are part of an obstacle. Insert new ones")
            self.set_goal()
        else:
            self.car.velocity = Vector(3, 0).rotate(self.car.angle)

    def verify_if_sand(self, goal_x, goal_y):
        if sand[goal_x, goal_y] == 1:
            return True
        else:
            return False

    def update(self, dt):

        global brain
        global last_reward
        global scores
        global last_distance
        global goal_x
        global goal_y
        global cleared_goals

        xx = goal_x - self.car.x
        yy = goal_y - self.car.y
        orientation = Vector(*self.car.velocity).angle((xx,yy))/180.
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation]
        action = brain.update(last_reward, last_signal)
        scores.append(brain.score())
        rotation = action2rotation[action]
        self.car.move(rotation)
        distance = np.sqrt((self.car.x - goal_x)**2 + (self.car.y - goal_y)**2)
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3

        if sand[int(self.car.x),int(self.car.y)] > 0:
            self.car.velocity = Vector(1, 0).rotate(self.car.angle)
            last_reward = -100
        else: # otherwise
            self.car.velocity = Vector(3, 0).rotate(self.car.angle)
            last_reward = 0.0
            if distance < last_distance:
                last_reward = 0.5

        if self.car.x < 10:
            self.car.x = 10
            last_reward = -1
        if self.car.x > self.width - 10:
            self.car.x = self.width - 10
            last_reward = -1
        if self.car.y < 10:
            self.car.y = 10
            last_reward = -1
        if self.car.y > self.height - 10:
            self.car.y = self.height - 10
            last_reward = -1

        if distance < 25:
            last_reward = 100
            cleared_goals = cleared_goals + 1
            print("Cleared Goals:" + str(cleared_goals))
            if cleared_goals < len(goals):
                goal_x = goals[cleared_goals][0]
                goal_y = goals[cleared_goals][1]
            else:
                self.set_goal()
            #goal_x = self.width - goal_x
            #goal_y = self.height - goal_y

        last_distance = distance


# Adding the painting tools

class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        global length, n_points, last_x, last_y
        with self.canvas:
            Color(0.8,0.7,0)
            d = 10.
            touch.ud['line'] = Line(points = (touch.x, touch.y), width = 10)
            last_x = int(touch.x)
            last_y = int(touch.y)
            n_points = 0
            length = 0
            sand[int(touch.x),int(touch.y)] = 1

    def on_touch_move(self, touch):
        global length, n_points, last_x, last_y
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            length += np.sqrt(max((x - last_x)**2 + (y - last_y)**2, 2))
            n_points += 1.
            density = n_points/(length)
            touch.ud['line'].width = int(20 * density + 1)
            sand[int(touch.x) - 10 : int(touch.x) + 10, int(touch.y) - 10 : int(touch.y) + 10] = 1
            last_x = x
            last_y = y

# Adding the API Buttons (clear, save and load)


class CarApp(App):

    def build(self):
        parent = Game()
        parent.serve_car()
        Clock.schedule_interval(parent.update, 1.0/60.0)
        self.painter = MyPaintWidget()
        clearbtn = Button(text = 'clear')
        savebtn = Button(text = 'save', pos = (parent.width, 0))
        loadbtn = Button(text = 'load', pos = (2 * parent.width, 0))
        clearbtn.bind(on_release = self.clear_canvas)
        savebtn.bind(on_release = self.save)
        loadbtn.bind(on_release = self.load)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(savebtn)
        parent.add_widget(loadbtn)
        return parent

    def clear_canvas(self, obj):
        global sand
        self.painter.canvas.clear()
        sand = np.zeros((longueur,largeur))
        # Rectangulo 1
        for x in range(200, 300):
            for y in range(200, 600):
                sand[x, y] = 1

        # Rectangulo 2
        for x in range(500, 700):
            for y in range(100, 150):
                sand[x, y] = 1

        # Rectangulo 3
        for x in range(1200, 1250):
            for y in range(800, 1100):
                sand[x, y] = 1

        # Rectangulo 4
        for x in range(500, 700):
            for y in range(500, 700):
                sand[x, y] = 1

        # Rectangulo 5
        for x in range(200, 250):
            for y in range(800, 1100):
                sand[x, y] = 1

        # Rectangulo 6
        for x in range(600, 1000):
            for y in range(800, 900):
                sand[x, y] = 1

        # Rectangulo 7
        for x in range(200, 300):
            for y in range(500, 700):
                sand[x, y] = 1

        # Rectangulo 8
        for x in range(900, 1300):
            for y in range(200, 300):
                sand[x, y] = 1

        # Rectangulo 9
        for x in range(1000, 1200):
            for y in range(500, 600):
                sand[x, y] = 1

        # Rectangulo 10
        for x in range(400, 750):
            for y in range(1100, 1150):
                sand[x, y] = 1

        # Rectangulo 11
        for x in range(1500, 1550):
            for y in range(500, 1000):
                sand[x, y] = 1

    def save(self, obj):
        print("saving brain...")
        brain.save()
        plt.plot(scores)
        plt.show()

    def load(self, obj):
        print("loading last saved brain...")
        brain.load()

# Running the whole thing
if __name__ == '__main__':
    CarApp().run()
