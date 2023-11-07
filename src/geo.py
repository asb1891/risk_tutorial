import json
import pygame as pg
import random
from pandas import Series
from shapely.geometry import Point, Polygon

from src.utils import draw_text, draw_multiline_text


class Country:
    def __init__(self, name: str, coords: list) -> None:
        self.name = name
        self.attack_armies= 1
        self.coords = coords
        self.font = pg.font.SysFont(None, 24)
        self.polygon = Polygon(self.coords)
        self.center = self.get_center()
        self.units = random.randint(1, 3)
        self.color = (72, 126, 176)
        self.hovered = False
        self.neighbours = None

    def update(self, mouse_pos: pg.Vector2) -> None:
        self.hovered = False
        if Point(mouse_pos.x, mouse_pos.y).within(self.polygon):
            self.hovered = True

    def draw(self, screen: pg.Surface, scroll: pg.Vector2) -> None:
        pg.draw.polygon(
            screen,
            (255, 0, 0) if self.hovered else self.color,
            [(x - scroll.x, y - scroll.y) for x, y in self.coords],
        )
        pg.draw.polygon(
            screen,
            (255, 255, 255),
            [(x - scroll.x, y - scroll.y) for x, y in self.coords],
            width=1,
        )
        draw_text(
            screen,
            self.font,
            str(self.units),
            (255, 255, 255),
            self.center.x - scroll.x,
            self.center.y - scroll.y,
            True,
        )

    def get_center(self) -> pg.Vector2:
        return pg.Vector2(
            Series([x for x, y in self.coords]).mean(),
            Series([y for x, y in self.coords]).mean(),
        )


class World:
    MAP_WIDTH = 2.05 * 4000 * 0.6
    MAP_HEIGHT = 1.0 * 4000 * 0.6
    
    SCALE_FACTOR = 1
    

    def __init__(self, game) -> None:
        self.game= game
        self.read_geo_data()
        self.countries = self.create_countries()
        self.create_neighbours()
        self.players = []
        self.scroll = pg.Vector2(2000, 500)
        self.font = pg.font.SysFont(None, 24)

        # hovering countries panel
        self.hovered_country = None
        self.hover_surface = pg.Surface((300, 100), pg.SRCALPHA)
        self.hover_surface.fill((25, 42, 86, 155))

    def read_geo_data(self) -> None:
        with open("./data/country_coords.json", "r") as f:
            self.geo_data = json.load(f)

    def create_countries(self) -> dict:
        countries = {}
        for name, coords in self.geo_data.items():
            xy_coords = []
            for coord in coords:
                x = ((self.MAP_WIDTH / 360) * (180 + coord[0])) * self.SCALE_FACTOR
                y = ((self.MAP_HEIGHT / 180) * (90 - coord[1])) * self.SCALE_FACTOR
                xy_coords.append(pg.Vector2(x, y))
            countries[name] = Country(name, xy_coords)
        return countries
    
    def create_players(self, num_players):
        from src.player import Player
        for i in range(num_players):
            player_name = f"Player (i+1)"
            new_player = Player(player_name)
            self.players.append(new_player)

    def draw(self, screen: pg.Surface) -> None:
        for country in self.countries.values():
            country.draw(screen, self.scroll)
        if self.hovered_country is not None:
            self.draw_hovered_country(screen)
        if self.game.error_message:
            self.game.display_error_message(screen)

    def update(self) -> None:
        self.update_camera()
        mouse_pos = pg.mouse.get_pos()
        self.hovered_country = None
        for country in self.countries.values():
            country.update(
                pg.Vector2(mouse_pos[0] + self.scroll.x, mouse_pos[1] + self.scroll.y)
            )
            if country.hovered:
                self.hovered_country = country
        # clicked = pg.mouse_get_pressed()[0]
        # if not clicked:
        #         self.hovered_country = None
        # for country in self.countries.values():
        #         country.update(
        #             pg.Vector2.mouse_pos[0] + self.scroll.x, mouse_pos[1] + self.scroll.y
        #         )
        #         if country.hovered:
        #             if clicked and not self.selected_country:
        #                 self.selected_country = country
        #             self.hovered_country = country
        # if clicked and not self.hovered_country: 
        #     self.selected_country = None

    def update_camera(self) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.scroll.x -= 10
        elif keys[pg.K_d]:
            self.scroll.x += 10

        if keys[pg.K_w]:
            self.scroll.y -= 10
        elif keys[pg.K_s]:
            self.scroll.y += 10

        if keys[pg.K_SPACE]:
            self.scroll = pg.Vector2(3650, 395)

    def draw_hovered_country(self, screen: pg.Surface) -> None:
        screen.blit(self.hover_surface, (1280 - 310, 720 - 110))

        plus_button_pos = (1280 - 310 + 200, 720- 90)
        minus_button_pos = (1280 - 310 + 150, 720-90)

        self.draw_button(screen, "+", plus_button_pos, self.increment_armies)
        self.draw_button(screen, "+", minus_button_pos, self.decrement_armies)

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

    def draw_button(self, screen:pg.Surface, text: str, position: tuple, on_click) -> None:
        button_rect = pg.Rect(position, (30, 30))  # Button size of 30x30
        pg.draw.rect(screen, (0, 0, 0), button_rect)  # Draw the button

        # Draw the button text
        draw_text(screen, self.font, text, (255, 255, 255), *position, True, 20)

        # Check for click events
        if button_rect.collidepoint(pg.mouse.get_pos()):
            if pg.mouse.get_pressed()[0]:
                on_click()

    def increment_armies(self) -> None:
        if self.hovered_country and self.hovered_country.units > self.attack_armies:
            self.attack_armies += 1

    def decrement_armies(self) -> None:
        if self.hovered_country and self.attack_armies > 1:
            self.attack_armies -= 1

    def create_neighbours(self) -> None:
        for k, v in self.countries.items():
            v.neighbours = self.get_country_neighbours(k)

    def get_country_neighbours(self, country: str) -> list:
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