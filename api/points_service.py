import random
from decimal import Decimal

def calculate_points(difficulty):
    points_map = {
        'TR': (5, 20),   # Trivial
        'EA': (15, 35),   # Easy
        'ME': (30, 55),   # Medium
        'HA': (50, 75),  # Hard
    }
    lp_chance = {
        'TR': 0.10,  # 10% chance to earn LP for Trivial tasks
        'EA': 0.225, # 22.5% chance for Easy
        'ME': 0.35,  # 35% chance for Medium
        'HA': 0.45,  # 45% chance for Hard
    }
    lp_range = {
        'TR': (0.5, 2),   # Trivial
        'EA': (1.5, 3.5), # Easy
        'ME': (3, 5.5),   # Medium
        'HA': (5, 7.5),   # Hard
    }
    
    hp_min, hp_max = points_map[difficulty]
    hp_earned = random.randint(hp_min, hp_max)
    
    lp_earned = Decimal('0.00')
    
    if random.random() < lp_chance[difficulty]:
        lp_min, lp_max = lp_range[difficulty]
        lp_earned = Decimal(str(random.uniform(lp_min, lp_max))).quantize(Decimal('0.01'))
    
    return hp_earned, lp_earned
