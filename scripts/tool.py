import pygame

class Tool(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        # Get the direction of the player using player.action_status, but only get up,down,left,right
        direction = player.action_status.split("_")[0]
        
        # Weapon tool
        full_path =  f"graphics/tools/{player.tool}/{direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()
        
        # Place tool
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left': 
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))