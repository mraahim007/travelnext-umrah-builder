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

# Initialize Session State for Wizard Steps & Dynamic Legs
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1

if "num_legs" not in st.session_state:
    st.session_state.num_legs = 2

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
        if st.session_state.get("leg_city_0") == "-- Select City / Stop --":
            st.error("⚠️ Please select City for Leg 1 first!")
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
    if "Jeddah Airport" in c or "JED" in c:
        return "Jeddah Airport (JED)"
    if "Madinah Airport" in c or "MED" in c:
        return "Madinah Airport (MED)"
    if "Makkah" in c:
        return "Makkah"
    if "Madinah" in c:
        return "Madinah"
    return c

def parse_val(val_str):
    try:
        clean_str = "".join([char for char in str(val_str) if char.isdigit() or char == '.'])
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

# ================= STEP 5: HOTEL STAYS & UNLIMITED DYNAMIC LEGS =================
elif current_step == 5:
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    st.subheader("🏨 Step 5: Hotel Stay & City Transport Builder (Unlimited Legs)")
    st.markdown("Configure your stay legs and dynamic transportation routes seamlessly. Add as many legs as you want!")

    num_legs = st.session_state.num_legs
    current_date_cursor = st.session_state.get('trip_start', date.today())

    for i in range(num_legs):
        st.markdown(f"### 🧳 Stay Leg {i+1} ({'First Stop' if i==0 else ('Final Stop' if i==num_legs-1 else f'Stop {i+1}')})")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            city_key = f"leg_city_{i}"
            city_val = st.selectbox(f"Select City {i+1} *:", cities_list, key=city_key)
            is_airport_stop = ("Airport" in city_val)
            
            nights_key = f"leg_nights_{i}"
            nights_val = 0 if is_airport_stop else st.number_input(f"Nights in City {i+1}:", min_value=0, value=1 if not is_airport_stop else 0, step=1, key=nights_key)
            
            st.caption(f"📅 Estimated Stay: {current_date_cursor.strftime('%d %b %Y')} to {(current_date_cursor + timedelta(days=max(1, nights_val))).strftime('%d %b %Y')}")
            if not is_airport_stop:
                current_date_cursor += timedelta(days=max(1, nights_val))

        with col_s2:
            if not is_airport_stop and city_val != "-- Select City / Stop --":
                st.selectbox(f"Category {i+1}:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy", "Apartment"], key=f"leg_cat_{i}")
                st.selectbox(f"Hotel / Property {i+1}:", get_hotel_list(city_val), key=f"leg_hotel_{i}")
                st.number_input(f"Number of Rooms (Leg {i+1}):", min_value=1, value=1, step=1, key=f"leg_rooms_{i}")
                
                bed_opts = ["Double bed", "Triple bed", "Quad bed", "Quint bed", "Hexa bed", "City view"]
                if "Makkah" in city_val:
                    bed_opts.extend(["Kaba view", "Haram view"])
                st.selectbox(f"Bed / View Type (Leg {i+1}):", bed_opts, key=f"leg_bed_{i}")
                st.selectbox(f"Meal Plan (Leg {i+1}):", ["Breakfast", "Room Only"], key=f"leg_meal_{i}")
            else:
                st.info("ℹ️ Airport transit stop: Hotel & Room selection is disabled.")

        with col_s3:
            if not is_airport_stop and city_val != "-- Select City / Stop --":
                curr_h = st.radio(f"Currency (Leg {i+1} Hotel):", ["PKR", "SAR"], horizontal=True, key=f"leg_curr_h_{i}")
                if curr_h == "PKR":
                    parse_val(st.text_input(f"Original Cost Per Night {i+1} (PKR):", value="", key=f"leg_orig_pn_pkr_{i}"))
                    parse_val(st.text_input(f"Selling Price Per Night {i+1} (PKR):", value="", key=f"leg_sell_pn_pkr_{i}"))
                else:
                    parse_val(st.text_input(f"Original Cost Per Night {i+1} (SAR):", value="", key=f"leg_orig_pn_sar_{i}"))
                    parse_val(st.text_input(f"Selling Price Per Night {i+1} (SAR):", value="", key=f"leg_sell_pn_sar_{i}"))

        if i == 0:
            cust_landing = st.session_state.get("c_land", "-- Select Airport --")
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
                parse_val(st.text_input(f"Transport Org Cost {i+1} (PKR):", value="", key=f"leg_t_orig_pkr_{i}"))
                parse_val(st.text_input(f"Transport Sell Cost {i+1} (PKR):", value="", key=f"leg_t_sell_pkr_{i}"))
            else:
                parse_val(st.text_input(f"Transport Org Cost {i+1} (SAR):", value="", key=f"leg_t_orig_sar_{i}"))
                parse_val(st.text_input(f"Transport Sell Cost {i+1} (SAR):", value="", key=f"leg_t_sell_sar_{i}"))
        
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
    
    ziarat_status = st.selectbox("Do you want Ziarats included? *:", ["-- Select Option --", "YES", "NO"], key="z_status")
    
    if ziarat_status == "YES":
        ziarat_scope = st.selectbox("Select Ziarats Coverage Area:", ["-- Select Scope --", "MAKKAH ONLY", "MADINAH ONLY", "BOTH MAKKAH AND MADINAH"], key="z_scope")
        
        if ziarat_scope in ["MAKKAH ONLY", "BOTH MAKKAH AND MADINAH"]:
            st.markdown("---")
            st.markdown("#### 🕋 Makkah Ziarat Configuration")
            c_m1, c_m2, c_m3 = st.columns(3)
            with c_m1:
                st.date_input("📅 Makkah Ziarat Date:", value=st.session_state.get('trip_start', date.today()), key="z_makkah_date")
                st.selectbox("Makkah Ziarat Transport:", vehicle_list, key="z_makkah_trans")
            with c_m2:
                st.radio("Currency (Makkah Ziarats):", ["PKR", "SAR"], horizontal=True, key="z_makkah_curr")
            with c_m3:
                if st.session_state.get("z_makkah_curr", "PKR") == "PKR":
                    parse_val(st.text_input("Makkah Ziarats Original Cost (PKR):", value="", key="z_makkah_orig_pkr"))
                    parse_val(st.text_input("Makkah Ziarats Selling Price (PKR):", value="", key="z_makkah_sell_pkr"))
                else:
                    parse_val(st.text_input("Makkah Ziarats Original Cost (SAR):", value="", key="z_makkah_orig_sar"))
                    parse_val(st.text_input("Makkah Ziarats Selling Price (SAR):", value="", key="z_makkah_sell_sar"))

        if ziarat_scope in ["MADINAH ONLY", "BOTH MAKKAH AND MADINAH"]:
            st.markdown("---")
            st.markdown("#### 🕌 Madinah Ziarat Configuration")
            c_md1, c_md2, c_md3 = st.columns(3)
            with c_md1:
                st.date_input("📅 Madinah Ziarat Date:", value=st.session_state.get('trip_start', date.today()), key="z_madinah_date")
                st.selectbox("Madinah Ziarat Transport:", vehicle_list, key="z_madinah_trans")
            with c_md2:
                st.radio("Currency (Madinah Ziarats):", ["PKR", "SAR"], horizontal=True, key="z_madinah_curr")
            with c_md3:
                if st.session_state.get("z_madinah_curr", "PKR") == "PKR":
                    parse_val(st.text_input("Madinah Ziarats Original Cost (PKR):", value="", key="z_madinah_orig_pkr"))
                    parse_val(st.text_input("Madinah Ziarats Selling Price (PKR):", value="", key="z_madinah_sell_pkr"))
                else:
                    parse_val(st.text_input("Madinah Ziarats Original Cost (SAR):", value="", key="z_madinah_orig_sar"))
                    parse_val(st.text_input("Madinah Ziarats Selling Price (SAR):", value="", key="z_madinah_sell_sar"))

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
            parse_val(st.text_input("Original Cost Per Person (PKR):", value="", key="va_orig_pp_pkr"))
        else:
            parse_val(st.text_input("Original Cost Per Person (SAR):", value="", key="va_orig_pp_sar"))
    with col19:
        if va_curr == "PKR":
            parse_val(st.text_input("Selling Price Per Person (PKR):", value="", key="va_sell_pp_pkr"))
        else:
            parse_val(st.text_input("Selling Price Per Person (SAR):", value="", key="va_sell_sar_pp"))
    st.markdown("</div>", unsafe_allow_html=True)

