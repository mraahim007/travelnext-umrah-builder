import streamlit as st
from datetime import date, timedelta
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

# ================= ROBUST SESSION STATE INITIALIZATION =================
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1
if "num_legs" not in st.session_state:
    st.session_state.num_legs = 2
if "daily_sar_rate" not in st.session_state:
    st.session_state.daily_sar_rate = 75.0

if "c_first_name" not in st.session_state: st.session_state.c_first_name = ""
if "c_last_name" not in st.session_state: st.session_state.c_last_name = ""
if "c_passport" not in st.session_state: st.session_state.c_passport = ""
if "common_adults" not in st.session_state: st.session_state.common_adults = 2
if "common_children" not in st.session_state: st.session_state.common_children = 0
if "trip_start" not in st.session_state: st.session_state.trip_start = date.today()

if "c_air" not in st.session_state: st.session_state.c_air = "Saudia Airlines"
if "c_land" not in st.session_state: st.session_state.c_land = "Jeddah Airport (JED)"

if "va_curr" not in st.session_state: st.session_state.va_curr = "PKR"
if "va_cost_pp_pkr" not in st.session_state: st.session_state.va_cost_pp_pkr = None
if "va_sell_pp_pkr" not in st.session_state: st.session_state.va_sell_pp_pkr = None
if "va_cost_pp_sar" not in st.session_state: st.session_state.va_cost_pp_sar = None
if "va_sell_pp_sar" not in st.session_state: st.session_state.va_sell_pp_sar = None

if "z_status" not in st.session_state: st.session_state.z_status = "YES"
if "z_scope" not in st.session_state: st.session_state.z_scope = "BOTH MAKKAH AND MADINAH"
if "z_makkah_date" not in st.session_state: st.session_state.z_makkah_date = date.today()
if "z_makkah_trans" not in st.session_state: st.session_state.z_makkah_trans = "GMC"
if "z_makkah_curr" not in st.session_state: st.session_state.z_makkah_curr = "PKR"
if "z_makkah_cost_pkr" not in st.session_state: st.session_state.z_makkah_cost_pkr = None
if "z_makkah_sell_pkr" not in st.session_state: st.session_state.z_makkah_sell_pkr = None
if "z_makkah_cost_sar" not in st.session_state: st.session_state.z_makkah_cost_sar = None
if "z_makkah_sell_sar" not in st.session_state: st.session_state.z_makkah_sell_sar = None

if "z_madinah_date" not in st.session_state: st.session_state.z_madinah_date = date.today() + timedelta(days=4)
if "z_madinah_trans" not in st.session_state: st.session_state.z_madinah_trans = "GMC"
if "z_madinah_curr" not in st.session_state: st.session_state.z_madinah_curr = "PKR"
if "z_madinah_cost_pkr" not in st.session_state: st.session_state.z_madinah_cost_pkr = None
if "z_madinah_sell_pkr" not in st.session_state: st.session_state.z_madinah_sell_pkr = None
if "z_madinah_cost_sar" not in st.session_state: st.session_state.z_madinah_cost_sar = None
if "z_madinah_sell_sar" not in st.session_state: st.session_state.z_madinah_sell_sar = None

# Initialize legs data up to 10 safely without forcing 0s
default_cities = ["Makkah Al-Mukarramah", "Al-Madinah Al-Munawwarah", "Makkah Al-Mukarramah"]
default_hotels = [
    "5-Star Makkah Clock Royal Tower, A Fairmont Hotel (0 km)",
    "5-Star Anwar Al Madinah Movenpick Hotel (100m)",
    "4-Star Emaar Royal Hotel (700 - 800m)"
]

