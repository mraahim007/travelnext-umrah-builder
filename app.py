import streamlit as st
from datetime import date, timedelta

# Page Configuration
st.set_page_config(page_title="TravelNext Umrah Builder", page_icon="🕋", layout="wide")

# CUSTOM BLACK THEME WITH CLEAN FOCUS BORDERS
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    label, p, span {
        color: #e0e0e0 !important;
    }
    .stAlert {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
    }
    .stButton>button {
        background-color: #1b4d3e !important;
        color: #ffffff !important;
        border: 1px solid #2e8b57 !important;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2e8b57 !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
    }
    div.stTextInput > div > div > input:focus, 
    div.stNumberInput > div > div > input:focus,
    div.stSelectbox > div > div > div:focus {
        border-color: #2e8b57 !important;
        box-shadow: 0 0 5px #2e8b57 !important;
    }
    hr {
        border-color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>✨ TRAVELNEXT - SMART UMRAH BUILDER ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #2e8b57; font-size: 18px; font-weight: bold;'>Aao Madiney Chalen 🕋</p>", unsafe_allow_html=True)
st.write("---")

# 1. CURRENCY EXCHANGE RATE
st.subheader("💱 Step 1: Daily Currency Exchange Rate")
sar_to_pkr = st.number_input("Enter current 1 SAR to PKR rate today:", min_value=0.1, max_value=100.0, value=75.0, step=0.5, key="daily_sar_rate")
st.info(f"💡 Active Exchange Rate: **1 SAR = {sar_to_pkr:,.2f} PKR**")

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

# CITIES & HOTELS LISTS
cities_list = ["-- Select City --", "Makkah Al-Mukarramah", "Al-Madinah Al-Munawwarah", "Jeddah (Airport / Transit Only - No Hotel Stay)"]
vehicle_list = ["-- Select Transport --", "Private Sedan / Car", "Private Hiace / Van", "Private GMC Yukon / VIP", "Private Coaster Saloon", "Haramain High-Speed Train", "Shared Bus Group"]

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
st.markdown("Configure your stay legs and local transport leg-by-leg dynamically:")

# Stay Leg 1 (Mandatory)
st.markdown("### 🧳 Stay Leg 1 (First Stop)")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    city_1 = st.selectbox("Select City 1:", cities_list, key="c1_city")
    is_jeddah_1 = ("Jeddah" in city_1)
    nights_1 = 0 if is_jeddah_1 else st.number_input("Nights in City 1:", min_value=0, value=0, step=1, key="c1_nights")
with col_s2:
    category_1, hotel_1 = "N/A", "N/A"
    if not is_jeddah_1:
        category_1 = st.selectbox("Category 1:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c1_cat")
        hotel_1 = st.selectbox("Hotel 1:", get_hotel_list(city_1), key="c1_hotel")
    else:
        st.info("ℹ️ Jeddah selected: No hotel stay required.")
with col_s3:
    orig_1 = 0.0 if is_jeddah_1 else (st.number_input("Original Cost 1 (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="c1_orig") or 0.0)
    sell_1 = 0.0 if is_jeddah_1 else (st.number_input("Selling Price 1 (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="c1_sell") or 0.0)

if sell_1 > 0:
    sar_preview_1 = sell_1 / sar_to_pkr if sar_to_pkr > 0 else 0
    st.caption(f"💱 Leg 1 Selling: **PKR {sell_1:,.2f} ~ SAR {sar_preview_1:,.2f}**")

# Leg 1 Transport
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    trans_1 = st.selectbox("Transport from Leg 1:", vehicle_list, key="t1_vehicle")
with col_t2:
    trans_orig_1 = st.number_input("Transport Org Cost 1 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t1_orig") or 0.0
with col_t3:
    trans_sell_1 = st.number_input("Transport Sell Cost 1 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t1_sell") or 0.0

if trans_sell_1 > 0:
    t_sar_1 = trans_sell_1 / sar_to_pkr if sar_to_pkr > 0 else 0
    st.caption(f"💱 Transport 1 Selling: **PKR {trans_sell_1:,.2f} ~ SAR {t_sar_1:,.2f}**")

# Stay Leg 2 (Appears only if Leg 1 is filled)
city_2, nights_2, orig_2, sell_2, category_2, hotel_2 = "-- None --", 0, 0.0, 0.0, "N/A", "N/A"
trans_2, trans_orig_2, trans_sell_2 = "-- Select Transport --", 0.0, 0.0

if (city_1 != "-- Select City --") and (is_jeddah_1 or nights_1 > 0):
    st.markdown("---")
    st.markdown("### 🧳 Stay Leg 2 (Next Stop)")
    col_s4, col_s5, col_s6 = st.columns(3)
    with col_s4:
        city_2 = st.selectbox("Select City 2:", cities_list, key="c2_city")
        is_jeddah_2 = ("Jeddah" in city_2)
        nights_2 = 0 if is_jeddah_2 else st.number_input("Nights in City 2:", min_value=0, value=0, step=1, key="c2_nights")
    with col_s5:
        if not is_jeddah_2:
            category_2 = st.selectbox("Category 2:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c2_cat")
            hotel_2 = st.selectbox("Hotel 2:", get_hotel_list(city_2), key="c2_hotel")
        else:
            st.info("ℹ️ Jeddah selected: No hotel stay required.")
    with col_s6:
        orig_2 = 0.0 if is_jeddah_2 else (st.number_input("Original Cost 2 (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="c2_orig") or 0.0)
        sell_2 = 0.0 if is_jeddah_2 else (st.number_input("Selling Price 2 (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="c2_sell") or 0.0)

    if sell_2 > 0:
        sar_preview_2 = sell_2 / sar_to_pkr if sar_to_pkr > 0 else 0
        st.caption(f"💱 Leg 2 Selling: **PKR {sell_2:,.2f} ~ SAR {sar_preview_2:,.2f}**")

    # Leg 2 Transport
    col_t4, col_t5, col_t6 = st.columns(3)
    with col_t4:
        trans_2 = st.selectbox("Transport from Leg 2:", vehicle_list, key="t2_vehicle")
    with col_t5:
        trans_orig_2 = st.number_input("Transport Org Cost 2 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t2_orig") or 0.0
    with col_t6:
        trans_sell_2 = st.number_input("Transport Sell Cost 2 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t2_sell") or 0.0

    if trans_sell_2 > 0:
        t_sar_2 = trans_sell_2 / sar_to_pkr if sar_to_pkr > 0 else 0
        st.caption(f"💱 Transport 2 Selling: **PKR {trans_sell_2:,.2f} ~ SAR {t_sar_2:,.2f}**")

# Stay Leg 3 (Appears only if Leg 2 is filled)
city_3, nights_3, orig_3, sell_3, category_3, hotel_3 = "-- None --", 0, 0.0, 0.0, "N/A", "N/A"
trans_3, trans_orig_3, trans_sell_3 = "-- Select Transport --", 0.0, 0.0

if (city_2 != "-- Select City --") and (("Jeddah" in city_2) or nights_2 > 0):
    st.markdown("---")
    st.markdown("### 🧳 Stay Leg 3 (Optional Final Stop)")
    col_s7, col_s8, col_s9 = st.columns(3)
    with col_s7:
        city_3 = st.selectbox("Select City 3:", cities_list, key="c3_city")
        is_jeddah_3 = ("Jeddah" in city_3)
        nights_3 = 0 if is_jeddah_3 else st.number_input("Nights in City 3:", min_value=0, value=0, step=1, key="c3_nights")
    with col_s8:
        if city_3 != "-- Select City --" and not is_jeddah_3:
            category_3 = st.selectbox("Category 3:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c3_cat")
            hotel_3 = st.selectbox("Hotel 3:", get_hotel_list(city_3), key="c3_hotel")
        elif is_jeddah_3:
            st.info("ℹ️ Jeddah selected: No hotel stay required.")
    with col_s9:
        if city_3 != "-- Select City --":
            orig_3 = 0.0 if is_jeddah_3 else (st.number_input("Original Cost 3 (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="c3_orig") or 0.0)
            sell_3 = 0.0 if is_jeddah_3 else (st.number_input("Selling Price 3 (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="c3_sell") or 0.0)
    
    if sell_3 > 0:
        sar_preview_3 = sell_3 / sar_to_pkr if sar_to_pkr > 0 else 0
        st.caption(f"💱 Leg 3 Selling: **PKR {sell_3:,.2f} ~ SAR {sar_preview_3:,.2f}**")

    if city_3 != "-- Select City --":
        # Leg 3 Transport
        col_t7, col_t8, col_t9 = st.columns(3)
        with col_t7:
            trans_3 = st.selectbox("Transport from Leg 3:", vehicle_list, key="t3_vehicle")
        with col_t8:
            trans_orig_3 = st.number_input("Transport Org Cost 3 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t3_orig") or 0.0
        with col_t9:
            trans_sell_3 = st.number_input("Transport Sell Cost 3 (PKR):", min_value=0.0, value=None, step=500.0, format="%.2f", key="t3_sell") or 0.0

        if trans_sell_3 > 0:
            t_sar_3 = trans_sell_3 / sar_to_pkr if sar_to_pkr > 0 else 0
            st.caption(f"💱 Transport 3 Selling: **PKR {trans_sell_3:,.2f} ~ SAR {t_sar_3:,.2f}**")

total_stay_nights = nights_1 + nights_2 + nights_3
hotels_orig_total = orig_1 + orig_2 + orig_3
hotels_sell_total = sell_1 + sell_2 + sell_3
hotels_total_profit = hotels_sell_total - hotels_orig_total

total_transport_orig = trans_orig_1 + trans_orig_2 + trans_orig_3
total_transport_sell = trans_sell_1 + trans_sell_2 + trans_sell_3
total_transport_profit = total_transport_sell - total_transport_orig

hotels_sar_total = hotels_sell_total / sar_to_pkr if sar_to_pkr > 0 else 0.0
transport_sar_total = total_transport_sell / sar_to_pkr if sar_to_pkr > 0 else 0.0

st.info(f"💡 Total Stays Duration: **{total_stay_nights} Nights** | Hotel Sell: **PKR {hotels_sell_total:,.2f} ~ SAR {hotels_sar_total:,.2f}** | Transport Sell: **PKR {total_transport_sell:,.2f} ~ SAR {transport_sar_total:,.2f}**")

st.write("---")

# 5. ZIARATS MANAGEMENT SECTION
st.subheader("🗺️ Step 5: Ziarats Selection & Management")
col13, col14 = st.columns(2)
with col13:
    ziarat_status = st.selectbox("Do you want Ziarats included?", ["-- Select Option --", "YES", "NO"], key="z_status")
    ziarat_scope = "-- Not Applicable --"
    if ziarat_status == "YES":
        ziarat_scope = st.selectbox("Select Ziarats Coverage Area:", ["-- Select Scope --", "MAKKAH ONLY", "MADINAH ONLY", "BOTH MAKKAH AND MADINAH"], key="z_scope")

with col14:
    ziarat_transport_type = st.selectbox("Ziarat Transport Type:", vehicle_list, key="z_trans_type")
    ziarat_orig_cost = st.number_input("Ziarats Original Cost (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="z_orig") or 0.0
    ziarat_sell_cost = st.number_input("Ziarats Selling Price to Customer (PKR):", min_value=0.0, value=None, step=1000.0, format="%.2f", key="z_sell") or 0.0

ziarat_profit = ziarat_sell_cost - ziarat_orig_cost
ziarat_sar = ziarat_sell_cost / sar_to_pkr if sar_to_pkr > 0 else 0.0
if ziarat_sell_cost > 0:
    st.caption(f"💱 Ziarats Selling: **PKR {ziarat_sell_cost:,.2f} ~ SAR {ziarat_sar:,.2f}**")

st.write("---")

# 6. VISA & AIRFARE (Per Person Rates Multiplied Automatically)
st.subheader("🎫 Step 6: Visa + Airfare (Per Person Rates)")
col17, col18 = st.columns(2)
with col17:
    visa_air_orig_pp = st.number_input("Original Cost Per Person (PKR):", min_value=0.0, value=None, step=5000.0, format="%.2f", key="va_orig_pp") or 0.0
with col18:
    visa_air_sell_pp = st.number_input("Selling Price Per Person (PKR):", min_value=0.0, value=None, step=5000.0, format="%.2f", key="va_sell_pp") or 0.0

# Multiply by total family members automatically
visa_air_orig = visa_air_orig_pp * total_people
visa_air_sell = visa_air_sell_pp * total_people

visa_profit = visa_air_sell - visa_air_orig
visa_sar = visa_air_sell / sar_to_pkr if sar_to_pkr > 0 else 0.0

if visa_air_sell > 0:
    st.info(f"👥 Total Family Members: **{total_people}** | Total Visa & Airfare Selling: **PKR {visa_air_sell:,.2f} ~ SAR {visa_sar:,.2f}**")

grand_total_selling = hotels_sell_total + total_transport_sell + ziarat_sell_cost + visa_air_sell
grand_total_original = hotels_orig_total + total_transport_orig + ziarat_orig_cost + visa_air_orig
total_agency_net_profit = grand_total_selling - grand_total_original
grand_total_sar = grand_total_selling / sar_to_pkr if sar_to_pkr > 0 else 0.0

st.write("---")

# 7. OFFICIAL CUSTOMER QUOTATION (Proper Form Format)
st.subheader("📄 Step 7: Official Customer Quotation Form")
if st.button("Generate Official Quotation Form 📋", type="primary", key="btn_gen_quotation"):
    st.success("Professional Quotation Form Generated Successfully!")
    
    d1 = trip_start_date
    d2 = d1 + timedelta(days=nights_1) if nights_1 > 0 else d1
    d3 = d2 + timedelta(days=nights_2) if nights_2 > 0 else d2
    
    # Clean Form Container / Box Design
    st.markdown(f"""
    <div style="background-color: #111111; padding: 25px; border-radius: 12px; border: 1px solid #2e8b57; color: #ffffff;">
        <h2 style="text-align: center; color: #2e8b57; margin-bottom: 0px;">✨ TRAVELNEXT INTERNATIONAL ✨</h2>
        <p style="text-align: center; color: #aaaaaa; font-size: 14px;">Official Umrah Packages & Travel Services</p>
        <hr style="border-color: #333333;">
        
        <table style="width: 100%; color: #ffffff; margin-bottom: 15px;">
            <tr>
                <td><b>Client Name:</b> {cust_first_name or 'Valued'} {cust_last_name or 'Customer'}</td>
                <td><b>Travel Date:</b> {trip_start_date.strftime('%d %b %Y')}</td>
            </tr>
            <tr>
                <td><b>Total Travelers:</b> {total_people} Persons ({adults} Adults, {children} Children)</td>
                <td><b>Airline / Flight:</b> {cust_airline if cust_airline != '-- Select Airline --' else 'N/A'}</td>
            </tr>
            <tr>
                <td><b>Total Duration:</b> {total_stay_nights} Nights</td>
                <td><b>Landing Airport:</b> {cust_landing if cust_landing != '-- Select Airport --' else 'N/A'}</td>
            </tr>
        </table>
        
        <h3 style="color: #2e8b57; border-bottom: 1px solid #333333; padding-bottom: 5px;">🏨 Itinerary & Accommodation Breakdown</h3>
        <ul>
            <li><b>Leg 1 ({city_1}):</b> {'Jeddah Transit / Stop' if 'Jeddah' in city_1 else hotel_1}<br>
                &nbsp;&nbsp;&nbsp;&nbsp;<i>Duration:</i> {nights_1} Nights ({d1.strftime('%d %b')} - {d2.strftime('%d %b %Y')}) | <i>Local Transport:</i> {trans_1}</li>
    """, unsafe_allow_html=True)
    
    if city_2 != "-- Select City --":
        is_j2 = "Jeddah" in city_2
        st.markdown(f"""
            <li><b>Leg 2 ({city_2}):</b> {'Jeddah Transit / Stop' if is_j2 else hotel_2}<br>
                &nbsp;&nbsp;&nbsp;&nbsp;<i>Duration:</i> {nights_2} Nights ({d2.strftime('%d %b')} - {d3.strftime('%d %b %Y')}) | <i>Local Transport:</i> {trans_2}</li>
        """, unsafe_allow_html=True)
        
    if city_3 != "-- Select City --":
        is_j3 = "Jeddah" in city_3
        d4 = d3 + timedelta(days=nights_3)
        st.markdown(f"""
            <li><b>Leg 3 ({city_3}):</b> {'Jeddah Transit / Stop' if is_j3 else hotel_3}<br>
                &nbsp;&nbsp;&nbsp;&nbsp;<i>Duration:</i> {nights_3} Nights ({d3.strftime('%d %b')} - {d4.strftime('%d %b %Y')}) | <i>Local Transport:</i> {trans_3}</li>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        </ul>
        
        <h3 style="color: #2e8b57; border-bottom: 1px solid #333333; padding-bottom: 5px;">🗺️ Ziarats & Services</h3>
        <p><b>Ziarat Status:</b> {ziarat_status} {f"({ziarat_scope} via {ziarat_transport_type})" if ziarat_status == "YES" else ""}</p>
        
        <hr style="border-color: #333333;">
        <h2 style="text-align: center; color: #2e8b57;">TOTAL PACKAGE INVESTMENT</h2>
        <h1 style="text-align: center; color: #ffffff;">PKR {grand_total_selling:,.2f} <span style="font-size: 20px; color: #2e8b57;">(~SAR {grand_total_sar:,.2f})</span></h1>
        
        <p style="text-align: center; font-style: italic; color: #aaaaaa; margin-top: 20px;">
            "THANKS FOR CHOOSING TRAVELNEXT. AAO MADINEY CHALEN! MAY ALLAH ACCEPT YOUR GOOD DEEDS!" 🕋✨
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# 8. AGENCY PROFIT DASHBOARD
st.subheader("📊 Step 8: Internal Agency Profit & Cost Breakdown")
if st.button("Show Internal Profit Sheet 📈", key="btn_profit_sheet"):
    st.markdown(f"""
    ### 💼 FINANCIAL MARGIN REPORT (For Office Use Only)
    - **Hotels Stays Total:** PKR {hotels_sell_total:,.2f} (~SAR {hotels_sar_total:,.2f}) | *Profit: PKR {hotels_total_profit:,.2f}*
    - **City Transports Total:** PKR {total_transport_sell:,.2f} (~SAR {transport_sar_total:,.2f}) | *Profit: PKR {total_transport_profit:,.2f}*
    - **Ziarats Total:** PKR {ziarat_sell_cost:,.2f} (~SAR {ziarat_sar:,.2f}) | *Profit: PKR {ziarat_profit:,.2f}*
    - **Visa & Airfare Total ({total_people} Persons):** PKR {visa_air_sell:,.2f} (~SAR {visa_sar:,.2f}) | *Profit: PKR {visa_profit:,.2f}*
    
    ---
    ### 🔥 TOTAL NET PROFIT FOR AGENCY: PKR {total_agency_net_profit:,.2f} (~SAR {(total_agency_net_profit / sar_to_pkr if sar_to_pkr > 0 else 0):,.2f})
    """)
    st.balloons()