import streamlit as st

# Page Configuration
st.set_page_config(page_title="TravelNext Umrah Builder", page_icon="🕋", layout="wide")

# CUSTOM BLACK THEME WITH DARK GREEN BUTTONS
st.markdown("""
    <style>
    /* Main Background & Text Color */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Headers & Subheaders */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Input Labels & General Text */
    label, p, span {
        color: #e0e0e0 !important;
    }
    
    /* Info boxes / Success boxes */
    .stAlert {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
    }
    
    /* Buttons Styling -> Dark Green with White Text */
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
    
    /* Dividers */
    hr {
        border-color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>✨ TRAVELNEXT - PROFESSIONAL UMRAH BUILDER ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #2e8b57; font-size: 18px; font-weight: bold;'>Aao Madiney Chalen 🕋</p>", unsafe_allow_html=True)
st.write("---")

# 1. CURRENCY EXCHANGE RATE
st.subheader("💱 Step 1: Daily Currency Exchange Rate")
sar_to_pkr = st.number_input("Enter current 1 SAR to PKR rate today:", min_value=0.0, max_value=100.0, value=75.0, step=0.5, key="daily_sar_rate")
st.info(f"💡 Active Exchange Rate: **1 SAR = {sar_to_pkr} PKR**")

st.write("---")

# 2. CUSTOMER DETAILS
st.subheader("👤 Step 2: Customer Details")
col1, col2 = st.columns(2)
with col1:
    cust_first_name = st.text_input("First Name:", key="c_first_name")
    adults = st.number_input("Enter number of adults:", min_value=1, value=1, key="common_adults")
with col2:
    cust_last_name = st.text_input("Last Name:", key="c_last_name")
    children = st.number_input("Enter number of children:", min_value=0, value=0, key="common_children")

total_people = adults + children
st.info(f"👉 Total Family Members: **{total_people}** ({adults} Adults, {children} Children)")

st.write("---")

# 3. FLIGHT & ROUTE DETAILS
st.subheader("✈️ Step 3: Flight & Route Details")
col3, col4 = st.columns(2)
with col3:
    cust_airline = st.selectbox("Select Airline Name:", ["-- Select Airline --", "Saudia Airlines", "PIA", "AirBlue", "SereneAir", "Fly Jinnah", "Emirates", "Qatar Airways"], key="c_air")
    cust_landing = st.selectbox("Arrival Airport:", ["-- Select Airport --", "Jeddah Airport (JED)", "Madinah Airport (MED)"], key="c_land")
with col4:
    cust_route_choice = st.selectbox("Travel Route Pattern:", [
        "-- Select Route Pattern --",
        "Standard Classic (Jeddah -> Makkah -> Madinah -> Jeddah)",
        "Madinah First (Madinah -> Makkah -> Jeddah)",
        "Direct Madinah Round-Trip (Madinah -> Makkah -> Madinah)",
        "Multi-City Round (Jeddah -> Makkah -> Madinah -> Makkah -> Jeddah)",
        "➕ Custom Route (Type manually below)"
    ], key="c_route")

    cust_route = ""
    if cust_route_choice == "➕ Custom Route (Type manually below)":
        cust_route = st.text_input("Enter Custom Route Details:", "", key="cust_route_text_box", placeholder="e.g. Jeddah -> Makkah -> Madinah -> Jeddah")
    elif cust_route_choice != "-- Select Route Pattern --":
        cust_route = cust_route_choice

st.write("---")

# 4. MAKKAH STAY, CATEGORY & PRICING BREAKDOWN
st.subheader("🕋 Step 4: Makkah Stay, Category & Price Margin")
col5, col6 = st.columns(2)
with col5:
    cust_makkah_nights = st.number_input("Makkah Stay Days (Nights):", min_value=0, value=0, key="c_m_nights")
    cust_makkah_category = st.selectbox("Makkah Hotel Category:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c_m_cat")
with col6:
    makkah_orig_total = st.number_input("Makkah Hotel Original Cost (Total for all nights in PKR):", min_value=0.0, value=0.0, step=5000.0, key="m_orig")
    makkah_selling_total = st.number_input("Makkah Hotel Selling Price to Customer (Total in PKR):", min_value=0.0, value=0.0, step=5000.0, key="m_sell")

makkah_profit = makkah_selling_total - makkah_orig_total
st.info(f"💡 Makkah Profit Margin: **PKR {makkah_profit:,.2f}**")

st.write("---")

# 5. MAKKAH HOTEL SELECTION WITH EXACT STARS & DISTANCES
st.subheader("🏨 Step 5: Makkah Specific Hotel & Distance")

makkah_hotels_list = [
    "-- Select Specific Hotel --",
    "⭐⭐⭐⭐⭐ Makkah Clock Royal Tower, A Fairmont Hotel (Directly connected / 0 km)",
    "⭐⭐⭐⭐⭐ Swissôtel Makkah (Directly connected / 0 km)",
    "⭐⭐⭐⭐⭐ Swissôtel Al Maqam Makkah (Directly connected / 0 km)",
    "⭐⭐⭐⭐⭐ Pullmann Zamzam Makkah (Directly connected / 0 km)",
    "⭐⭐⭐⭐⭐ Address Jabal Omar Makkah (Approx. 200–300m / 2-3 min walk)",
    "⭐⭐⭐⭐⭐ Conrad Jabal Omar Makkah (Approx. 300m / 3-5 min walk)",
    "⭐⭐⭐⭐⭐ Jabal Omar Hyatt Regency Makkah (Approx. 500m / 5-7 min walk)",
    "⭐⭐⭐⭐⭐ Hilton Suites Jabal Omar Makkah (Approx. 300–400m / 4-5 min walk)",
    "⭐⭐⭐⭐⭐ InterContinental Dar Al Tawhid Makkah (Directly facing Haram / 0 km)",
    "⭐⭐⭐⭐⭐ Raffles Makkah Palace (Directly connected / 0 km)",
    "⭐⭐⭐⭐⭐ Al Marwa Rayhaan by Rotana (Directly connected / 0 km)",
    "⭐⭐⭐⭐⭐ Anjum Hotel Makkah (Approx. 450m / 5-10 min walk)",
    "⭐⭐⭐⭐ Voco Makkah (Approx. 1.8 - 2 km / Shuttle service)",
    "⭐⭐⭐⭐ Mercure Makkah Aziziah (Approx. 4 - 5 km / Aziziah district)",
    "⭐⭐⭐⭐ Emaar Royal Hotel (Approx. 700 - 800m / 10 min walk)",
    "⭐⭐⭐⭐ Makarem Ajyad Makkah Hotel (Approx. 500m / 6-8 min walk)",
    "⭐⭐⭐⭐ Al Ghufran Safwah Hotel (Directly facing Haram / Safwah Tower)",
    "⭐⭐⭐ Al Kiswah Towers (Approx. 1.5 - 1.7 km / Taysir shuttle)",
    "⭐⭐⭐ Snood Hotel (Approx. 1.5 km / Ibrahim Al Khalil road shuttle)",
    "⭐⭐⭐ Fakhir Al Azizia (Approx. 4.5 km / Aziziah district)",
    "⭐⭐⭐ Qilla Ajyad Hotel (Approx. 600 - 700m / 8-10 min walk)",
    "⭐⭐⭐ Taj Faddi Hotel (Approx. 2 km / Shuttle service)",
    "⭐⭐⭐ Time Ruba Hotel (Approx. 3.5 km / Al-Rashidiyyah)"
]

selected_makkah_hotel = st.selectbox("Choose Makkah Hotel (with Star Rating & Distance):", makkah_hotels_list, key="c_m_hotel")

st.write("---")

# 6. MADINAH STAY, CATEGORY & PRICING BREAKDOWN
st.subheader("🕌 Step 6: Madinah Stay, Category & Price Margin")
col9, col10 = st.columns(2)
with col9:
    cust_madinah_nights = st.number_input("Madinah Stay Days (Nights):", min_value=0, value=0, key="c_md_nights")
    cust_madinah_category = st.selectbox("Madinah Hotel Category:", ["-- Select Category --", "5-Star Luxury", "4-Star Standard", "3-Star & Economy"], key="c_md_cat")
with col10:
    madinah_orig_total = st.number_input("Madinah Hotel Original Cost (Total for all nights in PKR):", min_value=0.0, value=0.0, step=5000.0, key="md_orig")
    madinah_selling_total = st.number_input("Madinah Hotel Selling Price to Customer (Total in PKR):", min_value=0.0, value=0.0, step=5000.0, key="md_sell")

madinah_profit = madinah_selling_total - madinah_orig_total
cust_total_nights = cust_makkah_nights + cust_madinah_nights
st.info(f"💡 Madinah Profit Margin: **PKR {madinah_profit:,.2f}** | Total Nights: **{cust_total_nights}**")

st.write("---")

# 7. MADINAH HOTEL SELECTION WITH EXACT STARS & DISTANCES
st.subheader("🏢 Step 7: Madinah Specific Hotel & Distance")

madinah_hotels_list = [
    "-- Select Specific Hotel --",
    "⭐⭐⭐⭐⭐ Anwar Al Madinah Movenpick Hotel (Connected to courtyard / 100m)",
    "⭐⭐⭐⭐⭐ Crowne Plaza Madinah (Approx. 200m / 3-4 min walk)",
    "⭐⭐⭐⭐⭐ Oberoi Madinah (Directly facing courtyard / 100m)",
    "⭐⭐⭐⭐⭐ Dar Al Taqwa Hotel (Directly facing courtyard / 0-50m)",
    "⭐⭐⭐⭐⭐ Pullman Zamzam Madinah (Approx. 150m / 2-3 min walk)",
    "⭐⭐⭐⭐ Al Aqeeq Madinah Hotel (Approx. 200–300m / 3-5 min walk)",
    "⭐⭐⭐⭐ Elaf Taiba Hotel (Approx. 200m / 3 min walk)",
    "⭐⭐⭐⭐ Leader Muna Kareem Hotel (Approx. 150–200m / 2-3 min walk)",
    "⭐⭐⭐⭐ Swiss International Hotel (Approx. 500m / 7 min walk)",
    "⭐⭐⭐⭐ Tulip Inn Dar Al Rufead (Approx. 600m / 8 min walk)",
    "⭐⭐⭐⭐ Rua Hijra Hotel (Approx. 400m / 5 min walk)",
    "⭐⭐⭐⭐ Al Haram Madinah (Approx. 250m / 3-4 min walk)",
    "⭐⭐⭐ Mysk Touch Hotel (Approx. 700 - 800m / 10 min walk)",
    "⭐⭐⭐ Shaza Al Hijra Hotel (Approx. 500m / 6-7 min walk)",
    "⭐⭐⭐ Plaza Inn Ohud (Approx. 900m / 12 min walk or shuttle)",
    "⭐⭐⭐ Manazil Al Marjan (Approx. 600m / 8 min walk)",
    "⭐⭐⭐ Diyar Al Safa (Approx. 700m / 10 min walk)",
    "⭐⭐⭐ Wahat Al Shark (Approx. 1 km / 12-15 min walk)",
    "⭐⭐⭐ Hala Taiba Hotel (Approx. 600m / 8 min walk)"
]

selected_madinah_hotel = st.selectbox("Choose Madinah Hotel (with Star Rating & Distance):", madinah_hotels_list, key="c_md_hotel")

st.write("---")

# 8. ZIARATS MANAGEMENT SECTION
st.subheader("🗺️ Step 8: Ziarats Selection & Management")
col13, col14 = st.columns(2)
with col13:
    ziarat_status = st.selectbox("Do you want Ziarats included?", ["-- Select Option --", "YES", "NO"], key="z_status")
    
    ziarat_scope = "-- Not Applicable --"
    if ziarat_status == "YES":
        ziarat_scope = st.selectbox("Select Ziarats Coverage Area:", [
            "-- Select Scope --",
            "MAKKAH ONLY",
            "MADINAH ONLY",
            "BOTH MAKKAH AND MADINAH"
        ], key="z_scope")

with col14:
    ziarat_transport_type = st.selectbox("Ziarat Transport Type:", [
        "-- Select Transport Type --",
        "Private - Toyota Hiace / Van",
        "Private - GMC Yukon / VIP SUV",
        "Private - Coaster Saloon",
        "Public Bus Group Sharing"
    ], key="z_trans_type")
    
    ziarat_orig_cost = st.number_input("Ziarats Original Cost (PKR):", min_value=0.0, value=0.0, step=1000.0, key="z_orig")
    ziarat_sell_cost = st.number_input("Ziarats Selling Price to Customer (PKR):", min_value=0.0, value=0.0, step=1000.0, key="z_sell")

ziarat_profit = ziarat_sell_cost - ziarat_orig_cost

st.write("---")

# 9. ARRIVAL, DEPARTURE & INTER-CITY TRANSPORT
st.subheader("🚗 Step 9: Airport Transfers & Inter-City Transport")
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

# 10. VISA & AIRFARE WITH PROFIT BREAKDOWN
st.subheader("🎫 Step 10: Visa + Airfare (Original vs Selling)")
col17, col18 = st.columns(2)
with col17:
    visa_air_orig = st.number_input("Total Visa + Airfare Original Cost (PKR):", min_value=0.0, value=0.0, step=10000.0, key="va_orig")
with col18:
    visa_air_sell = st.number_input("Total Visa + Airfare Selling Price to Customer (PKR):", min_value=0.0, value=0.0, step=10000.0, key="va_sell")

visa_profit = visa_air_sell - visa_air_orig

# Grand Totals Calculation
grand_total_selling = makkah_selling_total + madinah_selling_total + ziarat_sell_cost + arr_sell + dep_sell + inter_sell + visa_air_sell
grand_total_original = makkah_orig_total + madinah_orig_total + ziarat_orig_cost + arr_orig + dep_orig + inter_orig + visa_air_orig
total_agency_net_profit = grand_total_selling - grand_total_original

st.write("---")

# 11. CUSTOMER QUOTATION
st.subheader("📄 Step 11: Official Customer Quotation")
if st.button("Generate Shareable Quotation 📄", type="primary", key="btn_gen_quotation"):
    st.success("Quotation Ready!")
    st.markdown(f"""
    ---
    ### 🕋 TRAVELNEXT OFFICIAL UMRAH QUOTATION
    **Client Name:** {cust_first_name or 'Valued'} {cust_last_name or 'Customer'} | **Travelers:** {total_people} Persons ({adults} Adults, {children} Children)
    **Duration:** {cust_total_nights} Nights | **Airline:** {cust_airline if cust_airline != '-- Select Airline --' else 'N/A'}
    
    #### 🏨 Accommodation Details:
    - **Makkah Hotel:** {selected_makkah_hotel if selected_makkah_hotel != '-- Select Specific Hotel --' else 'N/A'} ({cust_makkah_nights} Nights)
      - Category: {cust_makkah_category}
    - **Madinah Hotel:** {selected_madinah_hotel if selected_madinah_hotel != '-- Select Specific Hotel --' else 'N/A'} ({cust_madinah_nights} Nights)
      - Category: {cust_madinah_category}
      
    #### 🚗 Transport & Logistics:
    - **Ziarats:** Status: {ziarat_status} | Scope: {ziarat_scope} ({ziarat_transport_type})
    - **Transfers:** Arrival: {arr_transfer_type} | Inter-City: {inter_transfer_type} | Departure: {dep_transfer_type}
    
    ---
    ### 💰 TOTAL PACKAGE PRICE: PKR {grand_total_selling:,.2f}  *(~SAR {grand_total_selling/sar_to_pkr:,.2f if sar_to_pkr > 0 else 0.0})*
    
    > **"THANKS FOR CHOOSING TRAVELNEXT. AAO MADINEY CHALEN! MAY ALLAH ACCEPT YOUR GOOD DEEDS!"** 😊
    ---
    """)

st.write("---")

# 12. AGENCY PROFIT DASHBOARD
st.subheader("📊 Step 12: Internal Agency Profit & Cost Breakdown")
if st.button("Show Internal Profit Sheet 📈", key="btn_profit_sheet"):
    st.markdown(f"""
    ### 💼 FINANCIAL MARGIN REPORT (For Office Use Only)
    - **Makkah Hotel Profit:** PKR {makkah_profit:,.2f} *(Orig: {makkah_orig_total:,.2f} | Sell: {makkah_selling_total:,.2f})*
    - **Madinah Hotel Profit:** PKR {madinah_profit:,.2f} *(Orig: {madinah_orig_total:,.2f} | Sell: {madinah_selling_total:,.2f})*
    - **Ziarats Profit:** PKR {ziarat_profit:,.2f} *(Orig: {ziarat_orig_cost:,.2f} | Sell: {ziarat_sell_cost:,.2f})*
    - **Transfers Profit:** PKR {transfers_profit:,.2f}
    - **Visa & Airfare Profit:** PKR {visa_profit:,.2f} *(Orig: {visa_air_orig:,.2f} | Sell: {visa_air_sell:,.2f})*
    
    ---
    ### 🔥 TOTAL NET PROFIT FOR AGENCY: PKR {total_agency_net_profit:,.2f}
    """)
    st.balloons()