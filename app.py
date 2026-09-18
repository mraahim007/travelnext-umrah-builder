import streamlit as st
from datetime import date, timedelta
import urllib.parse

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

# 2. CUSTOMER DETAILS
st.subheader("👤 Step 2: Customer Details & Travel Dates")
col1, col2 = st.columns(2)
with col1:
    cust_first_name = st.text_input("First Name:", key="c_first_name")
    adults = st.number_input("Enter number of adults:", min_value=1, value=1, key="common_adults")
    trip_start_date = st.date_input("Overall Trip Start Date (Arrival Date):", value=date.today(), key="trip_start")
with col2:
    cust_last_name = st.text_input("Last Name:", key="c_last_name")
    children = st.number_input("Enter number of children:", min_value=0, value=0, key="common_children")

total_people = adults + children
st.info(f"👉 Total Family Members: **{total_people}** ({adults} Adults, {children} Children)")

st.write("---")

# 3. FLIGHT DETAILS
st.subheader("✈️ Step 3: Flight Information")
col3, col4 = st.columns(2)
with col3:
    cust_airline = st.selectbox("Select Airline Name:", ["-- Select Airline --", "Saudia Airlines", "PIA", "AirBlue", "SereneAir", "Fly Jinnah", "Emirates", "Qatar Airways"], key="c_air")
with col4:
    cust_landing = st.selectbox("Arrival Airport (Landing City):", ["-- Select Airport --", "Jeddah Airport (JED)", "Madinah Airport (MED)"], key="c_land")

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
            "⭐⭐⭐⭐⭐ Makkah Clock Royal Tower, A Fairmont Hotel (0 km)",
            "⭐⭐⭐⭐⭐ Swissôtel Makkah (0 km)",
            "⭐⭐⭐⭐⭐ Swissôtel Al Maqam Makkah (0 km)",
            "⭐⭐⭐⭐⭐ Pullmann Zamzam Makkah (0 km)",
            "⭐⭐⭐⭐⭐ Address Jabal Omar Makkah (200–300m)",
            "⭐⭐⭐⭐⭐ Conrad Jabal Omar Makkah (300m)",
            "⭐⭐⭐⭐⭐ Jabal Omar Hyatt Regency Makkah (500m)",
            "⭐⭐⭐⭐⭐ Hilton Suites Jabal Omar Makkah (300–400m)",
            "⭐⭐⭐⭐⭐ InterContinental Dar Al Tawhid Makkah (0 km)",
            "⭐⭐⭐⭐ Voco Makkah (1.8 - 2 km / Shuttle)",
            "⭐⭐⭐⭐ Mercure Makkah Aziziah (4 - 5 km)",
            "⭐⭐⭐⭐ Emaar Royal Hotel (700 - 800m)",
            "⭐⭐⭐ Al Kiswah Towers (1.5 - 1.7 km / Shuttle)",
            "⭐⭐⭐ Snood Hotel (1.5 km)",
            "⭐⭐⭐ Qilla Ajyad Hotel (600 - 700m)"
        ]
    elif city == "Al-Madinah Al-Munawwarah":
        return [
            "-- Select Specific Hotel --",
            "⭐⭐⭐⭐⭐ Anwar Al Madinah Movenpick Hotel (100m)",
            "⭐⭐⭐⭐⭐ Crowne Plaza Madinah (200m)",
            "⭐⭐⭐⭐⭐ Oberoi Madinah (100m)",
            "⭐⭐⭐⭐⭐ Dar Al Taqwa Hotel (0-50m)",
            "⭐⭐⭐⭐⭐ Pullman Zamzam Madinah (150m)",
            "⭐⭐⭐⭐ Dallah Taiba Hotel (50-100m)",
            "⭐⭐⭐⭐ Al Aqeeq Madinah Hotel (200–300m)",
            "⭐⭐⭐⭐ Leader Muna Kareem Hotel (150–200m)",
            "⭐⭐⭐⭐ Swiss International Hotel (500m)",
            "⭐⭐⭐ Mysk Touch Hotel (700 - 800m)",
            "⭐⭐⭐ Plaza Inn Ohud (900m / Shuttle)",
            "⭐⭐⭐ Manazil Al Marjan (600m)"
        ]
    return ["-- Select Specific Hotel --"]

# 4. STEP-BY-STEP DYNAMIC STAY & TRANSPORT BUILDER
st.subheader("🏨 Step 4: Step-by-Step Hotel Stay & City Transport Builder")
st.markdown("Configure your stay legs. Enter values either in **PKR** or **SAR**:")

