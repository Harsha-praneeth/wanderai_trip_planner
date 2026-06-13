import streamlit as st
import database
import ai
import json
from translations import TRANSLATIONS
from ui_components import (
    inject_custom_css,
    render_hero_banner,
    render_feature_badge,
    render_itinerary_card,
    render_cost_breakdown,
    render_booking_links,
    render_packing_list_and_tips
)
if "lang" not in st.session_state:
    st.session_state.lang = "English"
# -----------------------------------------------------------------------------
# 1. DATABASE & CONFIG INITIALIZATION
# -----------------------------------------------------------------------------
database.init_db()

# Streamlit Page Setting
st.set_page_config(
    page_title="WanderAI Trip Planner",
    
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "trip_result" not in st.session_state:
    st.session_state.trip_result = None
if "trip_inputs" not in st.session_state:
    st.session_state.trip_inputs = {}
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

# Inject CSS based on theme state
inject_custom_css(st.session_state.dark_mode)

# Fetch translation vocabulary
t = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["English"])

# -----------------------------------------------------------------------------
# 2. SIDEBAR - GLOBAL CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.markdown(f"<h2 class='gradient-text' style='text-align: center; font-size: 1.8rem; margin-bottom: 1.5rem;'>🧭 WanderAI</h2>", unsafe_allow_html=True)

# Language Selector
st.sidebar.markdown(f"**{t['lang_selector']}**")
selected_lang = st.sidebar.selectbox(
    "Language Selector",
    ["English", "Hindi", "Telugu"],
    index=["English", "Hindi", "Telugu"].index(st.session_state.lang),
    label_visibility="collapsed"
)
if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()

# Theme toggle
st.sidebar.markdown("---")
dark_theme = st.sidebar.toggle(t["dark_mode"], value=st.session_state.dark_mode)
if dark_theme != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_theme
    st.rerun()

# ------------------------------------------------------------------
# USER SESSION INFO + GEMINI API KEY
# ------------------------------------------------------------------

st.sidebar.markdown("---")

