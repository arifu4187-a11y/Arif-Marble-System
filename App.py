import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Arif Khan Marble Supplier", layout="wide")

# Database initialize (Temporary)
if 'gari_records' not in st.session_state:
    st.session_state['gari_records'] = []

st.title("🏗️ Arif Khan Marble Supplier")

menu = ["📊 Dashboard", "🚚 Gari ki Entry (Nafa/Nuqsan)", "📒 Records"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "🚚 Gari ki Entry (Nafa/Nuqsan)":
    st.header("Gari aur Pera (Lot) ka Mukammal Hisab")
    
    with st.form("gari_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            gari_no = st.text_input("Gari Number / Driver")
            pera_type = st.radio("Pera (Lot) Select Karen", ["Pehla Pera", "Doosra Pera", "Teesra Pera"])
            tons = st.number_input("Kul Tan (Tons)", min_value=0.0)
            purchase_cost = st.number_input("Pahad ki Qeemat + Kiraya", min_value=0)
            cutting_expenses = st.number_input("Charai + Mazdoori + Other", min_value=0)
        
        with col2:
            st.info("Sale ki Detail")
            total_feet = st.number_input("Gari se Nikla Kul Foot (Sq. Ft)", min_value=0)
            avg_sale_rate = st.number_input("Average Sale Rate (Per Foot)", min_value=0)
            extra_income = st.number_input("Koi aur Aamadni (Kachra/Chips)", min_value=0)

        submit = st.form_submit_button("Gari ka Hisab Check Karen")
        
        if submit:
            # Calculations
            total_cost = purchase_cost + cutting_expenses
            total_sale = (total_feet * avg_sale_rate) + extra_income
            profit_loss = total_sale - total_cost
            
            # Record save karna
            st.session_state['gari_records'].append({
                "Gari": gari_no, "Pera": pera_type, "Cost": total_cost, 
                "Sale": total_sale, "P_L": profit_loss
            })
            
            st.divider()
            st.subheader("Nateeja (Result)")
            if profit_loss > 0:
                st.success(f"Mubarak! Is gari par Rs. {profit_loss:,.2f} MUNAFA hua hai.")
            elif profit_loss < 0:
                st.error(f"Afsos! Is gari par Rs. {abs(profit_loss):,.2f} NUQSAN hua hai.")
            else:
                st.warning("Barabar raha, na nafa na nuqsan.")

elif choice == "📊 Dashboard":
    st.header("Karobar ka Kul Nafa Nuqsan")
    if st.session_state['gari_records']:
        df = pd.DataFrame(st.session_state['gari_records'])
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Garian", len(df))
        col2.metric("Total Sale", f"Rs. {df['Sale'].sum():,.0f}")
        total_pl = df['P_L'].sum()
        col3.metric("Net Profit/Loss", f"Rs. {total_pl:,.0f}", delta=float(total_pl))
        
        st.write("### Pera (Lot) ke Hisab se Performance")
        st.bar_chart(df.set_index('Pera')['P_L'])
    else:
        st.info("Abhi tak koi gari record nahi ki gayi.")

elif choice == "📒 Records":
    st.header("Purani Gariyon ka Record")
    if st.session_state['gari_records']:
        st.table(pd.DataFrame(st.session_state['gari_records']))
    else:
        st.write("Record khali hai.")
    
          
