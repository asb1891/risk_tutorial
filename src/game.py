import pygame as pg

from src.geo import World
from src.player import Player
from src.utils import draw_text
from src.dice import Dice


class Game:
    def __init__(
        self, screen: pg.Surface, clock: pg.time.Clock, window_size: pg.Vector2
    ) -> None:
        self.error_message = None
        self.error_message_time= 0
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.font = pg.font.SysFont(None, 24)
        self.playing = True
        self.phases = ["place_units", "move_units", "attack_country"]
        self.phase_idx = 0
        self.phase = self.phases[self.phase_idx]
        self.phase_timer = pg.time.get_ticks()
        self.world = World(self)
        self.player = Player(
            name="Player 1",  # You can replace "Player 1" with any desired player name
            country=self.world.countries.get("United States of America"),
            world=self.world,
            color=(0, 0, 255)  # RGB color code for blue
        )
        self.create_phase_ui()

    def run(self) -> None:
        while self.playing:
            self.clock.tick(60)
            self.screen.fill((245, 245, 220))
            self.events()
            self.update()
            self.draw()
            pg.display.update()

    def events(self) -> None:
        current_time = pg.time.get_ticks()
        self.roll_dice_button_hovered = False  # Reset this flag for each new event loop

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
            elif event.type == pg.MOUSEMOTION:
                if self.roll_dice_button.collidepoint(pg.mouse.get_pos()):
                    self.roll_dice_button_hovered = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
             if self.roll_dice_button_hovered and self.phase == "attack_country":
                # Roll the dice when the button is pressed and in the correct phase
                attacker_dice = Dice.attacker_dice_roll(3)  # Assuming the attacker rolls 3 dice
                defender_dice = Dice.defender_dice_roll(2)  # Assuming the defender rolls 2 dice
                print("Attacker Dice:", attacker_dice)
                print("Defender Dice:", defender_dice)
                # Now you can use the result of the dice roll for the attack
            elif self.roll_dice_button_hovered:
                self.error_message = "Can't roll dice until you enter attack phase"
                pg.time.set_timer(pg.USEREVENT, 2000)  # Start a timer for 2 seconds
            elif event.type == pg.USEREVENT:
                self.error_message = None  # Clear the error message after 2 seconds
                pg.time.set_timer(pg.USEREVENT, 0)  # Stop the timer



    def display_error_message(self, screen: pg.Surface) -> None:
        # Check if there's an error message to display
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, (255, 0, 0))  # Red text for error
            error_rect = error_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))  # Position it under the roll dice button
            screen.blit(error_surface, error_rect)

            # Now reset the error_message after 2 seconds
            pg.time.set_timer(pg.USEREVENT, 2000)


    def update(self) -> None:
        now = pg.time.get_ticks()
        self.world.update()
        self.player.update(self.phase)

        self.finish_phase_button_hovered = False
        if self.finish_phase_button.collidepoint(pg.mouse.get_pos()):
            self.finish_phase_button_hovered = True

        if self.finish_phase_button_hovered:
            if pg.mouse.get_pressed()[0] and (now - self.phase_timer > 500):
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

    def create_phase_ui(self) -> None:
        self.current_phase_image = pg.Surface((200, 50))
        self.current_phase_image.fill((25, 42, 86))
        self.current_phase_rect = self.current_phase_image.get_rect(topleft=(10, 10))

        self.finish_phase_image = pg.Surface((200, 50))
        self.finish_phase_image.fill((25, 42, 86))
        self.finish_phase_button = self.finish_phase_image.get_rect(topleft=(10, 70))
        self.finish_phase_button_hovered = False

        self.roll_dice_image = pg.Surface((200, 50))
        self.roll_dice_image.fill((25, 42, 86))
        self.roll_dice_button = self.roll_dice_image.get_rect(topleft=(10, 130))
        self.roll_dice_button_hovered = False

    def draw_phase_ui(self) -> None:
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

            # attacker_armies = self.player.get_attacker_armies()  # Define this method in Player class
            # defender_armies = self.enemy_player.get_defender_armies()  # Define this method in Player class
            # defender_player = self.enemy_player  # This assumes you have a reference to the enemy player

            # # Now, call the attack_country method with the correct arguments
            # self.player.attack_country(attacker_armies, defender_armies, defender_player)

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
