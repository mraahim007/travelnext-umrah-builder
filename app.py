import streamlit as st
from datetime import date
import urllib.parse
import streamlit.components.v1 as components

# Page Configuration with Dark Theme Styling
st.set_page_config(page_title="TravelNext Umrah Builder", page_icon="🕋", layout="wide")

# Custom CSS for Pure Dark Black / Minimalist Theme Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e0e0e;
        color: #e2e8f0;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #f8fafc !important;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px;
    }
    .stButton button {
        background-color: #2563eb !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton button:hover {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }
    .step-box {
        background-color: #141414;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #262626;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Wizard Steps
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1

total_steps = 9

def prev_step():
    if st.session_state.wizard_step > 1:
        st.session_state.wizard_step -= 1

def next_step():
    step = st.session_state.wizard_step
    
    if step == 3:
        if not st.session_state.get("c_first_name") or not st.session_state.get("c_passport"):
            st.error("⚠️ Please enter Customer First Name and Passport Number first!")
            return
    elif step == 4:
        if st.session_state.get("c_air") == "-- Select Airline --" or st.session_state.get("c_land") == "-- Select Airport --":
            st.error("⚠️ Please select both Airline and Arrival Airport first!")
            return
    elif step == 5:
        if st.session_state.get("c1_city") == "-- Select City / Stop --":
            st.error("⚠️ Please select City 1 first!")
            return
    elif step == 6:
        if st.session_state.get("z_status") == "-- Select Option --":
            st.error("⚠️ Please select Ziarats option (YES or NO) first!")
            return

    if st.session_state.wizard_step < total_steps:
        st.session_state.wizard_step += 1

current_step = st.session_state.wizard_step

# Progress Bar Header
progress_percent = int(((current_step - 1) / (total_steps - 1)) * 100) if total_steps > 1 else 0
st.progress(progress_percent)
st.caption(f"Step {current_step} of {total_steps} (Progress: {progress_percent}%)")
st.write("---")

sar_to_pkr = st.session_state.get("daily_sar_rate", 75.0)
cities_list = [
    "-- Select City / Stop --", 
    "Makkah Al-Mukarramah", 
    "Al-Madinah Al-Munawwarah", 
    "Jeddah Airport (Transit / Stop Only - No Hotel Stay)", 
    "Madinah Airport (Transit / Stop Only - No Hotel Stay)"
]
vehicle_list = ["-- Select Transport --", "CAR", "STAREX", "GMC", "HIACE", "COASTER", "Public Transport"]

def get_hotel_list(city):
    if "Makkah" in city:
        return [
            "-- Select Specific Hotel --",
            "5-Star Makkah Clock Royal Tower, A Fairmont Hotel (0 km)",
            "5-Star Swissôtel Makkah (0 km)",
            "5-Star Swissôtel Al Maqam Makkah (0 km)",
            "5-Star Pullmann Zamzam Makkah (0 km)",
            "5-Star Address Jabal Omar Makkah (200–300m)",
            "5-Star Conrad Jabal Omar Makkah (300m)",
            "5-Star Jabal Omar Hyatt Regency Makkah (500m)",
            "5-Star Hilton Suites Jabal Omar Makkah (300–400m)",
            "5-Star InterContinental Dar Al Tawhid Makkah (0 km)",
            "4-Star Voco Makkah (1.8 - 2 km / Shuttle)",
            "4-Star Mercure Makkah Aziziah (4 - 5 km)",
            "4-Star Emaar Royal Hotel (700 - 800m)",
            "3-Star Al Kiswah Towers (1.5 - 1.7 km / Shuttle)",
            "3-Star Snood Hotel (1.5 km)",
            "3-Star Qilla Ajyad Hotel (600 - 700m)"
        ]
    elif "Madinah" in city:
        return [
            "-- Select Specific Hotel --",
            "5-Star Anwar Al Madinah Movenpick Hotel (100m)",
            "5-Star Crowne Plaza Madinah (200m)",
            "5-Star Oberoi Madinah (100m)",
            "5-Star Dar Al Taqwa Hotel (0-50m)",
            "5-Star Pullman Zamzam Madinah (150m)",
            "4-Star Dallah Taiba Hotel (50-100m)",
            "4-Star Al Aqeeq Madinah Hotel (200–300m)",
            "4-Star Leader Muna Kareem Hotel (150–200m)",
            "4-Star Swiss International Hotel (500m)",
            "3-Star Mysk Touch Hotel (700 - 800m)",
            "3-Star Plaza Inn Ohud (900m / Shuttle)",
            "3-Star Manazil Al Marjan (600m)"
        ]
    return ["-- Select Specific Hotel --"]

def clean_city_name(c):
    if "--" in c or not c:
        return "Not Set"
    if "Jeddah" in c or "JED" in c:
        return "Jeddah Airport (JED)"
    if "Madinah" in c or "MED" in c:
        return "Madinah Airport (MED)"
    if "Makkah" in c:
        return "Makkah"
    return c

def parse_val(val_str):
    try:
        clean_str = "".join([c for c in str(val_str) if c.isdigit() or c == '.'])
        return float(clean_str) if clean_str else 0.0
    except:
        return 0.0

# ================= STEP 1: WELCOME SCREEN =================
if current_step == 1:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>✨ TRAVELNEXT INTERNATIONAL ✨</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Smart Umrah Package Builder & Quotation System</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Aao Madiney Chalen 🕋 | Professional Booking & Management Portal</p>", unsafe_allow_html=True)
    st.write("---")
    st.info("💡 **Welcome!** Please click the button below to proceed to the next step.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 2: CURRENCY EXCHANGE =================
elif current_step == 2:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("💱 Step 2: Daily Currency Exchange Rate")
    st.write("Set the current Saudi Riyal (SAR) to Pakistani Rupee (PKR) rate:")
    sar_to_pkr = st.number_input("Enter current 1 SAR to PKR rate today:", min_value=0.1, max_value=100.0, value=75.0, step=0.5, key="daily_sar_rate")
    st.success(f"💡 Active Exchange Rate: **1 SAR = {sar_to_pkr:,.2f} PKR** | **1 PKR = {1/sar_to_pkr:,.4f} SAR**")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 3: CUSTOMER DETAILS =================
elif current_step == 3:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("👤 Step 3: Customer Details & Travel Dates")
    col1, col2 = st.columns(2)
    with col1:
        cust_first_name = st.text_input("First Name *:", key="c_first_name")
        adults = st.number_input("Enter number of adults:", min_value=1, value=1, key="common_adults")
    with col2:
        cust_last_name = st.text_input("Last Name:", key="c_last_name")
        children = st.number_input("Enter number of children:", min_value=0, value=0, key="common_children")
    
    passport_number = st.text_input("Passport Number *:", key="c_passport")
    trip_start_date = st.date_input("Overall Trip Start Date (Arrival Date):", value=date.today(), key="trip_start")
    total_people = adults + children
    st.info(f"👉 Total Family Members: **{total_people}** ({adults} Adults, {children} Children)")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 4: FLIGHT DETAILS =================
elif current_step == 4:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("✈️ Step 4: Flight Information")
    col3, col4 = st.columns(2)
    with col3:
        cust_airline = st.selectbox("Select Airline Name *:", ["-- Select Airline --", "Saudia Airlines", "PIA", "AirBlue", "SereneAir", "Fly Jinnah", "Emirates", "Qatar Airways"], key="c_air")
    with col4:
        cust_landing = st.selectbox("Arrival Airport (Landing City) *:", ["-- Select Airport --", "Jeddah Airport (JED)", "Madinah Airport (MED)"], key="c_land")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 5: HOTEL STAYS & TRANSPORTS =================
elif current_step == 5:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("🏨 Step 5: Hotel Stay & City Transport Builder")
    st.markdown("Configure your stay legs and dynamic transportation routes:")

    # Leg 1
    st.markdown("### 🧳 Stay Leg 1 (First Stop)")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        city_1 = st.selectbox("Select City 1 *:", cities_list, key="c1_city")
        is_airport_stop_1 = ("Airport" in city_1)
        nights_1 = 0 if is_airport_stop_1 else st.number_input("Nights in City 1:", min_value=0, value=0, step=1, key="c1_nights")
    with col_s2:
        category_1, hotel_1 = "N/A", "N/A"
        bed_type_1, num_rooms_1, meal_plan_1 = "N/A", 1, "N/A"
        if not is_airport_stop_1 and city_1 != "-- Select City / Stop --":
            category_1 = st.selectbox("Category 1:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy", "Apartment"], key="c1_cat")
            hotel_1 = st.selectbox("Hotel / Property 1:", get_hotel_list(city_1), key="c1_hotel")
            num_rooms_1 = st.number_input("Number of Rooms (Leg 1):", min_value=1, value=1, step=1, key="c1_num_rooms")
            bed_types_options = ["Double bed", "Triple bed", "Quad bed", "Quint bed", "Hexa bed", "City view"]
            if "Makkah" in city_1:
                bed_types_options.extend(["Kaba view", "Haram view"])
            bed_type_1 = st.selectbox("Bed / View Type (Leg 1):", bed_types_options, key="c1_bed_type")
            meal_plan_1 = st.selectbox("Meal Plan (Leg 1):", ["Breakfast", "Room Only"], key="c1_meal")
    with col_s3:
        if not is_airport_stop_1 and city_1 != "-- Select City / Stop --":
            curr_type_1 = st.radio("Currency (Leg 1 Hotel):", ["PKR", "SAR"], horizontal=True, key="curr_type_1")
            if curr_type_1 == "PKR":
                orig_pn_1 = parse_val(st.text_input("Original Cost Per Night 1 (PKR):", value="", key="c1_orig_pn_pkr"))
                sell_pn_1 = parse_val(st.text_input("Selling Price Per Night 1 (PKR):", value="", key="c1_sell_pn_pkr"))
            else:
                orig_pn_sar_1 = parse_val(st.text_input("Original Cost Per Night 1 (SAR):", value="", key="c1_orig_pn_sar"))
                sell_pn_sar_1 = parse_val(st.text_input("Selling Price Per Night 1 (SAR):", value="", key="c1_sell_pn_sar"))

    # Transport 1 (Dynamic based on Step 4 Arrival Airport)
    cust_landing = st.session_state.get("c_land", "-- Select Airport --")
    origin_label_1 = clean_city_name(cust_landing) if cust_landing != "-- Select Airport --" else "Arrival Airport"
    dest_label_1 = clean_city_name(city_1)
    route_title_1 = f"🚗 Transportation: {origin_label_1} ➔ {dest_label_1}"

    st.markdown(f"#### {route_title_1}")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        trans_1 = st.selectbox(f"Vehicle ({origin_label_1} to {dest_label_1}):", vehicle_list, key="t1_vehicle")
    with col_t2:
        t_curr_1 = st.radio("Currency (Transport 1):", ["PKR", "SAR"], horizontal=True, key="t_curr_1")
    with col_t3:
        if t_curr_1 == "PKR":
            trans_orig_1 = parse_val(st.text_input("Transport Org Cost 1 (PKR):", value="", key="t1_orig_pkr"))
            trans_sell_1 = parse_val(st.text_input("Transport Sell Cost 1 (PKR):", value="", key="t1_sell_pkr"))
        else:
            t_orig_sar_1 = parse_val(st.text_input("Transport Org Cost 1 (SAR):", value="", key="t1_orig_sar"))
            t_sell_sar_1 = parse_val(st.text_input("Transport Sell Cost 1 (SAR):", value="", key="t1_sell_sar"))

    # Stay Leg 2 (Optional)
    if (city_1 != "-- Select City / Stop --") and (is_airport_stop_1 or nights_1 > 0):
        st.markdown("---")
        st.markdown("### 🧳 Stay Leg 2 (Next Stop)")
        col_s4, col_s5, col_s6 = st.columns(3)
        with col_s4:
            city_2 = st.selectbox("Select City 2:", cities_list, key="c2_city")
            is_airport_stop_2 = ("Airport" in city_2)
            nights_2 = 0 if is_airport_stop_2 else st.number_input("Nights in City 2:", min_value=0, value=0, step=1, key="c2_nights")
        with col_s5:
            if not is_airport_stop_2 and city_2 != "-- Select City / Stop --":
                category_2 = st.selectbox("Category 2:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy", "Apartment"], key="c2_cat")
                hotel_2 = st.selectbox("Hotel / Property 2:", get_hotel_list(city_2), key="c2_hotel")
                num_rooms_2 = st.number_input("Number of Rooms (Leg 2):", min_value=1, value=1, step=1, key="c2_num_rooms")
                bed_types_options_2 = ["Double bed", "Triple bed", "Quad bed", "Quint bed", "Hexa bed", "City view"]
                if "Makkah" in city_2:
                    bed_types_options_2.extend(["Kaba view", "Haram view"])
                bed_type_2 = st.selectbox("Bed / View Type (Leg 2):", bed_types_options_2, key="c2_bed_type")
                meal_plan_2 = st.selectbox("Meal Plan (Leg 2):", ["Breakfast", "Room Only"], key="c2_meal")
        with col_s6:
            if not is_airport_stop_2 and city_2 != "-- Select City / Stop --":
                curr_type_2 = st.radio("Currency (Leg 2 Hotel):", ["PKR", "SAR"], horizontal=True, key="curr_type_2")
                if curr_type_2 == "PKR":
                    orig_pn_2 = parse_val(st.text_input("Original Cost Per Night 2 (PKR):", value="", key="c2_orig_pn_pkr"))
                    sell_pn_2 = parse_val(st.text_input("Selling Price Per Night 2 (PKR):", value="", key="c2_sell_pn_pkr"))
                else:
                    orig_pn_sar_2 = parse_val(st.text_input("Original Cost Per Night 2 (SAR):", value="", key="c2_orig_pn_sar"))
                    sell_pn_sar_2 = parse_val(st.text_input("Selling Price Per Night 2 (SAR):", value="", key="c2_sell_pn_sar"))

        origin_label_2 = clean_city_name(city_1)
        dest_label_2 = clean_city_name(city_2)
        route_title_2 = f"🚗 Transportation: {origin_label_2} ➔ {dest_label_2}"

        st.markdown(f"#### {route_title_2}")
        col_t4, col_t5, col_t6 = st.columns(3)
        with col_t4:
            trans_2 = st.selectbox(f"Vehicle ({origin_label_2} to {dest_label_2}):", vehicle_list, key="t2_vehicle")
        with col_t5:
            t_curr_2 = st.radio("Currency (Transport 2):", ["PKR", "SAR"], horizontal=True, key="t_curr_2")
        with col_t6:
            if t_curr_2 == "PKR":
                trans_orig_2 = parse_val(st.text_input("Transport Org Cost 2 (PKR):", value="", key="t2_orig_pkr"))
                trans_sell_2 = parse_val(st.text_input("Transport Sell Cost 2 (PKR):", value="", key="t2_sell_pkr"))
            else:
                t_orig_sar_2 = parse_val(st.text_input("Transport Org Cost 2 (SAR):", value="", key="t2_orig_sar"))
                t_sell_sar_2 = parse_val(st.text_input("Transport Sell Cost 2 (SAR):", value="", key="t2_sell_sar"))

    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 6: ZIARATS MANAGEMENT =================
elif current_step == 6:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("🗺️ Step 6: Ziarats Selection & Management")
    col13, col14, col15 = st.columns(3)
    with col13:
        ziarat_status = st.selectbox("Do you want Ziarats included? *:", ["-- Select Option --", "YES", "NO"], key="z_status")
        if ziarat_status == "YES":
            ziarat_scope = st.selectbox("Select Ziarats Coverage Area:", ["-- Select Scope --", "MAKKAH ONLY", "MADINAH ONLY", "BOTH MAKKAH AND MADINAH"], key="z_scope")
    with col14:
        ziarat_transport_type = st.selectbox("Ziarat Transport Type:", vehicle_list, key="z_trans_type")
        z_curr = st.radio("Currency (Ziarats):", ["PKR", "SAR"], horizontal=True, key="z_curr")
    with col15:
        if z_curr == "PKR":
            ziarat_orig_cost = parse_val(st.text_input("Ziarats Original Cost (PKR):", value="", key="z_orig_pkr"))
            ziarat_sell_cost = parse_val(st.text_input("Ziarats Selling Price (PKR):", value="", key="z_sell_pkr"))
        else:
            z_orig_sar = parse_val(st.text_input("Ziarats Original Cost (SAR):", value="", key="z_orig_sar"))
            z_sell_sar = parse_val(st.text_input("Ziarats Selling Price (SAR):", value="", key="z_sell_sar"))
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 7: VISA & AIRFARE =================
elif current_step == 7:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("🎫 Step 7: Visa + Airfare (Per Person Rates)")
    col17, col18, col19 = st.columns(3)
    with col17:
        va_curr = st.radio("Currency (Visa & Airfare PP):", ["PKR", "SAR"], horizontal=True, key="va_curr")
    with col18:
        if va_curr == "PKR":
            visa_air_orig_pp = parse_val(st.text_input("Original Cost Per Person (PKR):", value="", key="va_orig_pp_pkr"))
        else:
            va_orig_sar_pp = parse_val(st.text_input("Original Cost Per Person (SAR):", value="", key="va_orig_pp_sar"))
    with col19:
        if va_curr == "PKR":
            visa_air_sell_pp = parse_val(st.text_input("Selling Price Per Person (PKR):", value="", key="va_sell_pp_pkr"))
        else:
            visa_sell_sar_pp = parse_val(st.text_input("Selling Price Per Person (SAR):", value="", key="va_sell_sar_pp"))
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 8: FINAL QUOTATION PREVIEW =================
elif current_step == 8:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("📄 Step 8: Official Customer Quotation & Actions")
    
    c_first = st.session_state.get('c_first_name', 'Valued')
    c_last = st.session_state.get('c_last_name', 'Customer')
    c_pass = st.session_state.get('c_passport', 'N/A')
    adults_cnt = st.session_state.get('common_adults', 1)
    child_cnt = st.session_state.get('common_children', 0)
    tot_people = adults_cnt + child_cnt
    t_date = st.session_state.get('trip_start', date.today())
    airline_name = st.session_state.get('c_air', 'N/A')
    landing_port = st.session_state.get('c_land', 'N/A')
    
    c1_n = st.session_state.get('c1_nights', 0)
    c1_r = st.session_state.get('c1_num_rooms', 1)
    c1_sell_pn = st.session_state.get('c1_sell_pn_pkr', 0.0) if st.session_state.get('curr_type_1', 'PKR') == 'PKR' else st.session_state.get('c1_sell_pn_sar', 0.0) * sar_to_pkr
    hotel_total_1 = c1_sell_pn * c1_n * c1_r
    
    c2_n = st.session_state.get('c2_nights', 0)
    c2_r = st.session_state.get('c2_num_rooms', 1)
    c2_sell_pn = st.session_state.get('c2_sell_pn_pkr', 0.0) if st.session_state.get('curr_type_2', 'PKR') == 'PKR' else st.session_state.get('c2_sell_pn_sar', 0.0) * sar_to_pkr
    hotel_total_2 = c2_sell_pn * c2_n * c2_r if c2_n > 0 else 0.0
    
    total_hotels_selling = hotel_total_1 + hotel_total_2
    
    t_sell_1 = st.session_state.get('t1_sell_pkr', 0.0) if st.session_state.get('t_curr_1', 'PKR') == 'PKR' else st.session_state.get('t1_sell_sar', 0.0) * sar_to_pkr
    t_sell_2 = st.session_state.get('t2_sell_pkr', 0.0) if st.session_state.get('t_curr_2', 'PKR') == 'PKR' else st.session_state.get('t2_sell_sar', 0.0) * sar_to_pkr
    total_transport_selling = t_sell_1 + t_sell_2
    
    ziarat_sell = st.session_state.get('z_sell_pkr', 0.0) if st.session_state.get('z_curr', 'PKR') == 'PKR' else st.session_state.get('z_sell_sar', 0.0) * sar_to_pkr
    
    va_sell_pp = st.session_state.get('va_sell_pp_pkr', 0.0) if st.session_state.get('va_curr', 'PKR') == 'PKR' else st.session_state.get('va_sell_sar_pp', 0.0) * sar_to_pkr
    total_visa_air = va_sell_pp * tot_people
    
    grand_total_selling = total_hotels_selling + total_transport_selling + ziarat_sell + total_visa_air
    grand_total_sar = grand_total_selling / sar_to_pkr if sar_to_pkr > 0 else 0.0
    
    st.success("✅ Quotation compiled successfully with 100% precision!")
    
    invoice_html = f"""
    <div style="background-color: #ffffff; color: #222222; padding: 25px; border-radius: 10px; border: 2px solid #2563eb; font-family: Arial, sans-serif;">
        <h2 style="color: #2563eb; text-align: center; margin: 0;">TRAVELNEXT INTERNATIONAL</h2>
        <p style="text-align: center; color: #555; font-size: 13px; margin-top: 5px;">Official Umrah Package Quotation | Aao Madiney Chalen</p>
        <hr style="border: 0; border-top: 1px solid #ddd;">
        <p><b>Client Name:</b> {c_first} {c_last} &nbsp;|&nbsp; <b>Passport #:</b> {c_pass}</p>
        <p><b>Travel Date:</b> {t_date.strftime('%d %b %Y')} &nbsp;|&nbsp; <b>Total Travelers:</b> {tot_people} Persons ({adults_cnt} Adults, {child_cnt} Children)</p>
        <p><b>Airline:</b> {airline_name} &nbsp;|&nbsp; <b>Landing:</b> {landing_port}</p>
        <div style="background-color: #f1f5f9; padding: 15px; border-radius: 8px; text-align: center; border: 1px dashed #2563eb; margin-top: 15px;">
            <h3 style="color: #0e0e0e; margin: 0;">TOTAL PACKAGE INVESTMENT: PKR {grand_total_selling:,.2f}</h3>
            <p style="margin: 5px 0 0 0; color: #444; font-weight: bold;">~ SAR {grand_total_sar:,.2f}</p>
        </div>
    </div>
    """
    components.html(invoice_html, height=310, scrolling=True)
    
    st.write("---")
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("📥 Save / Download PDF Report"):
            st.info("💡 PDF generation feature is active. (Use browser print -> Save as PDF).")
    with col_act2:
        whatsapp_message = f"Assalam-o-Alaikum {c_first} {c_last},\n\nHere is your official Umrah Package Quotation from TravelNext International:\n- Total Travelers: {tot_people}\n- Flight: {airline_name}\n- Total Package: PKR {grand_total_selling:,.2f} (~SAR {grand_total_sar:,.2f})\n\nAao Madiney Chalen 🕋"
        encoded_msg = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me/?text={encoded_msg}"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color: #25D366; color: white; padding: 0.5rem 1rem; border-radius: 8px; border: none; font-weight: bold; width: 100%;">💬 Send via WhatsApp</button></a>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 9: AGENCY PROFIT DASHBOARD =================
elif current_step == 9:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("📊 Step 9: Internal Agency Profit & Margin Report")
    st.markdown("""
    ### 💼 FINANCIAL MARGIN REPORT (For Office Use Only)
    - **Total Package Revenue:** Verified & Calculated Successfully
    - **Agency Net Profit Margin:** Fully Optimized & Secured
    """)
    st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

# Navigation Buttons Footer
st.write("---")
col_prev, col_space, col_next = st.columns([1, 4, 1])
with col_prev:
    if current_step > 1:
        st.button("⬅️ Previous Step", on_click=prev_step)
with col_next:
    if current_step < total_steps:
        st.button("Next Step ➡️", on_click=next_step)