import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("f49e3769edd292a189239e69a692958c")

st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️")

# --- FUNGSI AMBIL DATA ---
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=id"
    response = requests.get(url)
    return response.json()

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=id"
    response = requests.get(url)
    return response.json()

# --- UI APP ---
st.title("🌤️ Real-Time Weather Dashboard")
city = st.text_input("Masukkan Nama Kota:", "Jakarta")

if city:
    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("Kota tidak ditemukan!")
    else:
        # Menampilkan Cuaca Saat Ini
        col1, col2, col3 = st.columns(3)
        col1.metric("Suhu", f"{data['main']['temp']} °C")
        col2.metric("Kelembapan", f"{data['main']['humidity']}%")
        col3.metric("Kondisi", data['weather'][0]['description'].capitalize())

        # Menampilkan Forecast (Ramalan Cuaca)
        st.subheader("📅 Ramalan Cuaca 5 Hari Ke Depan")
        forecast_data = get_forecast(city)

        # Olah data untuk grafik
        list_forecast = []
        for item in forecast_data['list']:
            list_forecast.append({
                "Waktu": item['dt_txt'],
                "Suhu": item['main']['temp']
            })

        df = pd.DataFrame(list_forecast)
        fig = px.line(df, x='Waktu', y='Suhu', title=f"Tren Suhu di {city}")
        st.plotly_chart(fig, use_container_width=True)
