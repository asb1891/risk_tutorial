import json
import pygame
import random
from pandas import Series
from shapely.geometry import Point, Polygon

from src.utils import draw_text, draw_multiline_text


class Country:
    # Constructor for the Country class: Initializes a country with its name, coordinates, and other properties.
    def __init__(self, name: str, coords: list) -> None:
        self.name = name  # Name of the country.
        self.attack_armies = 1  # The initial number of attacking armies is set to 1.
        self.coords = coords  # Coordinates defining the country's polygon on the map.
        self.font = pygame.font.SysFont(None, 24)  # Font for rendering text.
        self.polygon = Polygon(self.coords)  # Create a polygon from the coordinates.
        self.center = self.get_center()  # Calculate the geometric center of the country.
        self.units = random.randint(1, 3)  # Randomly assign 1-3 units to the country.
        self.color = (72, 126, 176)  # Default color for the country.
        self.hovered = False  # State to track if the mouse is hovering over the country.
        self.neighbours = None  # Neighboring countries, not initialized here.

    # Method to update the country's state based on the mouse position.
    def update(self, mouse_pos: pygame.Vector2) -> None:
        self.hovered = False  # Reset the hovered state.
        # Check if the mouse position is within the country's polygon area.
        if Point(mouse_pos.x, mouse_pos.y).within(self.polygon):
            self.hovered = True  # Set hovered to true if the mouse is over the country.

    # Method to draw the country on the screen, including its armies count.
    def draw(self, screen: pygame.Surface, scroll: pygame.Vector2) -> None:
        # Draw the country's polygon. If hovered, the color changes to red.
        pygame.draw.polygon(
            screen,
            (255, 0, 0) if self.hovered else self.color,
            [(x - scroll.x, y - scroll.y) for x, y in self.coords],
        )
        # Draw the polygon's outline in white.
        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            [(x - scroll.x, y - scroll.y) for x, y in self.coords],
            width=1,
        )
        # Render the text showing the number of units on the country, centered.
        draw_text(
            screen,
            self.font,
            str(self.units),
            (255, 255, 255),
            self.center.x - scroll.x,
            self.center.y - scroll.y,
            True,
        )
    # Helper method to calculate the geometric center of the country's polygon.
    def get_center(self) -> pygame.Vector2:
        # Use pandas Series to calculate the mean of x and y coordinates.
        return pygame.Vector2(
            Series([x for x, y in self.coords]).mean(),
            Series([y for x, y in self.coords]).mean(),
        )


