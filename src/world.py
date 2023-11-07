import pygame as pg

class World:
    # ... other methods and initializations ...

    def get_country_at_pos(self, pos):
        # Loop through all countries and check if the position is within any country's boundaries
        for country_name, country in self.countries.items():
            if country.contains(pos):
                return country
        return None