# Stay Leg 1 (Mandatory)
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
        category_1 = st.selectbox("Category 1:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c1_cat")
        hotel_1 = st.selectbox("Hotel 1:", get_hotel_list(city_1), key="c1_hotel")
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
            orig_per_night_1 = orig_pn_1
            sell_per_night_1 = sell_pn_1
        else:
            orig_pn_sar_1 = st.number_input("Original Cost Per Night 1 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c1_orig_pn_sar") or 0.0
            sell_pn_sar_1 = st.number_input("Selling Price Per Night 1 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c1_sell_pn_sar") or 0.0
            orig_per_night_1 = orig_pn_sar_1 * sar_to_pkr
            sell_per_night_1 = sell_pn_sar_1 * sar_to_pkr
    else:
        orig_per_night_1 = 0.0
        sell_per_night_1 = 0.0

orig_1 = orig_per_night_1 * nights_1 * num_rooms_1
sell_1 = sell_per_night_1 * nights_1 * num_rooms_1

if sell_1 > 0:
    sar_preview_1 = sell_1 / sar_to_pkr if sar_to_pkr > 0 else 0
    st.success(f"💱 Leg 1 Hotel Total ({nights_1} Nights, {num_rooms_1} Room(s)) ➔ **PKR {sell_1:,.2f}** | **SAR {sar_preview_1:,.2f}**")

# Leg 1 Transport
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    trans_1 = st.selectbox("Transport from Leg 1:", vehicle_list, key="t1_vehicle")
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
            category_2 = st.selectbox("Category 2:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c2_cat")
            hotel_2 = st.selectbox("Hotel 2:", get_hotel_list(city_2), key="c2_hotel")
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
                orig_per_night_2 = orig_pn_2
                sell_per_night_2 = sell_pn_2
            else:
                orig_pn_sar_2 = st.number_input("Original Cost Per Night 2 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c2_orig_pn_sar") or 0.0
                sell_pn_sar_2 = st.number_input("Selling Price Per Night 2 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c2_sell_pn_sar") or 0.0
                orig_per_night_2 = orig_pn_sar_2 * sar_to_pkr
                sell_per_night_2 = sell_pn_sar_2 * sar_to_pkr
        else:
            orig_per_night_2 = 0.0
            sell_per_night_2 = 0.0

    orig_2 = orig_per_night_2 * nights_2 * num_rooms_2
    sell_2 = sell_per_night_2 * nights_2 * num_rooms_2

    if sell_2 > 0:
        sar_preview_2 = sell_2 / sar_to_pkr if sar_to_pkr > 0 else 0
        st.success(f"💱 Leg 2 Hotel Total ({nights_2} Nights, {num_rooms_2} Room(s)) ➔ **PKR {sell_2:,.2f}** | **SAR {sar_preview_2:,.2f}**")

    # Leg 2 Transport
    col_t4, col_t5, col_t6 = st.columns(3)
    with col_t4:
        trans_2 = st.selectbox("Transport from Leg 2:", vehicle_list, key="t2_vehicle")
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

# Stay Leg 3
city_3, nights_3, orig_3, sell_3, category_3, hotel_3 = "-- None --", 0, 0.0, 0.0, "N/A", "N/A"
bed_type_3, num_rooms_3, meal_plan_3 = "N/A", 1, "N/A"
trans_3, trans_orig_3, trans_sell_3 = "-- Select Transport --", 0.0, 0.0