class World:
    # Class-level constants defining the size of the game world map.
    MAP_WIDTH = 2.05 * 4000 * 0.6  # The width of the map, calculated using a base width and a scaling factor.
    MAP_HEIGHT = 1.0 * 4000 * 0.6  # The height of the map, calculated similarly to the width.
    SCALE_FACTOR = 1  # A scaling factor used for coordinate scaling; currently set to 1, so it has no effect.

    # Constructor for the World class.
    def __init__(self, game) -> None:
        self.game = game  # A reference to the main game object.
        self.read_geo_data()  # Method call to read geographical data, not defined in this snippet.
        self.countries = self.create_countries()  # Creates country objects, method not defined in this snippet.
        self.create_neighbours()  # Sets up neighboring countries, method not defined in this snippet.
        self.players = []  # A list to hold player objects.
        self.scroll = pygame.Vector2(2000, 500)  # Initial scrolling offset for the map view.
        self.font = pygame.font.SysFont(None, 24)  # Font for rendering text on the UI.

        # Initializes a UI element that appears when a country is hovered over.
        self.hovered_country = None  # The country object that is currently being hovered by the mouse.
        self.hover_surface = pygame.Surface((300, 100), pygame.SRCALPHA)  # A surface for the hovering UI panel.
        self.hover_surface.fill((25, 42, 86, 155))  # Fills the hover surface with a semi-transparent color.

    def read_geo_data(self) -> None:
        #loads the geo data from the JSON file
        with open("./data/country_coords.json", "r") as f:
            self.geo_data = json.load(f)

    def create_countries(self) -> dict:
        #Porcesses the go data to create country objects
        countries = {}
        for name, coords in self.geo_data.items():
            xy_coords = []
            for coord in coords:
                x = ((self.MAP_WIDTH / 360) * (180 + coord[0])) * self.SCALE_FACTOR
                y = ((self.MAP_HEIGHT / 180) * (90 - coord[1])) * self.SCALE_FACTOR
                xy_coords.append(pygame.Vector2(x, y))
            countries[name] = Country(name, xy_coords)
        return countries
    
    def create_players(self, num_players):
        #initializes player objects for the game
        from src.player import Player
        for i in range(num_players):
            player_name = f"Player (i+1)"
            new_player = Player(player_name)
            self.players.append(new_player)

    def draw(self, screen: pygame.Surface) -> None:
        #draws the world and countries on screen
        for country in self.countries.values():
            country.draw(screen, self.scroll)
        if self.hovered_country is not None:
            self.draw_hovered_country(screen)
        # if self.game.error_message:
        #     self.game.display_error_message(screen)

    def update(self) -> None:
        #Handles the logic for updating the state of the world, movement and mouse
        self.update_camera()
        mouse_pos = pygame.mouse.get_pos()
        # self.hovered_country = None
        for country in self.countries.values():
            country.update(
                pygame.Vector2(mouse_pos[0] + self.scroll.x, mouse_pos[1] + self.scroll.y)
            )
            if country.hovered:
                self.hovered_country = country
        clicked = pygame.mouse.get_pressed()[0]
        # if not clicked:
                # self.hovered_country = None
        for country in self.countries.values():
                country.update(
                    pygame.Vector2(mouse_pos[0] + self.scroll.x, mouse_pos[1] + self.scroll.y)
                )
                if country.hovered:
                    if clicked:
                        # if self.hovered_country is None:
                        #     pass
                        # else:
                        #     self.hovered_country = country
                        self.hovered_country = country
    #sets up user camera controls and keys for movement and movement speed 
    def update_camera(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.scroll.x -= 10
        elif keys[pygame.K_d]:
            self.scroll.x += 10

        if keys[pygame.K_w]:
            self.scroll.y -= 10
        elif keys[pygame.K_s]:
            self.scroll.y += 10

        if keys[pygame.K_SPACE]:
            self.scroll = pygame.Vector2(3650, 395)

    def draw_hovered_country(self, screen: pygame.Surface) -> None:
        #drawes the UI elements related to the country the mouse is hovering over
        screen.blit(self.hover_surface, (1280 - 310, 720 - 110))

        plus_button_pos = (1280 - 310 + 200, 720- 90)
        minus_button_pos = (1280 - 310 + 150, 720-90)
        #draws interactive buttons on the screen
        self.draw_button(screen, "+", plus_button_pos, self.increment_armies)
        self.draw_button(screen, "-", minus_button_pos, self.decrement_armies)
    # def draw_hovered_country(self, screen: pygame.Surface) -> None:
    # Draw the UI elements related to the country the mouse is hovering over
        # screen.blit(self.hover_surface, (1280 - 310, 720 - 110))

        # plus_button_pos = (1280 - 310 + 200, 720 - 90)
        # minus_button_pos = (1280 - 310 + 150, 720 - 90)

        # # Draws interactive buttons on the screen
        # self.draw_button(screen, "+", plus_button_pos, self.increment_armies)
        # self.draw_button(screen, "-", minus_button_pos, self.decrement_armies)

        # # Check for a click event
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         # Get the mouse position
        #         mouse_pos = event.pos

        #         # Check if the plus or minus button was clicked
        #         if plus_button_rect.collidepoint(mouse_pos):
        #             self.increment_armies()
        #         elif minus_button_rect.collidepoint(mouse_pos):
        #             self.decrement_armies()

    # # You would define the rectangles for the buttons when you create them
    # plus_button_rect = pygame.Rect(plus_button_pos[0], plus_button_pos[1], button_width, button_height)
    # minus_button_rect = pygame.Rect(minus_button_pos[0], minus_button_pos[1], button_width, button_height)  
    # def draw_hovered_country(self, screen: pygame.Surface) -> None:
    #     #drawes the UI elements related to the country the mouse is hovering over
    #     screen.blit(self.hover_surface, (1280 - 310, 720 - 110))

    #     plus_button_pos = (1280 - 310 + 200, 720- 90)
    #     minus_button_pos = (1280 - 310 + 150, 720-90)
    #     #draws interactive buttons on the screen
    #     self.draw_button(screen, "+", plus_button_pos, self.increment_armies)
    #     self.draw_button(screen, "-", minus_button_pos, self.decrement_armies)

        draw_text(
            screen,
            self.font,
            self.hovered_country.name,
            (255, 255, 255),
            1280 - 310 / 2,
            720 - 100,
            True,
            24,
        )
        #creates a box for hovered countries and displayes Armies and a "+" and "-" button to add or subtract armies
        draw_multiline_text(
            screen,
            self.font,
            [f"Armies: {str(self.hovered_country.units)}"],
            (255, 255, 255),
            1280 - 310 + 5,
            720 - 90 + 5,
            False,
            20,
        )
    #dreaws actual button sizes 
    # def draw_button(self, screen:pygame.Surface, text: str, position: tuple, on_click) -> None:
    #     button_rect = pygame.Rect(position, (30, 30))  # Button size of 30x30
    #     pygame.draw.rect(screen, (0, 0, 0), button_rect)  # Draw the button

    #     # Draw the button text
    #     draw_text(screen, self.font, text, (255, 255, 255), *position, True, 20)

    #     # Check for click events
    #     if button_rect.collidepoint(pygame.mouse.get_pos()):
    #         if pygame.mouse.get_pressed()[0]:
    #             on_click()
    def draw_button(self, screen: pygame.Surface, text: str, position: tuple, on_click) -> None:
        button_rect = pygame.Rect(position, (30, 30))  # Button size of 30x30
        pygame.draw.rect(screen, (255, 255, 255), button_rect)  # Draw the button with white color

        # Get the size of the text to be rendered
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_size = text_surface.get_size()

        # Calculate the position to center the text
        text_x = position[0] + (button_rect.width - text_size[0]) // 2
        text_y = position[1] + (button_rect.height - text_size[1]) // 2

        # Draw the button text, now with black color, centered in the button
        screen.blit(text_surface, (text_x, text_y))

        # Check for click events
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                on_click()

# This draw_text function must be defined elsewhere in your code
# It should be responsible for rendering text on the screen

# You would use draw_button like this:
        # self.draw_button(screen, "+", plus_button_pos, self.increment_armies)
        # self.draw_button(screen, "-", minus_button_pos, self.decrement_armies)

    def increment_armies(self) -> None:
        if self.hovered_country and self.hovered_country.units > self.hovered_country.attack_armies:
            self.hovered_country.attack_armies += 1

    def decrement_armies(self) -> None:
        if self.hovered_country and self.hovered_country.attack_armies > 1:
            self.hovered_country.attack_armies -= 1

    def create_neighbours(self) -> None:
        for k, v in self.countries.items():
            v.neighbours = self.get_country_neighbours(k)

    def get_country_neighbours(self, country: str) -> list:
        #retrieves a list of neighboring countries for a given country
        neighbours = []
        country_poly = self.countries[country].polygon
        for other_country_key, other_country_value in self.countries.items():
            if country != other_country_key:
                if country_poly.intersects(other_country_value.polygon):
                    neighbours.append(other_country_key)
            if country == "United States of America":
                neighbours += ["Canada", "Mexico"]
            elif country == "Canada":
                neighbours += ["United States of America"]
            elif country == "Mexico":
                neighbours += ["United States of America", "Belize", "Guatemala"]
            elif country == "Belize":
                neighbours += ["Mexico", "Guatemala"]
            elif country == "Guatemala":
                neighbours += ["Mexico", "Belize", "Honduras", "El Salvador"]
            elif country == "Honduras":
                neighbours += ["Guatemala", "El Salvador", "Nicaragua"]
            elif country == "El Salvador":
                neighbours += ["Guatemala", "Honduras"]
            elif country == "Nicaragua":
                neighbours += ["Honduras", "Costa Rica"]
            elif country == "Costa Rica":
                neighbours += ["Nicaragua", "Panama"]
            elif country == "Panama":
                neighbours += ["Costa Rica"]
            elif country == "Cuba":
                neighbours += ["Haiti", "Jamaica", "Bahamas"]
            elif country == "Haiti":
                neighbours += ["Dominican Republic", "Cuba"]
            elif country == "Dominican Republic":
                neighbours += ["Haiti"]
            elif country == "Jamaica":
                neighbours += ["Cuba"]
            elif country == "The Bahamas":
                neighbours += ["Cuba"]
            elif country == "Puerto Rico":
                neighbours += ["Dominican Republic", "Virgin Islands (US)"]
            elif country == "US Virgin Islands":
                neighbours += ["Puerto Rico", "British Virgin Islands"]
            elif country == "British Virgin Islands":
                neighbours += ["US Virgin Islands", "Anguilla"]
            elif country == "Anguilla":
                neighbours += ["British Virgin Islands", "Saint Martin"]
            elif country == "Saint Martin":
                neighbours += ["Sint Maarten", "Anguilla", "Saint Barthelemy"]
            elif country == "Sint Maarten":
                neighbours += ["Saint Martin"]
            elif country == "Saint Barthelemy":
                neighbours += ["Saint Martin"]
            elif country == "Antigua and Barbuda":
                neighbours += ["Saint Kitts and Nevis", "Montserrat"]
            elif country == "Montserrat":
                neighbours += ["Antigua and Barbuda"]
            elif country == "Saint Kitts and Nevis":
                neighbours += ["Antigua and Barbuda"]
            elif country == "Dominica":
                neighbours += ["Guadeloupe", "Martinique"]
            elif country == "Saint Lucia":
                neighbours += ["Martinique", "Saint Vincent and the Grenadines"]
            elif country == "Saint Vincent and the Grenadines":
                neighbours += ["Saint Lucia", "Barbados"]
            elif country == "Barbados":
                neighbours += ["Saint Vincent and the Grenadines"]
            elif country == "Grenada":
                neighbours += ["Trinidad and Tobago"]
            elif country == "Trinidad and Tobago":
                neighbours += ["Grenada"]
            elif country == "Aruba":
                neighbours += ["Curaçao"]
            elif country == "Curaçao":
                neighbours += ["Aruba"]
            elif country == "Greenland":
                neighbours += ["Canada"]
            elif country == "Cayman Islands":
                neighbours += ["Jamaica"]
            elif country == "Turks and Caicos Islands":
                neighbours += ["Bahamas"]
            elif country == "Saint Pierre and Miquelon":
                neighbours += ["Canada"]
            return neighbours