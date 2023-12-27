import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice

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
        # Getting the path location of assets
        layouts = {
            "boundary": import_csv_layout("graphics/csv_maps/boundary.csv"),
            "grass": import_csv_layout("graphics/csv_maps/grass.csv"),
            "objects": import_csv_layout("graphics/csv_maps/objects.csv")
        }
        
        graphics = {
            "grass": import_folder("graphics/grass"),
            "objects": import_folder("graphics/objects")
        }
        
        # Draw the map
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        
                        # Check which style sprite is and draw it
                        if style == "boundary":
                            Tile((x,y), [self.obstacle_sprites], "invisible")
                            
                        if style == "grass":
                            # Choose a random grass
                            random_grass_image = choice(graphics["grass"])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], "grass", random_grass_image)

                        # Place objects specifically based on CSV file
                        if style == "objects":
                            surface = graphics["objects"][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], "object", surface)
                            
        self.player = Player((1800,2000),[self.visible_sprites],self.obstacle_sprites)
    
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
        
        # Create the floor
        self.floor_surface = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
    
    # Draw the sprites on an offset so the map moves instead of the player
    def custom_draw(self, player):
        # Get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # Draw the floor
        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_position)
        
        # Draw sprites with the offset and with YSort (so player is always ontop of for example rocks)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)