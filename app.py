import streamlit as st
from datetime import date
import urllib.parse
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(page_title="TravelNext Umrah Builder", page_icon="🕋", layout="wide")

st.markdown("<h1 style='text-align: center;'>✨ TRAVELNEXT - SMART UMRAH BUILDER ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #2e8b57; font-size: 18px; font-weight: bold;'>Aao Madiney Chalen 🕋</p>", unsafe_allow_html=True)
st.write("---")

# 1. CURRENCY EXCHANGE RATE
st.subheader("💱 Step 1: Daily Currency Exchange Rate")
sar_to_pkr = st.number_input("Enter current 1 SAR to PKR rate today:", min_value=0.1, max_value=100.0, value=75.0, step=0.5, key="daily_sar_rate")
st.info(f"💡 Active Exchange Rate: **1 SAR = {sar_to_pkr:,.2f} PKR** | **1 PKR = {1/sar_to_pkr:,.4f} SAR**")

st.write("---")

# 2. CUSTOMER DETAILS & FLIGHT INFO
st.subheader("👤 Step 2: Customer Details & Arrival Flight Information")
col1, col2 = st.columns(2)
with col1:
    cust_first_name = st.text_input("First Name:", key="c_first_name")
    adults = st.number_input("Enter number of adults:", min_value=1, value=1, key="common_adults")
    cust_airline = st.selectbox("Select Arrival Airline Name:", ["-- Select Airline --", "Saudia Airlines", "PIA", "AirBlue", "SereneAir", "Fly Jinnah", "Emirates", "Qatar Airways"], key="c_air")
with col2:
    cust_last_name = st.text_input("Last Name:", key="c_last_name")
    children = st.number_input("Enter number of children:", min_value=0, value=0, key="common_children")
    cust_landing = st.selectbox("Arrival Airport (Landing City):", ["-- Select Airport --", "Jeddah Airport (JED)", "Madinah Airport (MED)"], key="c_land")

total_people = adults + children

col_f_date, col_f_cost = st.columns(2)
with col_f_date:
    trip_start_date = st.date_input("Arrival Flight Date:", value=date.today(), key="trip_start")
    arrival_day_name = trip_start_date.strftime("%A")
    st.info(f"📅 Arrival Day: **{arrival_day_name}** | Total Family Members: **{total_people}** ({adults} Adults, {children} Children)")

