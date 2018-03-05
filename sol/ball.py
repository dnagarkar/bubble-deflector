import pygame
import numpy as np
import numpy.linalg as la

class Ball:
    def __init__(self, position, radius, color):
        self.position = np.array(position, dtype=np.float)
        self.velocity = np.array([0, 0], dtype=np.float)
        self.acceleration = np.array([0, 0], dtype=np.float)
        self.radius = radius
        self.mass = radius ** 2
        self.color = color
        self.thickness = 3
        self.speed_limit = 500

    def limit_speed(self, v):
        speed = la.norm(v)
        if speed < self.speed_limit:
            return v
        else:
            return self.speed_limit * v / speed

    def apply_force(self, force):
        self.acceleration = self.acceleration + force / self.mass

    def update(self, dt):
        self.velocity = self.limit_speed(dt * self.acceleration + self.velocity)
        self.position = dt * self.velocity + self.position
        self.acceleration = np.array([0, 0], dtype=np.float)

    def ball_ball_collision(ball_a, ball_b, dt):
        if la.norm(ball_a.position - ball_b.position) <= ball_a.radius + ball_b.radius:
            # Hide this in another function
            error = ((ball_a.radius + ball_b.radius - la.norm(ball_a.position - ball_b.position)) / 2
                        * (ball_a.position - ball_b.position) / la.norm(ball_a.position - ball_b.position))
            ball_a.position = ball_a.position + error
            ball_b.position = ball_b.position - error

            # Hide in compute ball collision function
            force_a = (-2 / dt * ball_a.mass * ball_b.mass / (ball_a.mass + ball_b.mass)
                        * np.dot(ball_a.velocity - ball_b.velocity,
                                 ball_a.position - ball_b.position)
                        / la.norm(ball_a.position - ball_b.position) ** 2
                        * (ball_a.position - ball_b.position))
            force_b = (-2 / dt * ball_a.mass * ball_b.mass / (ball_a.mass + ball_b.mass)
                        * np.dot(ball_b.velocity - ball_a.velocity,
                                 ball_b.position - ball_a.position)
                        / la.norm(ball_b.position - ball_a.position) ** 2
                        * (ball_b.position - ball_a.position))

            ball_a.apply_force(force_a)
            ball_b.apply_force(force_b)

    def wall_collision(self, wall, dt):
        if la.norm(wall.a - wall.b) == 0:
            return

        d_norm = np.dot((wall.b - wall.a) / la.norm(wall.b - wall.a), self.position - wall.a)
        if 0 <= d_norm and d_norm <= la.norm(wall.b - wall.a):
            d = d_norm * (wall.b - wall.a) / la.norm(wall.b - wall.a) + wall.a
        elif -self.radius <= d_norm and d_norm < 0:
            d = wall.a
        elif la.norm(wall.b - wall.a) < d_norm and d_norm <= la.norm(wall.b - wall.a) + self.radius:
            d = wall.b
        else:
            return

        normal = self.position - d
        distance = la.norm(normal)
        normal = normal / distance
        if distance <= self.radius:
            self.position = d + self.radius * normal
            force = self.mass / dt * 2 * normal * np.dot(-self.velocity, normal)
            self.apply_force(force)

    def draw(self, screen):
        position = self.position.astype(np.int)
        screen_bounds = np.array([[0, 0], [screen.get_width(), screen.get_height()]], dtype=np.int)
        if np.all(screen_bounds[0] < position) and np.all(position < screen_bounds[1]):
            pygame.draw.circle(screen, self.color, position, self.radius, self.thickness)