for i in range(10):
    if f"leg_city_{i}" not in st.session_state: 
        st.session_state[f"leg_city_{i}"] = default_cities[i] if i < len(default_cities) else "-- Select City / Stop --"
    if f"leg_nights_{i}" not in st.session_state: st.session_state[f"leg_nights_{i}"] = 3 if i < 2 else 0
    if f"leg_cat_{i}" not in st.session_state: st.session_state[f"leg_cat_{i}"] = "5-Star Luxury"
    if f"leg_hotel_{i}" not in st.session_state: 
        st.session_state[f"leg_hotel_{i}"] = default_hotels[i] if i < len(default_hotels) else "-- Select Specific Hotel --"
    if f"leg_rooms_{i}" not in st.session_state: st.session_state[f"leg_rooms_{i}"] = 1
    if f"leg_bed_{i}" not in st.session_state: st.session_state[f"leg_bed_{i}"] = "Double bed"
    if f"leg_meal_{i}" not in st.session_state: st.session_state[f"leg_meal_{i}"] = "Breakfast"
    if f"leg_curr_h_{i}" not in st.session_state: st.session_state[f"leg_curr_h_{i}"] = "PKR"
    
    if f"leg_cost_pn_pkr_{i}" not in st.session_state: st.session_state[f"leg_cost_pn_pkr_{i}"] = None
    if f"leg_sell_pn_pkr_{i}" not in st.session_state: st.session_state[f"leg_sell_pn_pkr_{i}"] = None
    if f"leg_cost_pn_sar_{i}" not in st.session_state: st.session_state[f"leg_cost_pn_sar_{i}"] = None
    if f"leg_sell_pn_sar_{i}" not in st.session_state: st.session_state[f"leg_sell_pn_sar_{i}"] = None
    
    if f"leg_trans_veh_{i}" not in st.session_state: st.session_state[f"leg_trans_veh_{i}"] = "GMC"
    if f"leg_t_curr_{i}" not in st.session_state: st.session_state[f"leg_t_curr_{i}"] = "PKR"
    if f"leg_t_cost_pkr_{i}" not in st.session_state: st.session_state[f"leg_t_cost_pkr_{i}"] = None
    if f"leg_t_sell_pkr_{i}" not in st.session_state: st.session_state[f"leg_t_sell_pkr_{i}"] = None
    if f"leg_t_cost_sar_{i}" not in st.session_state: st.session_state[f"leg_t_cost_sar_{i}"] = None
    if f"leg_t_sell_sar_{i}" not in st.session_state: st.session_state[f"leg_t_sell_sar_{i}"] = None

total_steps = 9

def prev_step():
    if st.session_state.wizard_step > 1:
        st.session_state.wizard_step -= 1

def next_step():
    if st.session_state.wizard_step < total_steps:
        st.session_state.wizard_step += 1

current_step = st.session_state.wizard_step

# Progress Bar Header
progress_percent = int(((current_step - 1) / (total_steps - 1)) * 100) if total_steps > 1 else 0
st.progress(progress_percent)
st.caption(f"Step {current_step} of {total_steps} (Progress: {progress_percent}%)")
st.write("---")

sar_to_pkr = st.session_state.daily_sar_rate
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
    if "Jeddah Airport" in c or "JED" in c:
        return "Jeddah Airport (JED)"
    if "Madinah Airport" in c or "MED" in c:
        return "Madinah Airport (MED)"
    if "Makkah" in c:
        return "Makkah"
    if "Madinah" in c:
        return "Madinah"
    return c

