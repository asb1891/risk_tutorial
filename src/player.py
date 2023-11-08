import pygame
import random
from src.geo import World, Country
from src.dice import Dice

# x_attacker= 50
# y_attacker= 50

# x_defender= 50
# y_defender= 100

# Assuming the necessary classes are imported from their respective modules
class Player:
    def __init__(self, name, country: Country, world: World,  color: tuple) -> None:
        self.name = name
        self.country = country
        self.countries = []
        self.world = world
        self.color = color
        self.mouse_get_pressed= pygame.mouse.get_pressed
        self.country.color = self.color
        self.timer = pygame.time.get_ticks()
        self.controlled_countries = [self.country.name]
        self.neighbours = self.get_neighbours()

    def update(self, phase: str) -> None:
        if phase == "place_units":
            self.place_units()
        elif phase == "attack_country":
            self.attack_country()

    def place_units(self) -> None:
        navigable_countries = self.get_navigable_countries()
        now = pygame.time.get_ticks()
        for navigable_country in navigable_countries:
            if navigable_country.hovered and pygame.mouse.get_pressed()[0] and (now - self.timer > 300):
                self.timer = now
                navigable_country.units += 1

    def get_navigable_countries(self) -> list:
        navigable_countries = []
        print(f"\n>> CURRENT CONTROLLED COUNTRIES PRE-ITERATION: {self.controlled_countries}")
        for name_of_country in self.controlled_countries:
            controlled_country = self.world.countries.get(name_of_country)
            print(f"\t>> CURRENT NAVIGABLE COUNTRIES PRE-ADDITION OF CONTROLLED COUNTRY: {navigable_countries}")
            navigable_countries.append(controlled_country)
            print(f"\t>> CURRENT NAVIGABLE COUNTRIES POST-ADDITION OF CONTROLLED COUNTRY: {navigable_countries}")
            names_of_neighboring_countries = self.world.get_country_neighbours(name_of_country)
            print(f"\t>> CURRENT NEIGHBORING COUNTRIES FOR COUNTRY={name_of_country}: {self.world.get_country_neighbours(name_of_country)}")
            for name_of_neighbor in names_of_neighboring_countries:
                neighboring_country = self.world.countries.get(name_of_neighbor)
                if neighboring_country not in navigable_countries:
                    print(f"\t\t>> CURRENT NAVIGABLE COUNTRIES PRE-ADDITION OF NEIGHBORING COUNTRY: {navigable_countries}")
                    navigable_countries.append(neighboring_country)
                    print(f"\t\t>> CURRENT NAVIGABLE COUNTRIES POST-ADDITION OF NEIGHBORING COUNTRY: {navigable_countries}")
        print(f"\nFINAL NAVIGABLE COUNTRIES: {navigable_countries}\n")
        return navigable_countries
    #method to attack another country
    def attack_country(self):
        attacking_country = self.country #sets attacking_country to players current country
        defending_country = None
        for each_country in self.world.countries.values(): #iterates over all countries to find a country not in "attacking_country"
            if each_country != attacking_country and each_country.hovered and pygame.mouse.get_pressed()[0]:
                defending_country = each_country
                break

        if defending_country: #if a defending country is found, execute attack
            self.execute_attack(attacking_country, defending_country)
    
    def execute_attack(self, attacking_country, defending_country):
        attacker_dice = Dice.attacker_dice_roll(min(3, attacking_country.units - 1))
        defender_dice = Dice.defender_dice_roll(min(2, defending_country.units))

        for attacker_roll, defender_roll in zip(attacker_dice, defender_dice):
            if attacker_roll > defender_roll:
                defending_country.units -= 1
                print(defending_country.units)
            else:
                attacking_country.units -= 1
                print(attacking_country.units)

        if defending_country.units <= 0:
            self.transfer_ownership(attacking_country, defending_country)

    def transfer_ownership(self, attacking_country, defending_country):
        defending_country.owner = self
        defending_country.units = attacking_country.units - 1
        attacking_country.units -= 1

    def get_neighbours(self) -> set:
        neighbours = {neighbour for country in self.controlled_countries
                      for neighbour in self.world.countries[country].neighbours
                      if neighbour not in self.controlled_countries}
        return neighbours
    

  # def update_dice_display(self, attacker_dice, defender_dice):
    #     font= pygame.font.Font(None, 36)

    #     attacker_text = ', '.join(str(roll) for roll in attacker_dice)
    #     attacker_surface = font.render(f"Attacker rolls: (attacker_text)", True, (255, 255, 255))

    #     defender_text = ', '.join(str(roll) for roll in defender_dice)
    #     defender_surface = font.render(f"Defender rolls: (defender_text)", True (255, 255, 255))

    #     self.game.screen.blit(attacker_surface, (x_attacker, y_attacker))
    #     self.game.screen.blit(defender_surface, (x_defender, y_defender))

    #     pygame.display.update([attacker_surface.get_rect(topleft=(x_attacker, y_attacker)), defender_surface.get_rect(topleft=(x_defender, y_defender))])