import pygame

class Platform:
    def __init__(self, x, y, type):
        platform_sprites = pygame.image.load("./assets/platforms.png")
        world_tiles = pygame.image.load("./assets/world_tileset.png")

        if type == "P":
            P_tile = world_tiles.subsurface((0, 0, 16, 16))
            P_tile = pygame.transform.scale(P_tile, (64, 64))
            self.rect = pygame.Rect(x, y, 64, 64)
            self.image = P_tile

        elif type == "p":
            p_tile = platform_sprites.subsurface((0, 0, 16, 9))
            p_tile = pygame.transform.scale(p_tile, (64, 36))
            self.rect = pygame.Rect(x, y, 64, 36)
            self.image = p_tile

        elif type == "G":
            G_tile = world_tiles.subsurface((0, 16, 16, 16))
            G_tile = pygame.transform.scale(G_tile, (64, 64))
            self.rect = pygame.Rect(x, y, 64, 64)
            self.image = G_tile