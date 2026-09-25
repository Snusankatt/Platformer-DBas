import pygame

class Player:
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.accX = 0
        self.accY = 0

        self.speedCap = 750
        self.friction = 0.95
        self.gravity = 4000

        self.isAlive = True

        self.rect = pygame.Rect(self.posX, self.posY, 6, 10)

    def updateX(self, T):

        # Apply accelerations to get velocity
        self.velX += self.accX * T
        self.velX *= self.friction

        # Code to so it's impossible to accelerate over speed cap
        if self.velX >= self.speedCap:
            self.velX = self.speedCap
        if self.velX <= -self.speedCap:
            self.velX = -self.speedCap

        # Code to stop going out of the screen
        if self.posX <= 0 and self.velX < 0:
            self.posX = 0
            self.velX = 0
        if self.posX + self.rect.width >= 1920 and self.velX > 0:
            self.posX = 1920 - self.rect.width
            self.velX = 0

        # Update position
        self.posX += self.velX * T

        # Send new pos to rect
        self.rect.x = self.posX

    def updateY(self, T):

        # Apply accel upward
        self.velY += self.accY * T
        # Apply gravity
        self.velY += self.gravity * T

        # Ground check
        if self.posY + self.rect.height >= 1080 and self.velY > 0:
            self.posY = 1080 - self.rect.height
            self.velY = 0

        # Update pos
        self.posY += self.velY * T

        # Send pos to rect
        self.rect.y = self.posY