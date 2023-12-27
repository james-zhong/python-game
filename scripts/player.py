import pygame
from settings import *

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

        self.obstacle_sprites = obstacle_sprites
        
    # Detecting input from user for movement
    def input(self):
        # Getting input
        keys = pygame.key.get_pressed()
        
        # Adjusting direction based on input
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
    
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
    
    # Call the functions
    def update(self):
        self.input()
        self.move(self.speed)