import pygame
import random
import math

class Enemy:
    def __init__(self, target_x, target_y, image, speed=2):
        self.x = -100  # atsiranda už ekrano ribų (iš kairės)
        self.y = random.randint(0, 940 - 150)
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.image = image

        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy) or 1.0
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surf):
        surf.blit(self.image, (int(self.x), int(self.y)))
