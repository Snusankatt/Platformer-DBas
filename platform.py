import pygame

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

        self.image = pygame.Surface((width, height))
        self.image.fill("green")