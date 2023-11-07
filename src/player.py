import pygame as pg
import random

from src.geo import Country, World


class Player:
    def __init__(self, name ,country: Country, world: World, color: tuple) -> None:
        self.name = name
        self.country = country
        self.countries = []
        self.world = world
        self.color = color
        #self.enemy.player=enemy.player
        self.country.color = self.color
        self.timer = pg.time.get_ticks()
        self.controlled_countries = [self.country.name]
        self.neighbours = self.get_neighbours()
        print(self.neighbours)

    def update(self, phase: str) -> None:
        if phase == "place_units":
            self.place_units()
        elif phase == "move_units":
            self.move_units()
        elif phase == "attack_country":
            self.attack_country()
            # self.attack_country(currently controlled country that's attacking,
            #                     country that the controlled country is attacking,
            #                     enemy player object)
        

    def place_units(self) -> None:
        
        navigable_countries = []
        for name_of_country in self.controlled_countries:
            controlled_country = self.world.countries.get(name_of_country)
            navigable_countries.append(controlled_country)
            names_of_neighboring_countries = self.world.get_country_neighbours(name_of_country)
            for name_of_neighbor in names_of_neighboring_countries:
                neighboring_country= self.world.countries.get(name_of_neighbor)
                navigable_countries.append(neighboring_country)

        now = pg.time.get_ticks()      
        for navigable_country in navigable_countries:
            if navigable_country.hovered and pg.mouse.get_pressed()[0] and (now - self.timer > 300):
                self.timer = now
                navigable_country.units += 1 #increment code to add armies


    def initialize_units(self):
        # Start by ensuring each country has one army
        for country_name in self.controlled_countries:
            country = self.world.countries[country_name]
            country.units = 1

        # Each player starts with 30 armies, minus one for each country they control initially
        remaining_armies = 30 - len(self.controlled_countries)
        
        # Randomly distribute the remaining armies
        while remaining_armies > 0:
            for country_name in self.controlled_countries:
                country = self.world.countries[country_name]
                country.units += 1
                remaining_armies -= 1
                if remaining_armies <= 0:
                    break

    def randomize_countries(self):
        all_countries = list(self.world.countries.keys())  # Assuming this is a dict of all countries
        random.shuffle(all_countries)  # Shuffle the list of countries
        
        num_players = len(self.world.players)  # You'll need to have a list of all players somewhere
        countries_per_player = len(all_countries) // num_players
        
        # Assign countries to players
        for i, player in enumerate(self.world.players):
            player_countries = all_countries[i*countries_per_player:(i+1)*countries_per_player]
            player.controlled_countries = player_countries
            
            # Assign one army to each country
            for country_name in player_countries:
                self.world.countries[country_name].units = 1

        # If there are leftover countries due to uneven division, distribute them one by one to players
        leftover_countries = all_countries[num_players*countries_per_player:]
        for i, country_name in enumerate(leftover_countries):
            player_index = i % num_players  # This will cycle through the players
            self.world.players[player_index].controlled_countries.append(country_name)
            self.world.countries[country_name].units = 1

    def place_armies(self):
    #lets the player place their armies onto their assigned countries
    #i want to place a text where it says how many armies you have left to assign
        
        pass

    def move_units(self) -> None:
        #if the countries are neighbors, a player can move armies from one neighboring country to another
        #need to access self.controlled.countries

        pass

    def get_attacker_armies(self):
    # Assuming the player has selected a country to attack from
        selected_country = self.select_country_to_attack_from()  # You'll need to implement this method
        if selected_country in self.controlled_countries:
            return self.world.countries[selected_country].units
        else:
            return 0  # Or handle the error case appropriately

    def get_defender_armies(self):
    # Assuming the player has selected a country to attack
        target_country = self.select_country_to_attack()  # You'll need to implement this method
        if target_country not in self.controlled_countries:
            return self.world.countries[target_country].units
        else:
            return 0  # Or handle the error case appropriately

    def select_country_to_attack_from(self):
        # Logic to select a country to attack from.
        # This can be a random selection, a user input, or some AI decision logic.

        # Example of a simple selection (the first controlled country):
        if self.controlled_countries:
            return self.controlled_countries[0]
        else:
            return None  # or handle the case where the player controls no countries.

    def attack_country(self):
    # Retrieve the attacking country object using its name
        attacking_country = self.country

        # Retrieve the defending country object using its name
        # LOOP THROUGH ALL COUNTRIES (THAT'S NOT CONTROLLED OR THE ATTACKER)
        uncontrolled_countries = [uncontrolled_country for uncontrolled_country in self.world.countries if uncontrolled_country not in self]
        for each_country in uncontrolled_countries:
            # IF CURRENTLY ITERATED COUNTRY IS CLICKED ON
            # if navigable_country.hovered and pg.mouse.get_pressed()[0] and (now - self.timer > 300):
            if each_country.hovered and pg.mouse.get_pressed()[0]:
                # SET AS DEFENDING COUNTRY
                defending_country = each_country

    # Get the number of armies in the attacking country
        attacker_armies = attacking_country.units

    # Get the number of armies in the defending country
        defender_armies = defending_country.units
        if attacker_armies > defender_armies:
        # Attacker wins, defender loses all units
            defending_country.units = 0
            defending_country.owner = self  # Transfer ownership
        # Move a number of units from the attacking country to the conquered country
        # (leaving at least one behind)
            defending_country.units = attacker_armies - 1
            attacking_country.units = 1
        else:
        # Defender wins, attacker loses all attacking units except one
            attacking_country.units = 1

    def get_neighbours(self) -> list:
        neighbours = []
        for country in self.controlled_countries:
            for neighbour in self.world.countries[country].neighbours:
                if neighbour not in self.controlled_countries:
                    neighbours.append(neighbour)
        return set(neighbours)