# ================= STEP 1: WELCOME SCREEN =================
if current_step == 1:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>✨ TRAVELNEXT INTERNATIONAL ✨</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #f8fafc;'>Smart Umrah Package Builder & Quotation System</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Aao Madiney Chalen 🕋 | Professional Booking & Management Portal</p>", unsafe_allow_html=True)
    st.write("---")
    st.info("💡 **Welcome!** Click **Next Step ➡️** below to start building your professional Umrah quotation.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 2: CURRENCY EXCHANGE =================
elif current_step == 2:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("💱 Step 2: Daily Currency Exchange Rate")
    st.write("Set the current Saudi Riyal (SAR) to Pakistani Rupee (PKR) rate:")
    st.number_input("Enter current 1 SAR to PKR rate today:", min_value=0.1, max_value=100.0, step=0.5, key="daily_sar_rate")
    st.success(f"💡 Active Exchange Rate: **1 SAR = {st.session_state.daily_sar_rate:,.2f} PKR** | **1 PKR = {1/st.session_state.daily_sar_rate:,.4f} SAR**")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 3: CUSTOMER DETAILS =================
elif current_step == 3:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("👤 Step 3: Customer Details & Travel Dates")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("First Name *:", key="c_first_name")
        st.number_input("Enter number of adults:", min_value=1, key="common_adults")
    with col2:
        st.text_input("Last Name:", key="c_last_name")
        st.number_input("Enter number of children:", min_value=0, key="common_children")
    
    st.text_input("Passport Number *:", key="c_passport")
    st.date_input("Overall Trip Start Date (Arrival Date):", key="trip_start")
    
    total_people = st.session_state.common_adults + st.session_state.common_children
    st.info(f"👉 Total Family Members: **{total_people}** ({st.session_state.common_adults} Adults, {st.session_state.common_children} Children)")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 4: FLIGHT DETAILS =================
elif current_step == 4:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("✈️ Step 4: Flight Information")
    col3, col4 = st.columns(2)
    with col3:
        st.selectbox("Select Airline Name *:", ["-- Select Airline --", "Saudia Airlines", "PIA", "AirBlue", "SereneAir", "Fly Jinnah", "Emirates", "Qatar Airways"], key="c_air")
    with col4:
        st.selectbox("Arrival Airport (Landing City) *:", ["-- Select Airport --", "Jeddah Airport (JED)", "Madinah Airport (MED)"], key="c_land")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 5: HOTEL STAYS & UNLIMITED DYNAMIC LEGS =================
elif current_step == 5:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("🏨 Step 5: Hotel Stay & City Transport Builder (Actual vs Selling)")
    st.markdown("Provide both Actual Cost and Selling Price for precise agency profit tracking.")

    num_legs = st.session_state.num_legs
    current_date_cursor = st.session_state.trip_start

    for i in range(num_legs):
        st.markdown(f"### 🧳 Stay Leg {i+1} ({'First Stop' if i==0 else ('Final Stop' if i==num_legs-1 else f'Stop {i+1}')})")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            city_val = st.selectbox(f"Select City {i+1} *:", cities_list, key=f"leg_city_{i}")
            is_airport_stop = ("Airport" in city_val)
            
            nights_val = 0 if is_airport_stop else st.number_input(f"Nights in City {i+1}:", min_value=0, step=1, key=f"leg_nights_{i}")
            
            st.caption(f"📅 Estimated Stay: {current_date_cursor.strftime('%d %b %Y')} to {(current_date_cursor + timedelta(days=max(1, nights_val))).strftime('%d %b %Y')}")
            if not is_airport_stop:
                current_date_cursor += timedelta(days=max(1, nights_val))

        with col_s2:
            if not is_airport_stop and city_val != "-- Select City / Stop --":
                st.selectbox(f"Category {i+1}:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy", "Apartment"], key=f"leg_cat_{i}")
                st.selectbox(f"Hotel / Property {i+1}:", get_hotel_list(city_val), key=f"leg_hotel_{i}")
                st.number_input(f"Number of Rooms (Leg {i+1}):", min_value=1, step=1, key=f"leg_rooms_{i}")
                
                bed_opts = ["Double bed", "Triple bed", "Quad bed", "Quint bed", "Hexa bed", "City view"]
                if "Makkah" in city_val:
                    bed_opts.extend(["Kaba view", "Haram view"])
                st.selectbox(f"Bed / View Type (Leg {i+1}):", bed_opts, key=f"leg_bed_{i}")
                st.selectbox(f"Meal Plan (Leg {i+1}):", ["Breakfast", "Room Only"], key=f"leg_meal_{i}")
            else:
                st.info("ℹ️ Airport transit stop: Hotel selection disabled.")

        with col_s3:
            if not is_airport_stop and city_val != "-- Select City / Stop --":
                curr_h = st.radio(f"Currency (Leg {i+1} Hotel):", ["PKR", "SAR"], horizontal=True, key=f"leg_curr_h_{i}")
                if curr_h == "PKR":
                    st.number_input(f"Actual Cost Per Night {i+1} (PKR):", min_value=0.0, step=1000.0, format="%.2f", key=f"leg_cost_pn_pkr_{i}")
                    st.number_input(f"Selling Price Per Night {i+1} (PKR):", min_value=0.0, step=1000.0, format="%.2f", key=f"leg_sell_pn_pkr_{i}")
                else:
                    st.number_input(f"Actual Cost Per Night {i+1} (SAR):", min_value=0.0, step=100.0, format="%.2f", key=f"leg_cost_pn_sar_{i}")
                    st.number_input(f"Selling Price Per Night {i+1} (SAR):", min_value=0.0, step=100.0, format="%.2f", key=f"leg_sell_pn_sar_{i}")

        if i == 0:
            cust_landing = st.session_state.c_land
            origin_lbl = clean_city_name(cust_landing) if cust_landing != "-- Select Airport --" else "Arrival Airport"
        else:
            prev_city_val = st.session_state.get(f"leg_city_{i-1}", "-- Select City / Stop --")
            origin_lbl = clean_city_name(prev_city_val)
            
        dest_lbl = clean_city_name(city_val)
        route_title = f"🚗 Transportation: {origin_lbl} ➔ {dest_lbl}"

        st.markdown(f"#### {route_title}")
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.selectbox(f"Vehicle ({origin_lbl} to {dest_lbl}):", vehicle_list, key=f"leg_trans_veh_{i}")
        with col_t2:
            st.radio(f"Currency (Transport {i+1}):", ["PKR", "SAR"], horizontal=True, key=f"leg_t_curr_{i}")
        with col_t3:
            t_curr_val = st.session_state.get(f"leg_t_curr_{i}", "PKR")
            if t_curr_val == "PKR":
                st.number_input(f"Transport Actual Cost {i+1} (PKR):", min_value=0.0, step=500.0, format="%.2f", key=f"leg_t_cost_pkr_{i}")
                st.number_input(f"Transport Sell Cost {i+1} (PKR):", min_value=0.0, step=500.0, format="%.2f", key=f"leg_t_sell_pkr_{i}")
            else:
                st.number_input(f"Transport Actual Cost {i+1} (SAR):", min_value=0.0, step=50.0, format="%.2f", key=f"leg_t_cost_sar_{i}")
                st.number_input(f"Transport Sell Cost {i+1} (SAR):", min_value=0.0, step=50.0, format="%.2f", key=f"leg_t_sell_sar_{i}")
        
        if i < num_legs - 1:
            st.markdown("---")

    st.write("---")
    if st.button("➕ Add Another Destination Leg"):
        st.session_state.num_legs += 1
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 6: ZIARATS MANAGEMENT =================
elif current_step == 6:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("🗺️ Step 6: Ziarats Selection & Schedule")
    
    st.selectbox("Do you want Ziarats included? *:", ["-- Select Option --", "YES", "NO"], key="z_status")
    
    if st.session_state.z_status == "YES":
        st.selectbox("Select Ziarats Coverage Area:", ["-- Select Scope --", "MAKKAH ONLY", "MADINAH ONLY", "BOTH MAKKAH AND MADINAH"], key="z_scope")
        
        if st.session_state.z_scope in ["MAKKAH ONLY", "BOTH MAKKAH AND MADINAH"]:
            st.markdown("---")
            st.markdown("#### 🕋 Makkah Ziarat Configuration")
            c_m1, c_m2, c_m3 = st.columns(3)
            with c_m1:
                st.date_input("📅 Makkah Ziarat Date:", key="z_makkah_date")
                st.selectbox("Makkah Ziarat Transport:", vehicle_list, key="z_makkah_trans")
            with c_m2:
                st.radio("Currency (Makkah Ziarats):", ["PKR", "SAR"], horizontal=True, key="z_makkah_curr")
            with c_m3:
                if st.session_state.z_makkah_curr == "PKR":
                    st.number_input("Makkah Ziarats Actual Cost (PKR):", min_value=0.0, step=500.0, format="%.2f", key="z_makkah_cost_pkr")
                    st.number_input("Makkah Ziarats Selling Price (PKR):", min_value=0.0, step=500.0, format="%.2f", key="z_makkah_sell_pkr")
                else:
                    st.number_input("Makkah Ziarats Actual Cost (SAR):", min_value=0.0, step=50.0, format="%.2f", key="z_makkah_cost_sar")
                    st.number_input("Makkah Ziarats Selling Price (SAR):", min_value=0.0, step=50.0, format="%.2f", key="z_makkah_sell_sar")

        if st.session_state.z_scope in ["MADINAH ONLY", "BOTH MAKKAH AND MADINAH"]:
            st.markdown("---")
            st.markdown("#### 🕌 Madinah Ziarat Configuration")
            c_md1, c_md2, c_md3 = st.columns(3)
            with c_md1:
                st.date_input("📅 Madinah Ziarat Date:", key="z_madinah_date")
                st.selectbox("Madinah Ziarat Transport:", vehicle_list, key="z_madinah_trans")
            with c_md2:
                st.radio("Currency (Madinah Ziarats):", ["PKR", "SAR"], horizontal=True, key="z_madinah_curr")
            with c_md3:
                if st.session_state.z_madinah_curr == "PKR":
                    st.number_input("Madinah Ziarats Actual Cost (PKR):", min_value=0.0, step=500.0, format="%.2f", key="z_madinah_cost_pkr")
                    st.number_input("Madinah Ziarats Selling Price (PKR):", min_value=0.0, step=500.0, format="%.2f", key="z_madinah_sell_pkr")
                else:
                    st.number_input("Madinah Ziarats Actual Cost (SAR):", min_value=0.0, step=50.0, format="%.2f", key="z_madinah_cost_sar")
                    st.number_input("Madinah Ziarats Selling Price (SAR):", min_value=0.0, step=50.0, format="%.2f", key="z_madinah_sell_sar")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 7: VISA & AIRFARE =================
