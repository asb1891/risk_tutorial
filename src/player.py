import pygame
import random
from src.geo import World, Country
from src.dice import Dice

# Assuming the necessary classes are imported from their respective modules
class Player:
    def __init__(self, game, name, country: Country, world: World, color: tuple) -> None:
        self.name = name #players name
        self.game = game #reference to game instance
        self.country = country # the starting country for the player 
        self.countries = [] # list of countries owned by the player
        self.world = world #reference to world instance
        self.plus_button_pos = (0, 0)  # coordinates for the + button
        self.minus_button_pos = (0, 0) # coordinates for the - button
        self.color = color #color assigned ot the player
        self.mouse_get_pressed= pygame.mouse.get_pressed
        self.country.color = self.color #color of the countries
        self.timer = pygame.time.get_ticks() # pygame timeer to contorl tick rate
        self.controlled_countries = [self.country.name] #list of countries controlled by player, initialized with countries name
        self.neighbours = self.get_neighbours() #neighboring countries of the player's controlled countries 

    #update mehtod to handle different phases of the game
    def update(self, phase: str) -> None:
        if phase == "place_units":
            self.place_units()
        elif phase == "attack_country":
            self.attack_country()

    #place units method for placing new units on the player's countries
    def place_units(self) -> None:
        #get a list of countries the player can navigate to 
        navigable_countries = self.get_navigable_countries()
        now = pygame.time.get_ticks()
        # loop through the navigable countries and place units on hovered country when clicked
        for navigable_country in navigable_countries:
            if navigable_country.hovered and pygame.mouse.get_pressed()[0] and (now - self.timer > 300):
                self.timer = now
                navigable_country.units += 1 #increase units by 1

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
                neighboring_country= self.world.countries.get(name_of_neighbor)
                navigable_countries.append(neighboring_country)

        now = pg.time.get_ticks()      
        for navigable_country in navigable_countries:
            if navigable_country.hovered and pg.mouse.get_pressed()[0] and (now - self.timer > 300):
                self.timer = now
                navigable_country.units += 1 #increment code to add armies


                ##### COMMENTED OUT CODE 
    # def place_units(self) -> None:
    #     # from src.game import Game
    #     navigable_countries = self.get_navigable_countries()
    #     now = pygame.time.get_ticks()
        
    #     # Draw and interact with plus and minus buttons
    #     for navigable_country in navigable_countries:
    #         if navigable_country.hovered:
    #             # Define positions for plus and minus buttons relative to the country's location
    #             plus_button_pos= (navigable_country.center[0] +50, navigable_country.center[1]) # Example position
    #             minus_button_pos= (navigable_country.center[0] -50, navigable_country.center[1]) # Example position

    #             # Check if the plus button is clicked
    #             if self.world.draw_button(plus_button_pos) and (now - self.timer > 300):
    #                 self.timer = now
    #                 navigable_country.units += 1  # Increment units
                
    #             # Check if the minus button is clicked
    #             if self.world.draw_button(minus_button_pos) and (now - self.timer > 300):
    #                 self.timer = now
    #                 navigable_country.units -= 1  # Decrement units

    #         # existing code for unit placement by clicking on the country itself
    #             if navigable_country.hovered and pygame.mouse.get_pressed()[0] and (now - self.timer > 300):
    #                 self.timer = now
    #                 navigable_country.units += 1




    # Helper function to determine if a button is clicked
    def button_clicked(self, button_pos) -> bool:
        button_rect = pygame.Rect(button_pos, (30, 30))
        return button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
    
    # Increment units for a country
    def increment_units(self, country):
        country.units += 1
    
    # Decrement units for a country
    def decrement_units(self, country):
        if country.units > 0:  # Prevent negative units
            country.units -= 1


            ### COMMENTED OUT CODE 
    # def place_units(self) -> None:
    #     navigable_countries = self.get_navigable_countries()
    #     now = pygame.time.get_ticks()
    #     for navigable_country in navigable_countries:
    #         if navigable_country.hovered and pygame.mouse.get_pressed()[0] and (now - self.timer > 300):
    #             self.timer = now
    #             navigable_country.units += 1

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
    
    # An attack method using the roll dice method 
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
    
        ### COMMENTED OUT CODE
  # def update_dice_display(self, attacker_dice, defender_dice):
    #     font= pygame.font.Font(None, 36)

    #     attacker_text = ', '.join(str(roll) for roll in attacker_dice)
    #     attacker_surface = font.render(f"Attacker rolls: (attacker_text)", True, (255, 255, 255))

    #     defender_text = ', '.join(str(roll) for roll in defender_dice)
    #     defender_surface = font.render(f"Defender rolls: (defender_text)", True (255, 255, 255))

    #     self.game.screen.blit(attacker_surface, (x_attacker, y_attacker))
    #     self.game.screen.blit(defender_surface, (x_defender, y_defender))

    #     pygame.display.update([attacker_surface.get_rect(topleft=(x_attacker, y_attacker)), defender_surface.get_rect(topleft=(x_defender, y_defender))])