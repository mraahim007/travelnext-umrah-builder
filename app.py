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
sar_to_pkr = st.number_input("Enter current 1 SAR to PKR rate today:", min_value=0.0, max_value=100.0, value=75.0, step=0.5, key="daily_sar_rate")
st.info(f"💡 Active Exchange Rate: **1 SAR = {sar_to_pkr} PKR**")

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

# HOTELS LISTS
makkah_hotels_list = [
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

madinah_hotels_list = [
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

# 4. STEP-BY-STEP DYNAMIC STAY BUILDER
st.subheader("🏨 Step 4: Step-by-Step Hotel Stay Builder")
st.markdown("Configure your stay legs dynamically one by one:")

# Stay Leg 1 (Mandatory)
st.markdown("### 🧳 Stay Leg 1 (First Stop)")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    city_1 = st.selectbox("Select City 1:", ["-- Select City --", "Makkah Al-Mukarramah", "Al-Madinah Al-Munawwarah"], key="c1_city")
    nights_1 = st.number_input("Nights in City 1:", min_value=0, value=0, key="c1_nights")
with col_s2:
    category_1 = st.selectbox("Category 1:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c1_cat")
    hotel_1 = st.selectbox("Hotel 1:", makkah_hotels_list if city_1 == "Makkah Al-Mukarramah" else madinah_hotels_list, key="c1_hotel")
with col_s3:
    orig_1 = st.number_input("Original Cost 1 (PKR):", min_value=0.0, value=0.0, step=5000.0, key="c1_orig")
    sell_1 = st.number_input("Selling Price 1 (PKR):", min_value=0.0, value=0.0, step=5000.0, key="c1_sell")

# Stay Leg 2 (Appears only if Leg 1 has city & nights)
city_2, nights_2, orig_2, sell_2, category_2, hotel_2 = "-- None --", 0, 0.0, 0.0, "N/A", "N/A"
if city_1 != "-- Select City --" and nights_1 > 0:
    st.markdown("### 🧳 Stay Leg 2 (Next Stop)")
    col_s4, col_s5, col_s6 = st.columns(3)
    with col_s4:
        city_2 = st.selectbox("Select City 2:", ["-- Select City --", "Makkah Al-Mukarramah", "Al-Madinah Al-Munawwarah"], key="c2_city")
        nights_2 = st.number_input("Nights in City 2:", min_value=0, value=0, key="c2_nights")
    with col_s5:
        category_2 = st.selectbox("Category 2:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c2_cat")
        hotel_2 = st.selectbox("Hotel 2:", makkah_hotels_list if city_2 == "Makkah Al-Mukarramah" else madinah_hotels_list, key="c2_hotel")
    with col_s6:
        orig_2 = st.number_input("Original Cost 2 (PKR):", min_value=0.0, value=0.0, step=5000.0, key="c2_orig")
        sell_2 = st.number_input("Selling Price 2 (PKR):", min_value=0.0, value=0.0, step=5000.0, key="c2_sell")

# Stay Leg 3 (Appears only if Leg 2 has city & nights)
city_3, nights_3, orig_3, sell_3, category_3, hotel_3 = "-- None --", 0, 0.0, 0.0, "N/A", "N/A"
if city_2 != "-- Select City --" and nights_2 > 0:
    st.markdown("### 🧳 Stay Leg 3 (Optional Final Stop)")
    col_s7, col_s8, col_s9 = st.columns(3)
    with col_s7:
        city_3 = st.selectbox("Select City 3:", ["-- None --", "Makkah Al-Mukarramah", "Al-Madinah Al-Munawwarah"], key="c3_city")
        nights_3 = st.number_input("Nights in City 3:", min_value=0, value=0, key="c3_nights")
    with col_s8:
        category_3 = st.selectbox("Category 3:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c3_cat")
        hotel_3 = st.selectbox("Hotel 3:", makkah_hotels_list if city_3 == "Makkah Al-Mukarramah" else madinah_hotels_list, key="c3_hotel")
    with col_s9:
        orig_3 = st.number_input("Original Cost 3 (PKR):", min_value=0.0, value=0.0, step=5000.0, key="c3_orig")
        sell_3 = st.number_input("Selling Price 3 (PKR):", min_value=0.0, value=0.0, step=5000.0, key="c3_sell")
    
    if city_3 == "-- None --":
        nights_3 = 0
        orig_3 = 0.0
        sell_3 = 0.0

total_stay_nights = nights_1 + nights_2 + nights_3
hotels_orig_total = orig_1 + orig_2 + orig_3
hotels_sell_total = sell_1 + sell_2 + sell_3
hotels_total_profit = hotels_sell_total - hotels_orig_total

st.info(f"💡 Total Stays Duration: **{total_stay_nights} Nights** | Total Hotel Profit Margin: **PKR {hotels_total_profit:,.2f}**")

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
    ziarat_transport_type = st.selectbox("Ziarat Transport Type:", ["-- Select Transport Type --", "Private - Toyota Hiace / Van", "Private - GMC Yukon / VIP SUV", "Private - Coaster Saloon", "Public Bus Group Sharing"], key="z_trans_type")
    ziarat_orig_cost = st.number_input("Ziarats Original Cost (PKR):", min_value=0.0, value=0.0, step=1000.0, key="z_orig")
    ziarat_sell_cost = st.number_input("Ziarats Selling Price to Customer (PKR):", min_value=0.0, value=0.0, step=1000.0, key="z_sell")

ziarat_profit = ziarat_sell_cost - ziarat_orig_cost

st.write("---")

# 6. TRANSPORTS & TRANSFERS
st.subheader("🚗 Step 6: Airport Transfers & Inter-City Transport")
col15, col16 = st.columns(2)
with col15:
    st.markdown("##### 🛬 Arrival Transfer (Airport to Hotel)")
    arr_transfer_type = st.selectbox("Arrival Vehicle:", ["-- Select --", "Private Car / Sedan", "Private Hiace", "Private GMC", "Shared Bus"], key="arr_trans")
    arr_orig = st.number_input("Arrival Original Cost (PKR):", min_value=0.0, value=0.0, step=500.0, key="arr_o")
    arr_sell = st.number_input("Arrival Selling Price (PKR):", min_value=0.0, value=0.0, step=500.0, key="arr_s")

    st.markdown("##### 🚙 Inter-City Transfer")
    inter_transfer_type = st.selectbox("Inter-City Vehicle:", ["-- Select --", "Private Hiace", "Private Coaster", "Haramain Train", "Public Bus"], key="inter_trans")
    inter_orig = st.number_input("Inter-City Original Cost (PKR):", min_value=0.0, value=0.0, step=1000.0, key="inter_o")
    inter_sell = st.number_input("Inter-City Selling Price (PKR):", min_value=0.0, value=0.0, step=1000.0, key="inter_s")

with col16:
    st.markdown("##### 🛫 Departure Transfer (Hotel to Airport)")
    dep_transfer_type = st.selectbox("Departure Vehicle:", ["-- Select --", "Private Car / Sedan", "Private Hiace", "Private GMC", "Shared Bus"], key="dep_trans")
    dep_orig = st.number_input("Departure Original Cost (PKR):", min_value=0.0, value=0.0, step=500.0, key="dep_o")
    dep_sell = st.number_input("Departure Selling Price (PKR):", min_value=0.0, value=0.0, step=500.0, key="dep_s")

transfers_profit = (arr_sell - arr_orig) + (dep_sell - dep_orig) + (inter_sell - inter_orig)

st.write("---")

# 7. VISA & AIRFARE
st.subheader("🎫 Step 7: Visa + Airfare (Original vs Selling)")
col17, col18 = st.columns(2)
with col17:
    visa_air_orig = st.number_input("Total Visa + Airfare Original Cost (PKR):", min_value=0.0, value=0.0, step=10000.0, key="va_orig")
with col18:
    visa_air_sell = st.number_input("Total Visa + Airfare Selling Price to Customer (PKR):", min_value=0.0, value=0.0, step=10000.0, key="va_sell")

visa_profit = visa_air_sell - visa_air_orig

grand_total_selling = hotels_sell_total + ziarat_sell_cost + arr_sell + dep_sell + inter_sell + visa_air_sell
grand_total_original = hotels_orig_total + ziarat_orig_cost + arr_orig + dep_orig + inter_orig + visa_air_orig
total_agency_net_profit = grand_total_selling - grand_total_original

st.write("---")

# 8. CUSTOMER QUOTATION
st.subheader("📄 Step 8: Official Customer Quotation")
if st.button("Generate Shareable Quotation 📄", type="primary", key="btn_gen_quotation"):
    st.success("Quotation Ready with Dynamic Itinerary Schedule!")
    
    d1 = trip_start_date
    d2 = d1 + timedelta(days=nights_1) if nights_1 > 0 else d1
    d3 = d2 + timedelta(days=nights_2) if nights_2 > 0 else d2
    
    st.markdown(f"""
    ---
    ### 🕋 TRAVELNEXT OFFICIAL UMRAH QUOTATION
    **Client Name:** {cust_first_name or 'Valued'} {cust_last_name or 'Customer'} | **Travelers:** {total_people} Persons ({adults} Adults, {children} Children)
    **Trip Start Date:** {trip_start_date.strftime('%d %b %Y')} | **Total Duration:** {total_stay_nights} Nights | **Airline:** {cust_airline if cust_airline != '-- Select Airline --' else 'N/A'}
    
    #### 🏨 Accommodation & Itinerary Schedule:
    - **Stay Leg 1 ({city_1}):** {hotel_1} 
      - *Duration:* {nights_1} Nights ({d1.strftime('%d %b')} to {d2.strftime('%d %b %Y')}) | *Category:* {category_1}
    """)
    
    if city_2 != "-- Select City --" and nights_2 > 0:
        st.markdown(f"""
    - **Stay Leg 2 ({city_2}):** {hotel_2} 
      - *Duration:* {nights_2} Nights ({d2.strftime('%d %b')} to {d3.strftime('%d %b %Y')}) | *Category:* {category_2}
        """)
        
    if city_3 != "-- None --" and nights_3 > 0:
        d4 = d3 + timedelta(days=nights_3)
        st.markdown(f"""
    - **Stay Leg 3 ({city_3}):** {hotel_3} 
      - *Duration:* {nights_3} Nights ({d3.strftime('%d %b')} to {d4.strftime('%d %b %Y')}) | *Category:* {category_3}
        """)
        
    st.markdown(f"""
    #### 🚗 Transport & Logistics:
    - **Ziarats:** Status: {ziarat_status} | Scope: {ziarat_scope} ({ziarat_transport_type})
    - **Transfers:** Arrival: {arr_transfer_type} | Inter-City: {inter_transfer_type} | Departure: {dep_transfer_type}
    
    ---
    ### 💰 TOTAL PACKAGE PRICE: PKR {grand_total_selling:,.2f}  *(~SAR {grand_total_selling/sar_to_pkr:,.2f if sar_to_pkr > 0 else 0.0})*
    
    > **"THANKS FOR CHOOSING TRAVELNEXT. AAO MADINEY CHALEN! MAY ALLAH ACCEPT YOUR GOOD DEEDS!"** 😊
    ---
    """)

st.write("---")

# 9. AGENCY PROFIT DASHBOARD
st.subheader("📊 Step 9: Internal Agency Profit & Cost Breakdown")
if st.button("Show Internal Profit Sheet 📈", key="btn_profit_sheet"):
    st.markdown(f"""
    ### 💼 FINANCIAL MARGIN REPORT (For Office Use Only)
    - **Hotels Stays Total Profit:** PKR {hotels_total_profit:,.2f} *(Orig: {hotels_orig_total:,.2f} | Sell: {hotels_sell_total:,.2f})*
    - **Ziarats Profit:** PKR {ziarat_profit:,.2f} *(Orig: {ziarat_orig_cost:,.2f} | Sell: {ziarat_sell_cost:,.2f})*
    - **Transfers Profit:** PKR {transfers_profit:,.2f}
    - **Visa & Airfare Profit:** PKR {visa_profit:,.2f} *(Orig: {visa_air_orig:,.2f} | Sell: {visa_air_sell:,.2f})*
    
    ---
    ### 🔥 TOTAL NET PROFIT FOR AGENCY: PKR {total_agency_net_profit:,.2f}
    """)
    st.balloons()