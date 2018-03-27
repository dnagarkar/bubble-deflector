import pygame
import numpy as np
import numpy.linalg as la

class Ball:
    def __init__(self, position, radius, color):
        self.position = np.array(position, dtype=np.float)
        self.velocity = np.array([0, 0], dtype=np.float)
        self.acceleration = np.array([0, 0], dtype=np.float)
        self.radius = radius
        self.mass = radius ** 2.
        self.color = color
        self.thickness = 3
        self.speed_limit = 500


    def limit_speed(self, velocity):
        """
        Returns a velocity that is no faster than self.speed_limit.
        """
        speed = la.norm(velocity)
        if speed < self.speed_limit:
            return velocity
        else:
            return self.speed_limit * velocity / speed


    def apply_force(self, force):
        """
        Add this force to this ball.
        Hint: Force = Mass * Acceleration
        """
        pass # TODO: Delete this line and add your code!


    def update(self, dt):
        """
        Update the velocity using acceleration.
        (We also want to make sure the ball is not moving too fast)
        Update position using velocity.
        """
        pass # TODO: Delete this line and add your code!
        # We reset acceleration back to zero.
        self.acceleration = np.array([0, 0], dtype=np.float)


    def ball_ball_collision(ball_a, ball_b, dt):
        """
        We first want to check if `ball_a` and `ball_b` are colliding.
        If so, we need to apply a force to each ball.
        Hint: Take a look at `Ball.reset_ball_collision_positions`
                and `Ball.compute_ball_collision_forces`
        """
        pass # TODO: Delete this line and add your code!


    def wall_collision(self, wall, dt):
        """
        We first want to check if this ball is colliding with `wall`.
        If so, we want to compute the force on the ball.
        Hint: Take a look at `self.compute_wall_collision_point`
        """
        pass # TODO: Delete this line and add your code!


    def draw(self, screen):
        """
        Draw this ball to the screen.
        """
        position = self.position.astype(np.int)
        screen_bounds = np.array([[0, 0], [screen.get_width(), screen.get_height()]], dtype=np.int)
        if np.all(screen_bounds[0] < position) and np.all(position < screen_bounds[1]):
            pygame.draw.circle(screen, self.color, position, self.radius, self.thickness)


    def compute_wall_collision_point(self, wall):
        """
        Returns the point where ball and wall intersect or False if they do not
        intersect.
        """
        if la.norm(wall.a - wall.b) == 0:
            return False

        d_norm = np.dot((wall.b - wall.a) / la.norm(wall.b - wall.a), self.position - wall.a)
        if 0 <= d_norm and d_norm <= la.norm(wall.b - wall.a):
            d = d_norm * (wall.b - wall.a) / la.norm(wall.b - wall.a) + wall.a
        elif -self.radius <= d_norm and d_norm < 0:
            d = wall.a
        elif la.norm(wall.b - wall.a) < d_norm and d_norm <= la.norm(wall.b - wall.a) + self.radius:
            d = wall.b
        else:
            return False

        if la.norm(self.position - d) <= self.radius:
            return d
        return False

    def compute_ball_collision_forces(ball_a, ball_b, dt):
        """
        Returns the two forces acting on `ball_a` and `ball_b` when
        they collide.
        """
        force_a = (-2. / dt * ball_a.mass * ball_b.mass / (ball_a.mass + ball_b.mass)
                    * np.dot(ball_a.velocity - ball_b.velocity,
                             ball_a.position - ball_b.position)
                    / la.norm(ball_a.position - ball_b.position) ** 2.
                    * (ball_a.position - ball_b.position))
        force_b = (-2. / dt * ball_a.mass * ball_b.mass / (ball_a.mass + ball_b.mass)
                    * np.dot(ball_b.velocity - ball_a.velocity,
                             ball_b.position - ball_a.position)
                    / la.norm(ball_b.position - ball_a.position) ** 2.
                    * (ball_b.position - ball_a.position))

        return force_a, force_b


    def reset_ball_collision_positions(ball_a, ball_b):
        """
        Set the positions of `ball_a` and `ball_b` so that they intersect at
        exactly one point.
        """
        distance = la.norm(ball_a.position - ball_b.position)
        error = ((ball_a.radius + ball_b.radius - distance) / 2.
                    * (ball_a.position - ball_b.position) / distance)
        ball_a.position = ball_a.position + error
        ball_b.position = ball_b.position - error
