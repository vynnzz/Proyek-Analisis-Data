import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

# Judul streamlit
st.title("Data Analysis Dashboard")
st.text('by Danish Gyan Pramana')
st.header('Bike Sharing Visualization')

# Menambahkan logo
#st.image("E:\MAGANGGG\project analisa data DBS\mountain bike.png", width=250)

st.text('Pada dashboard ini, anda bisa melihat project analisa data Bike sharing yang sudah saya lakukan. Pada Project ini, saya menggunakan dua dataset, yaitu day.csv dan hour.csv. Kedua dataset ini telah saya olah sedemikian rupa sehingga menjadi lebih mudah unutk dilakukan analisa dan visualisasi.')
st.text('Berikut adalah beberapa pertanyaan analisa bisnis saya.\n 1. Bagaimana pola penggunaan pengguna kasual jika dibandingkan dengan pengguna terdaftar?\n 2. Bagaimana distribusi jumlah sepeda yang digunakan dari pagi hingga malam?\n 3. kapan terakhir kali sepeda disewa dalam jumlah besar?\n')

st.header('Kesimpulan')
st.text('Pengguna terdaftar menggunakan sepeda untuk keperluan transportasi harian, sementara pengguna kasual lebih aktif di akhir pekan untuk rekreasi. Peminjaman sepeda mengalami dua puncak utama pada pagi dan sore hari, mencerminkan pola perjalanan kerja. Puncak peminjaman tertinggi terjadi pada 15 September 2012, tetapi setelah itu terjadi fluktuasi dan sedikit penurunan. Secara keseluruhan, tren peminjaman meningkat dalam jangka panjang, meskipun ada beberapa fluktuasi akibat faktor eksternal.')

# Membuat sidebar interaktif
with st.sidebar:

    st.text('Bike Sharing Visualization')

    Select_Data = st.selectbox(
        label="Select Data",
        options=('Home', 'Day', 'Hour')
    )

# Membaca dataset day.csv
df_day = pd.read_csv("day_dfclean.csv")
df_day["Date"] = pd.to_datetime(df_day["Date"])

# Filter berdasarkan rentang tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", df_day['Date'].min())
end_date = st.sidebar.date_input("End Date", df_day['Date'].max())

# Filter dataset berdasarkan rentang tanggal yang dipilih untuk dataset 'day'
filtered_df_day = df_day[(df_day['Date'] >= pd.to_datetime(start_date)) & (df_day['Date'] <= pd.to_datetime(end_date))]