with col_f_cost:
    arr_curr = st.radio("Currency (Arrival Flight):", ["PKR", "SAR"], horizontal=True, key="arr_curr")
    if arr_curr == "PKR":
        arr_orig_pp = st.number_input("Arrival Flight Actual Cost Per Person (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="arr_orig_pkr") or 0.0
        arr_sell_pp = st.number_input("Arrival Flight Selling Price Per Person (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="arr_sell_pkr") or 0.0
    else:
        arr_orig_sar_pp = st.number_input("Arrival Flight Actual Cost Per Person (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="arr_orig_sar") or 0.0
        arr_sell_sar_pp = st.number_input("Arrival Flight Selling Price Per Person (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="arr_sell_sar") or 0.0
        arr_orig_pp = arr_orig_sar_pp * sar_to_pkr
        arr_sell_pp = arr_sell_sar_pp * sar_to_pkr

arrival_orig_total = arr_orig_pp * total_people
arrival_sell_total = arr_sell_pp * total_people
if arrival_sell_total > 0:
    arr_sar_prev = arrival_sell_total / sar_to_pkr if sar_to_pkr > 0 else 0
    st.success(f"✈️ Arrival Flight Total ({total_people} Persons) ➔ **PKR {arrival_sell_total:,.2f}** | **SAR {arr_sar_prev:,.2f}**")

st.write("---")

# CITIES, HOTELS, & VEHICLES LISTS
cities_list = [
    "-- Select City / Stop --", 
    "Makkah Al-Mukarramah", 
    "Al-Madinah Al-Munawwarah", 
    "Jeddah Airport (Transit / Stop Only - No Hotel Stay)", 
    "Madinah Airport (Transit / Stop Only - No Hotel Stay)"
]

vehicle_list = ["-- Select Transport --", "CAR", "STAREX", "GMC", "HIACE", "COASTER", "Public Transport"]

def get_hotel_list(city):
    if city == "Makkah Al-Mukarramah":
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
    elif city == "Al-Madinah Al-Munawwarah":
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
    if "--" in c:
        return ""
    if "Jeddah Airport" in c:
        return "Jeddah Airport (JED)"
    if "Madinah Airport" in c:
        return "Madinah Airport (MED)"
    if "Makkah" in c:
        return "Makkah"
    if "Madinah" in c:
        return "Madinah"
    return c

# 3. UNLIMITED DYNAMIC STAY & TRANSPORT BUILDER
st.subheader("🏨 Step 3: Hotel Stays & City Transport Builder (Unlimited Legs)")
st.markdown("You can add as many destination legs as you want using the button below:")

if 'num_legs' not in st.session_state:
    st.session_state.num_legs = 1

col_add, col_rem = st.columns([1, 1])
with col_add:
    if st.button("➕ Add Another Stay Leg"):
        st.session_state.num_legs += 1
        st.rerun()
with col_rem:
    if st.session_state.num_legs > 1:
        if st.button("➖ Remove Last Leg"):
            st.session_state.num_legs -= 1
            st.rerun()

legs_data = []
prev_city_label = clean_city_name(cust_landing) if cust_landing != "-- Select Airport --" else "Arrival Airport"

for i in range(st.session_state.num_legs):
    leg_num = i + 1
    st.markdown("---")
    st.markdown(f"### 🧳 Stay Leg {leg_num}")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        city = st.selectbox(f"Select City {leg_num}:", cities_list, key=f"c_{leg_num}_city")
        is_airport_stop = ("Airport" in city)
        nights = 0 if is_airport_stop else st.number_input(f"Nights in City {leg_num}:", min_value=0, value=0, step=1, key=f"c_{leg_num}_nights")
    
    with col_s2:
        category, hotel = "N/A", "N/A"
        bed_type, num_rooms, meal_plan = "N/A", 1, "N/A"
        if not is_airport_stop and city != "-- Select City / Stop --":
            category = st.selectbox(f"Category {leg_num}:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy", "Apartment"], key=f"c_{leg_num}_cat")
            hotel = st.selectbox(f"Hotel / Property {leg_num}:", get_hotel_list(city), key=f"c_{leg_num}_hotel")
            num_rooms = st.number_input(f"Number of Rooms (Leg {leg_num}):", min_value=1, value=1, step=1, key=f"c_{leg_num}_rooms")
            bed_types_options = ["Double bed", "Triple bed", "Quad bed", "Quint bed", "Hexa bed", "City view"]
            if "Makkah" in city:
                bed_types_options.extend(["Kaba view", "Haram view"])
            bed_type = st.selectbox(f"Bed / View Type (Leg {leg_num}):", bed_types_options, key=f"c_{leg_num}_bed")
            meal_plan = st.selectbox(f"Meal Plan (Leg {leg_num}):", ["Breakfast", "Room Only"], key=f"c_{leg_num}_meal")
        elif is_airport_stop:
            st.info("ℹ️ Airport Stop selected: No hotel stay required.")
    
    with col_s3:
        if not is_airport_stop and city != "-- Select City / Stop --":
            curr_type = st.radio(f"Currency (Leg {leg_num} Hotel):", ["PKR", "SAR"], horizontal=True, key=f"curr_type_{leg_num}")
            if curr_type == "PKR":
                orig_pn = st.number_input(f"Original Cost Per Night {leg_num} (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key=f"c_{leg_num}_orig_pkr") or 0.0
                sell_pn = st.number_input(f"Selling Price Per Night {leg_num} (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key=f"c_{leg_num}_sell_pkr") or 0.0
                orig_per_night, sell_per_night = orig_pn, sell_pn
            else:
                orig_pn_sar = st.number_input(f"Original Cost Per Night {leg_num} (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key=f"c_{leg_num}_orig_sar") or 0.0
                sell_pn_sar = st.number_input(f"Selling Price Per Night {leg_num} (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key=f"c_{leg_num}_sell_sar") or 0.0
                orig_per_night = orig_pn_sar * sar_to_pkr
                sell_per_night = sell_pn_sar * sar_to_pkr
        else:
            orig_per_night, sell_per_night = 0.0, 0.0

    hotel_orig = orig_per_night * nights * num_rooms
    hotel_sell = sell_per_night * nights * num_rooms
    if hotel_sell > 0:
        sar_prev = hotel_sell / sar_to_pkr if sar_to_pkr > 0 else 0
        st.success(f"💱 Leg {leg_num} Hotel Total ➔ **PKR {hotel_sell:,.2f}** | **SAR {sar_prev:,.2f}**")

    # Transport for this leg
    current_dest_label = clean_city_name(city)
    route_title = f"🚗 Transportation: {prev_city_label} ➔ {current_dest_label}"
    
    st.markdown(f"#### {route_title}")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        trans_vehicle = st.selectbox(f"Vehicle ({prev_city_label} to {current_dest_label}):", vehicle_list, key=f"t_{leg_num}_vehicle")
    with col_t2:
        t_curr = st.radio(f"Currency (Transport {leg_num}):", ["PKR", "SAR"], horizontal=True, key=f"t_curr_{leg_num}")
    with col_t3:
        if t_curr == "PKR":
            trans_orig = st.number_input(f"Transport Org Cost {leg_num} (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key=f"t_{leg_num}_orig_pkr") or 0.0
            trans_sell = st.number_input(f"Transport Sell Cost {leg_num} (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key=f"t_{leg_num}_sell_pkr") or 0.0
        else:
            t_orig_sar = st.number_input(f"Transport Org Cost {leg_num} (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key=f"t_{leg_num}_orig_sar") or 0.0
            t_sell_sar = st.number_input(f"Transport Sell Cost {leg_num} (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key=f"t_{leg_num}_sell_sar") or 0.0
            trans_orig = t_orig_sar * sar_to_pkr
            trans_sell = t_sell_sar * sar_to_pkr

    if trans_sell > 0:
        t_sar = trans_sell / sar_to_pkr if sar_to_pkr > 0 else 0
        st.success(f"💱 Transport {leg_num} Total ➔ **PKR {trans_sell:,.2f}** | **SAR {t_sar:,.2f}**")

    legs_data.append({
        "leg_num": leg_num,
        "city": city,
        "is_airport": is_airport_stop,
        "nights": nights,
        "hotel": hotel,
        "category": category,
        "num_rooms": num_rooms,
        "bed_type": bed_type,
        "meal_plan": meal_plan,
        "hotel_orig": hotel_orig,
        "hotel_sell": hotel_sell,
        "from_loc": prev_city_label,
        "to_loc": current_dest_label,
        "vehicle": trans_vehicle,
        "trans_orig": trans_orig,
        "trans_sell": trans_sell
    })

    prev_city_label = current_dest_label

# Calculate Totals from all dynamic legs
total_stay_nights = sum(l['nights'] for l in legs_data)
hotels_orig_total = sum(l['hotel_orig'] for l in legs_data)
hotels_sell_total = sum(l['hotel_sell'] for l in legs_data)
hotels_total_profit = hotels_sell_total - hotels_orig_total

total_transport_orig = sum(l['trans_orig'] for l in legs_data)
total_transport_sell = sum(l['trans_sell'] for l in legs_data)
total_transport_profit = total_transport_sell - total_transport_orig

st.write("---")

# 4. ZIARATS MANAGEMENT SECTION (Updated with Yes/No & Specific City/Both breakdown)
st.subheader("🗺️ Step 4: Ziarats Selection & Management")
col_z_opt, col_z_scope = st.columns(2)
with col_z_opt:
    ziarat_status = st.selectbox("Do you want Ziarats included?", ["-- Select Option --", "YES", "NO"], key="z_status")

ziarat_scope = "-- Not Applicable --"
ziarat_transport_type = "N/A"
ziarat_orig_cost = 0.0
ziarat_sell_cost = 0.0

# Separate variables for BOTH scope
makkah_z_orig, makkah_z_sell = 0.0, 0.0
madinah_z_orig, madinah_z_sell = 0.0, 0.0
makkah_z_date = None
madinah_z_date = None
makkah_z_trans, madinah_z_trans = "N/A", "N/A"

if ziarat_status == "YES":
    with col_z_scope:
        ziarat_scope = st.selectbox("Select Ziarats Coverage Area:", ["-- Select Scope --", "MAKKAH ONLY", "MADINAH ONLY", "BOTH MAKKAH AND MADINAH"], key="z_scope")

    if ziarat_scope in ["MAKKAH ONLY", "MADINAH ONLY"]:
        st.markdown(f"#### 🚙 Ziarat Details for {ziarat_scope}")
        zc1, zc2, zc3 = st.columns(3)
        with zc1:
            ziarat_transport_type = st.selectbox("Ziarat Transport Type:", vehicle_list, key="z_trans_type_single")
            ziarat_date = st.date_input("Ziarat Date:", value=date.today(), key="z_date_single")
        with zc2:
            z_curr = st.radio("Currency (Ziarats):", ["PKR", "SAR"], horizontal=True, key="z_curr_single")
        with zc3:
            if z_curr == "PKR":
                ziarat_orig_cost = st.number_input("Ziarats Original Cost (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="z_orig_pkr_single") or 0.0
                ziarat_sell_cost = st.number_input("Ziarats Selling Price (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="z_sell_pkr_single") or 0.0
            else:
                z_orig_sar = st.number_input("Ziarats Original Cost (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="z_orig_sar_single") or 0.0
                z_sell_sar = st.number_input("Ziarats Selling Price (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="z_sell_sar_single") or 0.0
                ziarat_orig_cost = z_orig_sar * sar_to_pkr
                ziarat_sell_cost = z_sell_sar * sar_to_pkr

    elif ziarat_scope == "BOTH MAKKAH AND MADINAH":
        st.markdown("#### 🕌 Makkah Ziarat Details")
        zm1, zm2, zm3 = st.columns(3)
        with zm1:
            makkah_z_trans = st.selectbox("Makkah Ziarat Transport:", vehicle_list, key="makkah_z_trans")
            makkah_z_date = st.date_input("Makkah Ziarat Date:", value=date.today(), key="makkah_z_date")
        with zm2:
            m_curr = st.radio("Currency (Makkah Ziarat):", ["PKR", "SAR"], horizontal=True, key="m_curr_z")
        with zm3:
            if m_curr == "PKR":
                makkah_z_orig = st.number_input("Makkah Ziarat Org Cost (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="m_z_orig_pkr") or 0.0
                makkah_z_sell = st.number_input("Makkah Ziarat Sell Price (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="m_z_sell_pkr") or 0.0
            else:
                mo_sar = st.number_input("Makkah Ziarat Org Cost (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="m_z_orig_sar") or 0.0
                ms_sar = st.number_input("Makkah Ziarat Sell Price (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="m_z_sell_sar") or 0.0
                makkah_z_orig = mo_sar * sar_to_pkr
                makkah_z_sell = ms_sar * sar_to_pkr

        st.markdown("#### 🕌 Madinah Ziarat Details")
        zmd1, zmd2, zmd3 = st.columns(3)
        with zmd1:
            madinah_z_trans = st.selectbox("Madinah Ziarat Transport:", vehicle_list, key="madinah_z_trans")
            madinah_z_date = st.date_input("Madinah Ziarat Date:", value=date.today(), key="madinah_z_date")
        with zmd2:
            md_curr = st.radio("Currency (Madinah Ziarat):", ["PKR", "SAR"], horizontal=True, key="md_curr_z")
        with zmd3:
            if md_curr == "PKR":
                madinah_z_orig = st.number_input("Madinah Ziarat Org Cost (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="md_z_orig_pkr") or 0.0
                madinah_z_sell = st.number_input("Madinah Ziarat Sell Price (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="md_z_sell_pkr") or 0.0
            else:
                mdo_sar = st.number_input("Madinah Ziarat Org Cost (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="md_z_orig_sar") or 0.0
                mds_sar = st.number_input("Madinah Ziarat Sell Price (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="md_z_sell_sar") or 0.0
                madinah_z_orig = mdo_sar * sar_to_pkr
                madinah_z_sell = mds_sar * sar_to_pkr

        ziarat_orig_cost = makkah_z_orig + madinah_z_orig
        ziarat_sell_cost = makkah_z_sell + madinah_z_sell

ziarat_profit = ziarat_sell_cost - ziarat_orig_cost
ziarat_sar = ziarat_sell_cost / sar_to_pkr if sar_to_pkr > 0 else 0.0
if ziarat_sell_cost > 0:
    st.success(f"💱 Ziarats Selling Total ➔ **PKR {ziarat_sell_cost:,.2f}** | **SAR {ziarat_sar:,.2f}**")

st.write("---")

# 5. VISA & RETURN AIRPORT FLIGHT
st.subheader("🎫 Step 5: Visa Services & Return Airport Flight")
col_v1, col_v2 = st.columns(2)
with col_v1:
    st.markdown("#### 🟢 Visa Cost (Per Person)")
    va_curr = st.radio("Currency (Visa PP):", ["PKR", "SAR"], horizontal=True, key="va_curr")
    if va_curr == "PKR":
        visa_orig_pp = st.number_input("Visa Original Cost PP (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="v_orig_pp_pkr") or 0.0
        visa_sell_pp = st.number_input("Visa Selling Price PP (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="v_sell_pp_pkr") or 0.0
    else:
        v_orig_sar_pp = st.number_input("Visa Original Cost PP (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="v_orig_pp_sar") or 0.0
        v_sell_sar_pp = st.number_input("Visa Selling Price PP (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="v_sell_pp_sar") or 0.0
        visa_orig_pp = v_orig_sar_pp * sar_to_pkr
        visa_sell_pp = v_sell_sar_pp * sar_to_pkr

with col_v2:
    st.markdown("#### ✈️ Return Flight (Departure from Airport)")
    return_airline = st.selectbox("Return Airline Name:", ["-- Select Airline --", "Saudia Airlines", "PIA", "AirBlue", "SereneAir", "Fly Jinnah", "Emirates", "Qatar Airways"], key="ret_air")
    return_airport = st.selectbox("Return Departure Airport:", ["-- Select Airport --", "Jeddah Airport (JED) - King Abdulaziz", "Madinah Airport (MED) - Prince Mohammad"], key="ret_port")
    
    ret_curr = st.radio("Currency (Return Flight):", ["PKR", "SAR"], horizontal=True, key="ret_curr")
    if ret_curr == "PKR":
        ret_orig_pp = st.number_input("Return Flight Actual Cost PP (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="ret_orig_pkr") or 0.0
        ret_sell_pp = st.number_input("Return Flight Selling Price PP (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="ret_sell_pkr") or 0.0
    else:
        ret_orig_sar_pp = st.number_input("Return Flight Actual Cost PP (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="ret_orig_sar") or 0.0
        ret_sell_sar_pp = st.number_input("Return Flight Selling Price PP (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="ret_sell_sar") or 0.0
        ret_orig_pp = ret_orig_sar_pp * sar_to_pkr
        ret_sell_pp = ret_sell_sar_pp * sar_to_pkr

visa_orig_total = visa_orig_pp * total_people
visa_sell_total = visa_sell_pp * total_people
visa_profit = visa_sell_total - visa_orig_total

return_orig_total = ret_orig_pp * total_people
return_sell_total = ret_sell_pp * total_people
return_profit = return_sell_total - return_orig_total

grand_total_selling = hotels_sell_total + total_transport_sell + ziarat_sell_cost + arrival_sell_total + visa_sell_total + return_sell_total
grand_total_original = hotels_orig_total + total_transport_orig + ziarat_orig_cost + arrival_orig_total + visa_orig_total + return_orig_total
total_agency_net_profit = grand_total_selling - grand_total_original
grand_total_sar = grand_total_selling / sar_to_pkr if sar_to_pkr > 0 else 0.0

st.write("---")

# 6. OFFICIAL CUSTOMER QUOTATION SHEET
st.subheader("📄 Step 6: Official Customer Quotation & Sheet Preview")
if st.button("Generate Quotation 📋", key="btn_gen_quotation"):
    st.success("Quotation Generated Successfully!")
    
    share_text = f"""══════════════════════
🕋 *TRAVELNEXT INTERNATIONAL* 🕋
*Official Umrah Package Quotation*
══════════════════════
👤 *Client Name:* {cust_first_name or 'Valued'} {cust_last_name or 'Customer'}
📅 *Arrival Date:* {trip_start_date.strftime('%d %b %Y')} ({arrival_day_name})
👥 *Total Travelers:* {total_people} Persons ({adults} Adults, {children} Children)
🌙 *Total Duration:* {total_stay_nights} Nights
✈️ *Arrival Flight:* {cust_airline if cust_airline != '-- Select Airline --' else 'N/A'} via {cust_landing if cust_landing != '-- Select Airport --' else 'N/A'}
✈️ *Return Flight:* {return_airline if return_airline != '-- Select Airline --' else 'N/A'} from {return_airport if return_airport != '-- Select Airport --' else 'N/A'}
──────────────────────
🏨 *Itinerary & Services:*"""

    itinerary_html_rows = ""
    
    for leg in legs_data:
        l_num = leg['leg_num']
        l_city = leg['city']
        is_ap = leg['is_airport']
        t_route_desc = f"{leg['from_loc']} ➔ {leg['to_loc']} ({leg['vehicle']})" if leg['vehicle'] != "-- Select Transport --" else f"{leg['from_loc']} ➔ {leg['to_loc']}"
        
        if not is_ap and l_city != "-- Select City / Stop --":
            itinerary_html_rows += f"<tr><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>Leg {l_num}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>{l_city}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6;'><b>Hotel:</b> {leg['hotel']}<br><b>Stay:</b> {leg['nights']} Nights, {leg['num_rooms']} Room(s) | <b>Bed/View:</b> {leg['bed_type']} | <b>Meal:</b> {leg['meal_plan']}<br>🚗 <i>Transfer:</i> {t_route_desc}</td></tr>"
            share_text += f"\n\n▫️ *Leg {l_num} ({l_city}):*\n   • Hotel: {leg['hotel']}\n   • Stay: {leg['nights']} Nights | {leg['num_rooms']} Room(s)\n   • Bed/View: {leg['bed_type']} | Meal: {leg['meal_plan']}\n   • Transfer: {t_route_desc}"
        elif l_city != "-- Select City / Stop --":
            itinerary_html_rows += f"<tr><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>Leg {l_num}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>{l_city}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6;'>Airport Transit / Stop<br>🚗 <i>Transfer:</i> {t_route_desc}</td></tr>"
            share_text += f"\n\n▫️ *Leg {l_num} ({l_city}):*\n   • Airport Transit / Stop\n   • Transfer: {t_route_desc}"

    # Ziarat text formatting for invoice and share
    if ziarat_status == "YES":
        if ziarat_scope in ["MAKKAH ONLY", "MADINAH ONLY"]:
            ziarat_text = f"{ziarat_scope} (Date: {ziarat_date.strftime('%d %b %Y')}, Transport: {ziarat_transport_type})"
        elif ziarat_scope == "BOTH MAKKAH AND MADINAH":
            ziarat_text = f"Both Makkah & Madinah Ziarats<br>• Makkah Ziarat: {makkah_z_date.strftime('%d %b %Y')} ({makkah_z_trans})<br>• Madinah Ziarat: {madinah_z_date.strftime('%d %b %Y')} ({madinah_z_trans})"
        else:
            ziarat_text = "Included"
    else:
        ziarat_text = "Not Included"

    share_text += f"\n\n🗺️ *Ziarats:* {ziarat_text.replace('<br>', ' | ')}"

    share_text += f"""
──────────────────────
💰 *TOTAL PACKAGE INVESTMENT:*
👉 *PKR {grand_total_selling:,.2f}*
👉 *~ SAR {grand_total_sar:,.2f}*
──────────────────────
_Thanks for choosing TravelNext. Aao Madiney Chalen!_"""

    invoice_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ background-color: #ffffff; color: #222222; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 15px; }}
        .invoice-box {{ padding: 30px; border-radius: 12px; border: 2px solid #2e8b57; box-shadow: 0 4px 15px rgba(0,0,0,0.08); background: #ffffff; }}
        .header-section {{ text-align: center; border-bottom: 2px solid #2e8b57; padding-bottom: 15px; margin-bottom: 20px; }}
        .details-table {{ width: 100%; font-size: 14px; margin-bottom: 25px; border-collapse: collapse; }}
        .details-table td {{ padding: 8px 12px; line-height: 1.6; }}
        .itinerary-table {{ width: 100%; font-size: 13.5px; border-collapse: collapse; margin-bottom: 25px; }}
        .itinerary-table th {{ background-color: #f2f9f5; color: #1b5e3a; padding: 12px; border: 1px solid #d0e8dc; text-align: left; font-weight: 600; }}
        .total-box {{ background-color: #f8f9fa; padding: 18px; border-radius: 8px; text-align: center; border: 1px dashed #2e8b57; margin-bottom: 20px; }}
        .print-btn {{ background-color: #2e8b57; color: white; padding: 14px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; display: block; width: 100%; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .print-btn:hover {{ background-color: #246b43; }}
        @media print {{ .print-btn {{ display: none; }} .invoice-box {{ border: none; box-shadow: none; padding: 0; }} }}
    </style>
    </head>
    <body>
    <div class="invoice-box">
        <div class="header-section">
            <h2 style="color: #2e8b57; margin: 0; font-size: 24px;">TRAVELNEXT INTERNATIONAL</h2>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #555; font-weight: 500;">Official Umrah Packages & Travel Services | Aao Madiney Chalen</p>
        </div>
        
        <table class="details-table">
            <tr>
                <td><b>Client Name:</b> {cust_first_name or 'Valued'} {cust_last_name or 'Customer'}</td>
                <td><b>Arrival Date:</b> {trip_start_date.strftime('%d %b %Y')} ({arrival_day_name})</td>
            </tr>
            <tr>
                <td><b>Total Travelers:</b> {total_people} Persons ({adults} Adults, {children} Children)</td>
                <td><b>Arrival Flight:</b> {cust_airline if cust_airline != '-- Select Airline --' else 'N/A'}</td>
            </tr>
            <tr>
                <td><b>Total Duration:</b> {total_stay_nights} Nights</td>
                <td><b>Return Flight:</b> {return_airline if return_airline != '-- Select Airline --' else 'N/A'} ({return_airport})</td>
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
        </table>
        
        <div class="total-box">
            <h3 style="margin: 0; color: #1b5e3a; font-size: 20px;">TOTAL PACKAGE INVESTMENT: PKR {grand_total_selling:,.2f}</h3>
            <p style="margin: 8px 0 0 0; font-size: 14.5px; color: #444; font-weight: 500;">Equivalent to approx. SAR {grand_total_sar:,.2f}</p>
        </div>
        
        <p style="text-align: center; font-size: 13px; color: #666; margin-top: 15px; font-style: italic;">Thanks for choosing TravelNext. May Allah accept your good deeds!</p>
        
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save Invoice as PDF</button>
    </div>
    </body>
    </html>
    """

    components.html(invoice_html, height=750, scrolling=True)
    st.write("")

    encoded_text = urllib.parse.quote(share_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:14px 20px; border:none; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer; width: 100%;">📤 Share Formatted Text via WhatsApp</button></a>', unsafe_allow_html=True)
    st.write("---")

# 7. AGENCY PROFIT DASHBOARD
st.subheader("📊 Step 7: Internal Agency Profit & Cost Breakdown")
if st.button("Show Internal Profit Sheet 📈", key="btn_profit_sheet"):
    agency_sar_profit = total_agency_net_profit / sar_to_pkr if sar_to_pkr > 0 else 0
    st.markdown(f"""
    ### 💼 FINANCIAL MARGIN REPORT (For Office Use Only)
    - **Arrival Flight Total ({total_people} Persons):** PKR {arrival_sell_total:,.2f} *(Profit: PKR {arrival_sell_total - arrival_orig_total:,.2f})*
    - **Hotels Stays Total ({total_stay_nights} Nights):** PKR {hotels_sell_total:,.2f} *(Profit: PKR {hotels_total_profit:,.2f})*
    - **City Transports Total:** PKR {total_transport_sell:,.2f} *(Profit: PKR {total_transport_profit:,.2f})*
    - **Ziarats Total:** PKR {ziarat_sell_cost:,.2f} *(Profit: PKR {ziarat_profit:,.2f})*
    - **Visa Cost Total:** PKR {visa_sell_total:,.2f} *(Profit: PKR {visa_profit:,.2f})*
    - **Return Flight Total:** PKR {return_sell_total:,.2f} *(Profit: PKR {return_profit:,.2f})*
    
    ---
    ### 🔥 TOTAL NET PROFIT FOR AGENCY: PKR {total_agency_net_profit:,.2f}  |  SAR {agency_sar_profit:,.2f}
    """)
    st.balloons()