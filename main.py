import pickle
from contextlib import nullcontext

import door
import platform
import player
import pygame
import sys
import enemy
import prize
import asyncio

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

    level_prizes = []

    spawn_point = (0, 0)

    level_doors = []

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

            if char == "C":
                x_pos = col_index * tile_size
                y_pos = row_index * tile_size
                # Append to prizes list
                new_prize = prize.Prize(x_pos, y_pos)
                level_prizes.append(new_prize)

            if char == "S":
                x_pos = col_index * tile_size
                y_pos = row_index * tile_size
                spawn_point = (x_pos, y_pos)

            if char == "D":
                x_pos = col_index * tile_size
                y_pos = row_index * tile_size
                new_door = door.Door(x_pos, y_pos)
                level_doors.append(new_door)

    # Return the platforms list
    return level_platforms, level_enemies, level_prizes, spawn_point, level_doors

def end_screen(screen, game_over_text, text_rect):
    # GAME OVER text
    screen.blit(game_over_text, text_rect)

def win_screen(screen, win_text, text_rect):
    # YOU WIN text
    screen.blit(win_text, text_rect)

def show_exit_button(screen, button_rect, button_text, button_text_rect):
    # Exit button
    pygame.draw.rect(screen, "red", button_rect)
    # Text for button
    screen.blit(button_text, button_text_rect)



async def main():
    # Starta pygame
    pygame.init()


    # Prepare end screen
    # Load font
    large_font = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 200)
    small_font = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 80)

    # GAME OVER text
    game_over_text = large_font.render("GAME OVER", False, (255, 255, 255))
    go_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # YOU WON text
    you_won_text = large_font.render("YOU WIN!", False, "green")
    yw_text_rect = you_won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Exit button
    button_rect = pygame.Rect(0, 0, 500, 120)
    button_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 300)
    button_text = small_font.render("EXIT", False, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)



    # Load screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Create the level
    platforms, enemies, prizes, spawn_point, doors = load_level("map2.txt")

    # Create bg image
    bg_image = pygame.image.load("assets/background.jpeg")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Make it darker to distinguish fore/background
    darken_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    darken_overlay.fill((0, 0, 0))
    darken_overlay.set_alpha(100)
    bg_image.blit(darken_overlay, (0, 0))

    death_timer = 0

    # Connect to server
    reader, writer = await asyncio.open_connection("127.0.0.1", 5000)

    # Get player ID
    id_package = await reader.read(2048)
    current_player_id = pickle.loads(id_package)

    # Create players
    p = player.Player(SCREEN_WIDTH, SCREEN_HEIGHT, current_player_id)
    p2 = player.Player(SCREEN_WIDTH, SCREEN_HEIGHT, 2 if current_player_id == 1 else 1)

    # Spawn them at spawn point
    p.posX, p.posY = spawn_point
    p.posY -= p.rect.height
    p2.posX, p2.posY = spawn_point
    p2.posY -= p2.rect.height

    running = True
    while running:

        # Create the dict that will be sent through network
        player_data = {"x": p.rect.x, "y": p.rect.y, "vel": p.velX,
                       "is_alive": p.is_alive, "has_won": p.has_won, "facing_left": p._facing_left,
                       "current_idle_frame": p._current_idle_frame, "current_running_frame": p._current_running_frame, "current_death_frame": p._current_death_frame,
                       "prizes": [prize.is_collected for prize in prizes]}

        # Package and send data
        writer.write(pickle.dumps(player_data))
        await writer.drain()

        # Receive data from server
        game_state_package = await reader.read(2048)
        # If empty -> server has problems, exit game
        if game_state_package == b"":
            break
        ngs = pickle.loads(game_state_package) # New game state

        # Unflatten all data
        for i in ngs:
            if i != current_player_id:
                p2.rect.x = ngs[i]["x"]
                p2.rect.y = ngs[i]["y"]
                p2.velX = ngs[i]["vel"]
                p2.is_alive = ngs[i]["is_alive"]
                p2.has_won = ngs[i]["has_won"]
                p2._facing_left = ngs[i]["facing_left"]
                p2._current_idle_frame = ngs[i]["current_idle_frame"]
                p2._current_running_frame = ngs[i]["current_running_frame"]
                p2._current_death_frame = ngs[i]["current_death_frame"]

                prizes_collected = ngs[i]["prizes"]
                for i, status in enumerate(prizes_collected):
                    prizes[i].is_collected = status

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
        if p.is_alive and not p.has_won:
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

        # Prizes
        for coin in prizes:
            coin.update(dt)
            if not coin.should_be_killed:
                screen.blit(coin.image, coin.rect)

        # Doors
        for d in doors:
            d.update(dt)
            screen.blit(d.image, d.rect)

        """
        Display and player update
        """
        p.update(dt, platforms, enemies, prizes)
        p2._updateAnimation(dt)

        # Draw Players
        screen.blit(p.image, p.rect)
        screen.blit(p2.image, p2.rect)

        # Draw ending if dead
        if not p.is_alive and not p.has_won:
            death_timer += dt

            if death_timer >= 1:
                end_screen(screen, game_over_text, go_text_rect)

                # Only let player exit if both are dead
                if not p2.is_alive:
                    show_exit_button(screen, button_rect, button_text, button_text_rect)


        # Draw win screen if done
        if p.has_won or p2.has_won:

            p.has_won = True
            death_timer += dt
            if death_timer >= 1:
                win_screen(screen, you_won_text, yw_text_rect)
                show_exit_button(screen, button_rect, button_text, button_text_rect)

        pygame.display.flip()

        # Create asynchronous event to allow other processes to run
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())