import player
import pygame
import sys

def main():
    # Starta pygame med ett fönster, sätt storlek och skapa klockan
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    # Skapa spelaren
    p = player.Player()

    while True:
        """
        Time and physics
        """
        # Set delta time, used for out of frame physics calculations
        dt = clock.tick(60) / 1000
        # Set initial player values, may or may not update
        p.accX = 0
        p.accY = -500 # Gravity

        """
        Event handling discrete inputs
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break


        """
        Event handling continuous inputs
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            p.accX = 2000

        if keys[pygame.K_LEFT]:
            p.accX = -2000

        if keys[pygame.K_UP] and (p.rect.bottom == 1080):
            p.accY = -70000
        """
        Rendering
        """
        # Reset screen
        screen.fill((0, 0, 0))

        # Draw Player
        pygame.draw.rect(screen, "red", p.rect)

        """
        Display and player update
        """
        p.updateX(dt)
        p.updateY(dt)

        pygame.display.flip()


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()