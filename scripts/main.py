import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):
		# General setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Python Game')
		self.clock = pygame.time.Clock()

		# Game setup
		self.level = Level()

	def run(self):
		while True:
			# Get user input
			for event in pygame.event.get():
				# Close window on X press
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == "__main__":
	game = Game()
	game.run()	