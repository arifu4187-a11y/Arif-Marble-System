import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Settings
st.set_page_config(page_title="Arif Khan Marble", layout="wide")

# Google Sheet Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Login System
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.header("Arif Khan Marble - Login")
    user = st.text_input("User Name")
    passw = st.text_input("Password", type="password")
    if st.button("Login"):
        # Yahan aap apna username aur password check kar sakte hain
        if user.lower() == "arif" and passw == "123":
            st.session_state['auth'] = True
            st.session_state['username'] = user
            st.rerun()
        else:
            st.error("Ghalat User Name ya Password!")
else:
    st.sidebar.success(f"Khush Amdeed: {st.session_state['username']}")
    menu = ["📊 Dashboard", "🚚 Gari Entry", "📒 Full Record"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "🚚 Gari Entry":
        st.header("Nayi Gari ka Hisab")
        with st.form("gari_form"):
            g_no = st.text_input("Gari Number")
            pera = st.selectbox("Pera Select Karen", ["Pehla Pera", "Doosra Pera", "Teesra Pera"])
            ton = st.number_input("Kul Tan (Tons)", min_value=0.0)
            cost = st.number_input("Kul Kharcha (Pahad + Kiraya + Charai)", min_value=0)
            feet = st.number_input("Tayar Feet", min_value=0)
            rate = st.number_input("Average Sale Rate", min_value=0)
            
            if st.form_submit_button("Sheet mein Save Karen"):
                sale = feet * rate
                pl = sale - cost
                
                new_data = pd.DataFrame([{
                    "Date": str(datetime.now().date()),
                    "User": st.session_state['username'],
                    "Gari": g_no, "Pera": pera, "Tons": ton,
                    "Cost": cost, "Sale": sale, "Profit_Loss": pl
                }])
                
                # Reading and Updating Google Sheet
                try:
                    df = conn.read(worksheet="Sheet1")
                    updated_df = pd.concat([df, new_data], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.success(f"Gari {g_no} ka record save ho gaya!")
                except:
                    st.error("Google Sheet connect nahi ho saki. Check Secrets!")

    elif choice == "📊 Dashboard":
        st.header("Karobar ki Report")
        try:
            data = conn.read(worksheet="Sheet1")
            user_data = data[data['User'] == st.session_state['username']]
            if not user_data.empty:
                col1, col2 = st.columns(2)
                col1.metric("Kul Garian", len(user_data))
                col2.metric("Total Profit/Loss", f"Rs. {user_data['Profit_Loss'].sum():,.0f}")
                st.dataframe(user_data)
            else:
                st.info("Abhi koi record nahi mila.")
        except:
            st.warning("Data load nahi ho raha. Pehli entry karen.")
            
