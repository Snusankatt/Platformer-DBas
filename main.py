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

        dt = clock.tick(60) / 1000

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
        if keys[pygame.K_LEFT]:
            p.accelerate(5, dt)


        """
        Rendering
        """
        # Reset screen
        screen.fill((0, 0, 0))

        # Draw Player
        pygame.draw.rect(screen, "red", p.posX, p.posY)

        """
        Display update
        """
        pygame.display.flip()


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()