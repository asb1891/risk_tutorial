import random

class Dice:

    def attacker_dice_roll(num_dice):
    # Attacker rolls up to 3 dice
        return sorted([random.randint(1, 6) for _ in range(num_dice)], reverse=True)

    def defender_dice_roll(num_dice):
    # Defender rolls up to 2 dice
         return sorted([random.randint(1, 6) for _ in range(num_dice)], reverse=True)
