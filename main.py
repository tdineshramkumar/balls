""" This simulates when multiple balls in a container where collisions are perfectly elastic"""

from ball import Ball
import pygame
from pygame import Vector2
from itertools import combinations
from random import randint, randrange

""" Create a pygame window """
pygame.init()
width, height = 400, 400
win = pygame.display.set_mode((width, height))
winRect = win.get_rect()
clock = pygame.time.Clock()

""" Setting radius and mass of all balls same"""
radius = 10
mass = 1
max_speed = 10
num_balls = 40

""" Create balls at random locations with random velocities """
balls = [Ball(Vector2(randint(radius, width-radius), randint(radius, height-radius)),
              Vector2(randrange(max_speed), randrange(max_speed)), winRect, radius=radius, mass=mass) for _ in range(num_balls)]

""" Colors to use for the balls """
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
Run = True
while Run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False

    """ Fill the background """
    win.fill((255, 255, 255))
    """ Draw each of the ball """
    for index, ball in enumerate(balls):
        pygame.draw.circle(win, colors[index%len(colors)], (int(ball.position.x), int(ball.position.y)), int(ball.radius))

    for _ in range(10):
        """ Update velocities on collision """
        for ball1, ball2 in combinations(balls, 2):
            if ball1.check_collision(ball2):
                ball1.collide(ball2)
        """ Update positions of balls """
        for ball in balls:
            ball.update(0.1)

        # print("Total kinetic energy:", sum(ball.kinetic_energy() for ball in balls))
    pygame.display.update()