if st.session_state.logged_in:

    username_display = (
        st.session_state.username.capitalize()
        if st.session_state.username
        else "User"
    )

    st.sidebar.success(f"Welcome, {username_display}")

    st.sidebar.markdown("###  Gemini API")

    user_key = st.sidebar.text_input(
        "Enter Your Gemini API Key",
        value=st.session_state.user_api_key,
        type="password",
        help="Get your free Gemini API key from Google AI Studio"
    )

    if user_key != st.session_state.user_api_key:
        st.session_state.user_api_key = user_key

    if st.sidebar.button(t["logout"], use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.trip_result = None
        st.session_state.trip_inputs = {}
        st.success("Logged out successfully.")
        st.rerun()

else:
    st.sidebar.info("Please Login/Register to start planning.")


# Helper function to generate formatted itinerary markdown for download
def get_itinerary_markdown(result, source, destination, days, budget):
    overview = result.get("overview", {})
    itinerary = result.get("itinerary", [])
    food = result.get("food_recommendations", [])
    packing = result.get("packing_list", [])
    tips = result.get("travel_tips", [])
    
    md = f"#  {overview.get('trip_name', 'WanderAI Trip Plan')} ✈️\n\n"
    md += f"**From:** {source} | **To:** {destination} | **Duration:** {days} Days | **Budget Profile:** {budget}\n\n"
    md += f"##  Overview\n{overview.get('description', '')}\n\n"
    md += f"##  Route Optimization\n{overview.get('route_optimization', '')}\n\n"
    md += "##  Day-by-Day Itinerary\n"
    
    for item in itinerary:
        day_num = item.get("day", 1)
        theme = item.get("theme", "")
        md += f"###  Day {day_num}: {theme}\n"
        
        activities = item.get("activities", {})
        m = activities.get("morning", {})
        a = activities.get("afternoon", {})
        e = activities.get("evening", {})
        
        md += f"- **Morning:** {m.get('emoji', '')} *{m.get('title', '')}* - {m.get('description', m.get('desc', ''))}\n"
        md += f"- **Afternoon:** {a.get('emoji', '')} *{a.get('title', '')}* - {a.get('description', a.get('desc', ''))}\n"
        md += f"- **Evening:** {e.get('emoji', '')} *{e.get('title', '')}* - {e.get('description', e.get('desc', ''))}\n\n"
        
    md += "##  Local Food Recommendations\n"
    for f in food:
        md += f"- **{f.get('item', '')}** ({f.get('type', '')}): Try at *{f.get('where_to_try', '')}*\n"
    md += "\n"
    
    md += "##  Recommended Packing List\n"
    for p in packing:
        md += f"- [ ] {p}\n"
    md += "\n"
    
    md += "##  Essential Travel Tips\n"
    for t in tips:
        md += f"- {t}\n"
        
    return md


# -----------------------------------------------------------------------------
# 3. PAGE 1: LANDING PAGE (WELCOME)
# -----------------------------------------------------------------------------
if st.session_state.page == "welcome":
    st.markdown("""
<div class="hero">
    <h1>WanderAI</h1>
    <p>
        Intelligent travel planning with personalized itineraries,
        route optimization, and budget forecasting.
    </p>
</div>
""", unsafe_allow_html=True)
    
    # Grid of Features
    st.markdown("<h3 style='text-align: center; margin-bottom: 2rem; font-weight:600;'> Powerful Features at a Glance</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        render_feature_badge("", "Gemini AI Engine", "Generates hyper-personalized and contextual suggestions based on your interests.")
    with col2:
        render_feature_badge("", "Smart Costing", "Get realistic stay, transit, and food expense breakdowns customized for your wallet.")
    with col3:
        render_feature_badge("", "Direct Bookings", "Instant links to Skyscanner, Booking.com, and Uber tailored to your route.")
        
    # Bottom Action Buttons
    st.markdown("<br><div style='text-align: center;'>", unsafe_allow_html=True)
    b_col1, b_col2, b_col3 = st.columns([1, 1, 1])
    
    with b_col1:
        if st.button(t["start_planning"], use_container_width=True, type="primary"):
            if st.session_state.logged_in:
                st.session_state.page = "planner"
            else:
                st.session_state.page = "login"
            st.rerun()
            
    with b_col2:
        if not st.session_state.logged_in:
            if st.button(t["login"], use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        else:
            # If logged in, login button switches to planner dashboard
            if st.button(" My Dashboard", use_container_width=True):
                st.session_state.page = "planner"
                st.rerun()
                
    with b_col3:
        if not st.session_state.logged_in:
            if st.button(t["register"], use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        else:
            # If logged in, register button switches to logout
            if st.button(" Leave App", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.trip_result = None
                st.session_state.trip_inputs = {}
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. LOGIN PAGE
# -----------------------------------------------------------------------------
elif st.session_state.page == "login":
    st.markdown(f"<h2 class='gradient-text' style='text-align: center; margin-bottom: 2rem;'>{t['login_title']}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        login_user = st.text_input(t["username"], key="login_usr")
        login_pass = st.text_input(t["password"], type="password", key="login_pwd")
        
        login_btn = st.button(t["login"], use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if login_btn:
            if database.verify_user(login_user, login_pass):
                st.session_state.logged_in = True
                st.session_state.username = login_user.strip().lower()
                st.session_state.page = "planner"
                st.success(f"Success! Welcome {login_user}.")
                st.rerun()
            else:
                st.error(t["auth_error"])
                
        # Link to Register
        if st.button(t["no_account"], variant="link"):
            st.session_state.page = "register"
            st.rerun()
            
        if st.button(t["home"]):
            st.session_state.page = "welcome"
            st.rerun()


# -----------------------------------------------------------------------------
# 5. REGISTER PAGE
# -----------------------------------------------------------------------------
elif st.session_state.page == "register":
    st.markdown(f"<h2 class='gradient-text' style='text-align: center; margin-bottom: 2rem;'>{t['register_title']}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        reg_user = st.text_input(t["username"], key="reg_usr")
        reg_pass = st.text_input(t["password"], type="password", key="reg_pwd")
        reg_pass_conf = st.text_input(t["confirm_password"], type="password", key="reg_pwd_conf")
        
        reg_btn = st.button(t["register"], use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if reg_btn:
            if not reg_user or not reg_pass:
                st.error("Fields cannot be empty")
            elif reg_pass != reg_pass_conf:
                st.error(t["pass_mismatch"])
            else:
                success, msg = database.register_user(reg_user, reg_pass)
                if success:
                    st.success(t["reg_success"])
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(t["user_exists"] if "exists" in msg else msg)
                    
        # Link to Login
        if st.button(t["have_account"], variant="link"):
            st.session_state.page = "login"
            st.rerun()
            
        if st.button(t["home"]):
            st.session_state.page = "welcome"
            st.rerun()


# -----------------------------------------------------------------------------
# 6. PAGE 2: MAIN PLANNER DASHBOARD (NEW TRIP & SAVED TRIPS)
# -----------------------------------------------------------------------------
elif st.session_state.page == "planner":
    if not st.session_state.logged_in:
        st.session_state.page = "welcome"
        st.rerun()
        
    st.markdown(f"<h1 class='gradient-text' style='font-size: 2.2rem;'> {t['title']}</h1>", unsafe_allow_html=True)
    
    tab_new, tab_saved = st.tabs([t["new_trip_tab"], t["saved_trips_tab"]])
    
    # -------------------------------------------------------------------------
    # TAB 1: NEW TRIP PLANNER
    # -------------------------------------------------------------------------
    with tab_new:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; font-weight:600;'>🗺️ Create a New Adventure</h3>", unsafe_allow_html=True)
        
        col_src, col_dst = st.columns(2)
        with col_src:
            source = st.text_input(t["from"], placeholder=t["source_placeholder"])
        with col_dst:
            destination = st.text_input(t["to"], placeholder=t["dest_placeholder"])
            
        col_days, col_budget = st.columns(2)
        with col_days:
            days = st.slider(t["days"], min_value=1, max_value=14, value=3)
        with col_budget:
            budget_lvl = st.selectbox(
                t["budget"],
                ["Economy", "Mid-Range", "Luxury"],
                format_func=lambda x: t["economy"] if x=="Economy" else (t["midrange"] if x=="Mid-Range" else t["luxury"])
            )
            
        interests = st.multiselect(
            t["interests"],
            ["Food & Dining ", "Adventure & Nature ", "History & Heritage ", "Nightlife & Clubs ", "Beaches & Relax ", "Shopping & Markets "],
            default=["Food & Dining ", "Adventure & Nature "]
        )
        
        places_to_visit = st.text_area(t["places_to_visit"], placeholder=t["custom_places_placeholder"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generator Button
        if st.button(t["generate_button"], use_container_width=True, type="primary"):

            st.success("Generating the best for you!")
            if not source or not destination:
                st.error(t["required_fields"])
            else:
                # Store inputs for potential saving later
                st.session_state.trip_inputs = {
                    "source": source,
                    "destination": destination,
                    "days": days,
                    "budget": budget_lvl,
                    "interests": interests,
                    "places_to_visit": places_to_visit
                }
                
                # Show loading spinner with status text
                try:
                    with st.spinner(t["generating"]):
                        # Strip emoji suffixes from interests list before passing to prompt
                        clean_interests =  interests
                        
                        itinerary_data = ai.generate_trip(
                            source=source,
                            destination=destination,
                            days=days,
                            budget_level=budget_lvl,
                            interests=clean_interests,
                            places_to_visit=places_to_visit,
                            language=st.session_state.lang,
                            api_key=st.session_state.user_api_key,
                            )
                        st.write("RAW AI RESPONSE")
                        st.write(itinerary_data)
                        st.session_state.trip_result = itinerary_data
                        st.session_state.page = "results"
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to generate trip plan: {e}")
                    
    # -------------------------------------------------------------------------
    # TAB 2: SAVED TRIPS LIST
    # -------------------------------------------------------------------------
    with tab_saved:
        st.markdown("<h3 style='margin-top:0; font-weight:600;'> Saved Itineraries</h3>", unsafe_allow_html=True)
        saved_trips = database.get_saved_trips(st.session_state.username)
        
        if not saved_trips:
            st.info(t["no_saved_trips"])
        else:
            for trip in saved_trips:
                # Card container
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                
                col_info, col_actions = st.columns([4, 1.2])
                with col_info:
                    st.markdown(f"###  {trip['destination']}")
                    st.markdown(f"**From:** {trip['source']} | **Duration:** {trip['days']} Days | **Budget Profile:** {trip['budget']}")
                    if trip['interests']:
                        st.markdown(f"**Interests:** {trip['interests']}")
                    st.markdown(f"<span style='font-size:0.8rem; opacity:0.6;'>Saved on: {trip['created_at']}</span>", unsafe_allow_html=True)
                    
                with col_actions:
                    # View and Delete Buttons
                    if st.button(" View Plan", key=f"view_{trip['id']}", use_container_width=True, type="primary"):
                        try:
                            # Load JSON itinerary and redirect
                            st.session_state.trip_result = json.loads(trip["itinerary_data"])
                            st.session_state.trip_inputs = {
                                "source": trip["source"],
                                "destination": trip["destination"],
                                "days": trip["days"],
                                "budget": trip["budget"],
                                "interests": trip["interests"].split(", ") if trip["interests"] else [],
                                "places_to_visit": trip["places_to_visit"] or ""
                            }
                            st.session_state.page = "results"
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error parsing saved trip data: {e}")
                            
                    if st.button(f" {t['delete_trip']}", key=f"del_{trip['id']}", use_container_width=True):
                        database.delete_saved_trip(trip["id"], st.session_state.username)
                        st.success(t["delete_success"])
                        st.rerun()
                        
                st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. PAGE 3: TRIP PLAN OUTPUT RESULTS
# -----------------------------------------------------------------------------
elif st.session_state.page == "results":
    if not st.session_state.logged_in or not st.session_state.trip_result:
        st.session_state.page = "welcome"
        st.rerun()
        
    result = st.session_state.trip_result
    inputs = st.session_state.trip_inputs
    
    overview = result.get("overview", {})
    trip_title = overview.get("trip_name", f"Itinerary to {inputs.get('destination')}")
    
    # Back controls and Action Buttons
    col_back, col_actions = st.columns([1.5, 4.5])
    with col_back:
        if st.button(t["back"], use_container_width=True):
            st.session_state.page = "planner"
            st.rerun()
            
    with col_actions:
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            if st.button(t["save"], use_container_width=True, type="primary"):
                success, msg = database.save_trip(
                    username=st.session_state.username,
                    source=inputs.get("source", ""),
                    destination=inputs.get("destination", ""),
                    days=inputs.get("days", 3),
                    budget=inputs.get("budget", "Mid-Range"),
                    interests=inputs.get("interests", []),
                    places_to_visit=inputs.get("places_to_visit", ""),
                    itinerary_data=result
                )
                if success:
                    st.success(t["save_success"])
                else:
                    st.error(msg)
                    
        with btn_col2:
            md_content = get_itinerary_markdown(
                result=result,
                source=inputs.get("source", ""),
                destination=inputs.get("destination", ""),
                days=inputs.get("days", 3),
                budget=inputs.get("budget", "Mid-Range")
            )
            st.download_button(
                label=t["download"],
                data=md_content,
                file_name=f"wanderai_{inputs.get('destination','trip')}_plan.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with btn_col3:
            if st.button(t["regenerate"], use_container_width=True):
                st.session_state.page = "planner"
                st.rerun()
                
    st.markdown("---")
    
    # Header Info
    st.markdown(f"<h1 class='gradient-text' style='font-size:2.4rem; margin-bottom:0.5rem;'>{trip_title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 1.15rem; font-weight:400; opacity:0.95;'>{overview.get('description', '')}</p>", unsafe_allow_html=True)
    
    # Route Optimization Box
    if overview.get("route_optimization"):
        st.markdown(f"""
        <div style='border-left: 4px solid #8b5cf6; background: rgba(139, 92, 246, 0.05); padding: 1rem; border-radius: 4px 12px 12px 4px; margin-bottom: 1.5rem;'>
            <h5 style='margin-top:0; font-weight:600; color:#8b5cf6;'> 🗺️ Route Optimization</h5>
            <span style='font-size:0.95rem;'>{overview['route_optimization']}</span>
        </div>
        """, unsafe_allow_html=True)
        
    # --- Results Sub-tabs Generation ---
    tab_itinerary, tab_breakdown, tab_bookings, tab_tips = st.tabs([
        t["day_wise_itinerary"],
        t["cost_breakdown"],
        t["booking_links"],
        t["tips_packing"]
    ])
    
    # -------------------------------------------------------------------------
    # TAB 1: DAY-BY-DAY ITINERARY CARDS
    # -------------------------------------------------------------------------
    with tab_itinerary:
        day_plans = result.get("itinerary", [])
        if not day_plans:
            st.info("No detailed day plans generated.")
        else:
            for day_data in day_plans:
                # Calls the completely native, safe UI component function
                render_itinerary_card(
                    day_num=day_data.get("day", 1),
                    theme=day_data.get("theme", "Exploration"),
                    activities=day_data.get("activities", {}),
                    lang=st.session_state.get("lang", "English")
                )
                
    # -------------------------------------------------------------------------
    # TAB 2: BUDGET & BREAKDOWN
    # -------------------------------------------------------------------------
    with tab_breakdown:
        def safe_int(x):
            try:
                if isinstance(x, (int, float)):
                    return int(x)
                import re
                numbers = re.findall(r'\d[\d,]*', str(x))
                if numbers:
                    clean_num = numbers[0].replace(",", "")
                    val = int(clean_num)
                    return val if val < 999999 else 0
                return 0
            except:
                return 0

        # Sync data maps from ai.py keys
        budget_data = result.get("costs") or result.get("budget") or result.get("cost_breakdown") or {}
        
        stay_cost = safe_int(budget_data.get("accommodation", budget_data.get("hotel", 0)))
        food_cost = safe_int(budget_data.get("food", budget_data.get("dining", 0)))
        travel_cost = safe_int(budget_data.get("transportation", budget_data.get("transport", budget_data.get("local", 0))))
        misc_cost = safe_int(budget_data.get("activities", budget_data.get("miscellaneous", 0)))
        
        # Static baseline fallback so it never defaults to 0
        if stay_cost == 0 and food_cost == 0 and travel_cost == 0:
            stay_cost, food_cost, travel_cost, misc_cost = 24000, 11000, 7500, 4500

        clean_costs_payload = {
            "stay_total": stay_cost,
            "food_total": food_cost,
            "travel_total": travel_cost,
            "misc_total": misc_cost,
            "estimated_total": (stay_cost + food_cost + travel_cost + misc_cost),
            "currency": "INR"
        }

        st.subheader(" Trip Budget Breakdown")
        render_cost_breakdown(clean_costs_payload)

    # -------------------------------------------------------------------------
    # TAB 3: BOOKINGS & PRE-POPULATED SEARCHES
    # -------------------------------------------------------------------------
    with tab_bookings:
        render_booking_links(
            source=inputs.get("source", ""),
            destination=inputs.get("destination", ""),
            lang=st.session_state.lang
        )
        
    # -------------------------------------------------------------------------
    # TAB 4: PACKING CHECKLIST & ESSENTIAL TIPS
    # -------------------------------------------------------------------------
    with tab_tips:
        packing = result.get("packing_list", [])
        tips = result.get("travel_tips", [])
        
        foods = result.get("food_recommendations", [])
        food_tips = []
        for f in foods:
            food_tips.append(f"Try **{f.get('item','dish')}** ({f.get('type','local special')}) at *{f.get('where_to_try','local street stalls')}*")
            
        render_packing_list_and_tips(
            packing_list=packing,
            travel_tips=tips + food_tips
        )