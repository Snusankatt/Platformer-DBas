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
        clock.tick(60)

        print("Hello World")