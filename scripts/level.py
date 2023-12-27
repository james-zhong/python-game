import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # Draw map
        self.create_map()

    # Assign tiles to respective position and groups
    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                # Place tiles according to WORLD_MAP
                if col == "x": # Rock
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                    
                if col == "p":
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
    
    # Draw the sprites
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

# Player camera and sort sprites based on Y position
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
    # Draw the sprites on an offset so the map moves instead of the player
    def custom_draw(self, player):
        # Get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # Draw sprites with the offset and with YSort (so player is always ontop of for example rocks)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)