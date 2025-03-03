import streamlit as st
import requests

def convert_units(category, from_unit, to_unit, value):
    conversions = {
        "📏 Length": {"Meter": 1, "Kilometer": 0.001, "Mile": 0.000621371, "Yard": 1.09361, "Foot": 3.28084},
        "⚖️ Weight": {"Kilogram": 1, "Gram": 1000, "Pound": 2.20462, "Ounce": 35.274},
        "🌡️ Temperature": "special",
        "⏳ Time": {"Second": 1, "Minute": 1/60, "Hour": 1/3600, "Day": 1/86400},
    }
    
    if category == "🌡️ Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        else:
            return "❌ Invalid Conversion"

    if from_unit in conversions[category] and to_unit in conversions[category]:
        return value * (conversions[category][to_unit] / conversions[category][from_unit])
    return "❌ Invalid Conversion"

def get_live_currency_rate(from_currency, to_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url).json()
        rate = response.get("rates", {}).get(to_currency)
        return rate if rate else "❌ Invalid Currency"
    except:
        return "⚠️ Error fetching rates"
st.set_page_config(page_title="Unit Converter", layout="wide", page_icon="💱")
st.markdown("<h1 style='text-align: center;'>🔄 Unit Converter 🔄</h1>", unsafe_allow_html=True)

category = st.sidebar.radio("🛠️ Choose a Category", ["📏 Length", "⚖️ Weight", "🌡️ Temperature", "⏳ Time", "💰 Currency", "🔧 Custom Conversion"])

if category == "💰 Currency":
    col1, col2, col3 = st.columns(3)
    with col1:
        from_currency = st.text_input("🔹 From Currency (e.g., USD)", "USD").upper()
    with col2:
        to_currency = st.text_input("🔹 To Currency (e.g., EUR)", "EUR").upper()
    with col3:
        amount = st.number_input("💵 Enter Amount", min_value=0.01, value=1.0)
    
    if st.button("🔄 Convert Currency"):
        rate = get_live_currency_rate(from_currency, to_currency)
        if isinstance(rate, str):
            st.error("❌ Invalid currency code or error fetching rates!")
        else:
            st.success(f"✅ {amount} {from_currency} = **{round(amount * rate, 2)} {to_currency}** 💲")

elif category == "🔧 Custom Conversion":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        unit_name = st.text_input("📌 Unit Name", "Custom Unit")
    with col2:
        from_unit = st.text_input("🔹 From Unit", "Unit A")
    with col3:
        to_unit = st.text_input("🔹 To Unit", "Unit B")
    with col4:
        conversion_factor = st.number_input("🔢 Conversion Factor", min_value=0.0001, value=1.0)
    
    value = st.number_input("📏 Enter Value", min_value=0.0, value=1.0)
    if st.button("🔄 Convert Custom Unit"):
        st.success(f"✅ {value} {from_unit} = **{round(value * conversion_factor, 4)} {to_unit}** 🎯")

else:
    units = {
        "📏 Length": ["Meter", "Kilometer", "Mile", "Yard", "Foot"],
        "⚖️ Weight": ["Kilogram", "Gram", "Pound", "Ounce"],
        "🌡️ Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
        "⏳ Time": ["Second", "Minute", "Hour", "Day"]
    }
    col1, col2, col3 = st.columns(3)
    with col1:
        from_unit = st.selectbox("🔹 From Unit", units[category])
    with col2:
        to_unit = st.selectbox("🔹 To Unit", units[category])
    with col3:
        value = st.number_input("📏 Enter Value", min_value=0.0, value=1.0)
    
    if st.button("🔄 Convert Unit"):
        result = convert_units(category, from_unit, to_unit, value)
        if result == "❌ Invalid Conversion":
            st.error("⚠️ Invalid conversion! Please check your units.")
        else:
            st.success(f"✅ {value} {from_unit} = **{round(result, 4)} {to_unit}** 🎯")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🔹 <b>Unit Converter</b> | Built with ❤️ using Streamlit 🚀</p>", unsafe_allow_html=True)



