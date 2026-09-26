import pygame

class Enemy:
    def __init__(self, x, y):
        self._spritesheet = pygame.image.load("./assets/slime_purple.png")

        offset_x = 5
        offset_y = 9
        crop_width = 14
        crop_height = 16
        frame_size = 24

        self._idle_frames = []

        for i in range(4):
            frame_x = i * frame_size

            rect = pygame.Rect(frame_x + offset_x, frame_size + offset_y, crop_width, crop_height)

            image = self._spritesheet.subsurface(rect)

            image = pygame.transform.scale(image, (56, 63))

            self._idle_frames.append(image)

        # Init values
        self._animation_speed = 10
        self._current_idle_frame = 0
        self.image = self._idle_frames[0]
        self.rect = self.image.get_rect(topleft=(x+offset_x, y+offset_y))

    def update(self, T):
        self._current_idle_frame += self._animation_speed * T

        if self._current_idle_frame >= len(self._idle_frames):
            self._current_idle_frame = 0

        self.image = self._idle_frames[int(self._current_idle_frame)]