if (city_2 != "-- Select City / Stop --") and (("Airport" in city_2) or nights_2 > 0):
    st.markdown("---")
    st.markdown("### 🧳 Stay Leg 3 (Optional Final Stop)")
    col_s7, col_s8, col_s9 = st.columns(3)
    with col_s7:
        city_3 = st.selectbox("Select City 3:", cities_list, key="c3_city")
        is_airport_stop_3 = ("Airport" in city_3)
        nights_3 = 0 if is_airport_stop_3 else st.number_input("Nights in City 3:", min_value=0, value=0, step=1, key="c3_nights")
    with col_s8:
        if city_3 != "-- Select City / Stop --" and not is_airport_stop_3:
            category_3 = st.selectbox("Category 3:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c3_cat")
            hotel_3 = st.selectbox("Hotel 3:", get_hotel_list(city_3), key="c3_hotel")
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
                    orig_per_night_3 = orig_pn_3
                    sell_per_night_3 = sell_pn_3
                else:
                    orig_pn_sar_3 = st.number_input("Original Cost Per Night 3 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c3_orig_pn_sar") or 0.0
                    sell_pn_sar_3 = st.number_input("Selling Price Per Night 3 (SAR):", min_value=0.0, value=None, step=50.0, format="%.2f", key="c3_sell_pn_sar") or 0.0
                    orig_per_night_3 = orig_pn_sar_3 * sar_to_pkr
                    sell_per_night_3 = sell_pn_sar_3 * sar_to_pkr
            else:
                orig_per_night_3 = 0.0
                sell_per_night_3 = 0.0
            
            orig_3 = orig_per_night_3 * nights_3 * num_rooms_3
            sell_3 = sell_per_night_3 * nights_3 * num_rooms_3
    
    if sell_3 > 0:
        sar_preview_3 = sell_3 / sar_to_pkr if sar_to_pkr > 0 else 0
        st.success(f"💱 Leg 3 Hotel Total ({nights_3} Nights, {num_rooms_3} Room(s)) ➔ **PKR {sell_3:,.2f}** | **SAR {sar_preview_3:,.2f}**")

    if city_3 != "-- Select City / Stop --":
        # Leg 3 Transport
        col_t7, col_t8, col_t9 = st.columns(3)
        with col_t7:
            trans_3 = st.selectbox("Transport from Leg 3:", vehicle_list, key="t3_vehicle")
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

st.info(f"💡 Total Stays Duration: **{total_stay_nights} Nights** | Hotel Sell Total: **PKR {hotels_sell_total:,.2f} ~ SAR {hotels_sar_total:,.2f}** | Transport Sell Total: **PKR {total_transport_sell:,.2f} ~ SAR {transport_sar_total:,.2f}**")

st.write("---")

# 5. ZIARATS MANAGEMENT SECTION
st.subheader("🗺️ Step 5: Ziarats Selection & Management")
col13, col14, col15 = st.columns(3)
with col13:
    ziarat_status = st.selectbox("Do you want Ziarats included?", ["-- Select Option --", "YES", "NO"], key="z_status")
    ziarat_scope = "-- Not Applicable --"
    if ziarat_status == "YES":
        ziarat_scope = st.selectbox("Select Ziarats Coverage Area:", ["-- Select Scope --", "MAKKAH ONLY", "MADINAH ONLY", "BOTH MAKKAH AND MADINAH"], key="z_scope")

with col14:
    ziarat_transport_type = st.selectbox("Ziarat Transport Type:", vehicle_list, key="z_trans_type")
    z_curr = st.radio("Currency (Ziarats):", ["PKR", "SAR"], horizontal=True, key="z_curr")

with col15:
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

# 6. VISA & AIRFARE
st.subheader("🎫 Step 6: Visa + Airfare (Per Person Rates)")
col17, col18, col19 = st.columns(3)
with col17:
    va_curr = st.radio("Currency (Visa & Airfare PP):", ["PKR", "SAR"], horizontal=True, key="va_curr")
