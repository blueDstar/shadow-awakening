"""EXP Calculator - handles leveling and EXP requirements"""
import math


def exp_to_next_level(level: int) -> int:
    """Calculate EXP needed for next level.
    Formula: 100 * level * (1 + level * 0.1)
    Level 1->2: 110
    Level 2->3: 240
    Level 10->11: 2000
    Level 50->51: 30000
    """
    return int(100 * level * (1 + level * 0.1))


def check_level_up(current_level: int, current_exp: int) -> tuple:
    """Check if user should level up.
    Returns (new_level, remaining_exp, leveled_up)
    """
    needed = exp_to_next_level(current_level)
    if current_exp >= needed:
        new_level = current_level + 1
        remaining_exp = current_exp - needed
        # Recursive check for multiple level ups
        final_level, final_exp, _ = check_level_up(new_level, remaining_exp)
        return final_level, final_exp, True
    return current_level, current_exp, False


def calculate_quest_exp(difficulty: int, quest_type: str, level: int) -> int:
    """Calculate EXP reward for a quest based on difficulty and type."""
    base_exp = {
        "main": 30,
        "side": 15,
        "habit": 10,
        "challenge": 40,
        "penalty": 20,
        "special": 50,
        "breakthrough": 100,
    }
    base = base_exp.get(quest_type, 15)
    return int(base * (1 + difficulty * 0.15) * (1 + level * 0.02))


def calculate_stat_gain(base_gain: float, difficulty: int, streak: int) -> float:
    """Calculate stat gain with difficulty and streak bonuses."""
    streak_bonus = 1 + min(streak * 0.02, 0.5)  # max +50%
    difficulty_bonus = 1 + difficulty * 0.1
    return round(base_gain * difficulty_bonus * streak_bonus, 2)
