import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_groq_client():
    """Singleton-ish pattern to get the client safely."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        return None

client = get_groq_client()

def get_ai_suggestions(budget, interests, country=None):
    """
    Asks AI for destination suggestions based on criteria.
    This is useful for the 'where should I go?' feature.
    """
    if not client:
        return "Error: Groq API Key missing."

    country_context = f"in {country}" if country and country != "Anywhere" else "anywhere in the world"
    
    prompt = f"""
    Suggest 3 best student-friendly travel destinations {country_context} for a budget of {budget}.
    
    User Interests: {', '.join(interests)}
    
    Output Format (Markdown list):
    1. **City, Country**: Why it's good (1 sentence).
    2. ...
    3. ...
    
    Keep it brief and inspiring.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=300
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error getting suggestions: {e}"

def _build_itinerary_prompt(city, days, budget_info, interests, travel_type):
    """
    Constructs the detailed prompt for the AI.
    Separated for readability.
    """
    # Defensive check for currency code
    currency = budget_info.get('currency', 'EUR')
    breakdown_str = "\n".join([f"- {k}: {v} {currency}" for k, v in budget_info['breakdown'].items()])
    
    return f"""
    You are an expert AI Travel Planner for STUDENTS.
    Create a {days}-day itinerary for {city}.
    
    Context:
    - Travelers: {budget_info['travelers']}
    - Total Budget: {budget_info['total']} (Avg {budget_info['daily_avg_per_person']} per person/day)
    - Interests: {', '.join(interests)}
    - Type: {travel_type}
    
    Budget Guidelines:
    {breakdown_str}
    
    Goal: Create a HIGHLY DETAILED itinerary that is strictly reverse-engineered to fit the Total Budget of {budget_info['total']}.
    
    **PRICING & PLANNING STRATEGY (CRITICAL):**
    1. **Plan According to Budget:** Do not just list random places. You MUST choose hotels, transport concepts, and restaurants that mathematically fit into the {budget_info['total']} limit.
    2. **Exact Costing:** Every price you list must be a realistic estimate.
    3. **Transport:** Estimate EXTACT fares for cabs/autos/trains/taxis between stops. (e.g., "Uber from Airport to Hotel             450 INR").
    4. **Accommodation:** Suggest a specific hotel/hostel that fits the daily allowance.
    5. **Food:** Suggest real restaurants with prices that match the budget.
    
    - **Total Budget Optimization:** The sum of all your listed costs MUST be very close to {budget_info['total']}. If your initial plan is too cheap, upgrade the hotel or add a fancy dinner. If too expensive, switch to public transport or cheaper hostels. MAKE IT FIT.
    
    - Break down each day into: Morning, Afternoon, Evening.
    - For EVERY activity, include:
        * Specific timestamps (e.g., 10:00 AM - 12:00 PM).
        * Valid Cost for tickets/entry.
        * Exact transport method between stops with price + duration. Format: "Transport to Place (Duration)" then the price tag.
    
    **FORMATTING RULES:**
    1. **Punctuation:** Do NOT put spaces before commas or inside parentheses. (Correct: "(Taj Express, 3 hours)"; Incorrect: "( Taj Express , 3 hours)").
    2. **Price Tag:** The `<span class='price-tag'>...</span>` MUST be the VERY LAST element in the `<li>`. Put nothing after it.
    3. **Links:** Wrap the *Name* of every Hotel, Restaurant, or Attraction in a clickable link: `<a href='https://www.google.com/search?q=[Name]+[City]' target='_blank' style='color:#a78bfa; text-decoration:none; border-bottom:1px dashed #a78bfa;'>[Name]</a>`.
    
    - Include one 'Hidden Gem' location per day.
    
    - **GIFT GUIDE:** Suggest specific gifts for:
      * 🎁 Relatives (Traditional)
      * 🎒 Friends (Fun/Quirky)
      * 💝 Girlfriend/Partner (Special/Romantic)

    - **FINAL COST SUMMARY:** At the very end of the HTML, add a section showing the calculated sum of ALL costs mentioned above.
      * Format it as a simple table or list.
      * Categories: Accommodation, Transport, Food, Activities, Gifts, Total.
      * **CRITICAL MATH CHECK:** You MUST sum up every single value from the `<span class='price-tag'>...</span>` tags you generated. The "Grand Total" in this summary MUST equal the sum of those tags exactly. Do not make up a total that doesn't match your line items.

    OUTPUT FORMAT: JSON with "html" containing PRE-STYLED HTML using these classes:
    - `.day-card`: Wrapper for each day.
    - `.segment`: Wrapper for Morning/Afternoon/Evening sections.
    - `.price-tag`: Span for costs (Make these visually distinct).
    - `<ul><li>`: For list items.
    
    Example JSON Structure:
    {{
        "html": "<div class='day-card'><h3>Day 1: Arrival...</h3>...</div>",
        "locations": ["Place 1", "Place 2"],
        "total_cost": 1250,
        "currency": "{currency}"
    }}
    """

def generate_itinerary(city, days, budget_info, interests, travel_type):
    """
    Generates a student-friendly itinerary using Groq.
    """
    if not client:
        return json.dumps({
            "html": "<p>Error: Groq API Key not found. Please check your .env file.</p>",
            "locations": [],
            "total_cost": 0
        })

    prompt = _build_itinerary_prompt(city, days, budget_info, interests, travel_type)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful travel assistant. Output strictly valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=6000,
            response_format={"type": "json_object"}
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"Error during AI generation: {e}")
        # Return a valid JSON error structure so the frontend doesn't crash via JSONDecodeError immediately
        return json.dumps({
            "html": f"<div class='error'>Error generating itinerary: {str(e)}</div>",
            "locations": [],
            "total_cost": 0
        })
