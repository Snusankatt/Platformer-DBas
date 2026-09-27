import pygame

class Door:
    def __init__(self, x, y):
        self._spritesheet = pygame.image.load('./assets/world_tileset.png')

        self.closed = True
        self.alpha = 255

        offset_x = 3
        offset_y = 0
        crop_width = 10
        crop_height = 16
        frame_size = 16

        rect = pygame.Rect(2*frame_size + offset_x, 8*frame_size, crop_width, crop_height)
        self.image = self._spritesheet.subsurface(rect)
        self.image = pygame.transform.scale(self.image, (40, 64))
        self.rect = self.image.get_rect(topleft=(x + offset_x*4, y))

    def update(self, T):
        if self.closed:
            if self.alpha < 255:
                self.alpha += int(20 * T)
            else:
                self.alpha = 255

        if not self.closed:
            if self.alpha > 0:
                self.alpha -= int(20 * T)
            else:
                self.alpha = 0
