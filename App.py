import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ویب سائٹ کی سیٹنگ
st.set_page_config(page_title="Arif Khan Marble", layout="wide")

# گوگل شیٹ سے کنکشن
conn = st.connection("gsheets", type=GSheetsConnection)

# سادہ لاگ ان سسٹم
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.header("Arif Khan Marble - Login")
    user = st.text_input("User Name")
    passw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "arif" and passw == "123": # یہاں آپ اپنا پاس ورڈ بدل سکتے ہیں
            st.session_state['auth'] = True
            st.session_state['username'] = user
            st.rerun()
else:
    st.sidebar.title(f"خوش آمدید، {st.session_state['username']}")
    menu = ["📊 Dashboard", "🚚 Gari Entry", "📒 Full Record"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "🚚 Gari Entry":
        st.header("نئی گاڑی کا حساب")
        with st.form("gari_form"):
            g_no = st.text_input("Gari No")
            pera = st.selectbox("Pera", ["Pehla", "Doosra", "Teesra"])
            ton = st.number_input("Tons", min_value=0.0)
            cost = st.number_input("ٹوٹل خرچہ (پتھر کی قیمت + کرائی + چرائی)", min_value=0)
            feet = st.number_input("Total Feet", min_value=0)
            sale_rate = st.number_input("Average Sale Rate", min_value=0)
            
            if st.form_submit_button("Sheet mein Save Karen"):
                # حساب کتاب
                total_sale = feet * sale_rate
                pl = total_sale - cost
                
                # نیا ڈیٹا
                new_entry = pd.DataFrame([{
                    "Date": str(datetime.now().date()),
                    "User": st.session_state['username'],
                    "Gari": g_no, "Pera": pera, "Tons": ton,
                    "Total_Cost": cost, "Total_Sale": total_sale, "Profit_Loss": pl
                }])
                
                # شیٹ میں ڈیٹا بھیجنا
                old_data = conn.read(worksheet="Sheet1")
                updated_df = pd.concat([old_data, new_entry], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                st.success(f"Gari {g_no} ka record save ho gaya!")

    elif choice == "📊 Dashboard":
        st.header("آپ کا کل منافع اور نقصان")
        data = conn.read(worksheet="Sheet1")
        # صرف اس یوزر کا ڈیٹا دکھانا
        user_data = data[data['User'] == st.session_state['username']]
        if not user_data.empty:
            total_pl = user_data['Profit_Loss'].sum()
            st.metric("Net Profit/Loss", f"Rs. {total_pl:,.0f}")
            st.dataframe(user_data)
        else:
            st.info("ابھی تک کوئی ریکارڈ نہیں ہے")
            