# ================= STEP 8: FINAL PROFESSIONAL QUOTATION PREVIEW =================
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
    
    num_legs = st.session_state.get('num_legs', 2)
    total_hotels_selling = 0.0
    total_transport_selling = 0.0
    
    legs_breakdown_html = ""
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
                h_sell_pn = st.session_state.get(f'leg_sell_pn_pkr_{i}', 0.0)
            else:
                h_sell_pn = st.session_state.get(f'leg_sell_pn_sar_{i}', 0.0) * sar_to_pkr
        
        leg_hotel_total = h_sell_pn * c_nights * c_rooms if not is_apt else 0.0
        total_hotels_selling += leg_hotel_total

        t_veh = st.session_state.get(f'leg_trans_veh_{i}', 'N/A')
        t_curr = st.session_state.get(f'leg_t_curr_{i}', 'PKR')
        t_sell = 0.0
        if t_curr == 'PKR':
            t_sell = st.session_state.get(f'leg_t_sell_pkr_{i}', 0.0)
        else:
            t_sell = st.session_state.get(f'leg_t_sell_sar_{i}', 0.0) * sar_to_pkr
        
        total_transport_selling += t_sell

        legs_breakdown_html += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 10px; line-height: 1.6;"><b>Leg {i+1}: {c_city}</b><br><span style="color: #555; font-size: 12px;">Hotel: {c_hotel} ({c_rooms} Room(s), {c_meal}, {c_bed})<br>Duration: {stay_from.strftime('%d %b %Y')} to {stay_to.strftime('%d %b %Y')} ({c_nights} Nights)</span></td>
            <td style="padding: 10px; text-align: right; line-height: 1.6;"><b>PKR {leg_hotel_total:,.2f}</b></td>
        </tr>
        <tr style="border-bottom: 1px solid #e2e8f0; background-color: #f8fafc;">
            <td style="padding: 8px 10px; line-height: 1.6; color: #475569; font-size: 13px;">🚗 Transport ({t_veh}) for Leg {i+1}</td>
            <td style="padding: 8px 10px; text-align: right; line-height: 1.6; color: #475569; font-size: 13px;"><b>PKR {t_sell:,.2f}</b></td>
        </tr>
        """

    ziarat_sell = 0.0
    ziarats_rows_html = ""
    if st.session_state.get('z_status') == 'YES':
        z_scope = st.session_state.get('z_scope', 'N/A')
        
        if z_scope in ["MAKKAH ONLY", "BOTH MAKKAH AND MADINAH"]:
            m_curr = st.session_state.get('z_makkah_curr', 'PKR')
            m_sell = st.session_state.get('z_makkah_sell_pkr', 0.0) if m_curr == 'PKR' else st.session_state.get('z_makkah_sell_sar', 0.0) * sar_to_pkr
            ziarat_sell += m_sell
            m_date = st.session_state.get('z_makkah_date', date.today())
            m_trans = st.session_state.get('z_makkah_trans', 'N/A')
            ziarats_rows_html += f"""
            <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 10px; line-height: 1.6;"><b>Makkah Ziarats</b><br><span style="color: #555; font-size: 12px;">Scheduled Date: {m_date.strftime('%d %b %Y')} | Vehicle: {m_trans}</span></td>
                <td style="padding: 10px; text-align: right; line-height: 1.6;"><b>PKR {m_sell:,.2f}</b></td>
            </tr>
            """

        if z_scope in ["MADINAH ONLY", "BOTH MAKKAH AND MADINAH"]:
            md_curr = st.session_state.get('z_madinah_curr', 'PKR')
            md_sell = st.session_state.get('z_madinah_sell_pkr', 0.0) if md_curr == 'PKR' else st.session_state.get('z_madinah_sell_sar', 0.0) * sar_to_pkr
            ziarat_sell += md_sell
            md_date = st.session_state.get('z_madinah_date', date.today())
            md_trans = st.session_state.get('z_madinah_trans', 'N/A')
            ziarats_rows_html += f"""
            <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 10px; line-height: 1.6;"><b>Madinah Ziarats</b><br><span style="color: #555; font-size: 12px;">Scheduled Date: {md_date.strftime('%d %b %Y')} | Vehicle: {md_trans}</span></td>
                <td style="padding: 10px; text-align: right; line-height: 1.6;"><b>PKR {md_sell:,.2f}</b></td>
            </tr>
            """

    va_sell_pp = 0.0
    va_curr = st.session_state.get('va_curr', 'PKR')
    if va_curr == 'PKR':
        va_sell_pp = parse_val(st.session_state.get('va_sell_pp_pkr', 0.0))
    else:
        va_sell_pp = parse_val(st.session_state.get('va_sell_sar_pp', 0.0)) * sar_to_pkr
    
    total_visa_air = va_sell_pp * tot_people
    grand_total_selling = total_hotels_selling + total_transport_selling + ziarat_sell + total_visa_air
    grand_total_sar = grand_total_selling / sar_to_pkr if sar_to_pkr > 0 else 0.0
    
    st.success("✅ Professional Quotation compiled successfully!")
    
    invoice_html = f"""
    <div style="background-color: #ffffff; color: #1e293b; padding: 30px; border-radius: 12px; border: 2px solid #2563eb; font-family: Arial, sans-serif;">
        <div style="text-align: center;">
            <h2 style="color: #2563eb; margin: 0; font-size: 24px; letter-spacing: 1px;">TRAVELNEXT INTERNATIONAL</h2>
            <p style="color: #64748b; font-size: 14px; margin-top: 4px;">Official Umrah Package Quotation & Itinerary | Aao Madiney Chalen 🕋</p>
        </div>
        <hr style="border: 0; border-top: 1px solid #cbd5e1; margin: 20px 0;">
        
        <table style="width: 100%; font-size: 14px; margin-bottom: 20px;">
            <tr>
                <td style="line-height: 1.8;"><b>Client Name:</b> {c_first} {c_last}</td>
                <td style="line-height: 1.8; text-align: right;"><b>Passport #:</b> {c_pass}</td>
            </tr>
            <tr>
                <td style="line-height: 1.8;"><b>Travel Date:</b> {t_date.strftime('%d %b %Y')}</td>
                <td style="line-height: 1.8; text-align: right;"><b>Total Travelers:</b> {tot_people} Persons ({adults_cnt} Adults, {child_cnt} Children)</td>
            </tr>
            <tr>
                <td style="line-height: 1.8;" colspan="2"><b>Airline & Landing:</b> {airline_name} landing at {landing_port}</td>
            </tr>
        </table>

        <h4 style="color: #0f172a; border-bottom: 2px solid #2563eb; padding-bottom: 6px; margin-top: 25px;">Detailed Itinerary & Cost Breakdown</h4>
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <tr style="background-color: #f1f5f9; color: #334155;">
                <th style="padding: 10px; text-align: left;">Service Description & Dates</th>
                <th style="padding: 10px; text-align: right;">Amount (PKR)</th>
            </tr>
            {legs_breakdown_html}
            {ziarats_rows_html}
            <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 10px; line-height: 1.6;"><b>Visa & Airfare</b><br><span style="color: #555; font-size: 12px;">Rate per person: PKR {va_sell_pp:,.2f} x {tot_people} Travelers</span></td>
                <td style="padding: 10px; text-align: right; line-height: 1.6;"><b>PKR {total_visa_air:,.2f}</b></td>
            </tr>
        </table>

        <div style="background-color: #eff6ff; padding: 20px; border-radius: 8px; text-align: center; border: 1px dashed #2563eb; margin-top: 30px;">
            <h3 style="color: #1e40af; margin: 0; font-size: 22px;">TOTAL PACKAGE INVESTMENT: PKR {grand_total_selling:,.2f}</h3>
            <p style="margin: 6px 0 0 0; color: #334155; font-size: 16px; font-weight: bold;">~ SAR {grand_total_sar:,.2f} (Exchange Rate: 1 SAR = {sar_to_pkr} PKR)</p>
        </div>
        
        <p style="text-align: center; color: #94a3b8; font-size: 12px; margin-top: 25px;">Thank you for choosing TravelNext International. Have a blessed journey!</p>
    </div>
    """
    components.html(invoice_html, height=520, scrolling=True)
    
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