import pygame
import numpy as np
import numpy.linalg as la

class Wall:
    def __init__(self, a, b, color):
        self.a = np.array(a, dtype=np.int)
        self.b = np.array(b, dtype=np.int)
        self.color = color
        self.thickness = 3


    def draw(self, screen):
        if la.norm(self.a - self.b) > 0:
            pygame.draw.line(screen, self.color, self.a, self.b, self.thickness)
