import random
from ..db.models import GameState

# Simple Simulation Rules
POPULATION_FOOD_CONSUMPTION = 2
WORKER_GOLD_PRODUCTION = 5
WORKER_FOOD_PRODUCTION = 3

def process_turn(current_state: GameState, actions: dict, seed: int) -> dict:
    """
    Takes current state and actions, computes next state.
    Returns Dictionary of new state values (not DB object).
    """
    random.seed(seed + current_state.year) # Deterministic randomness based on seed + year
    
    # Unpack current resources
    economy = current_state.economy.copy()
    gold = economy.get("gold", 0)
    food = economy.get("food", 0)
    population = economy.get("population", 0)
    
    # User Actions
    # e.g., "rationing" could reduce consumption but lower happiness (not impl yet)
    
    # 1. Consumption
    food_needed = population * POPULATION_FOOD_CONSUMPTION
    food_consumed = min(food, food_needed)
    food -= food_consumed
    
    starvation = 0
    if food_consumed < food_needed:
        # Starvation mechanics
        starvation = (food_needed - food_consumed) // POPULATION_FOOD_CONSUMPTION
        population = max(0, population - starvation)

    # 2. Production
    # Simplified: All population works
    gold += population * WORKER_GOLD_PRODUCTION
    food += population * WORKER_FOOD_PRODUCTION
    
    # 3. Events (Simple RNG)
    event_roll = random.random()
    event_log = {"event": "Normal Year", "effect": "None"}
    
    if event_roll < 0.1:
        event_log = {"event": "Bountiful Harvest", "effect": "+50 Food"}
        food += 50
    elif event_roll > 0.9:
        event_log = {"event": "Locust Swarm", "effect": "-50 Food"}
        food = max(0, food - 50)
        
    # Growth
    if starvation == 0:
        population += int(population * 0.05) # 5% growth if plenty

    # Next Season/Year
    next_year = current_state.year + 1
    # Simple rotation: Inundation -> Growing -> Harvest -> Inundation...
    # For MVP, let's just say 1 Turn = 1 Year
    
    return {
        "year": next_year,
        "season": "inundation", # Default start of year
        "economy": {"gold": gold, "food": food, "population": population},
        "last_event_log": event_log
    }
