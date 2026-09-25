import pygame

class Player:
    def __init__(self):
        """
        Physics
        """
        self._ground_friction = 0.90
        self._air_friction = 0.99

        self.posX = 0
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.accX = 0
        self.accY = 0

        self.speedCap = 500
        self.gravity = 4000
        self.friction = self._ground_friction
        self._onground = False

        """
        Animations
        """
        self._spriteSheet = pygame.image.load('assets/knight.png')
        self._frame_width = 32
        self._frame_height = 32

        self._facing_left = False

        # Cropping dimensions for accurate sprite hitbox
        offset_x = 9
        offset_y = 9
        crop_width = 13
        crop_height = 19

        # Create idle frame list
        self._idle_frames = []

        # Load idle animation
        for i in range(4):
            # Find the current x coordinate of the frame
            frame_x = i*self._frame_width

            # Create the rect starting at frame_x, 0 and with size width height
            rect = pygame.Rect(frame_x + offset_x, offset_y, crop_width, crop_height)

            image = self._spriteSheet.subsurface(rect)

            # Rescale
            image = pygame.transform.scale(image, (39, 57))
            self._idle_frames.append(image)

        # Create running frame list
        self._running_frames = []

        # Load running frames from spritesheet
        for i in range(16):
            # Find current x y coord for frame
            frame_x = (i%8) * self._frame_width
            frame_y = 3*self._frame_height if i > 8 else 2*self._frame_height

            # Create the rect
            rect = pygame.Rect(frame_x + offset_x, frame_y + offset_y, crop_width, crop_height)
            # Create and rescale
            image = self._spriteSheet.subsurface(rect)
            image = pygame.transform.scale(image, (39, 57))
            # Append the image to list
            self._running_frames.append(image)


        # Init values for animation
        self._animation_speed = 10
        self._current_idle_frame = 0
        self._current_running_frame = 0

        # Set the player image, rect, and hitbox
        self.image = self._idle_frames[0]
        self.rect = self.image.get_rect(topleft=(self.posX, self.posY))

    def update(self, T, platforms):
        self._updateX(T, platforms)
        self._updateY(T, platforms)
        self._updateAnimation(T)

    """
    Physics
    """
    def _updateX(self, T, platforms):

        # Cancel velocity if it's too small to prevent sliding forever
        if abs(self.velX) < 30:
            self.velX = 0

        # Apply accelerations to get velocity
        self.velX += self.accX * T
        self.velX *= self.friction


        # Code to so it's impossible to accelerate over speed cap
        if self.velX >= self.speedCap:
            self.velX = self.speedCap
        if self.velX <= -self.speedCap:
            self.velX = -self.speedCap

        # Code to stop going out of the screen
        # Left side
        if self.posX <= 0 and self.velX < 0:
            self.posX = 0
            self.velX = 0
        # Right side
        if self.posX + self.rect.width >= 1920 and self.velX > 0:
            self.posX = 1920 - self.rect.width
            self.velX = 0

        # Platform collision detection
        """
        if self.rect.collidelist(platforms):
            self.velX = 0
        """

        # Update position
        self.posX += self.velX * T

        # Send new pos to rect
        self.rect.x = self.posX


    def _updateY(self, T, platforms):

        # Standard state is not on ground
        self._onground = False

        # Apply accel upward
        self.velY += self.accY * T
        # Apply gravity
        self.velY += self.gravity * T

        # Ground check
        if self.posY + self.rect.height >= 1080 and self.velY > 0:
            self.posY = 1080 - self.rect.height
            self._onground = True
        else:
            self.friction = self._air_friction

        # Platform collision, -1 means no collision
        if self.rect.collidelist(platforms) != -1:
            self._onground = True

        # Ground logic
        if self._onground:
            self.velY = 0
            self.friction = self._ground_friction
        else:
            self.friction = self._air_friction

        # Update pos
        self.posY += self.velY * T

        # Send pos to rect
        self.rect.y = self.posY

    """
    Animations
    """
    def _updateAnimation(self, T):
        # If moving
        if abs(self.velX) > 0.1:
            # Advance the current idle frame
            self._current_running_frame += self._animation_speed * T

            # Repeat animation
            if self._current_running_frame >= len(self._running_frames):
                self._current_running_frame = 0

            # Update the pygame image
            self.image = self._running_frames[int(self._current_running_frame)]
            self._facing_left = False

            # Flip logic
            if self.velX < 0:
                self.image = pygame.transform.flip(self.image, True, False)
                self._facing_left = True

        # If idle
        else:
            self._current_idle_frame += self._animation_speed * T

            if self._current_idle_frame >= len(self._idle_frames):
                self._current_idle_frame = 0

            self.image = self._idle_frames[int(self._current_idle_frame)]

            if self._facing_left:
                self.image = pygame.transform.flip(self.image, True, False)



