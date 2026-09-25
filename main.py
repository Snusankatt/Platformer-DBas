import platform
import player
import pygame
import sys

def load_level(level):
    # Create the map list
    level_map = []
    # Open file and put all lines in level_map
    with open(level) as f:
        for line in f:
            level_map.append(line)

    # Set tile size and create the "platform list"
    tile_size = 64
    level_platforms = []

    # Row index becomes y pos and col index the x pos
    for row_index, row_string in enumerate(level_map):
        for col_index, char in enumerate(row_string):

            if char in ("P", "p", "G"):
                # Add the platform with correct coords
                x_pos = col_index * tile_size
                y_pos = row_index * tile_size
                # Append to the platform list
                new_platform = platform.Platform(x_pos, y_pos, char)
                level_platforms.append(new_platform)

    # Return the platforms list
    return level_platforms

def main():
    # Starta pygame med ett fönster, sätt storlek och skapa klockan
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    # Skapa spelaren
    p = player.Player()


    # Create the level
    platforms = load_level("map.txt")

    while True:
        """
        Time and physics
        """
        # Set delta time, used for out of frame physics calculations and animations
        dt = clock.tick(60) / 1000
        # Set initial player values, may or may not update
        p.accX = 0
        p.accY = 0

        """
        Event handling discrete inputs
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        if pygame.key.get_pressed()[pygame.K_DELETE]:
            pygame.quit()
            sys.exit()


        """
        Event handling continuous inputs
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            p.accX = 4000

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            p.accX = -4000

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]) and (p.on_ground == True):
            p.accY = -80000
        """
        Rendering
        """
        # Reset screen
        screen.fill((0, 0, 0))
        # Platforms
        for plat in platforms:
            screen.blit(plat.image, plat.rect)

        """
        Display and player update
        """
        p.update(dt, platforms)

        # Draw Player
        screen.blit(p.image, p.rect)

        pygame.display.flip()


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()