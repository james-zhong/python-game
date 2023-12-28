import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        # Player asset
        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        # Custom collison so player can go "behind" rocks
        self.hitbox = self.rect.inflate(-10, -26)
        
        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400 #ms
        self.time_attacked = None
        self.holding = False
        
        # Player animation
        self.import_player_animations()
        self.action_status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        self.obstacle_sprites = obstacle_sprites
    
    # Get the player animation sprites/frames
    def import_player_animations(self):
        character_path = "graphics/player/"
        self.animation_states = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_attack": [],
            "down_attack": [],
            "left_attack": [],
            "right_attack": [],
        }
        
        for animation in self.animation_states.keys():
            full_path = character_path + animation
            self.animation_states[animation] = import_folder(full_path)
    
    # Detecting input from user for movement
    def input(self):
        # Make sure player cannot move during attack action
        if not self.attacking:
            # Getting input
            keys = pygame.key.get_pressed()
            
            # Adjusting direction based on input for movement
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.action_status = "up"
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.action_status = "down"
            else:
                self.direction.y = 0
            
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.action_status = "left"
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.action_status = "right"
            else:
                self.direction.x = 0

            # Attack input
            if keys[pygame.K_SPACE] and not self.attacking and not self.holding:
                # Set attack cooldown
                self.attacking = True
                self.time_attacked = pygame.time.get_ticks()
            
            # Holding objects
            if keys[pygame.K_e] and not self.holding:
                # Set holding cooldown
                self.holding = True
            
            # Drop held object
            if keys[pygame.K_q] and self.holding:
                self.holding = False
    
    # Figure out which action the player is doing and change status
    def get_status(self):
        # Idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.action_status and not "attack" in self.action_status: # Check if not already idle or attacking
                self.action_status += "_idle"
                
        # Attack status
        if self.attacking:
            # Prevent player from moving when attacking
            self.direction.x, self.direction.y = 0,0
            
            if not "attack" in self.action_status: # Check if not already attacking
                # Overwrite status if necessary
                if "idle" in self.action_status:
                    print("yes")
                    self.action_status = self.action_status.replace("_idle", "_attack")
                else:
                    self.action_status += "_attack"
                    
        else: # Remove attack animation after cooldown and make status idle
            if "attack" in self.action_status:
                self.action_status = self.action_status.replace("_attack","")
    
    def move(self, speed):
        # Prevent player from moving faster diagonally (because a^2+b^2=c^2)
        if self.direction.magnitude() != 0:
            # Normalise direction vector
            self.direction = self.direction.normalize()
        
        # Move player rect and check for collisions after movement on both axes
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center
    
    # Detect player collisions with obstacles
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # Check which side player collision has occured in using direction
                    if self.direction.x > 0: # Moving right
                        self.hitbox.right = sprite.hitbox.left # Move player to the left of obstacle
                    
                    if self.direction.x < 0: # Moving left
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # Check which side player collision has occured in using direction
                    if self.direction.y > 0: # Moving down
                        self.hitbox.bottom = sprite.hitbox.top # Move player to the left of obstacle
                    
                    if self.direction.y < 0: # Moving up
                        self.hitbox.top = sprite.hitbox.bottom
    
    # Manage the attack cooldown
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.time_attacked >= self.attack_cooldown:
                self.attacking = False
    
    # Animate the player movement
    def animate(self):
        animation = self.animation_states[self.action_status]
        
        # Loop the frame index so animation runs forever
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        # Set the image and rect
        self.image = animation[int(self.frame_index)] 
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
    # Call the functions
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)