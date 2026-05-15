import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="AgroConnect", layout="wide")

# this is test

# ----------------------------
# LOAD CSV FILES
# ----------------------------

users = pd.read_csv("users.csv")
products = pd.read_csv("products.csv")
orders = pd.read_csv("orders.csv")

# ----------------------------
# SIDEBAR
# ----------------------------

st.sidebar.title("AgroConnect")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Login",
        "Farmer Dashboard",
        "Vendor Dashboard",
        "Weather",
        "Analytics",
        "AI Prediction",
        "Contact"
    ]
)

# ----------------------------
# HOME PAGE
# ----------------------------

if menu == "Home":
    st.title("🌾 AgroConnect")
    st.subheader("Farmer Import-Export & Vegetable Marketplace")

    st.write("""
    AgroConnect helps farmers and vendors connect directly.
    
    Features:
    - Farmer Login
    - Vendor Orders
    - Weather Forecast
    - AI Price Prediction
    - Market Analytics
    """)

# ----------------------------
# LOGIN PAGE
# ----------------------------

elif menu == "Login":

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = users[
            (users["username"] == username) &
            (users["password"] == password)
        ]

        if not user.empty:
            role = user.iloc[0]["role"]
            st.success(f"Login Successful as {role}")
        else:
            st.error("Invalid Credentials")

# ----------------------------
# FARMER DASHBOARD
# ----------------------------

elif menu == "Farmer Dashboard":

    st.title("👨‍🌾 Farmer Dashboard")

    product = st.text_input("Vegetable Name")
    quantity = st.number_input("Quantity", min_value=1)
    price = st.number_input("Price Per KG", min_value=1)

    if st.button("Add Product"):

        new_product = pd.DataFrame({
            "product": [product],
            "quantity": [quantity],
            "price": [price],
            "farmer": ["farmer1"]
        })

        products = pd.concat([products, new_product])

        products.to_csv("products.csv", index=False)

        st.success("Product Added Successfully")

    st.subheader("Available Products")
    st.dataframe(products)

# ----------------------------
# VENDOR DASHBOARD
# ----------------------------

elif menu == "Vendor Dashboard":

    st.title("🛒 Vendor Dashboard")

    st.subheader("Available Vegetables")
    st.dataframe(products)

    selected_product = st.selectbox(
        "Select Product",
        products["product"]
    )

    order_qty = st.number_input(
        "Order Quantity",
        min_value=1
    )

    if st.button("Place Order"):

        new_order = pd.DataFrame({
            "vendor": ["vendor1"],
            "product": [selected_product],
            "quantity": [order_qty],
            "status": ["Pending"]
        })

        orders = pd.concat([orders, new_order])

        orders.to_csv("orders.csv", index=False)

        st.success("Order Placed Successfully")

    st.subheader("Orders")
    st.dataframe(orders)

# ----------------------------
# WEATHER PAGE
# ----------------------------

elif menu == "Weather":

    st.title("🌦 Weather Forecast")

    city = st.text_input("Enter City Name")

    API_KEY = "YOUR_OPENWEATHER_API_KEY"

    if st.button("Get Weather"):

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)

        data = response.json()

        if data["cod"] == 200:

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]

            st.metric("Temperature", f"{temp} °C")
            st.metric("Humidity", f"{humidity}%")

        else:
            st.error("City Not Found")

# ----------------------------
# ANALYTICS PAGE
# ----------------------------

elif menu == "Analytics":

    st.title("📊 Analytics Dashboard")

    fig = px.bar(
        products,
        x="product",
        y="quantity",
        color="product",
        title="Available Vegetable Quantity"
    )

    st.plotly_chart(fig)

# ----------------------------
# AI PREDICTION PAGE
# ----------------------------

elif menu == "AI Prediction":

    st.title("🤖 AI Price Prediction")

    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([20, 25, 30, 35, 40])

    model = LinearRegression()
    model.fit(X, y)

    future_day = st.slider("Select Future Day", 1, 10)

    prediction = model.predict([[future_day]])

    st.success(
        f"Predicted Price: ₹{prediction[0]:.2f}"
    )

# ----------------------------
# CONTACT PAGE
# ----------------------------

elif menu == "Contact":

    st.title("📞 Contact Us")

    st.write("""
    Email: support@agroconnect.com
    
    Phone: +91 9876543210
    
    Address: Pune, Maharashtra
    """)