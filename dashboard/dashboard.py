import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set(style='dark')

# Set full-width layout
st.set_page_config(layout="wide")

# Custom CSS to adjust font sizes
st.markdown("""
    <style>
    .big-font {
        font-size:100px !important;
    }
    .medium-font {
        font-size:26px !important;
    }
    .subheader-font {
        font-size:24px !important;
    }
    .small-font {
        font-size:20px !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Load the data
day_df = pd.read_csv("day_clear.csv")
hour_df = pd.read_csv("hour_clear.csv")

# Dashboard Title and Introduction
st.markdown('<p class="big-font">Bike Sharing Dashboard 🚴‍♂️</p>', unsafe_allow_html=True)
st.markdown('<p class="medium-font" style="margin-left: 10px;">by Muhamad Faqih Zacky | ML-58</p>', unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# Create dashboard layout using columns and containers
with st.container():
    col1, col2 = st.columns(2)

    # Visualization 1: Bike Rentals by Weather in col1
    with col1:
        st.markdown('<p class="subheader-font">🌤️ Penyewaan Sepeda Berdasarkan Cuaca</p>', unsafe_allow_html=True)
        weather_sum = day_df.groupby(by="weathersit").cnt.sum().reset_index()

        if 4 not in weather_sum['weathersit'].values:
            weather_sum = pd.concat([weather_sum, pd.DataFrame({'weathersit': [4], 'cnt': [0]})])

        weather_map = {1: 'Clear', 2: 'Misty', 3: 'Light Snow/Rain', 4: 'Heavy Snow/Rain'}
        weather_sum['weathersit'] = weather_sum['weathersit'].replace(weather_map)

        weather_sum = weather_sum.sort_values(by='cnt', ascending=False).reset_index(drop=True)

        plt.figure(figsize=(7,4.2))
        ax = sns.barplot(x='weathersit', y='cnt', data=weather_sum, color="royalblue")

        plt.title('Perbandingan Jumlah Penyewaan Sepeda Berdasarkan Cuaca')
        plt.xlabel('Cuaca')
        plt.ylabel('Jumlah Penyewaan Sepeda')

        for p in ax.patches:
            ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 30000, f'{int(p.get_height()):,}', ha='center')

        plt.ylim(0, 2500000)
        plt.yticks(range(0, 2500001, 500000), [f'{x:,}' for x in range(0, 2500001, 500000)])

        sns.lineplot(data=weather_sum, x='weathersit', y='cnt', marker='o', color='gold', linewidth=2, ax=ax)
        st.pyplot(plt)
        

    # Visualization 2: Bike Rentals by Season in col2
    with col2:
        st.markdown('<p class="subheader-font">🌱 Penyewaan Sepeda Berdasarkan Musim</p>', unsafe_allow_html=True)
        season_sum = day_df.groupby(by="season").cnt.sum().reset_index()
        season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
        season_sum['season'] = season_sum['season'].replace(season_map)
        season_sum = season_sum.sort_values(by='cnt', ascending=False).reset_index(drop=True)

        plt.figure(figsize=(7,4.2))
        ax = sns.barplot(x='season', y='cnt', data=season_sum, color="navajowhite")
        plt.title('Penyewaan Sepeda vs Musim')
        plt.xlabel('Musim')
        plt.ylabel('Jumlah Penyewaan Sepeda')

        for p in ax.patches:
            ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 30000, f'{int(p.get_height()):,}', ha='center')

        plt.ylim(0, 1250000)
        plt.yticks(range(0, 1250001, 250000), [f'{x:,}' for x in range(0, 1250001, 250000)])

        sns.lineplot(data=season_sum, x='season', y='cnt', marker='o', color='cornflowerblue', linewidth=2, ax=ax)
        st.pyplot(plt)

# Ratio of Working Days vs Non-working Days Visualization
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="subheader-font">📅 Rasio Penyewaan di Hari Kerja dan Hari Libur</p>', unsafe_allow_html=True)

        workingday_sum = day_df.groupby(by="workingday").agg({"cnt": "sum"}).sort_values(by="cnt", ascending=False).reset_index()

        total_workingday = workingday_sum.loc[workingday_sum['workingday'] == 1, 'cnt'].values[0]  
        total_nonworkingday = workingday_sum.loc[workingday_sum['workingday'] == 0, 'cnt'].values[0]  

        data = [total_workingday, total_nonworkingday]
        labels = ['Hari Kerja', 'Hari Libur']
        explode = (0.1, 0)

        total = total_workingday + total_nonworkingday
        persentase_workingday = (total_workingday / total) * 100
        persentase_nonworkingday = (total_nonworkingday / total) * 100

        plt.figure(figsize=(4, 2.85))
        plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'}, explode=explode)
        plt.title('Rasio Perbandingan Penyewa di Hari Kerja dan Hari Libur')
        plt.figtext(0.5, -0.1, f"Jarak Perbedaan Rasio Penyewa Hari Kerja dan Hari Libur: {persentase_workingday:.1f}% - {persentase_nonworkingday:.1f}% = {(persentase_workingday-persentase_nonworkingday):.1f}%", 
                    ha='center', fontsize=10)
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)

# Bike Rentals by Hour Visualization in Full Width
    with col2:
        # Visualization: Bike Rentals by Hour
        st.markdown('<p class="subheader-font">🕒 Penyewaan Sepeda Berdasarkan Jam</p>', unsafe_allow_html=True)

        hour_sum = hour_df.groupby(by="hr").agg({"cnt": "sum"}).reset_index()

        # Mendapatkan jam paling ramai dan paling sepi
        jam_ramai = hour_sum.loc[hour_sum['cnt'].idxmax()]
        jam_sepi = hour_sum.loc[hour_sum['cnt'].idxmin()]

        plt.figure(figsize=(10, 6))
        plt.bar(hour_sum['hr'], hour_sum['cnt'], color='royalblue', edgecolor='black')

        # Menambahkan garis untuk jam paling ramai dan paling sepi
        plt.axhline(y=jam_ramai['cnt'], color='red', linestyle='--')
        plt.axhline(y=jam_sepi['cnt'], color='green', linestyle='--')

        # Menambahkan teks di tengah-tengah sumbu x
        plt.text(x=hour_sum['hr'].median(), y=jam_ramai['cnt'] - 20000, 
                s=f'Jam Paling Ramai: Jam {int(jam_ramai["hr"])} ({jam_ramai["cnt"]})', 
                color='red', ha='center', fontsize=10, backgroundcolor='white')
        plt.text(x=hour_sum['hr'].median(), y=jam_sepi['cnt'] + 10000, 
                s=f'Jam Paling Sepi: Jam {int(jam_sepi["hr"])} ({jam_sepi["cnt"]})', 
                color='green', ha='center', fontsize=10, backgroundcolor='white')

        # Menambahkan judul dan label sumbu
        plt.title('Total Penyewaan Sepeda Setiap Jamnya')
        plt.xlabel('Jam')
        plt.ylabel('Sepeda Yang Disewa')

        # Mengatur ticks sumbu x berdasarkan jam
        plt.xticks(hour_sum['hr'])

        # Menyempurnakan layout agar lebih rapi
        plt.tight_layout()

        # Menampilkan plot di Streamlit
        st.pyplot(plt)

st.markdown('<hr>', unsafe_allow_html=True)
st.caption('Muhamad Faqih Zacky | ML-58')

