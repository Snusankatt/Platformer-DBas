import pickle

import door
import platform
import player
import pygame
import sys
import enemy
import prize
import asyncio
import button

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

    level_buttons = []

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

            if char in ("E", "e"):
                x_pos = col_index * tile_size
                y_pos = row_index * tile_size
                new_enemy = enemy.Enemy(x_pos, y_pos, char)
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

            if char == "B":
                x_pos = col_index * tile_size
                y_pos = row_index * tile_size
                new_button = button.Button(x_pos, y_pos)
                level_buttons.append(new_button)

    # Return the platforms list
    return level_platforms, level_enemies, level_prizes, spawn_point, level_doors, level_buttons

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

    # Unlocked Levels
    unlocked = [True, False, False, False]

    # Stay in the game loop
    while True:

        # Capture the string that your menu function returns
        selected_map = level_select_screen(screen, unlocked)

        current_level = int(selected_map[5:-4])

        beaten = await run_game(button_rect, button_text, button_text_rect, clock, game_over_text, go_text_rect, screen,
                           you_won_text, yw_text_rect, selected_map)

        # Only update in never beaten before
        if not unlocked[current_level]:
            unlocked[current_level] = beaten


def level_select_screen(screen, level_unlocked):
    running = True
    screen.fill((30, 30, 30)) # clear screen

    # 1. Load and scale the background image just like you did in run_game
    title_bg = pygame.image.load("assets/title_screen.jpg")
    title_bg = pygame.transform.scale(title_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.SysFont(None, 48)
    level1 = pygame.Rect(760, 490, 400, 80)
    level2 = pygame.Rect(760, 610, 400, 80)
    level3 = pygame.Rect(760, 730, 400, 80)
    level4 = pygame.Rect(760, 850, 400, 80)

    while running:

        # Game dev cheat
        keys = pygame.key.get_pressed()
        if keys[pygame.K_u]:
            level_unlocked = [True, True, True, True]

        screen.blit(title_bg, (0, 0)) # background


        pygame.draw.rect(screen, "green" if level_unlocked[0] else "red", level1)
        pygame.draw.rect(screen, "green" if level_unlocked[1] else "red", level2)
        pygame.draw.rect(screen, "green" if level_unlocked[2] else "red", level3)
        pygame.draw.rect(screen, "green" if level_unlocked[3] else "red", level4)

        level1_text = font.render("Level 1", True, (255, 255, 255))
        level1_text_rect = level1_text.get_rect(center=level1.center)
        screen.blit(level1_text, level1_text_rect)

        level2_text = font.render("Level 2", True, (255, 255, 255))
        level2_text_rect = level2_text.get_rect(center=level2.center)
        screen.blit(level2_text, level2_text_rect)

        level3_text = font.render("Level 3", True, (255, 255, 255))
        level3_text_rect = level3_text.get_rect(center=level3.center)
        screen.blit(level3_text, level3_text_rect)

        level4_text = font.render("Level 4", True, (255, 255, 255))
        level4_text_rect = level4_text.get_rect(center=level4.center)
        screen.blit(level4_text, level4_text_rect)


        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_position = event.pos # xy koordinat for vart musknappentrycktes
                    if level1.collidepoint(mouse_position):
                        return "level1.txt"
                    elif level2.collidepoint(mouse_position) and level_unlocked[1]:
                        return "level2.txt"
                    elif level3.collidepoint(mouse_position) and level_unlocked[2]:
                        return "level3.txt"
                    elif level4.collidepoint(mouse_position) and level_unlocked[3]:
                        return "level4.txt"


async def run_game(button_rect, button_text, button_text_rect, clock, game_over_text, go_text_rect, screen,
                   you_won_text, yw_text_rect, map_filename):
    # Create the level
    platforms, enemies, prizes, spawn_point, doors, buttons = load_level(map_filename)
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
    reader, writer = await asyncio.open_connection("195.178.161.102", 6967)
    # Get player ID
    id_package = await reader.read(2048)
    current_player_id = pickle.loads(id_package)

    # debug
    print(f"DEBUG: The server gave me ID: {current_player_id} (Type: {type(current_player_id)})")

    # Create players
    p = player.Player(SCREEN_WIDTH, SCREEN_HEIGHT, current_player_id)
    p2 = player.Player(SCREEN_WIDTH, SCREEN_HEIGHT, 2 if current_player_id == 1 else 1)
    # Spawn them at spawn point
    p.posX, p.posY = spawn_point
    p.posY -= p.rect.height
    p2.posX, p2.posY = spawn_point
    p2.posY -= p2.rect.height
    running = True

    exit_button_active = False

    clock.tick(60) # reset timer otherwise character falls 4000 blocks cause it takes the time in level selector as falling time
    while running:

        # Create the dict that will be sent through network
        player_data = {"x": p.rect.x, "y": p.rect.y, "vel": p.velX,
                       "is_alive": p.is_alive, "has_won": p.has_won, "facing_left": p._facing_left,
                       "current_idle_frame": p._current_idle_frame, "current_running_frame": p._current_running_frame,
                       "current_death_frame": p._current_death_frame,
                       "prizes": [prize.is_collected for prize in prizes]}

        # Package and send data
        writer.write(pickle.dumps(player_data))
        await writer.drain()

        # Receive data from server
        game_state_package = await reader.read(2048)
        # If empty -> server has problems, exit game
        if game_state_package == b"":
            break
        ngs = pickle.loads(game_state_package)  # New game state

        p2_connected = False

        # Unflatten all data
        for i in ngs:
            if i != current_player_id:
                # We found a p2
                p2_connected = True

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
            # Close game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Exit button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos) and exit_button_active:
                    running = False

        # Debug force quit
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
            d.update(dt, buttons)
            screen.blit(d.image, d.rect)

        # Buttons
        for b in buttons:
            b.update([p, p2])
            screen.blit(b.image, b.rect)

        """
        Display and player update
        """
        # Update and draw p1
        p.update(dt, platforms, enemies, prizes, doors, buttons)
        screen.blit(p.image, p.rect)

        # Update and draw p2 if theyre connected
        if p2_connected:
            p2._updateAnimation(dt)
            screen.blit(p2.image, p2.rect)

        # Draw ending if both dead or p2 is DCed
        if not p.is_alive and not p.has_won:
            death_timer += dt

            if death_timer >= 1:
                end_screen(screen, game_over_text, go_text_rect)

                # Only let player exit if both are dead
                if not p2.is_alive or not p2_connected:
                    show_exit_button(screen, button_rect, button_text, button_text_rect)
                    exit_button_active = True

        # Draw win screen if done
        if p.has_won or p2.has_won:

            p.has_won = True
            death_timer += dt
            if death_timer >= 1:
                win_screen(screen, you_won_text, yw_text_rect)
                show_exit_button(screen, button_rect, button_text, button_text_rect)
                exit_button_active = True

        pygame.display.flip()

        # Create asynchronous event to allow other processes to run
        await asyncio.sleep(0)

    writer.close()
    await writer.wait_closed()

    # Return completed state
    return p.has_won or p2.has_won


if __name__ == "__main__":
    asyncio.run(main())