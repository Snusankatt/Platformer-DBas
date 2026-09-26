import pygame

class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        """
        Physics
        """
        self._ground_friction = 0.85
        self._air_friction = 0.95

        self.posX = 0
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.accX = 0

        self.speedCap = 500
        self.running_speed = 5000
        self.jump_force = -1300
        self.gravity = 4000
        self.friction = self._ground_friction
        self.stop_velocity = 30 # DONT go over 30
        self.on_ground = False

        """
        States
        """
        self.is_alive = True
        self.has_won = False

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
        image_scale = 3

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
            image = pygame.transform.scale(image, (crop_width * image_scale, crop_height * image_scale))
            self._idle_frames.append(image)

        # Create running frame list
        self._running_frames = []

        # Load running frames from spritesheet
        for i in range(16):
            # Find current x y coord for frame
            frame_x = (i%8) * self._frame_width
            frame_y = 3*self._frame_height if i > 8 else 2*self._frame_height

            # Create the rect
            rect = pygame.Rect(frame_x + offset_x - 1, frame_y + offset_y, crop_width + 1, crop_height)
            # Create and rescale
            image = self._spriteSheet.subsurface(rect)
            image = pygame.transform.scale(image, ((crop_width + 1) * image_scale, crop_height * image_scale))
            # Append the image to list
            self._running_frames.append(image)

        self._death_frames = []
        for i in range(4):
            frame_x = i * self._frame_width
            frame_y = 7 * self._frame_height

            rect = pygame.Rect(frame_x + offset_x, frame_y + offset_y, crop_width + 5, crop_height)

            image = self._spriteSheet.subsurface(rect)
            image = pygame.transform.scale(image, ((crop_width + 5) * image_scale, crop_height * image_scale))
            self._death_frames.append(image)


        # Init values for animation
        self._animation_speed = 10
        self._current_idle_frame = 0
        self._current_running_frame = 0
        self._current_death_frame = 0

        # Set the player image, rect, and hitbox
        self.image = self._idle_frames[0]
        self.rect = self.image.get_rect(topleft=(self.posX, self.posY))


    def update(self, T, platforms, enemies, prizes):
        self._updateState(enemies, prizes)
        self._updateX(T, platforms)
        self._updateY(T, platforms)
        self._updateAnimation(T)

    """
    Physics
    """
    def _updateX(self, T, platforms):
        ## Physics Calculations ##

        # Cancel velocity if it's too small to prevent sliding forever
        if abs(self.velX) < self.stop_velocity:
            self.velX = 0

        # Apply accelerations to get velocity
        self.velX += self.accX * T
        self.velX *= self.friction

        # Update position
        self.posX += self.velX * T
        # Send new pos to rect
        self.rect.x = self.posX

        ## Collision checks ##

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
        if self.posX + self.rect.width >= self.screen_width and self.velX > 0:
            self.posX = self.screen_width - self.rect.width
            self.velX = 0

        # Platform collision detection
        if self.rect.collidelist(platforms) != -1:
            # Get correct plat object
            ind = self.rect.collidelist(platforms)
            plat = platforms[ind]
            # If colliding currently
            if self.rect.colliderect(plat.rect):
                # Hitting from the right
                if self.velX > 0:
                    # Snap body to edge and stop
                    self.rect.right = plat.rect.left
                    self.posX = self.rect.x
                    self.velX = 0

                # Hitting from the left
                elif self.velX < 0:
                    self.rect.left = plat.rect.right
                    self.posX = self.rect.x
                    self.velX = 0

    def _updateY(self, T, platforms):
        ## Physics calc ##

        # Standard state is not on ground
        self.on_ground = False

        # Apply gravity
        self.velY += self.gravity * T

        # Update pos
        self.posY += self.velY * T
        # Send pos to rect
        self.rect.y = self.posY

        ## Collision Checks ##

        # Ground check
        if self.posY + self.rect.height >= self.screen_height and self.velY > 0:
            self.posY = self.screen_height - self.rect.height
            self.velY = 0
            self.on_ground = True

        # Platform collision
        if self.rect.collidelist(platforms) != -1: # -1 if no collision
            # Get index for the collided rect
            ind = self.rect.collidelist(platforms)
            # Grab the actual platforms rect
            plat = platforms[ind]
            # If we are colliding with this specific platform
            if self.rect.colliderect(plat.rect):
                # Falling onto the platform
                if self.velY > 0:
                    # Snap player bottom to platform top
                    self.rect.bottom = plat.rect.top
                    # Set internal player pos correct value
                    self.posY = int(self.rect.y)
                    # Set on ground flag
                    self.on_ground = True

                # Hitting head on platform
                elif self.velY < 0:
                    # Snap head and set pos to correct
                    self.rect.top = plat.rect.bottom
                    self.posY = int(self.rect.y)
                    self.velY = 0


        # Ground logic
        if self.on_ground:
            self.velY = 0
            self.friction = self._ground_friction
        else:
            self.friction = self._air_friction

    """
    Animations
    """
    def _updateAnimation(self, T):

        # Death animation
        if not self.is_alive:
            self._current_death_frame += self._animation_speed * T

            if self._current_death_frame >= len(self._death_frames) - 1:
                self._current_death_frame = len(self._death_frames) - 1

            self.image = self._death_frames[int(self._current_death_frame)]

            if self._facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

            return

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

    """
    States and events
    """

    def _updateState(self, enemies, prizes):
        # Enemy collision detection
        if self.rect.collidelist(enemies) != -1:
            ind = self.rect.collidelist(enemies)
            enemy = enemies[ind]
            if self.rect.colliderect(enemy):
                if self.is_alive:
                    self.is_alive = False

        # Win collision detection
        if self.rect.collidelist(prizes) != -1:
            ind = self.rect.collidelist(prizes)
            prize = prizes[ind]
            if self.rect.colliderect(prize):
                if self.is_alive:
                    self.has_won = True
                    prize.is_collected = True
