import streamlit as st
from datetime import date, timedelta
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

# 2. CUSTOMER DETAILS & FLIGHT INFO (WITH CALENDAR & DAY)
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

# Arrival Flight Date & Day selection
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

# 3. STEP-BY-STEP DYNAMIC STAY & TRANSPORT BUILDER (UP TO 4 LEGS FOR EXTRA DESTINATION)
st.subheader("🏨 Step 3: Hotel Stays & City Transport Builder (Multiple Destinations)")
st.markdown("Configure your stay legs and inter-city transport:")

# Stay Leg 1
st.markdown("### 🧳 Stay Leg 1 (First Stop)")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    city_1 = st.selectbox("Select City 1:", cities_list, key="c1_city")
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
    elif is_airport_stop_1:
        st.info("ℹ️ Airport Stop selected: No hotel stay required.")
with col_s3:
    if not is_airport_stop_1 and city_1 != "-- Select City / Stop --":
        curr_type_1 = st.radio("Currency (Leg 1 Hotel):", ["PKR", "SAR"], horizontal=True, key="curr_type_1")
        if curr_type_1 == "PKR":
            orig_pn_1 = st.number_input("Original Cost Per Night 1 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="c1_orig_pn_pkr") or 0.0
            sell_pn_1 = st.number_input("Selling Price Per Night 1 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="c1_sell_pn_pkr") or 0.0
            orig_per_night_1, sell_per_night_1 = orig_pn_1, sell_pn_1
        else:
            orig_pn_sar_1 = st.number_input("Original Cost Per Night 1 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c1_orig_pn_sar") or 0.0
            sell_pn_sar_1 = st.number_input("Selling Price Per Night 1 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c1_sell_pn_sar") or 0.0
            orig_per_night_1 = orig_pn_sar_1 * sar_to_pkr
            sell_per_night_1 = sell_pn_sar_1 * sar_to_pkr
    else:
        orig_per_night_1, sell_per_night_1 = 0.0, 0.0

orig_1 = orig_per_night_1 * nights_1 * num_rooms_1
sell_1 = sell_per_night_1 * nights_1 * num_rooms_1
if sell_1 > 0:
    sar_preview_1 = sell_1 / sar_to_pkr if sar_to_pkr > 0 else 0
    st.success(f"💱 Leg 1 Hotel Total ➔ **PKR {sell_1:,.2f}** | **SAR {sar_preview_1:,.2f}**")

# Leg 1 Transport
origin_label_1 = clean_city_name(cust_landing) if cust_landing != "-- Select Airport --" else "Airport Arrival"
dest_label_1 = clean_city_name(city_1)
route_title_1 = f"🚗 Transportation: {origin_label_1} ➔ {dest_label_1}" if (cust_landing != "-- Select Airport --" and city_1 != "-- Select City / Stop --") else "🚗 Transportation from Arrival to Leg 1"

st.markdown(f"#### {route_title_1}")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    trans_1 = st.selectbox(f"Vehicle ({origin_label_1} to {dest_label_1}):", vehicle_list, key="t1_vehicle")
with col_t2:
    t_curr_1 = st.radio("Currency (Transport 1):", ["PKR", "SAR"], horizontal=True, key="t_curr_1")
with col_t3:
    if t_curr_1 == "PKR":
        trans_orig_1 = st.number_input("Transport Org Cost 1 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t1_orig_pkr") or 0.0
        trans_sell_1 = st.number_input("Transport Sell Cost 1 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t1_sell_pkr") or 0.0
    else:
        t_orig_sar_1 = st.number_input("Transport Org Cost 1 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="t1_orig_sar") or 0.0
        t_sell_sar_1 = st.number_input("Transport Sell Cost 1 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="t1_sell_sar") or 0.0
        trans_orig_1 = t_orig_sar_1 * sar_to_pkr
        trans_sell_1 = t_sell_sar_1 * sar_to_pkr

if trans_sell_1 > 0:
    t_sar_1 = trans_sell_1 / sar_to_pkr if sar_to_pkr > 0 else 0
    st.success(f"💱 Transport 1 Total ➔ **PKR {trans_sell_1:,.2f}** | **SAR {t_sar_1:,.2f}**")

# Stay Leg 2
city_2, nights_2, orig_2, sell_2, category_2, hotel_2 = "-- None --", 0, 0.0, 0.0, "N/A", "N/A"
bed_type_2, num_rooms_2, meal_plan_2 = "N/A", 1, "N/A"
trans_2, trans_orig_2, trans_sell_2 = "-- Select Transport --", 0.0, 0.0

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
        elif is_airport_stop_2:
            st.info("ℹ️ Airport Stop selected: No hotel stay required.")
    with col_s6:
        if not is_airport_stop_2 and city_2 != "-- Select City / Stop --":
            curr_type_2 = st.radio("Currency (Leg 2 Hotel):", ["PKR", "SAR"], horizontal=True, key="curr_type_2")
            if curr_type_2 == "PKR":
                orig_pn_2 = st.number_input("Original Cost Per Night 2 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="c2_orig_pn_pkr") or 0.0
                sell_pn_2 = st.number_input("Selling Price Per Night 2 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="c2_sell_pn_pkr") or 0.0
                orig_per_night_2, sell_per_night_2 = orig_pn_2, sell_pn_2
            else:
                orig_pn_sar_2 = st.number_input("Original Cost Per Night 2 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c2_orig_pn_sar") or 0.0
                sell_pn_sar_2 = st.number_input("Selling Price Per Night 2 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c2_sell_pn_sar") or 0.0
                orig_per_night_2 = orig_pn_sar_2 * sar_to_pkr
                sell_per_night_2 = sell_pn_sar_2 * sar_to_pkr
        else:
            orig_per_night_2, sell_per_night_2 = 0.0, 0.0

    orig_2 = orig_per_night_2 * nights_2 * num_rooms_2
    sell_2 = sell_per_night_2 * nights_2 * num_rooms_2
    if sell_2 > 0:
        sar_preview_2 = sell_2 / sar_to_pkr if sar_to_pkr > 0 else 0
        st.success(f"💱 Leg 2 Hotel Total ➔ **PKR {sell_2:,.2f}** | **SAR {sar_preview_2:,.2f}**")

    # Leg 2 Transport
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
            trans_orig_2 = st.number_input("Transport Org Cost 2 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t2_orig_pkr") or 0.0
            trans_sell_2 = st.number_input("Transport Sell Cost 2 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t2_sell_pkr") or 0.0
        else:
            t_orig_sar_2 = st.number_input("Transport Org Cost 2 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="t2_orig_sar") or 0.0
            t_sell_sar_2 = st.number_input("Transport Sell Cost 2 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="t2_sell_sar") or 0.0
            trans_orig_2 = t_orig_sar_2 * sar_to_pkr
            trans_sell_2 = t_sell_sar_2 * sar_to_pkr

    if trans_sell_2 > 0:
        t_sar_2 = trans_sell_2 / sar_to_pkr if sar_to_pkr > 0 else 0
        st.success(f"💱 Transport 2 Total ➔ **PKR {trans_sell_2:,.2f}** | **SAR {t_sar_2:,.2f}**")

# Stay Leg 3 (Extra Destination Option)
city_3, nights_3, orig_3, sell_3, category_3, hotel_3 = "-- None --", 0, 0.0, 0.0, "N/A", "N/A"
bed_type_3, num_rooms_3, meal_plan_3 = "N/A", 1, "N/A"
trans_3, trans_orig_3, trans_sell_3 = "-- Select Transport --", 0.0, 0.0

if (city_2 != "-- Select City / Stop --") and (("Airport" in city_2) or nights_2 > 0):
    st.markdown("---")
    st.markdown("### 🧳 Stay Leg 3 (Additional Destination / Extra Stop)")
    col_s7, col_s8, col_s9 = st.columns(3)
    with col_s7:
        city_3 = st.selectbox("Select City 3:", cities_list, key="c3_city")
        is_airport_stop_3 = ("Airport" in city_3)
        nights_3 = 0 if is_airport_stop_3 else st.number_input("Nights in City 3:", min_value=0, value=0, step=1, key="c3_nights")
    with col_s8:
        if city_3 != "-- Select City / Stop --" and not is_airport_stop_3:
            category_3 = st.selectbox("Category 3:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy", "Apartment"], key="c3_cat")
            hotel_3 = st.selectbox("Hotel / Property 3:", get_hotel_list(city_3), key="c3_hotel")
            num_rooms_3 = st.number_input("Number of Rooms (Leg 3):", min_value=1, value=1, step=1, key="c3_num_rooms")
            bed_types_options_3 = ["Double bed", "Triple bed", "Quad bed", "Quint bed", "Hexa bed", "City view"]
            if "Makkah" in city_3:
                bed_types_options_3.extend(["Kaba view", "Haram view"])
            bed_type_3 = st.selectbox("Bed / View Type (Leg 3):", bed_types_options_3, key="c3_bed_type")
            meal_plan_3 = st.selectbox("Meal Plan (Leg 3):", ["Breakfast", "Room Only"], key="c3_meal")
        elif is_airport_stop_3:
            st.info("ℹ️ Airport Stop selected: No hotel stay required.")
    with col_s9:
        if city_3 != "-- Select City / Stop --":
            if not is_airport_stop_3:
                curr_type_3 = st.radio("Currency (Leg 3 Hotel):", ["PKR", "SAR"], horizontal=True, key="curr_type_3")
                if curr_type_3 == "PKR":
                    orig_pn_3 = st.number_input("Original Cost Per Night 3 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="c3_orig_pn_pkr") or 0.0
                    sell_pn_3 = st.number_input("Selling Price Per Night 3 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="c3_sell_pn_pkr") or 0.0
                    orig_per_night_3, sell_per_night_3 = orig_pn_3, sell_pn_3
                else:
                    orig_pn_sar_3 = st.number_input("Original Cost Per Night 3 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c3_orig_pn_sar") or 0.0
                    sell_pn_sar_3 = st.number_input("Selling Price Per Night 3 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c3_sell_pn_sar") or 0.0
                    orig_per_night_3 = orig_pn_sar_3 * sar_to_pkr
                    sell_per_night_3 = sell_pn_sar_3 * sar_to_pkr
            else:
                orig_per_night_3, sell_per_night_3 = 0.0, 0.0
            
            orig_3 = orig_per_night_3 * nights_3 * num_rooms_3
            sell_3 = sell_per_night_3 * nights_3 * num_rooms_3
    
    if sell_3 > 0:
        sar_preview_3 = sell_3 / sar_to_pkr if sar_to_pkr > 0 else 0
        st.success(f"💱 Leg 3 Hotel Total ➔ **PKR {sell_3:,.2f}** | **SAR {sar_preview_3:,.2f}**")

    if city_3 != "-- Select City / Stop --":
        origin_label_3 = clean_city_name(city_2)
        dest_label_3 = clean_city_name(city_3)
        route_title_3 = f"🚗 Transportation: {origin_label_3} ➔ {dest_label_3}"

        st.markdown(f"#### {route_title_3}")
        col_t7, col_t8, col_t9 = st.columns(3)
        with col_t7:
            trans_3 = st.selectbox(f"Vehicle ({origin_label_3} to {dest_label_3}):", vehicle_list, key="t3_vehicle")
        with col_t8:
            t_curr_3 = st.radio("Currency (Transport 3):", ["PKR", "SAR"], horizontal=True, key="t_curr_3")
        with col_t9:
            if t_curr_3 == "PKR":
                trans_orig_3 = st.number_input("Transport Org Cost 3 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t3_orig_pkr") or 0.0
                trans_sell_3 = st.number_input("Transport Sell Cost 3 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t3_sell_pkr") or 0.0
            else:
                t_orig_sar_3 = st.number_input("Transport Org Cost 3 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="t3_orig_sar") or 0.0
                t_sell_sar_3 = st.number_input("Transport Sell Cost 3 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="t3_sell_sar") or 0.0
                trans_orig_3 = t_orig_sar_3 * sar_to_pkr
                trans_sell_3 = t_sell_sar_3 * sar_to_pkr

        if trans_sell_3 > 0:
            t_sar_3 = trans_sell_3 / sar_to_pkr if sar_to_pkr > 0 else 0
            st.success(f"💱 Transport 3 Total ➔ **PKR {trans_sell_3:,.2f}** | **SAR {t_sar_3:,.2f}**")

total_stay_nights = nights_1 + nights_2 + nights_3
hotels_orig_total = orig_1 + orig_2 + orig_3
hotels_sell_total = sell_1 + sell_2 + sell_3
hotels_total_profit = hotels_sell_total - hotels_orig_total

total_transport_orig = trans_orig_1 + trans_orig_2 + trans_orig_3
total_transport_sell = trans_sell_1 + trans_sell_2 + trans_sell_3
total_transport_profit = total_transport_sell - total_transport_orig

hotels_sar_total = hotels_sell_total / sar_to_pkr if sar_to_pkr > 0 else 0.0
transport_sar_total = total_transport_sell / sar_to_pkr if sar_to_pkr > 0 else 0.0

st.info(f"💡 Total Stays Duration: **{total_stay_nights} Nights** | Hotel Sell Total: **PKR {hotels_sell_total:,.2f}** | Transport Sell Total: **PKR {total_transport_sell:,.2f}**")

st.write("---")

# 4. ZIARATS MANAGEMENT SECTION (PROPER YES/NO & OPTIONS)
st.subheader("🗺️ Step 4: Ziarats Selection & Management")
col13, col14, col15 = st.columns(3)
with col13:
    ziarat_status = st.selectbox("Do you want Ziarats included?", ["-- Select Option --", "YES", "NO"], key="z_status")
    ziarat_scope = "-- Not Applicable --"
    if ziarat_status == "YES":
        ziarat_scope = st.selectbox("Select Ziarats Coverage Area:", ["-- Select Scope --", "MAKKAH ONLY", "MADINAH ONLY", "BOTH MAKKAH AND MADINAH"], key="z_scope")

with col14:
    ziarat_transport_type = "N/A"
    z_curr = "PKR"
    if ziarat_status == "YES":
        ziarat_transport_type = st.selectbox("Ziarat Transport Type:", vehicle_list, key="z_trans_type")
        z_curr = st.radio("Currency (Ziarats):", ["PKR", "SAR"], horizontal=True, key="z_curr")

with col15:
    ziarat_orig_cost, ziarat_sell_cost = 0.0, 0.0
    if ziarat_status == "YES":
        if z_curr == "PKR":
            ziarat_orig_cost = st.number_input("Ziarats Original Cost (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="z_orig_pkr") or 0.0
            ziarat_sell_cost = st.number_input("Ziarats Selling Price (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="z_sell_pkr") or 0.0
        else:
            z_orig_sar = st.number_input("Ziarats Original Cost (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="z_orig_sar") or 0.0
            z_sell_sar = st.number_input("Ziarats Selling Price (SAR):", min_value=0.0, value=None, step=100.0, format="%.2f", key="z_sell_sar") or 0.0
            ziarat_orig_cost = z_orig_sar * sar_to_pkr
            ziarat_sell_cost = z_sell_sar * sar_to_pkr

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
    st.markdown("#### ✈️ Return Flight (Depature from Airport)")
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
    
    if city_1 != "-- Select City / Stop --":
        is_ap1 = "Airport" in city_1
        t_route_desc_1 = f"{origin_label_1} ➔ {dest_label_1} ({trans_1})" if trans_1 != "-- Select Transport --" else f"{origin_label_1} ➔ {dest_label_1}"
        if not is_ap1:
            itinerary_html_rows += f"<tr><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>Leg 1</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>{city_1}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6;'><b>Hotel:</b> {hotel_1}<br><b>Stay:</b> {nights_1} Nights, {num_rooms_1} Room(s) | <b>Bed/View:</b> {bed_type_1} | <b>Meal:</b> {meal_plan_1}<br>🚗 <i>Transfer:</i> {t_route_desc_1}</td></tr>"
            share_text += f"\n\n▫️ *Leg 1 ({city_1}):*\n   • Hotel: {hotel_1}\n   • Stay: {nights_1} Nights | {num_rooms_1} Room(s)\n   • Bed/View: {bed_type_1} | Meal: {meal_plan_1}\n   • Transfer: {t_route_desc_1}"
        else:
            itinerary_html_rows += f"<tr><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>Leg 1</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>{city_1}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6;'>Airport Transit / Stop<br>🚗 <i>Transfer:</i> {t_route_desc_1}</td></tr>"
            share_text += f"\n\n▫️ *Leg 1 ({city_1}):*\n   • Airport Transit / Stop\n   • Transfer: {t_route_desc_1}"

    if city_2 != "-- Select City / Stop --":
        is_ap2 = "Airport" in city_2
        t_route_desc_2 = f"{origin_label_2} ➔ {dest_label_2} ({trans_2})" if trans_2 != "-- Select Transport --" else f"{origin_label_2} ➔ {dest_label_2}"
        if not is_ap2:
            itinerary_html_rows += f"<tr><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>Leg 2</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>{city_2}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6;'><b>Hotel:</b> {hotel_2}<br><b>Stay:</b> {nights_2} Nights, {num_rooms_2} Room(s) | <b>Bed/View:</b> {bed_type_2} | <b>Meal:</b> {meal_plan_2}<br>🚗 <i>Transfer:</i> {t_route_desc_2}</td></tr>"
            share_text += f"\n\n▫️ *Leg 2 ({city_2}):*\n   • Hotel: {hotel_2}\n   • Stay: {nights_2} Nights | {num_rooms_2} Room(s)\n   • Bed/View: {bed_type_2} | Meal: {meal_plan_2}\n   • Transfer: {t_route_desc_2}"
        else:
            itinerary_html_rows += f"<tr><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>Leg 2</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>{city_2}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6;'>Airport Transit / Stop<br>🚗 <i>Transfer:</i> {t_route_desc_2}</td></tr>"
            share_text += f"\n\n▫️ *Leg 2 ({city_2}):*\n   • Airport Transit / Stop\n   • Transfer: {t_route_desc_2}"

    if city_3 != "-- Select City / Stop --":
        is_ap3 = "Airport" in city_3
        t_route_desc_3 = f"{origin_label_3} ➔ {dest_label_3} ({trans_3})" if trans_3 != "-- Select Transport --" else f"{origin_label_3} ➔ {dest_label_3}"
        if not is_ap3:
            itinerary_html_rows += f"<tr><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>Leg 3</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>{city_3}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6;'><b>Hotel:</b> {hotel_3}<br><b>Stay:</b> {nights_3} Nights, {num_rooms_3} Room(s) | <b>Bed/View:</b> {bed_type_3} | <b>Meal:</b> {meal_plan_3}<br>🚗 <i>Transfer:</i> {t_route_desc_3}</td></tr>"
            share_text += f"\n\n▫️ *Leg 3 ({city_3}):*\n   • Hotel: {hotel_3}\n   • Stay: {nights_3} Nights | {num_rooms_3} Room(s)\n   • Bed/View: {bed_type_3} | Meal: {meal_plan_3}\n   • Transfer: {t_route_desc_3}"
        else:
            itinerary_html_rows += f"<tr><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>Leg 3</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top;'><b>{city_3}</b></td><td style='padding: 12px; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6;'>Airport Transit / Stop<br>🚗 <i>Transfer:</i> {t_route_desc_3}</td></tr>"
            share_text += f"\n\n▫️ *Leg 3 ({city_3}):*\n   • Airport Transit / Stop\n   • Transfer: {t_route_desc_3}"

    ziarat_text = f"{ziarat_scope} (Transport: {ziarat_transport_type})" if ziarat_status == "YES" else "Not Included"
    share_text += f"\n\n🗺️ *Ziarats:* {ziarat_text}"

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

    components.html(invoice_html, height=680, scrolling=True)
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