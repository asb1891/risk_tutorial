import pygame as pygame
import sys
from src.game import Game

# Initialize the pygame modules
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Define the dimensions of the window
WIDTH = 1600
HEIGHT = 1200
window_size = pygame.Vector2(WIDTH, HEIGHT)

# Create the screen surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # window_size should be a tuple here
# Initialize the clock
clock = pygame.time.Clock()

# Set the caption of the window
pygame.display.set_caption("Risk")

# Now that everything is initialized, create a Game object
game = Game(screen, clock, window_size)

# Run the game loop
game.run()

# Quit the game and exit
pygame.quit()
sys.exit()
