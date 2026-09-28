import pygame

class Button:
    def __init__(self, x, y):
        self._spritesheet = pygame.image.load("./assets/button.png")

        self.pressed = False

        offset_x = 2
        crop_width = 14
        scale = 4

        rect1 = pygame.Rect(offset_x, 11, crop_width, 5) # unpressed
        rect2 = pygame.Rect(16 + offset_x, 13, crop_width, 3) # pressed

        self.image_released = self._spritesheet.subsurface(rect1)
        self.image_pressed = self._spritesheet.subsurface(rect2)

        self.image_released = pygame.transform.scale(self.image_released, (14*scale, 5*scale))
        self.image_pressed = pygame.transform.scale(self.image_pressed, (14*scale, 3*scale))

        self.rect_released = self.image_released.get_rect(topleft=(x + offset_x*scale, y + 11*scale))
        self.rect_pressed = self.image_pressed.get_rect(topleft=(x + offset_x*scale, y + 13*scale))

        self.rect_hitbox = self.rect_released.copy()
        self.rect_hitbox.y -= 1
        self.rect_hitbox.height += 1

        # Init values
        self.image = self.image_released
        self.rect = self.rect_released

    def update(self, players):

        if self.rect_hitbox.collidelist(players) != -1:
            self.pressed = True
        else:
            self.pressed = False

        if self.pressed:
            self.image = self.image_pressed
            self.rect = self.rect_pressed
        else:
            self.image = self.image_released
            self.rect = self.rect_released