# Menampilkan dataset dan visualisasi jika memilih 'Day'
if Select_Data == "Day":
    st.write("📌 **Preview Dataset Day:**")
    st.dataframe(filtered_df_day.head()) 

    st.header('Hasil analisis')
    st.write("1. Bagaimana pola penggunaan pengguna kasual jika dibandingkan dengan pengguna terdaftar?")
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_df_day["Date"], filtered_df_day["Casual"], label="Casual Users", color="orange") 
    plt.plot(filtered_df_day["Date"], filtered_df_day["Registered"], label="Registered Users", color="blue") 
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Pengguna")
    plt.title("Perbandingan Pengguna Kasual vs Terdaftar")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    with st.expander("Penjelasan perbanfingan pengguna casual-terdaftar"):
        st.write(
            """
            **Insight:**
            - Jumlah penyewa sepeda *registered* setiap bulan selalu lebih banyak dibandingkan penyewa *casual*.
            - Namun, pada beberapa bulan tertentu, jumlah penyewa *registered* mengalami penurunan drastis.
            - Penyewa *registered* memiliki tren yang lebih stabil dengan sedikit fluktuasi dibandingkan penyewa *casual*,
              menunjukkan bahwa mereka menggunakan layanan ini secara lebih konsisten.
            - Musim panas (Mei - September) menunjukkan peningkatan signifikan dalam jumlah penyewa *casual*,
              kemungkinan karena lebih banyak orang menggunakan layanan ini untuk rekreasi.
            - Sebaliknya, musim dingin (Desember - Januari) mengalami penurunan drastis,
              kemungkinan disebabkan oleh cuaca dingin yang mengurangi aktivitas luar ruangan.
            """
        )

    # Mengelompokkan data berdasarkan hari dalam seminggu
    weekday_usage = filtered_df_day.groupby("Weekday")[["Casual", "Registered"]].mean() 
    plt.figure(figsize=(10, 5))
    plt.plot(weekday_usage.index, weekday_usage["Casual"], marker='o', linestyle="--", label="Casual")
    plt.plot(weekday_usage.index, weekday_usage["Registered"], marker='s', linestyle="-", label="Registered")
    plt.xticks(ticks=range(7), labels=["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
    plt.xlabel("Hari dalam Seminggu")
    plt.ylabel("Rata-rata Jumlah Peminjaman")
    plt.title("Pola Peminjaman Sepeda Berdasarkan Hari dalam Seminggu")
    plt.legend()
    plt.grid()
    plt.show()
    st.pyplot(plt)

    with st.expander("Penjelasan Pola Peminjaman Sepeda Berdasarkan Hari dalam Seminggu"):
        st.write(
            """
            **Insight:**
            Pola Peminjaman oleh Pengguna Terdaftar
            - Pengguna terdaftar cenderung meminjam sepeda lebih banyak pada hari kerja (Senin - Jumat).
            - Jumlah peminjaman tertinggi terjadi pada hari Kamis, lalu sedikit menurun pada hari Jumat.
            - Peminjaman menurun drastis pada Sabtu dan Minggu, yang menunjukkan bahwa pengguna terdaftar kemungkinan besar menggunakan sepeda untuk aktivitas rutin seperti pergi ke kantor atau sekolah.

            Pola Peminjaman oleh Pengguna Kasual
            - Berbeda dengan pengguna terdaftar, peminjaman oleh pengguna kasual lebih rendah selama hari kerja.
            - Peminjaman meningkat tajam pada Sabtu dan Minggu, mencapai puncaknya pada hari Sabtu.
            - Ini menunjukkan bahwa pengguna kasual lebih banyak menggunakan sepeda untuk keperluan rekreasi atau santai di akhir pekan.
            """
        )

    st.text('kapan terakhir kali sepeda disewa dalam jumlah besar?')
    filtered_df_day['Date'] = pd.to_datetime(filtered_df_day['Date'])
    filtered_df_day['Date'] = filtered_df_day['Date'].dt.date 
    
    daily_rentals = filtered_df_day.groupby('Date')['Total Penyewaan Sepeda'].sum() 

    # mencari tanggal dengan jumlah penyewaan terbesar
    peak_date = daily_rentals.idxmax()
    peak_value = daily_rentals.max()

    # Visualisasi
    plt.figure(figsize=(20, 5))
    plt.plot(daily_rentals.index, daily_rentals.values, label='Total Rentals', color='b')
    plt.axvline(x=peak_date, color='r', linestyle='--', label=f'Puncak: {peak_date}')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Peminjaman')
    plt.title('Analisis Peminjaman Sepeda Harian')
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    # Menampilkan informasi tanggal penyewaan tertinggi
    st.write(f'**Tanggal dengan jumlah penyewaan tertinggi:** {peak_date} dengan {peak_value} penyewaan.')

    with st.expander("Penjelasan Pola Peminjaman Sepeda Berdasarkan Hari dalam Seminggu"):
        st.write(
            """
            **Insight:**
            - Secara keseluruhan, jumlah peminjaman sepeda cenderung meningkat dari awal tahun 2011 hingga pertengahan 2012.
            - Terlihat ada fluktuasi besar dalam jumlah peminjaman, dengan beberapa penurunan tajam yang kemungkinan disebabkan oleh faktor cuaca, musim, atau hari libur.
            - Garis vertikal merah menandai tanggal dengan jumlah peminjaman tertinggi, yaitu pada 15 September 2012. Pada tanggal ini, jumlah penyewaan sepeda mencapai titik tertinggi.
            """
        )
#===================================================================================#

# Membaca dataset hour.csv
df_hour = pd.read_csv("hour_dfclean.csv")

# Filter dataset berdasarkan rentang tanggal yang dipilih 
df_hour['Date'] = pd.to_datetime(df_hour['Date']) 
filtered_df_hour = df_hour[(df_hour['Date'] >= pd.to_datetime(start_date)) & (df_hour['Date'] <= pd.to_datetime(end_date))]

# Menampilkan dataset dan visualisasi jika memilih 'Hour'
if Select_Data == "Hour":
    st.write("📌 **Preview Dataset Hour:**")
    st.dataframe(filtered_df_hour.head()) 
    st.header('Hasil analisis')
    st.text('Bagaimana distribusi jumlah sepeda yang digunakan dari pagi hingga malam?')

    hourly_usage = filtered_df_hour.groupby("Hour")[["Casual", "Registered"]].mean()

    # Plot hasil analisis
    plt.figure(figsize=(10, 5))
    plt.plot(hourly_usage.index, hourly_usage["Casual"], marker="o", linestyle="--", label="Casual Users", color="blue")
    plt.plot(hourly_usage.index, hourly_usage["Registered"], marker="s", linestyle="-", label="Registered Users", color="orange")
    plt.xlabel("Jam dalam Sehari")
    plt.ylabel("Rata-rata Jumlah Peminjaman")
    plt.title("Distribusi Penggunaan Sepeda dari Pagi hingga Malam")
    plt.xticks(range(0, 24)) 
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)

    with st.expander("Penjelasan Pola Peminjaman Sepeda Berdasarkan Hari dalam Seminggu"):
        st.write(
            """
            **Insight:**
            - Disini saya menyajikan visualisasi dalam dua bentuk grafik
            - jumlah penyewa sepeda registered tertinggi ada di jam 8:00 dan 17:00. ini terjadi karena pada jam itu banyak orang yang membutuhkan speda untuk berangkat dan pulang dari kegiatan nya masing-masing
            - jumlah penyewa sepeda registered cenderung stabil tidak ada lonjakan
            - jumlah penyewa sepeda registered selalu lebih banyak daripada penyewa sepeda casual
            """
        )

    # Membuat kategori waktu berdasarkan jam
    def categorize_time(hour):
        if 0 <= hour < 6:
            return 'Dini Hari'
        elif 6 <= hour < 12:
            return 'Pagi'
        elif 12 <= hour < 16:
            return 'Siang'
        elif 16 <= hour < 20:
            return 'Sore'
        else:
            return 'Malam'

    # Membuat kolom kategori waktu
    filtered_df_hour['kategori_waktu'] = filtered_df_hour['Hour'].apply(categorize_time) 
    average_rental_by_time = filtered_df_hour.groupby("kategori_waktu")[["Total Penyewaan Sepeda", "Casual", "Registered"]].mean() 
    print(average_rental_by_time)

    # Visualisasi 
    plt.figure(figsize=(8,5))
    average_rental_by_time.plot(kind="bar", figsize=(10,5), colormap="viridis")
    plt.title("Rata-rata Jumlah Peminjaman Sepeda per Kategori Waktu")
    plt.xlabel("Kategori Waktu")
    plt.ylabel("Rata-rata Peminjaman")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(["Total", "Casual", "Registered"])
    plt.show()
    st.pyplot(plt)

    with st.expander("Penjelasan Pola Peminjaman Sepeda Berdasarkan Hari dalam Seminggu"):
        st.write(
            """
            **Insight:**
            - Waktu terbaik untuk penyedia layanan peminjaman sepeda adalah sore dan siang hari, karena peminjaman tertinggi terjadi pada periode ini.
            - Peningkatan layanan pada pagi dan sore hari bisa meningkatkan jumlah sepeda di lokasi strategis dan dapat meningkatkan kepuasan pengguna.
            - Penyewa sepeda registered mendominasi peminjaman, sehingga strategi pemasaran bisa lebih difokuskan pada pengguna yang berlangganan.
            """
        )    
