from typing import List, Dict, Union

def calculate_budget_split(total_budget: float, days: int, interests: List[str], travelers: int = 1, currency: str = "USD") -> Dict:
    """
    Splits the budget into categories based on student-friendly logic.
    Adjusts based on interests and number of travelers.
    
    Args:
        total_budget: The total amount to spend.
        days: Duration of the trip.
        interests: List of user interests (e.g., 'Food', 'Adventure').
        travelers: Number of people sharing the trip.
        currency: The currency symbol/code.
        
    Returns:
        A dictionary containing budget metadata and the category breakdown.
    """
    
    # Base split logic for students (Zero-based budgeting approach)
    # We allocate percentages to buckets.
    split = {
        "Accommodation": 0.30, # Hostels/Dorms are usually the biggest chunk
        "Food": 0.25,          # Street food/budget eats
        "Transport": 0.20,     # Public transit
        "Activities": 0.15,    # Museums/Entry fees
        "Misc": 0.10           # Emergency/Shopping buffer
    }
    
    # Dynamic adjustments based on user personality
    if "Adventure" in interests or "Culture" in interests:
        split["Activities"] += 0.05
        split["Accommodation"] -= 0.05 # Sleep cheap, play hard
        
    if "Food" in interests:
        split["Food"] += 0.05
        split["Misc"] -= 0.05 # Eat more, buy less souvenirs

    # Normalize split just in case? (Optional, but good practice)
    # For now, we assume our logic sums to 1.0 or close enough.

    # Calculate raw amounts
    budget_breakdown = {k: round(v * total_budget, 2) for k, v in split.items()}
    
    # Per person per day calculation for quick reference
    daily_budget_per_person = round((total_budget / travelers) / days, 2)
    
    return {
        "total": total_budget,
        "currency": currency,
        "days": days,
        "travelers": travelers,
        "daily_avg_per_person": daily_budget_per_person,
        "breakdown": budget_breakdown
    }
