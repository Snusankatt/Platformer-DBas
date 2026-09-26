import pygame

class Prize:
    def __init__(self, x, y):
        self._spritesheet = pygame.image.load('./assets/coin.png')

        self.is_collected = False
        self.collect_timer = 0
        self.should_be_killed = False
        self.alpha = 255

        offset_x = 3
        offset_y = 3
        crop_width = 10
        crop_height = 10
        frame_size = 16

        self._frames = []

        for i in range(12):
            frame_x = i * frame_size

            rect = pygame.Rect(frame_x + offset_x, offset_y, crop_width, crop_height)

            image = self._spritesheet.subsurface(rect)

            image = pygame.transform.scale(image, (60, 60))

            self._frames.append(image)

        # Init values
        self._animation_speed = 10
        self._current_frame = 0
        self.image = self._frames[0]
        self.rect = self.image.get_rect(topleft=(x+offset_x, y+offset_y))

    def update(self, T):

        self._current_frame += self._animation_speed * T

        if self._current_frame >= len(self._frames):
            self._current_frame = 0

        self.image = self._frames[int(self._current_frame)]

        if self.is_collected:
            self.collect_timer += T

            self.alpha -= 10
            self.rect.y -= int(200 * T)

            self.image.set_alpha(self.alpha)

            if self.collect_timer >= 0.35:
                self.should_be_killed = True