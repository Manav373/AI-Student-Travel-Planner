import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

# Local imports
from src.budget import calculate_budget_split
from src.ai import generate_itinerary
from src.maps import create_map
from src.countries import COUNTRIES
from src.currency_utils import get_currency_for_country, COUNTRY_CURRENCY_MAP

# --- Configuration & Setup ---
def configure_page():
    """""Configures the Streamlit page settings.""""" 
    st.set_page_config(
        page_title="AI Travel Planner",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_custom_styles(css_file):
    """""Loads custom CSS styles from a file."""""
    try:
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Note: {css_file} not found. Using default styles.")

# --- Main Application Logic ---
def main():
    configure_page()
    load_custom_styles("src/styles.css")

    # Sidebar: User Inputs
    with st.sidebar:
        st.header("✈️ Plan Your Trip")
        
        # Smart defaults for India if available, else just the first one
        default_country_idx = COUNTRIES.index("India") if "India" in COUNTRIES else 0
        country = st.selectbox("Select Country", COUNTRIES, index=default_country_idx)
        
        city = st.text_input("City (Optional)", placeholder="e.g. Mumbai, Goa")
        
        # Currency Intelligence: Auto-select based on country, but allow override
        suggested_currency = get_currency_for_country(country)
        all_currencies = sorted(list(set(COUNTRY_CURRENCY_MAP.values())))
        
        currency_idx = 0
        if suggested_currency in all_currencies:
            currency_idx = all_currencies.index(suggested_currency)
            
        currency = st.selectbox("Currency", all_currencies, index=currency_idx)
        
        # Budget & Duration
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Budget", min_value=100, step=1000, help="Total trip budget")
        with col2:
            days = st.number_input("Days", min_value=1, max_value=30, value=5)
            
        travelers = st.slider("Travelers", 1, 10, 2)
        
        # Preferences
        available_interests = ["Culture", "Food", "Adventure", "Relaxation", "Nightlife", "Shopping"]
        interests = st.multiselect("Interests", available_interests, default=["Food", "Adventure"])
        
        travel_type = st.radio("Travel Style", ["Budget", "Standard", "Luxury"], index=0)
        
        generate_btn = st.button("✨ Generate Itinerary")

    # Main Content Area
    st.title("🌍 AI Student Travel Planner")
    target_place = city if city else country
    st.markdown(f"### Planning your dream trip to **{target_place}**")

    # Session State Initialization
    if "itinerary_data" not in st.session_state:
        st.session_state.itinerary_data = None
    if "map_obj" not in st.session_state:
        st.session_state.map_obj = None
    if "budget_data" not in st.session_state:
        st.session_state.budget_data = None

    # Processing the Request
    if generate_btn:
        if not interests:
            st.error("Please select at least one interest!")
            return

        with st.spinner("🤖 AI is contacting hostels, checking flights, and planning your detailed trip..."):
            
            # Step 1: Number crunching for the budget
            effective_budget = budget
            if budget < 1000:
                st.warning("⚠️ Your budget is quite low. We have calculated the itinerary based on a minimum viable budget of 1000. Please consider increasing your budget!")
                effective_budget = 1000

            budget_data = calculate_budget_split(float(effective_budget), int(days), interests, int(travelers), currency)
            
            # Step 2: The heavy lifting (AI Generation)
            try:
                ai_response_json = generate_itinerary(target_place, int(days), budget_data, interests, travel_type)
                
                # Parse the JSON response
                parsed_data = json.loads(ai_response_json)
                
                # Update session state with new data
                st.session_state.itinerary_data = parsed_data
                st.session_state.budget_data = budget_data
            
                # Step 3: Generate the map visualization
                # We pull locations from the AI response to plot them
                locations = parsed_data.get("locations", [])
                st.session_state.map_obj = create_map(target_place, locations)
                
            except json.JSONDecodeError:
                st.error("The AI generated an invalid response. Please try again.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    # Result Display
    if st.session_state.itinerary_data:
        display_results(st.session_state.itinerary_data, st.session_state.map_obj, st.session_state.budget_data, currency)

def display_results(data, map_obj, budget_data, currency):
    """Helper to render the tabs and content"""
    
    tab1, tab2, tab3 = st.tabs([" Itinerary", "🗺️ Map", "💰 Budget"])
    
    with tab1:
        st.markdown(f"### 💰 Estimated Trip Cost: **{data.get('total_cost', 'N/A')} {currency}**")
        st.markdown(data.get("html", ""), unsafe_allow_html=True)
        
    with tab2:
        if map_obj:
            # Render Folium map in Streamlit
            # Using components.html is a workaround for some folium display issues in older streamlit versions
            map_html = map_obj.get_root().render()
            components.html(map_html, width=800, height=500)
        else:
            st.info("Map data unavailable.")
            
    with tab3:
        st.subheader("Projected Budget Breakdown")
        if budget_data:
            df = pd.DataFrame([budget_data['breakdown']])
            df_melted = df.melt(var_name="Category", value_name="Amount")
            st.bar_chart(df_melted.set_index("Category"))
        


if __name__ == "__main__":
    main()
