"""Difficulty Scaler - adjusts quest difficulty based on user performance"""


def calculate_base_difficulty(level: int, overall_streak: int) -> int:
    """Calculate base difficulty for quest generation (1-10 scale)."""
    base = min(1 + level // 5, 8)
    streak_boost = min(overall_streak // 7, 2)
    return min(base + streak_boost, 10)


def apply_dynamic_adjustment(
    base_difficulty: int,
    consecutive_fails: int,
    consecutive_successes: int,
    completion_rate_7d: float,
) -> int:
    """Apply dynamic difficulty adjustment based on recent performance."""
    difficulty = base_difficulty
    
    # Reduce if struggling
    if consecutive_fails >= 3:
        difficulty = max(1, int(difficulty * 0.7))
    elif consecutive_fails >= 2:
        difficulty = max(1, difficulty - 1)
    
    # Increase if performing well
    if consecutive_successes >= 5:
        difficulty = min(10, int(difficulty * 1.2))
    elif consecutive_successes >= 3:
        difficulty = min(10, difficulty + 1)
    
    # Adjust based on 7-day completion rate
    if completion_rate_7d < 0.4:
        difficulty = max(1, difficulty - 2)
    elif completion_rate_7d < 0.6:
        difficulty = max(1, difficulty - 1)
    elif completion_rate_7d > 0.9:
        difficulty = min(10, difficulty + 1)
    
    return difficulty


def scale_quest_requirements(base_value: int, difficulty: int, level: int) -> int:
    """Scale quest requirements (e.g., push-ups, pages to read) by difficulty and level."""
    scale_factor = 1 + (difficulty - 1) * 0.15 + level * 0.02
    return max(1, int(base_value * scale_factor))
