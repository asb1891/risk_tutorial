import pygame

from src.geo import World
from src.player import Player
from src.utils import draw_text
from src.dice import Dice


class Game:

    def __init__(
        self, screen: pygame.Surface, clock: pygame.time.Clock, window_size: pygame.Vector2
    ) -> None:
        #initializes game state and attributes
        self.error_message = None
        self.error_message_time= 0
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.font = pygame.font.SysFont(None, 24)
        self.plus_button_pos = (0, 0)  # Replace with actual x and y coordinates for the "+" button
        self.minus_button_pos = (0, 0)
        self.playing = True
        self.phases = ["place_units", "move_units", "attack_country"]
        self.phase_idx = 0
        self.phase = self.phases[self.phase_idx]
        self.phase_timer = pygame.time.get_ticks()
        self.world = World(self)
        self.player = Player(
            name="Player 1",  # You can replace "Player 1" with any desired player name
            country=self.world.countries.get("United States of America"),
            world=self.world,
            color=(0, 0, 255),
            game=self  #set player color to blue
        )
        print("creating phase ui")
        self.create_phase_ui()

    def run(self) -> None:
        #runs game loop
        while self.playing:
            self.clock.tick(60)
            self.screen.fill((245, 245, 220))
            self.events()
            self.update()
            self.draw()
            pygame.display.update()

    def events(self) -> None:
        #handles user inputs and events
        current_time = pygame.time.get_ticks()
        # self.roll_dice_button_hovered = False  # Reset this flag for each new event loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
            elif event.type == pygame.MOUSEMOTION:
                if self.roll_dice_button.collidepoint(pygame.mouse.get_pos()):
                    self.roll_dice_button_hovered = True
                elif not self.roll_dice_button.collidepoint(pygame.mouse.get_pos()):
                    self.roll_dice_button_hovered = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                if self.roll_dice_button_hovered and self.phase == "attack_country":
                    # Roll the dice when the button is pressed and in the correct phase
                    attacker_dice = Dice.attacker_dice_roll(3)  # Assuming the attacker rolls 3 dice
                    defender_dice = Dice.defender_dice_roll(2)  # Assuming the defender rolls 2 dice
                    print("Attacker Dice:", attacker_dice)
                    print("Defender Dice:", defender_dice)
                    # Now you can use the result of the dice roll for the attack
                elif self.roll_dice_button_hovered:
                    error_duration = 2000
                    remove_error = False
                    while not remove_error:

                        self.error_message = "CANNOT ROLL DICE UNTIL YOU ENTER ATTACK PHASE!"
                        self.display_error_message(self.screen)

                        pygame.display.update()

                        error_duration -= self.clock.tick(60)
                        if error_duration <= 0:
                            remove_error = True
                        
                    self.error_message = None

    def display_error_message(self, screen: pygame.Surface) -> None:
        # Check if there's an error message to display
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, (255, 0, 0))  # Red text for error
            error_rect = error_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))  # Position it under the roll dice button
            screen.blit(error_surface, error_rect)

            # Now reset the error_message after 2 seconds
            pygame.time.set_timer(pygame.USEREVENT, 2000)


    def update(self) -> None:
        #updates game state 
        now = pygame.time.get_ticks()
        self.world.update()
        self.player.update(self.phase)

        self.finish_phase_button_hovered = False
        if self.finish_phase_button.collidepoint(pygame.mouse.get_pos()):
            self.finish_phase_button_hovered = True

        if self.finish_phase_button_hovered:
            if pygame.mouse.get_pressed()[0] and (now - self.phase_timer > 500):
                self.phase_timer = now
                self.phase_idx = (self.phase_idx + 1) % len(self.phases)
                self.phase = self.phases[self.phase_idx]

    def draw(self) -> None:
        self.world.draw(self.screen)
        self.draw_phase_ui()
        text_surface = self.font.render(
            f"FPS: {int(self.clock.get_fps())}", False, (255, 255, 255)
        )
        self.screen.blit(text_surface, (10, 10))
        self.world.draw_button(self.screen, "+", self.plus_button_pos, self.world.increment_armies)
        self.world.draw_button(self.screen, "-", self.minus_button_pos, self.world.decrement_armies)

    def create_phase_ui(self) -> None:
        #create the UI for the game phases
        self.current_phase_image = pygame.Surface((200, 50))
        self.current_phase_image.fill((25, 42, 86))
        self.current_phase_rect = self.current_phase_image.get_rect(topleft=(10, 10))

        self.finish_phase_image = pygame.Surface((200, 50))
        self.finish_phase_image.fill((25, 42, 86))
        self.finish_phase_button = self.finish_phase_image.get_rect(topleft=(10, 70))
        self.finish_phase_button_hovered = False

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
