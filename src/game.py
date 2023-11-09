import pygame  # Imports the pygame library for game development.

from src.geo import World  # Imports the World class from the geo module within the src package.
from src.player import Player  # Imports the Player class from the player module within the src package.
from src.utils import draw_text  # Imports the draw_text function from the utils module within the src package.
from src.dice import Dice  # Imports the Dice class from the dice module within the src package.


class Game:  # Defines a new class named Game.

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, window_size: pygame.Vector2) -> None:
        # The constructor for the Game class, which initializes the game state and attributes.
        self.error_message = None  # A variable to store the current error message, if any.
        self.error_message_time = 0  # A variable to keep track of the time for which an error message has been displayed.
        self.screen = screen  # The pygame Surface where the game will be drawn.
        self.clock = clock  # The pygame Clock used to control the game's frame rate.
        self.window_size = window_size  # A pygame Vector2 representing the size of the game window.
        self.font = pygame.font.SysFont(None, 24)  # Initializes the font used for drawing text.
        # The x and y coordinates for the "+" button (to be replaced with actual values).
        # self.plus_button_pos = (0, 0)
        # self.minus_button_pos = (0, 0)  # The x and y coordinates for the "-" button.
        self.playing = True  # A boolean indicating whether the game is currently being played.
        # A list of the different phases of gameplay.
        self.phases = ["place_units", "move_units", "attack_country"]
        self.phase_idx = 0  # The index of the current phase in the phases list.
        self.phase = self.phases[self.phase_idx]  # The current phase of gameplay.
        self.phase_timer = pygame.time.get_ticks()  # Stores the current time for phase timing.
        self.world = World(self)  # Creates a new World instance associated with this game.
        self.player = Player(
            name="Player 1",  # Sets the player's name. Can be replaced with any desired name.
            country=self.world.countries.get("United States of America"),  # Sets the player's starting country.
            world=self.world,  # References the World instance.
            color=(0, 0, 255),  # Sets the player's color to blue.
            game=self  # Provides a reference to the current game instance.
        )
        print("creating phase ui")  # Outputs a message indicating that the phase UI is being created.
        self.create_phase_ui()  # Calls the method to create the phase UI elements.

    def run(self) -> None:
        # This method contains the game loop where the game is run.
        while self.playing:  # Loops as long as the game is being played.
            self.clock.tick(60)  # Caps the frame rate at 60 frames per second.
            self.screen.fill((245, 245, 220))  # Fills the screen with a beige color.
            self.events()  # Calls the method to handle user inputs and events.
            self.update()  # Calls the method to update the game state.
            self.draw()  # Calls the method to draw the game state to the screen.
            pygame.display.update()  # Updates the display to show the new frame.


    def events(self) -> None:
        # This method handles user inputs and events.
        current_time = pygame.time.get_ticks()  # Gets the current time.
        # Loops over all the events in the event queue.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Checks if the quit event has been triggered.
                self.playing = False  # Ends the game loop.
            elif event.type == pygame.KEYDOWN:  # Checks if a key has been pressed.
                if event.key == pygame.K_ESCAPE:  # Checks if the key pressed is the escape key.
                    self.playing = False  # Ends the game loop.
            elif event.type == pygame.MOUSEMOTION:  # Checks if the mouse has been moved.
                # Changes the hover state of the roll dice button based on the mouse position.
                if self.roll_dice_button.collidepoint(pygame.mouse.get_pos()):
                    self.roll_dice_button_hovered = True
                elif not self.roll_dice_button.collidepoint(pygame.mouse.get_pos()):
                    self.roll_dice_button_hovered = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Checks for a left mouse click.
                if self.roll_dice_button.collidepoint(pygame.mouse.get_pos()):  # Checks if the roll dice button was clicked.
                    self.player.roll_dice()  # Calls the method to roll the dice for the player.
                # elif self.plus_button.collidepoint(pygame.mouse.get_pos()):  # Checks if the "+" button was clicked.
                #     self.player.change_unit_amount(1)  # Increases the number of units.
                # elif self.minus_button.collidepoint(pygame.mouse.get_pos()):  # Checks if the "-" button was clicked.
                #     self.player.change_unit_amount(-1)  # Decreases the number of units.

        if current_time - self.error_message_time > 5000:  # Checks if 5 seconds have passed since the error message was shown.
            self.error_message = None  # Clears the error message.

    def display_error_message(self, screen: pygame.Surface) -> None:
        # Check if there's an error message to display
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, (255, 0, 0))  # Red text for error
            error_rect = error_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))  # Position it under the roll dice button
            screen.blit(error_surface, error_rect)

            # Now reset the error_message after 2 seconds
            pygame.time.set_timer(pygame.USEREVENT, 2000)


    def update(self) -> None:
    # Record the current time to manage button press delay
        now = pygame.time.get_ticks()
        # Update the state of the world and player based on the current game phase
        self.world.update()
        self.player.update(self.phase)

        # Reset hover state for the finish phase button
        self.finish_phase_button_hovered = False
        # Check if the mouse is over the finish phase button
        if self.finish_phase_button.collidepoint(pygame.mouse.get_pos()):
            self.finish_phase_button_hovered = True

        # If the finish phase button is hovered, check for mouse click and phase change timer
        if self.finish_phase_button_hovered:
            # Check if left mouse button is clicked and enough time has passed since the last phase change
            if pygame.mouse.get_pressed()[0] and (now - self.phase_timer > 500):
                # Reset the phase timer to the current time
                self.phase_timer = now
                # Move to the next phase, wrapping around if necessary
                self.phase_idx = (self.phase_idx + 1) % len(self.phases)
                # Update the current phase based on the new phase index
                self.phase = self.phases[self.phase_idx]

    def draw(self) -> None:
        # Draw the world and phase UI onto the screen
        self.world.draw(self.screen)
        self.draw_phase_ui()
        # Render the FPS count on the screen
        text_surface = self.font.render(
            f"FPS: {int(self.clock.get_fps())}", False, (255, 255, 255)
        )
        # Display the FPS on the screen at position (10, 10)
        self.screen.blit(text_surface, (10, 10))
        # Draw buttons to increment and decrement armies
        # self.world.draw_button(self.screen, "+", self.plus_button_pos, self.world.increment_armies)
        # self.world.draw_button(self.screen, "-", self.minus_button_pos, self.world.decrement_armies)

    def create_phase_ui(self) -> None:
        # Initialize and set the current phase UI element
        self.current_phase_image = pygame.Surface((200, 50))
        self.current_phase_image.fill((25, 42, 86))
        self.current_phase_rect = self.current_phase_image.get_rect(topleft=(10, 10))

        # Initialize and set the finish phase button element
        self.finish_phase_image = pygame.Surface((200, 50))
        self.finish_phase_image.fill((25, 42, 86))
        self.finish_phase_button = self.finish_phase_image.get_rect(topleft=(10, 70))
        self.finish_phase_button_hovered = False

        # Initialize and set the roll dice button element
        self.roll_dice_image = pygame.Surface((200, 50))
        self.roll_dice_image.fill((25, 42, 86))
        self.roll_dice_button = self.roll_dice_image.get_rect(topleft=(10, 130))
        self.roll_dice_button_hovered = False

    def draw_phase_ui(self) -> None:
        #draw the phase UI elements on the screen
        self.screen.blit(self.current_phase_image, self.current_phase_rect)
        if self.phase == "place_units":
            draw_text(
                self.screen,
                self.font,
                "Place",
                (255, 255, 255),
                self.current_phase_rect.centerx,
                self.current_phase_rect.centery,
                True,
            )
        elif self.phase == "move_units":
            draw_text(
                self.screen,
                self.font,
                "Move",
                (255, 255, 255),
                self.current_phase_rect.centerx,
                self.current_phase_rect.centery,
                True,
            )
        elif self.phase == "attack_country":
            draw_text(
                self.screen,
                self.font,
                "Attack",
                (255, 255, 255),
                self.current_phase_rect.centerx,
                self.current_phase_rect.centery,
                True,
            )
        if self.roll_dice_button_hovered:
            self.roll_dice_image.fill((50, 82, 126))
        else:
            self.roll_dice_image.fill((25, 42, 86))

        # Draw the button on the screen
        self.screen.blit(self.roll_dice_image, self.roll_dice_button)

        # Draw the button text
        draw_text(
            self.screen,
            self.font,
            "Roll Dice",
            (255, 255, 255),
            self.roll_dice_button.centerx,
            self.roll_dice_button.centery,
            True,
        )

        if self.finish_phase_button_hovered:
            self.finish_phase_image.fill((255, 0, 0))
        else:
            self.finish_phase_image.fill((25, 42, 86))

        self.screen.blit(self.finish_phase_image, self.finish_phase_button)
        draw_text(
            self.screen,
            self.font,
            "Finish phase",
            (255, 255, 255),
            self.finish_phase_button.centerx,
            self.finish_phase_button.centery,
            True,
        )
