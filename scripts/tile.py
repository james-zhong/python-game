import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, sprite_type, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        
        # Prevent larger sprites from overlapping by changing its offset
        if self.sprite_type == "object":
            self.rect = self.image.get_rect(topleft = (position[0], position[1] - TILE_SIZE))
        else:
            self.rect = self.image.get_rect(topleft = position)
        
        # Custom hitbox
        self.hitbox = self.rect.inflate(0, -10)