with col18:
    if va_curr == "PKR":
        visa_air_orig_pp = st.number_input("Original Cost Per Person (PKR):", min_value=0.0, value=None, step=5000.0, format="%.2f", key="va_orig_pp_pkr") or 0.0
    else:
        va_orig_sar_pp = st.number_input("Original Cost Per Person (SAR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="va_orig_pp_sar") or 0.0
        visa_air_orig_pp = va_orig_sar_pp * sar_to_pkr
with col19:
    if va_curr == "PKR":
        visa_air_sell_pp = st.number_input("Selling Price Per Person (PKR):", min_value=0.0, value=None, step=5000.0, format="%.2f", key="va_sell_pp_pkr") or 0.0
    else:
        visa_sell_sar_pp = st.number_input("Selling Price Per Person (SAR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="va_sell_sar_pp") or 0.0
        visa_air_sell_pp = visa_sell_sar_pp * sar_to_pkr

visa_air_orig = visa_air_orig_pp * total_people
visa_air_sell = visa_air_sell_pp * total_people

visa_profit = visa_air_sell - visa_air_orig
visa_sar = visa_air_sell / sar_to_pkr if sar_to_pkr > 0 else 0.0

if visa_air_sell > 0:
    st.success(f"👥 Total Travelers: {total_people} | Visa & Airfare Total ➔ **PKR {visa_air_sell:,.2f}** | **SAR {visa_sar:,.2f}**")

grand_total_selling = hotels_sell_total + total_transport_sell + ziarat_sell_cost + visa_air_sell
grand_total_original = hotels_orig_total + total_transport_orig + ziarat_orig_cost + visa_air_orig
total_agency_net_profit = grand_total_selling - grand_total_original
grand_total_sar = grand_total_selling / sar_to_pkr if sar_to_pkr > 0 else 0.0

st.write("---")

# 7. OFFICIAL CUSTOMER QUOTATION (PRINTABLE SHEET STYLE) WITH WHATSAPP SHARE BUTTON
st.subheader("📄 Step 7: Official Customer Quotation & Share")
if st.button("Generate Quotation 📋", key="btn_gen_quotation"):
    st.success("Quotation Generated Successfully!")
    
    share_text = f"""*TRAVELNEXT INTERNATIONAL*
Official Umrah Packages & Travel Services
----------------------------------
Client Name: {cust_first_name or 'Valued'} {cust_last_name or 'Customer'}
Travel Date: {trip_start_date.strftime('%d %b %Y')}
Total Travelers: {total_people} Persons ({adults} Adults, {children} Children)
Total Duration: {total_stay_nights} Nights
Airline: {cust_airline if cust_airline != '-- Select Airline --' else 'N/A'}
Landing Airport: {cust_landing if cust_landing != '-- Select Airport --' else 'N/A'}
----------------------------------
Itinerary:"""

    itinerary_html_rows = ""
    
    if city_1 != "-- Select City / Stop --":
        is_ap1 = "Airport" in city_1
        if not is_ap1:
            itinerary_html_rows += f"<tr><td><b>Leg 1</b></td><td><b>{city_1}</b></td><td>{hotel_1}<br>{nights_1} Nights, {num_rooms_1} Room(s) ({bed_type_1}), Meal: {meal_plan_1}<br>Transport: {trans_1}</td></tr>"
            share_text += f"\n- Leg 1 ({city_1}): {hotel_1} ({nights_1} Nights, {num_rooms_1} Room(s), {bed_type_1}, {meal_plan_1})"
        else:
            itinerary_html_rows += f"<tr><td><b>Leg 1</b></td><td><b>{city_1}</b></td><td>Airport Transit / Stop<br>Transport: {trans_1}</td></tr>"
            share_text += f"\n- Leg 1 ({city_1})"

    if city_2 != "-- Select City / Stop --":
        is_ap2 = "Airport" in city_2
        if not is_ap2:
            itinerary_html_rows += f"<tr><td><b>Leg 2</b></td><td><b>{city_2}</b></td><td>{hotel_2}<br>{nights_2} Nights, {num_rooms_2} Room(s) ({bed_type_2}), Meal: {meal_plan_2}<br>Transport: {trans_2}</td></tr>"
            share_text += f"\n- Leg 2 ({city_2}): {hotel_2} ({nights_2} Nights, {num_rooms_2} Room(s), {bed_type_2}, {meal_plan_2})"
        else:
            itinerary_html_rows += f"<tr><td><b>Leg 2</b></td><td><b>{city_2}</b></td><td>Airport Transit / Stop<br>Transport: {trans_2}</td></tr>"
            share_text += f"\n- Leg 2 ({city_2})"

    if city_3 != "-- Select City / Stop --":
        is_ap3 = "Airport" in city_3
        if not is_ap3:
            itinerary_html_rows += f"<tr><td><b>Leg 3</b></td><td><b>{city_3}</b></td><td>{hotel_3}<br>{nights_3} Nights, {num_rooms_3} Room(s) ({bed_type_3}), Meal: {meal_plan_3}<br>Transport: {trans_3}</td></tr>"
            share_text += f"\n- Leg 3 ({city_3}): {hotel_3} ({nights_3} Nights, {num_rooms_3} Room(s), {bed_type_3}, {meal_plan_3})"
        else:
            itinerary_html_rows += f"<tr><td><b>Leg 3</b></td><td><b>{city_3}</b></td><td>Airport Transit / Stop<br>Transport: {trans_3}</td></tr>"
            share_text += f"\n- Leg 3 ({city_3})"

    ziarat_text = f"{ziarat_scope} (Transport: {ziarat_transport_type})" if ziarat_status == "YES" else "Not Included"
    share_text += f"\n- Ziarats: {ziarat_text}"

    share_text += f"\n----------------------------------\nTOTAL PACKAGE INVESTMENT: PKR {grand_total_selling:,.2f} (~ SAR {grand_total_sar:,.2f})\n----------------------------------\nThanks for choosing TravelNext. Aao Madiney Chalen!"

    # PROPER PRINTABLE INVOICE HTML CARD DESIGN
    invoice_html = f"""
    <div style="background-color: #ffffff; color: #111111; padding: 25px; border-radius: 12px; border: 2px solid #2e8b57; box-shadow: 0 4px 10px rgba(0,0,0,0.1); font-family: Arial, sans-serif;">
        <div style="text-align: center; border-bottom: 2px solid #2e8b57; padding-bottom: 10px; margin-bottom: 15px;">
            <h2 style="color: #2e8b57; margin: 0;">TRAVELNEXT INTERNATIONAL</h2>
            <p style="margin: 5px 0; font-size: 14px; color: #555;">Official Umrah Packages & Travel Services | Aao Madiney Chalen</p>
        </div>
        
        <table style="width: 100%; font-size: 14px; margin-bottom: 15px;">
            <tr>
                <td><b>Client Name:</b> {cust_first_name or 'Valued'} {cust_last_name or 'Customer'}</td>
                <td><b>Travel Date:</b> {trip_start_date.strftime('%d %b %Y')}</td>
            </tr>
            <tr>
                <td><b>Total Travelers:</b> {total_people} Persons ({adults} Adults, {children} Children)</td>
                <td><b>Airline:</b> {cust_airline if cust_airline != '-- Select Airline --' else 'N/A'}</td>
            </tr>
            <tr>
                <td><b>Total Duration:</b> {total_stay_nights} Nights</td>
                <td><b>Landing Airport:</b> {cust_landing if cust_landing != '-- Select Airport --' else 'N/A'}</td>
            </tr>
        </table>
        
        <h4 style="border-bottom: 1px solid #ddd; padding-bottom: 5px; color: #333;">Hotel Itinerary & Transport Breakdown</h4>
        <table style="width: 100%; font-size: 13px; border-collapse: collapse; margin-bottom: 15px;">
            <tr style="background-color: #f2f9f5; text-align: left;">
                <th style="padding: 8px; border: 1px solid #ddd;">Leg</th>
                <th style="padding: 8px; border: 1px solid #ddd;">City / Stop</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Details & Services</th>
            </tr>
            {itinerary_html_rows}
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><b>Ziarats</b></td>
                <td style="padding: 8px; border: 1px solid #ddd;" colspan="2">{ziarat_text}</td>
            </tr>
        </table>
        
        <div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center; border: 1px dashed #2e8b57;">
            <h3 style="margin: 0; color: #2e8b57;">TOTAL PACKAGE INVESTMENT: PKR {grand_total_selling:,.2f}</h3>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #444;">Equivalent to approx. SAR {grand_total_sar:,.2f}</p>
        </div>
        
        <p style="text-align: center; font-size: 12px; color: #777; margin-top: 15px;">Thanks for choosing TravelNext. May Allah accept your good deeds!</p>
    </div>
    """

    st.markdown(invoice_html, unsafe_allow_html=True)
    st.write("")

    encoded_text = urllib.parse.quote(share_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:12px 20px; border:none; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer; width: 100%;">📤 Share Quotation via WhatsApp</button></a>', unsafe_allow_html=True)
    st.write("---")

# 8. AGENCY PROFIT DASHBOARD
st.subheader("📊 Step 8: Internal Agency Profit & Cost Breakdown")
if st.button("Show Internal Profit Sheet 📈", key="btn_profit_sheet"):
    agency_sar_profit = total_agency_net_profit / sar_to_pkr if sar_to_pkr > 0 else 0
    st.markdown(f"""
    ### 💼 FINANCIAL MARGIN REPORT (For Office Use Only)
    - **Hotels Stays Total ({total_stay_nights} Nights):** PKR {hotels_sell_total:,.2f} | SAR {hotels_sar_total:,.2f}  *(Profit: PKR {hotels_total_profit:,.2f})*
    - **City Transports Total:** PKR {total_transport_sell:,.2f} | SAR {transport_sar_total:,.2f}  *(Profit: PKR {total_transport_profit:,.2f})*
    - **Ziarats Total:** PKR {ziarat_sell_cost:,.2f} | SAR {ziarat_sar:,.2f}  *(Profit: PKR {ziarat_profit:,.2f})*
    - **Visa & Airfare Total ({total_people} Persons):** PKR {visa_air_sell:,.2f} | SAR {visa_sar:,.2f}  *(Profit: PKR {visa_profit:,.2f})*
    
    ---
    ### 🔥 TOTAL NET PROFIT FOR AGENCY: PKR {total_agency_net_profit:,.2f}  |  SAR {agency_sar_profit:,.2f}
    """)
    st.balloons()