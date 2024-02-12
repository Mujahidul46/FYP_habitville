import random
from decimal import Decimal

def calculate_points(difficulty):
    points_map = {
        'TR': (1, 10), # Trivial
        'EA': (10, 25),   # Easy
        'ME': (25, 60),   # Medium
        'HA': (60, 100),  # Hard
    }
    lp_chance = {
        'TR': 0.10,  # 10% chance to earn LP for Trivial tasks
        'EA': 0.25, # 25% chance for Easy
        'ME': 0.75,  # 75% chance for Medium
        'HA': 1,  # 100% chance for Hard
    }
    lp_range = {
        'TR': (0.1, 1),   # Trivial
        'EA': (1, 2), # Easy
        'ME': (2, 3),   # Medium
        'HA': (3, 4),   # Hard
    }
    
    hp_min, hp_max = points_map[difficulty]
    hp_earned = random.randint(hp_min, hp_max)
    
    lp_earned = Decimal('0.00')
    
    if random.random() < lp_chance[difficulty]:
        lp_min, lp_max = lp_range[difficulty]
        lp_earned = Decimal(str(random.uniform(lp_min, lp_max))).quantize(Decimal('0.01'))
    
    return hp_earned, lp_earned
