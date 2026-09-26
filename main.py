import platform
import player
import pygame
import sys
import enemy

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

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

    level_enemies = []

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

            if char == "E":
                x_pos = col_index * tile_size
                y_pos = row_index * tile_size
                new_enemy = enemy.Enemy(x_pos, y_pos)
                level_enemies.append(new_enemy)


    # Return the platforms list
    return level_platforms, level_enemies

def end_screen(screen, game_over_text, text_rect, button_rect, button_text, button_text_rect):
    # GAME OVER text
    screen.blit(game_over_text, text_rect)

    # Exit button
    pygame.draw.rect(screen, "red", button_rect)
    # Text for button
    screen.blit(button_text, button_text_rect)

def main():
    # Starta pygame
    pygame.init()


    # Prepare end screen
    # Load font
    large_font = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 200)
    small_font = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 80)

    # GAME OVER text
    game_over_text = large_font.render("GAME OVER", False, (255, 255, 255))

    go_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Exit button
    button_rect = pygame.Rect(0, 0, 500, 120)
    button_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 300)
    button_text = small_font.render("EXIT", False, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)



    # Load screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Skapa spelaren
    p = player.Player(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Create the level
    platforms, enemies = load_level("map.txt")

    # Create bg image
    bg_image = pygame.image.load("assets/background.jpeg")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Make it darker to distinguish fore/background
    darken_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    darken_overlay.fill((0, 0, 0))
    darken_overlay.set_alpha(100)
    bg_image.blit(darken_overlay, (0, 0))

    death_timer = 0

    running = True
    while running:
        """
        Time and physics
        """
        # Set delta time, used for out of frame physics calculations and animations
        dt = clock.tick(60) / 1000
        # Set initial player values, may or may not update
        p.accX = 0

        """
        Event handling discrete inputs
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


        if pygame.key.get_pressed()[pygame.K_DELETE]:
            pygame.quit()
            sys.exit()



        """
        Event handling continuous inputs
        """
        keys = pygame.key.get_pressed()
        if p.is_alive:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                p.accX = p.running_speed

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                p.accX = -p.running_speed

            if (keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]) and (p.on_ground == True):
                p.velY = p.jump_force
        """
        Rendering
        """
        # Reset screen
        screen.fill((0, 0, 0))
        # Draw bg
        screen.blit(bg_image, (0, 0))
        # Platforms
        for plat in platforms:
            screen.blit(plat.image, plat.rect)

        # Enemies
        for e in enemies:
            e.update(dt)
            screen.blit(e.image, e.rect)

        """
        Display and player update
        """
        p.update(dt, platforms, enemies)

        # Draw Player
        screen.blit(p.image, p.rect)

        # Draw ending if dead
        if not p.is_alive:
            death_timer += dt

            if death_timer >= 1:
                end_screen(screen, game_over_text, go_text_rect, button_rect, button_text, button_text_rect)

        pygame.display.flip()


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()