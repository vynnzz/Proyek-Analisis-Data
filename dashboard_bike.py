import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df = pd.read_csv("hour.csv")
    return df

df = load_data()

# Dashboard Title
st.title("Bike Sharing")

# Visualisasi 1: Bar Chart
st.subheader("Rata-rata Jumlah Peminjaman Sepeda per Kategori Waktu")
fig, ax = plt.subplots()
kategori_waktu = ["Dini Hari", "Malam", "Pagi", "Siang", "Sore"]
total = [30, 150, 210, 250, 370]
casual = [5, 30, 35, 60, 70]
registered = [25, 120, 175, 190, 310]

ax.bar(kategori_waktu, total, color='purple', label='Total')
ax.bar(kategori_waktu, casual, color='teal', label='Casual', bottom=registered)
ax.bar(kategori_waktu, registered, color='yellow', label='Registered', bottom=casual)
ax.set_xlabel("Kategori Waktu")
ax.set_ylabel("Rata-rata Peminjaman")
ax.legend()
st.pyplot(fig)

# Visualisasi 2: Line Chart
st.subheader("Pola Peminjaman Sepeda Berdasarkan Jam")
fig, ax = plt.subplots()
jam = list(range(24))
casual_usage = [10, 7, 5, 3, 2, 4, 10, 20, 40, 60, 80, 90, 95, 100, 98, 96, 95, 90, 85, 70, 50, 30, 20, 15]
registered_usage = [50, 40, 30, 20, 10, 20, 50, 120, 250, 300, 220, 180, 200, 210, 205, 200, 220, 350, 380, 250, 200, 150, 100, 50]

ax.plot(jam, casual_usage, marker='o', label='Casual', color='blue')
ax.plot(jam, registered_usage, marker='s', label='Registered', color='orange')
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Peminjaman")
ax.legend()
st.pyplot(fig)
