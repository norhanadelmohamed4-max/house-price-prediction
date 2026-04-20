import streamlit as st
import pickle
import pandas as pd
import os

# تحميل الموديل
model_path = os.path.join(os.getcwd(), "model.pkl")
model = pickle.load(open(model_path, "rb"))

st.set_page_config(page_title="House Price Prediction", layout="centered")

st.title("🏠 House Price Prediction System")
st.write("Enter house details:")

# -----------------------
# اختيار الدولة 🌍
# -----------------------
country = st.selectbox(
    "Select Country",
    ["USA 🇺🇸", "Egypt 🇪🇬", "Saudi Arabia 🇸🇦", "UAE 🇦🇪"]
)

# -----------------------
# اختيار الوحدة 📏
# -----------------------
unit = st.radio("Select Area Unit", ["Square Feet (ft²)", "Square Meter (m²)"])

# -----------------------
# Inputs
# -----------------------
st.subheader("House Features")

col1, col2 = st.columns(2)

with col1:
    gr_liv_area_input = st.number_input("Living Area", value=1000)
    bedrooms = st.number_input("Number of Bedrooms", value=3)

with col2:
    garage_cars = st.number_input("Garage Cars", value=1)
    total_bsmt_input = st.number_input("Basement Area", value=500)

overall_qual = st.slider("Overall Quality", 1, 10, 5)

# -----------------------
# تحويل الوحدات
# -----------------------
if unit == "Square Meter (m²)":
    gr_liv_area = gr_liv_area_input * 10.764
    total_bsmt = total_bsmt_input * 10.764
else:
    gr_liv_area = gr_liv_area_input
    total_bsmt = total_bsmt_input

# -----------------------
# Prediction
# -----------------------
if st.button("Predict Price"):

    input_data = pd.DataFrame(columns=model.feature_names_in_)
    input_data.loc[0] = 0

    input_data["OverallQual"] = overall_qual
    input_data["GrLivArea"] = gr_liv_area
    input_data["BedroomAbvGr"] = bedrooms
    input_data["GarageCars"] = garage_cars
    input_data["TotalBsmtSF"] = total_bsmt

    prediction = model.predict(input_data)
    price = prediction[0]

    # تحويل العملة
    if country == "Egypt 🇪🇬":
        price = price * 50
        currency = "EGP"
    elif country == "Saudi Arabia 🇸🇦":
        price = price * 3.75
        currency = "SAR"
    elif country == "UAE 🇦🇪":
        price = price * 3.67
        currency = "AED"
    else:
        currency = "USD"

    st.success(f"💰 Predicted Price: {price:,.0f} {currency}")
    st.info("⚠️ Price is estimated based on US dataset")