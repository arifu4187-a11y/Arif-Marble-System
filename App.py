import streamlit as st
import pandas as pd
from datetime import datetime

# Website ki setting aur Title
st.set_page_config(page_title="Arif Khan Marble Supplier", layout="centered")

# CSS Styling (Design ke liye)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stHeader { color: #1E3A8A; }
    .stButton>button { background-color: #1E3A8A; color: white; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Arif Khan Marble Supplier")
st.write("Pathar ki khareedari se le kar sale aur munafa tak ka mukammal hisab.")

# Sidebar Menu (Button ki tarah)
menu = ["📊 Dashboard", "📥 Naya Maal (Purchase)", "💰 Daily Sale", "📒 Udhaar / Khata"]
choice = st.sidebar.selectbox("Main Menu", menu)

# 1. NAYA MAAL (PURCHASE LOGIC)
if choice == "📥 Naya Maal (Purchase)":
    st.header("Pahad se Maal ki Khareedari")
    
    with st.container():
        stone = st.selectbox("Pathar ki Kism", ["Badal", "Ziarat White", "Sunny Grey", "Chitral White", "Other"])
        col1, col2 = st.columns(2)
        
        with col1:
            tons = st.number_input("Tan (Tons)", min_value=0.0, step=1.0)
            p_price = st.number_input("Pahad ki Qeemat (Total)", min_value=0.0)
            gari_kiraya = st.number_input("Gari ka Kiraya", min_value=0.0)
        
        with col2:
            charai = st.number_input("Charai (Cutting Kharcha)", min_value=0.0)
            resize = st.number_input("Selection / Resize Kharcha", min_value=0.0)
            mazdoori = st.number_input("Bhrai / Utrai Mazdoori", min_value=0.0)
            
        total_feet = st.number_input("Tayar shuda Foot (Total Sq. Ft)", min_value=0.0)

    if st.button("Hisaab Lagayen"):
        total_investment = p_price + gari_kiraya + charai + resize + mazdoori
        cost_per_foot = total_investment / total_feet if total_feet > 0 else 0
        
        st.success(f"Apka Kul Kharcha: **Rs. {total_investment:,.2f}**")
        st.info(f"Apko ye maal **Rs. {cost_per_foot:.2f} Per Foot** mein para hai.")
        # Is data ko save karne ka logic yahan add ho sakta hai

# 2. DAILY SALE
elif choice == "💰 Daily Sale":
    st.header("Grahak Sale Entry")
    customer = st.text_input("Grahak ka Naam")
    feet_sold = st.number_input("Kitne Foot Becha?", min_value=0.0)
    rate = st.number_input("Kis Rate par becha?", min_value=0.0)
    paid = st.number_input("Kitne Paise Wasool Hue?", min_value=0.0)
    
    if st.button("Sale Record Karen"):
        total_bill = feet_sold * rate
        balance = total_bill - paid
        st.write(f"Total Bill: Rs. {total_bill:,.2f}")
        if balance > 0:
            st.warning(f"Baqi Udhaar: Rs. {balance:,.2f}")
        else:
            st.success("Poori Payment Mil Gayi!")

# 3. KHATA / UDHAAR (DUMMY DATA FOR VIEW)
elif choice == "📒 Udhaar / Khata":
    st.header("Logon ka Udhaar (Summary)")
    # Sample Table
    khata_data = {
        "Naam": ["Ali Khan", "Zubair Shah", "Bilal Marble"],
        "Paisa Lena (Lena)": [45000, 15000, 0],
        "Paisa Dena (Dena)": [0, 0, 30000]
    }
    df = pd.DataFrame(khata_data)
    st.table(df)

# 4. DASHBOARD
elif choice == "📊 Dashboard":
    st.header("Karobar ki Report")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Stock", "4,200 Ft")
    col2.metric("Aaj ki Sale", "Rs. 25,000")
    col3.metric("Baqi Udhaar", "Rs. 1,20,000")
          
