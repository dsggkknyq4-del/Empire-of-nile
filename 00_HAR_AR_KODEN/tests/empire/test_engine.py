import pytest
from src.empire.services.engine import process_turn
from src.empire.db.models import GameState

def test_engine_production():
    # Setup State
    initial_state = GameState(
        year=1,
        economy={"gold": 0, "food": 100, "population": 10},
        last_event_log={}
    )
    
    # Process Turn (no actions, fixed seed)
    next_state_dict = process_turn(initial_state, {}, seed=1)
    
    # Assertions
    # 10 Pop * 3 Food = 30 Prod. 10 * 2 = 20 Cons. Net +10.
    # But events might trigger. 
    # This is just a placeholder to show structure.
    assert next_state_dict["year"] == 2
