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
        self.rect_closed = self.image.get_rect(topleft=(x + offset_x*4, y))
        self.rect_open = pygame.Rect(0,0,0,0)

        self.rect = self.rect_closed

    def update(self, T, buttons):
        self.closed = True

        for b in buttons:
            if b.pressed:
                self.closed = False

        if self.closed:
            if self.alpha < 255:
                self.alpha += 200 * T
            else:
                self.alpha = 255
            self.rect = self.rect_closed

        if not self.closed:
            if self.alpha > 0:
                self.alpha -= 200 * T
            else:
                self.alpha = 0
                self.rect = self.rect_open

        self.image.set_alpha(self.alpha)
