import pygame
import time
import itertools
import numpy as np
import numpy.linalg as la

from ball import Ball
from wall import Wall

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.frames_per_second = 60
        self.max_num_balls = 30
        self.gravity = np.array([0, 300], dtype=np.float)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                self.is_running = False
            elif event.type is pygame.KEYDOWN:
                if event.key is pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key is pygame.K_RETURN:
                    if len(self.balls) < self.max_num_balls:
                        self.add_ball()
            elif event.type is pygame.MOUSEBUTTONDOWN:
                if event.button is 1:   # Left Mouse Button
                    self.is_building_wall = True
                    pos = pygame.mouse.get_pos()
                    self.add_wall(pos, pos)
            elif event.type is pygame.MOUSEBUTTONUP:
                if event.button is 1:   # Left Mouse Button
                    self.is_building_wall = False
            elif event.type is pygame.MOUSEMOTION:
                if self.is_building_wall:
                    pos = pygame.mouse.get_pos()
                    self.walls[-1].b = pos

    def update(self, dt):
        for ball_a, ball_b in itertools.combinations(self.balls, r=2):
            Ball.ball_ball_collision(ball_a, ball_b, dt)

        for ball in self.balls:
            ball.apply_force(self.gravity * ball.mass)

        for ball in self.balls:
            for wall in self.walls:
                ball.wall_collision(wall, dt)

        for ball in self.balls:
            ball.update(dt)

    def render(self):
        self.screen.fill((0, 0, 0))
        for _object in self.balls + self.walls:
            _object.draw(self.screen)
        pygame.display.flip()

    def play(self):
        self.is_running = True
        self.is_building_wall = False
        self.balls = []
        color = (255, 255, 255)
        self.walls = [Wall((1, 1), (self.width-1, 1), color),                           # ceiling
                      Wall((1, 1), (1, self.height-1), color),                          # left wall
                      Wall((1, self.height-1), (self.width-1, self.height-1), color),   # floor
                      Wall((self.width-1, 1), (self.width-1, self.height-1), color)]    # right wall

        last_frame_time = time.time()
        while self.is_running:
            time_remaining = 1. / self.frames_per_second - (time.time() - last_frame_time)
            if time_remaining > 0:
                time.sleep(time_remaining)
            current_frame_time = time.time()
            dt = current_frame_time - last_frame_time
            dt = max(0.00001, min(dt, 0.1))
            last_frame_time = current_frame_time

            self.event_handler()
            self.update(dt)
            self.render()

    def add_ball(self):
        radius = int(np.random.randint(10, 30))
        x = int(np.random.randint(radius, self.width - radius))
        y = radius + 5
        color = np.floor(np.random.random(3) * 200 + 55).astype(np.int)
        self.balls.append(Ball((x, y), radius, color))

    def add_wall(self, a, b):
        color = np.floor(np.random.rand(3) * 200 + 55).astype(np.int)
        self.walls.append(Wall(a, b, color))

if __name__ == "__main__":
    mygame = Game(width=400, height=400)
    mygame.play()