elif current_step == 7:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("🎫 Step 7: Visa + Airfare (Per Person Rates)")
    col17, col18, col19 = st.columns(3)
    with col17:
        st.radio("Currency (Visa & Airfare PP):", ["PKR", "SAR"], horizontal=True, key="va_curr")
    with col18:
        if st.session_state.va_curr == "PKR":
            st.number_input("Actual Cost Per Person (PKR):", min_value=0.0, step=1000.0, format="%.2f", key="va_cost_pp_pkr")
            st.number_input("Selling Price Per Person (PKR):", min_value=0.0, step=1000.0, format="%.2f", key="va_sell_pp_pkr")
        else:
            st.number_input("Actual Cost Per Person (SAR):", min_value=0.0, step=100.0, format="%.2f", key="va_cost_pp_sar")
            st.number_input("Selling Price Per Person (SAR):", min_value=0.0, step=100.0, format="%.2f", key="va_sell_pp_sar")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 8: FINAL PROFESSIONAL QUOTATION PREVIEW =================
elif current_step == 8:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("📄 Step 8: Official Customer Quotation & Actions")
    
    c_first = st.session_state.c_first_name if st.session_state.c_first_name else "Valued"
    c_last = st.session_state.c_last_name if st.session_state.c_last_name else "Customer"
    c_pass = st.session_state.c_passport if st.session_state.c_passport else "N/A"
    adults_cnt = st.session_state.common_adults
    child_cnt = st.session_state.common_children
    tot_people = adults_cnt + child_cnt
    t_date = st.session_state.trip_start
    airline_name = st.session_state.c_air
    landing_port = st.session_state.c_land
    
    num_legs = st.session_state.num_legs
    total_hotels_selling = 0.0
    total_transport_selling = 0.0
    
    share_text = f"""══════════════════════
🕋 *TRAVELNEXT INTERNATIONAL* 🕋
*Official Umrah Package Quotation*
══════════════════════
👤 *Client Name:* {c_first} {c_last}
📅 *Travel Date:* {t_date.strftime('%d %b %Y')}
👥 *Total Travelers:* {tot_people} Persons ({adults_cnt} Adults, {child_cnt} Children)
✈️ *Airline:* {airline_name if airline_name != '-- Select Airline --' else 'N/A'}
🛬 *Landing Airport:* {landing_port if landing_port != '-- Select Airport --' else 'N/A'}
──────────────────────
🏨 *Itinerary & Services:*"""

    itinerary_html_rows = ""
    running_date = t_date

    for i in range(num_legs):
        c_city = st.session_state.get(f'leg_city_{i}', '-- Select City / Stop --')
        if "--" in c_city:
            continue
        is_apt = ("Airport" in c_city)
        c_nights = st.session_state.get(f'leg_nights_{i}', 0)
        c_rooms = st.session_state.get(f'leg_rooms_{i}', 1)
        c_hotel = st.session_state.get(f'leg_hotel_{i}', 'N/A')
        c_meal = st.session_state.get(f'leg_meal_{i}', 'N/A')
        c_bed = st.session_state.get(f'leg_bed_{i}', 'N/A')
        
        stay_from = running_date
        stay_to = running_date + timedelta(days=max(1, c_nights)) if not is_apt else running_date
        if not is_apt:
            running_date = stay_to

        h_sell_pn = 0.0
        if not is_apt:
            curr_h = st.session_state.get(f'leg_curr_h_{i}', 'PKR')
            if curr_h == 'PKR':
                h_sell_pn = float(st.session_state.get(f'leg_sell_pn_pkr_{i}') or 0.0)
            else:
                h_sell_pn = float(st.session_state.get(f'leg_sell_pn_sar_{i}') or 0.0) * sar_to_pkr
        
        leg_hotel_total = h_sell_pn * c_nights * c_rooms if not is_apt else 0.0
        total_hotels_selling += leg_hotel_total

        t_veh = st.session_state.get(f'leg_trans_veh_{i}', 'N/A')
        t_curr = st.session_state.get(f'leg_t_curr_{i}', 'PKR')
        t_sell = 0.0
        if t_curr == 'PKR':
            t_sell = float(st.session_state.get(f'leg_t_sell_pkr_{i}') or 0.0)
        else:
            t_sell = float(st.session_state.get(f'leg_t_sell_sar_{i}') or 0.0) * sar_to_pkr
        
        total_transport_selling += t_sell

        if i == 0:
            origin_label = clean_city_name(landing_port) if landing_port != "-- Select Airport --" else "Arrival Airport"
        else:
            prev_city = st.session_state.get(f'leg_city_{i-1}', '-- Select City / Stop --')
            origin_label = clean_city_name(prev_city)
        dest_label = clean_city_name(c_city)
        t_route_desc = f"{origin_label} ➔ {dest_label} ({t_veh})" if t_veh != "-- Select Transport --" else f"{origin_label} ➔ {dest_label}"

        if not is_apt:
            itinerary_html_rows += f"<tr><td style='padding: 12px; border: 1px solid #d0e8dc; vertical-align: top;'><b>Leg {i+1}</b></td><td style='padding: 12px; border: 1px solid #d0e8dc; vertical-align: top;'><b>{c_city}</b></td><td style='padding: 12px; border: 1px solid #d0e8dc; vertical-align: top; line-height: 1.6;'><b>Hotel:</b> {c_hotel}<br><b>Stay:</b> {c_nights} Nights, {c_rooms} Room(s) | <b>Bed/View:</b> {c_bed} | <b>Meal:</b> {c_meal}<br>🚗 <i>Transfer:</i> {t_route_desc}</td></tr>"
            share_text += f"\n\n▫️ *Leg {i+1} ({c_city}):*\n   • Hotel: {c_hotel}\n   • Stay: {c_nights} Nights | {c_rooms} Room(s)\n   • Bed/View: {c_bed} | Meal: {c_meal}\n   • Transfer: {t_route_desc}"
        else:
            itinerary_html_rows += f"<tr><td style='padding: 12px; border: 1px solid #d0e8dc; vertical-align: top;'><b>Leg {i+1}</b></td><td style='padding: 12px; border: 1px solid #d0e8dc; vertical-align: top;'><b>{c_city}</b></td><td style='padding: 12px; border: 1px solid #d0e8dc; vertical-align: top; line-height: 1.6;'>Airport Transit / Stop<br>🚗 <i>Transfer:</i> {t_route_desc}</td></tr>"
            share_text += f"\n\n▫️ *Leg {i+1} ({c_city}):*\n   • Airport Transit / Stop\n   • Transfer: {t_route_desc}"

    ziarat_sell = 0.0
    ziarat_text = "Not Included"
    if st.session_state.z_status == 'YES':
        z_scope = st.session_state.z_scope
        ziarat_text_parts = []
        
        if z_scope in ["MAKKAH ONLY", "BOTH MAKKAH AND MADINAH"]:
            m_curr = st.session_state.z_makkah_curr
            m_sell = float(st.session_state.z_makkah_sell_pkr or 0.0) if m_curr == 'PKR' else float(st.session_state.z_makkah_sell_sar or 0.0) * sar_to_pkr
            ziarat_sell += m_sell
            ziarat_text_parts.append("Makkah Ziarat")

        if z_scope in ["MADINAH ONLY", "BOTH MAKKAH AND MADINAH"]:
            md_curr = st.session_state.z_madinah_curr
            md_sell = float(st.session_state.z_madinah_sell_pkr or 0.0) if md_curr == 'PKR' else float(st.session_state.z_madinah_sell_sar or 0.0) * sar_to_pkr
            ziarat_sell += md_sell
            ziarat_text_parts.append("Madinah Ziarat")
        
        if ziarat_text_parts:
            ziarat_text = f"{' & '.join(ziarat_text_parts)} Included"

    share_text += f"\n\n🗺️ *Ziarats:* {ziarat_text}"

    va_sell_pp = 0.0
    va_curr = st.session_state.va_curr
    if va_curr == 'PKR':
        va_sell_pp = float(st.session_state.va_sell_pp_pkr or 0.0)
    else:
        va_sell_pp = float(st.session_state.va_sell_pp_sar or 0.0) * sar_to_pkr
    
    total_visa_air = va_sell_pp * tot_people
    grand_total_selling = total_hotels_selling + total_transport_selling + ziarat_sell + total_visa_air
    grand_total_sar = grand_total_selling / sar_to_pkr if sar_to_pkr > 0 else 0.0

    share_text += f"""
──────────────────────
💰 *TOTAL PACKAGE INVESTMENT:*
👉 *PKR {grand_total_selling:,.2f}*
👉 *~ SAR {grand_total_sar:,.2f}*
──────────────────────
_Thanks for choosing TravelNext. Aao Madiney Chalen!_"""
    
    st.success("✅ Professional Quotation compiled successfully!")
    
    invoice_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            background-color: #ffffff;
            color: #222222;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 15px;
        }}
        .invoice-box {{
            padding: 30px;
            border-radius: 12px;
            border: 2px solid #2e8b57;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            background: #ffffff;
        }}
        .header-section {{
            text-align: center;
            border-bottom: 2px solid #2e8b57;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}
        .details-table {{
            width: 100%;
            font-size: 14px;
            margin-bottom: 25px;
            border-collapse: collapse;
        }}
        .details-table td {{
            padding: 8px 12px;
            line-height: 1.6;
        }}
        .itinerary-table {{
            width: 100%;
            font-size: 13.5px;
            border-collapse: collapse;
            margin-bottom: 25px;
        }}
        .itinerary-table th {{
            background-color: #f2f9f5;
            color: #1b5e3a;
            padding: 12px;
            border: 1px solid #d0e8dc;
            text-align: left;
            font-weight: 600;
        }}
        .total-box {{
            background-color: #f8f9fa;
            padding: 18px;
            border-radius: 8px;
            text-align: center;
            border: 1px dashed #2e8b57;
            margin-bottom: 20px;
        }}
        .print-btn {{
            background-color: #2e8b57;
            color: white;
            padding: 14px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            display: block;
            width: 100%;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .print-btn:hover {{
            background-color: #246b43;
        }}
        @media print {{
            .print-btn {{ display: none; }}
            .invoice-box {{ border: none; box-shadow: none; padding: 0; }}
        }}
    </style>
    </head>
    <body>
    <div class="invoice-box">
        <div class="header-section">
            <h2 style="color: #2e8b57; margin: 0; font-size: 24px; letter-spacing: 0.5px;">TRAVELNEXT INTERNATIONAL</h2>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #555; font-weight: 500;">Official Umrah Packages & Travel Services | Aao Madiney Chalen</p>
        </div>
        
        <table class="details-table">
            <tr>
                <td><b>Client Name:</b> {c_first} {c_last}</td>
                <td><b>Travel Date:</b> {t_date.strftime('%d %b %Y')}</td>
            </tr>
            <tr>
                <td><b>Total Travelers:</b> {tot_people} Persons ({adults_cnt} Adults, {child_cnt} Children)</td>
                <td><b>Airline:</b> {airline_name if airline_name != '-- Select Airline --' else 'N/A'}</td>
            </tr>
            <tr>
                <td><b>Total Duration:</b> Visa & Airfare Included</td>
                <td><b>Landing Airport:</b> {landing_port if landing_port != '-- Select Airport --' else 'N/A'}</td>
            </tr>
        </table>
        
        <h4 style="color: #2e8b57; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px; margin-bottom: 12px; font-size: 16px;">Hotel Itinerary & Transport Breakdown</h4>
        <table class="itinerary-table">
            <tr>
                <th>Leg</th>
                <th>City / Stop</th>
                <th>Accommodation & Route Transfer Details</th>
            </tr>
            {itinerary_html_rows}
            <tr>
                <td style="padding: 12px; border: 1px solid #d0e8dc; vertical-align: top;"><b>Ziarats</b></td>
                <td style="padding: 12px; border: 1px solid #d0e8dc; vertical-align: top;" colspan="2">{ziarat_text}</td>
            </tr>
            <tr>
                <td style="padding: 12px; border: 1px solid #d0e8dc; vertical-align: top;"><b>Visa & Air</b></td>
                <td style="padding: 12px; border: 1px solid #d0e8dc; vertical-align: top;" colspan="2">PKR {total_visa_air:,.2f} total ({tot_people} travelers @ PKR {va_sell_pp:,.2f} per person)</td>
            </tr>
        </table>
        
        <div class="total-box">
            <h3 style="margin: 0; color: #1b5e3a; font-size: 20px;">TOTAL PACKAGE INVESTMENT: PKR {grand_total_selling:,.2f}</h3>
            <p style="margin: 8px 0 0 0; font-size: 14.5px; color: #444; font-weight: 500;">Equivalent to approx. SAR {grand_total_sar:,.2f}</p>
        </div>
        
        <p style="text-align: center; font-size: 13px; color: #666; margin-top: 15px; font-style: italic;">Thanks for choosing TravelNext. May Allah accept your good deeds!</p>
        
        <!-- PRINT / SAVE AS PDF BUTTON -->
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save Invoice as PDF</button>
    </div>
    </body>
    </html>
    """
    
    components.html(invoice_html, height=650, scrolling=True)
    
    st.write("---")
    encoded_text = urllib.parse.quote(share_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color: #25D366; color: white; padding: 14px 20px; border-radius: 8px; border: none; font-weight: bold; width: 100%; font-size: 16px; cursor: pointer;">📤 Share Formatted Text via WhatsApp</button></a>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 9: AGENCY PROFIT DASHBOARD =================
elif current_step == 9:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("📊 Step 9: Internal Agency Profit & Margin Report")
    
    # Calculate Total Costs vs Selling
    tot_cost_hotels = 0.0
    tot_sell_hotels = 0.0
    tot_cost_trans = 0.0
    tot_sell_trans = 0.0
    
    for i in range(st.session_state.num_legs):
        c_city = st.session_state.get(f'leg_city_{i}', '-- Select City / Stop --')
        if "--" in c_city or "Airport" in c_city:
            continue
        c_nights = st.session_state.get(f'leg_nights_{i}', 0)
        c_rooms = st.session_state.get(f'leg_rooms_{i}', 1)
        curr_h = st.session_state.get(f'leg_curr_h_{i}', 'PKR')
        
        if curr_h == 'PKR':
            c_cost = float(st.session_state.get(f'leg_cost_pn_pkr_{i}') or 0.0)
            c_sell = float(st.session_state.get(f'leg_sell_pn_pkr_{i}') or 0.0)
        else:
            c_cost = float(st.session_state.get(f'leg_cost_pn_sar_{i}') or 0.0) * sar_to_pkr
            c_sell = float(st.session_state.get(f'leg_sell_pn_sar_{i}') or 0.0) * sar_to_pkr
            
        tot_cost_hotels += c_cost * c_nights * c_rooms
        tot_sell_hotels += c_sell * c_nights * c_rooms
        
        t_curr = st.session_state.get(f'leg_t_curr_{i}', 'PKR')
        if t_curr == 'PKR':
            t_cost = float(st.session_state.get(f'leg_t_cost_pkr_{i}') or 0.0)
            t_sell = float(st.session_state.get(f'leg_t_sell_pkr_{i}') or 0.0)
        else:
            t_cost = float(st.session_state.get(f'leg_t_cost_sar_{i}') or 0.0) * sar_to_pkr
            t_sell = float(st.session_state.get(f'leg_t_sell_sar_{i}') or 0.0) * sar_to_pkr
            
        tot_cost_trans += t_cost
        tot_sell_trans += t_sell

    total_cost_overall = tot_cost_hotels + tot_cost_trans
    total_sell_overall = tot_sell_hotels + tot_sell_trans
    net_profit = total_sell_overall - total_cost_overall

    st.markdown(f"""
    ### 💼 FINANCIAL MARGIN REPORT (For Office Use Only)
    - **Total Package Cost (Actual):** PKR {total_cost_overall:,.2f}
    - **Total Package Revenue (Selling):** PKR {total_sell_overall:,.2f}
    - 🟢 **Estimated Agency Net Profit:** PKR {net_profit:,.2f}
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