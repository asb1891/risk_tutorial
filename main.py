import pygame as pg
import sys
from src.game import Game

# Initialize the pygame modules
pg.init()
pg.mixer.init()
pg.font.init()

# Define the dimensions of the window
WIDTH = 1600
HEIGHT = 1200
window_size = pg.Vector2(WIDTH, HEIGHT)

# Create the screen surface
screen = pg.display.set_mode((WIDTH, HEIGHT))  # window_size should be a tuple here
# Initialize the clock
clock = pg.time.Clock()

# Set the caption of the window
pg.display.set_caption("Risk")

# Now that everything is initialized, create a Game object
game = Game(screen, clock, window_size)

# Run the game loop
game.run()

# Quit the game and exit
pg.quit()
sys.exit()
