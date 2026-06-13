import streamlit as st
import urllib.parse

def inject_custom_css(dark_mode=True):
    """
    Injects custom Google Fonts and custom CSS styles based on light/dark mode.
    Provides glassmorphism cards, premium text gradients, and sleek button animations.
    """
    # Color tokens based on dark/light mode
    if dark_mode:
        bg_color = "#0e1117"
        text_color = "#f3f4f6"
        sub_text_color = "#9ca3af"
        card_bg = "rgba(17, 24, 39, 0.7)"
        card_border = "rgba(255, 255, 255, 0.08)"
        card_shadow = "rgba(0, 0, 0, 0.37)"
        accent_color = "#ece8f7"
        accent_gradient = "linear-gradient(135deg, #6366f1, #a855f7)"
        metric_bg = "rgba(31, 41, 55, 0.6)"
        timeline_line = "rgba(99, 102, 241, 0.3)"
    else:
        bg_color = "#f9fafb"
        text_color = "#1f2937"
        sub_text_color = "#4b5563"
        card_bg = "rgba(255, 255, 255, 0.85)"
        card_border = "rgba(0, 0, 0, 0.06)"
        card_shadow = "rgba(0, 0, 0, 0.06)"
        accent_color = "#000000"
        accent_gradient = "linear-gradient(135deg, #4f46e5, #7c3aed)"
        metric_bg = "rgba(243, 244, 246, 0.8)"
        timeline_line = "rgba(79, 70, 229, 0.3)"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Outfit', sans-serif;
    }}
    
    /* Hide default streamlit decoration line */
    header {{
        background-color: transparent !important;
    }}
    
    /* Header Gradient Text */
    .gradient-text {{
        background: {accent_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
    }}
    
    /* Landing Banner */
    
    .hero-banner {{ 
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 4rem;
    text-align: center;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }}
        border-radius: 24px;
        padding: 3.5rem 2.5rem;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.25);
        text-align: center;
        position: relative;
        overflow: hidden;
    
    
    .hero-banner::before {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        pointer-events: none;
    }}
    
    .hero-title {{
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        line-height: 1.2;
    }}
    
    .hero-tagline {{
        font-size: 1.3rem;
        font-weight: 500;
        opacity: 0.95;
        margin-bottom: 1.5rem;
    }}
    
    .hero-desc {{
        font-size: 1.05rem;
        max-width: 700px;
        margin: 0 auto;
        opacity: 0.85;
        line-height: 1.6;
    }}
    
    /* Styled Glassmorphism Cards */
    .premium-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px {card_shadow};
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .premium-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 40px {card_shadow};
    }}
    
    /* Day Itinerary Headers */
    .day-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid {card_border};
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem;
    }}
    
    .day-badge {{
        background: {accent_gradient};
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
    }}
    
    .day-theme {{
        font-size: 1.25rem;
        font-weight: 600;
        color: {text_color};
    }}
    
    /* Timeline design */
    .timeline-item {{
        position: relative;
        padding-left: 2.2rem;
        margin-bottom: 1.5rem;
    }}
    
    .timeline-item:last-child {{
        margin-bottom: 0.5rem;
    }}
    
    .timeline-item::before {{
        content: "";
        position: absolute;
        left: 0.75rem;
        top: 1.8rem;
        bottom: -1.8rem;
        width: 2px;
        background: {timeline_line};
    }}
    
    .timeline-item:last-child::before {{
        display: none;
    }}
    
    .timeline-icon {{
        position: absolute;
        left: 0;
        top: 0;
        width: 1.6rem;
        height: 1.6rem;
        background: {card_bg};
        border: 2px solid {accent_color};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        z-index: 2;
    }}
    
    .timeline-content {{
        background: rgba(124, 58, 237, 0.03);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        border: 1px dashed {card_border};
    }}
    
    .timeline-title {{
        font-weight: 600;
        font-size: 1.1rem;
        color: {text_color};
        margin-bottom: 0.25rem;
    }}
    
    .timeline-desc {{
        font-size: 0.95rem;
        color: {sub_text_color};
        line-height: 1.5;
    }}
    
    /* Custom Metric Cards */
    .metric-panel {{
        background: {metric_bg};
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        border: 1px solid {card_border};
        margin-bottom: 1rem;
    }}
    
    .metric-val {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {accent_color};
    }}
    
    .metric-lbl {{
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {sub_text_color};
        margin-top: 0.25rem;
    }}
    
    /* Feature Badge Grid on Home Page */
    .feature-badge {{
        display: flex;
        align-items: center;
        padding: 1rem;
        border-radius: 16px;
        background: {card_bg};
        border: 1px solid {card_border};
        margin-bottom: 1rem;
    }}
    
    .feature-icon {{
        font-size: 2rem;
        margin-right: 1rem;
        background: rgba(99, 102, 241, 0.1);
        width: 3.5rem;
        height: 3.5rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .feature-title {{
        font-weight: 600;
        font-size: 1.1rem;
        color: {text_color};
    }}
    
    .feature-desc {{
        font-size: 0.85rem;
        color: {sub_text_color};
    }}
    
    /* Button Links */
    .booking-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        font-weight: 600;
        text-decoration: none;
        margin-bottom: 1rem;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid {card_border};
    }}
    
    .booking-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        color: white !important;
    }}
    
    .flight-btn {{
        background: #00b4d8;
        color: white !important;
    }}
    .hotel-btn {{
        background: #003580;
        color: white !important;
    }}
    .cab-btn {{
        background: #000000;
        color: white !important;
    }}
    
    /* Dynamic Cost Bar */
    .cost-bar-container {{
        width: 100%;
        background-color: {card_border};
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        display: flex;
        margin: 1.5rem 0;
    }}
    
    .cost-segment {{
        height: 100%;
        transition: width 0.5s ease;
    }}
    
    .stay-seg {{ background-color: #6366f1; }}
    .food-seg {{ background-color: #f59e0b; }}
    .travel-seg {{ background-color: #10b981; }}
    .misc-seg {{ background-color: #ec4899; }}
    
    .legend-item {{
        display: inline-flex;
        align-items: center;
        margin-right: 1.5rem;
        font-size: 0.9rem;
        color: {text_color};
    }}
    
    .legend-color {{
        width: 12px;
        height: 12px;
        border-radius: 3px;
        margin-right: 0.5rem;
    }}
    
    /* Checklist items */
    .checklist-item {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
        color: {text_color};
    }}
    
    .checklist-bullet {{
        color: {accent_color};
        margin-right: 0.75rem;
        font-weight: bold;
    }}
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_hero_banner(title, tagline, desc):
    """Renders the top landing page hero banner."""
    html = f"""
    <div class="hero-banner">
        <div class="hero-title">{title}</div>
        <div class="hero-tagline">{tagline}</div>
        <div class="hero-desc">{desc}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_feature_badge(emoji, title, desc):
    """Renders a feature description box (used on home screen)."""
    html = f"""
    <div class="feature-badge">
        <div class="feature-icon">{emoji}</div>
        <div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_itinerary_card(day_num, theme, activities, lang="English"):
    """
    Renders a single day itinerary card using 100% native Streamlit components.
    No HTML divs, completely bulletproof.
    """
    day_lbl = {
        "English": f" Day {day_num}",
        "Hindi": f" दिन {day_num}",
        "Telugu": f" రోజు {day_num}"
    }.get(lang, f" Day {day_num}")
    
    # Extract times blocks safely
    morning = activities.get("morning", {})
    afternoon = activities.get("afternoon", {})
    evening = activities.get("evening", {})
    
    # Extract values cleanly
    m_title = morning.get("title", "Morning Plan")
    m_desc = morning.get("description", morning.get("desc", ""))
    m_emoji = morning.get("emoji", "")

    a_title = afternoon.get("title", "Afternoon Plan")
    a_desc = afternoon.get("description", afternoon.get("desc", ""))
    a_emoji = afternoon.get("emoji", "")

    e_title = evening.get("title", "Evening Plan")
    e_desc = evening.get("description", evening.get("desc", ""))
    e_emoji = evening.get("emoji", "")

    # Native Streamlit Container acting as our card
    with st.container(border=True):
        # Header Row
        col_lbl, col_theme = st.columns([1, 3])
        with col_lbl:
            st.markdown(f"### **{day_lbl}**")
        with col_theme:
            st.markdown(f"### *{theme}*")
            
        st.write("---")
        
        # Morning Timeline Section
        col_icon_m, col_content_m = st.columns([0.5, 9.5])
        with col_icon_m:
            st.markdown(f"### {m_emoji}")
        with col_content_m:
            st.markdown(f"**{m_title}**")
            st.caption(m_desc)
            
        st.write("") # Padding Spacer
        
        # Afternoon Timeline Section
        col_icon_a, col_content_a = st.columns([0.5, 9.5])
        with col_icon_a:
            st.markdown(f"### {a_emoji}")
        with col_content_a:
            st.markdown(f"**{a_title}**")
            st.caption(a_desc)
            
        st.write("") # Padding Spacer
        
        # Evening Timeline Section
        col_icon_e, col_content_e = st.columns([0.5, 9.5])
        with col_icon_e:
            st.markdown(f"### {e_emoji}")
        with col_content_e:
            st.markdown(f"**{e_title}**")
            st.caption(e_desc)

    

    

def render_cost_breakdown(costs):
    """
    Renders metrics and an custom-colored segmented percentage bar for expenses.
    """
    stay_val = costs.get("stay_total", costs.get("stay_cost_per_day", 0))
    food_val = costs.get("food_total", costs.get("food_cost_per_day", 0))
    travel_val = costs.get("travel_total", costs.get("travel_cost_per_day", 0))
    misc_val = costs.get("misc_total", 0)
    total_val = costs.get("estimated_total", (stay_val + food_val + travel_val + misc_val))
    currency = costs.get("currency", "INR")
    curr_symbol = "₹" if currency == "INR" else f"{currency} "

    # Columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-panel"><div class="metric-val">{curr_symbol}{stay_val:,}</div><div class="metric-lbl"> Accommodation</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-panel"><div class="metric-val">{curr_symbol}{food_val:,}</div><div class="metric-lbl"> Food & Dining</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-panel"><div class="metric-val">{curr_symbol}{travel_val:,}</div><div class="metric-lbl"> Transit & Cabs</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-panel"><div class="metric-val">{curr_symbol}{misc_val:,}</div><div class="metric-lbl"> Sightseeing/Misc</div></div>', unsafe_allow_html=True)

    # Segmented progress bar
    total_val_safe = max(1, total_val)
    stay_pct = (stay_val / total_val_safe) * 100
    food_pct = (food_val / total_val_safe) * 100
    travel_pct = (travel_val / total_val_safe) * 100
    misc_pct = (misc_val / total_val_safe) * 100

    html_bar = f"""
    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; font-weight:600;">Expense Distribution</h4>
    <div class="cost-bar-container">
        <div class="cost-segment stay-seg" style="width: {stay_pct}%" title="Stay: {stay_pct:.1f}%"></div>
        <div class="cost-segment food-seg" style="width: {food_pct}%" title="Food: {food_pct:.1f}%"></div>
        <div class="cost-segment travel-seg" style="width: {travel_pct}%" title="Travel: {travel_pct:.1f}%"></div>
        <div class="cost-segment misc-seg" style="width: {misc_pct}%" title="Misc: {misc_pct:.1f}%"></div>
    </div>
    <div style="margin-bottom: 2rem;">
        <span class="legend-item"><span class="legend-color stay-seg"></span>Stay ({stay_pct:.0f}%)</span>
        <span class="legend-item"><span class="legend-color food-seg"></span>Food ({food_pct:.0f}%)</span>
        <span class="legend-item"><span class="legend-color travel-seg"></span>Transit ({travel_pct:.0f}%)</span>
        <span class="legend-item"><span class="legend-color misc-seg"></span>Misc ({misc_pct:.0f}%)</span>
    </div>
    
    <div style="border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem; text-align: center; background: rgba(99, 102, 241, 0.05); margin-bottom: 1.5rem;">
        <span style="font-size: 1.1rem; font-weight: 500;">Estimated Total Budget: </span>
        <span style="font-size: 1.6rem; font-weight: 800;" class="gradient-text">{curr_symbol}{total_val:,}</span>
    </div>
    """
    st.markdown(html_bar, unsafe_allow_html=True)

def render_booking_links(source, destination, lang="English"):
    """
    Renders Skyscanner, Booking.com and Uber pre-populated booking buttons in columns.
    """
    # URL Encode source and destination
    src_encoded = urllib.parse.quote(source)
    dst_encoded = urllib.parse.quote(destination)

    # Google Flights search url
    flights_url = f"https://www.google.com/travel/flights?q=Flights%20from%20{src_encoded}%20to%20{dst_encoded}"
    
    # Booking.com search url
    hotels_url = f"https://www.booking.com/searchresults.html?ss={dst_encoded}"
    
    # Uber link
    cabs_url = "https://m.uber.com/ul/?action=setPickup&pickup=my_location"

    labels = {
        "English": {
            "flights": " Search Flights (Google Flights)",
            "hotels": " Book Stays (Booking.com)",
            "cabs": " Hire Uber / Transit"
        },
        "Hindi": {
            "flights": " उड़ानें खोजें (Google Flights)",
            "hotels": " होटल बुक करें (Booking.com)",
            "cabs": " उबर / कैब बुक करें"
        },
        "Telugu": {
            "flights": " విమానాలు వెతకండి (Google Flights)",
            "hotels": "హోటల్స్ బుక్ చేయండి (Booking.com)",
            "cabs": " క్యాబ్ / ఉబెర్ బుక్ చేయండి"
        }
    }.get(lang, {
        "flights": " Search Flights (Google Flights)",
        "hotels": " Book Stays (Booking.com)",
        "cabs": " Hire Uber / Transit"
    })

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<a href="{flights_url}" target="_blank" class="booking-btn flight-btn">{labels["flights"]}</a>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<a href="{hotels_url}" target="_blank" class="booking-btn hotel-btn">{labels["hotels"]}</a>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<a href="{cabs_url}" target="_blank" class="booking-btn cab-btn">{labels["cabs"]}</a>', unsafe_allow_html=True)

def render_packing_list_and_tips(packing_list, travel_tips):
    """
    Renders packing list and tips in two columns with beautiful styles.
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0; margin-bottom: 1rem; font-weight:600;"> Recommended Packing</h3>', unsafe_allow_html=True)
        for item in packing_list:
            html_item = f"""
            <div class="checklist-item">
                <span class="checklist-bullet">✓</span>
                <div>{item}</div>
            </div>
            """
            st.markdown(html_item, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0; margin-bottom: 1rem; font-weight:600;"> Essential Travel Tips</h3>', unsafe_allow_html=True)
        for tip in travel_tips:
            html_tip = f"""
            <div class="checklist-item">
                <span class="checklist-bullet">★</span>
                <div>{tip}</div>
            </div>
            """
            st.markdown(html_tip, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
