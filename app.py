
import streamlit as st
import datetime

# Global variable to store receipt
if "receipt_text" not in st.session_state:
    st.session_state.receipt_text = ""

def calculate_rent(rent, food, electricity_spend, charge_per_unit, water, internet, persons, payment_date):
    if persons == 0:
        return "❌ Number of persons cannot be zero", None
    
    total_bill = electricity_spend * charge_per_unit
    total_cost = food + rent + total_bill + water + internet  
    
    if payment_date <= 5:
        discount = total_cost * 0.05  # 5% off
        total_cost -= discount
        message = f'✅ Early payment discount applied: -${discount:.2f}'
    elif payment_date > 25:
        penalty = total_cost * 0.10  # 10% penalty
        total_cost += penalty
        message = f'⚠️ Late Payment Penalty Added: +${penalty:.2f}'
    else:
        message = "✅ Paid on time! No discount or penalty applied."
    
    per_person_cost = total_cost / persons
    return message, per_person_cost

st.title("🏠 Rent Calculator App 💸")

rent = st.number_input("Enter Your hostel/flat rent:", min_value=0.0, step=0.1)
food = st.number_input("Enter The Amount of food ordered:", min_value=0.0, step=0.1)
electricity_spend = st.number_input("Enter total electricity units used:", min_value=0.0, step=0.1)
charge_per_unit = st.number_input("Enter charge per unit of electricity:", min_value=0.0, step=0.1)
water = st.number_input("Enter Water Bill:", min_value=0.0, step=0.1)
internet = st.number_input("Enter Internet Bill:", min_value=0.0, step=0.1)
persons = st.number_input("Enter number of persons living in the room/flat:", min_value=1, step=1)
payment_date = st.slider("Enter the date you paid rent (1-30):", 1, 30, 15)

if st.button("Calculate Rent"):
    message, per_person_cost = calculate_rent(rent, food, electricity_spend, charge_per_unit, water, internet, persons, payment_date)
    st.write(message)
    if per_person_cost:
        st.success(f'💵 Final amount per person: **${per_person_cost:.2f}**')
    
    # 📄 Create Rent Receipt
    receipt_text = f"""
    🏠 Rent Calculator Receipt: ({datetime.date.today()})
    -----------------------------------
    🏠 Total Rent: ${rent}
    🍕 Total Food: ${food}
    ⚡ Total Electricity: ${electricity_spend * charge_per_unit}
    📡 Total Internet: ${internet}
    💧 Total Water: ${water}
    💵 Final Amount per person: ${per_person_cost:.2f}
    -----------------------------------
    """

    # Store in session state
    st.session_state.receipt_text = receipt_text

    # 💾 Save to File
    with open("rent_receipt.txt", "w", encoding="utf-8") as file:
        file.write(receipt_text)

    st.success("✅ Receipt saved as 'rent_receipt.txt' 📄")

# 📌 **Show Rent Receipt in Sidebar on Button Click**
st.sidebar.header("📄 Rent Receipt")
if st.sidebar.button("📜 Show Rent Receipt"):
    if st.session_state.receipt_text:  # Use stored receipt
        st.sidebar.text(st.session_state.receipt_text)
    else:
        st.sidebar.warning("⚠️ No receipt available! Calculate rent first.")
