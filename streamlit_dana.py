# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import glob

# Konfigurasi halaman
st.set_page_config(page_title="Sales Analysis 2019", layout="wide")

# Fungsi load & gabung semua CSV
@st.cache_data
def load_data():
    files = glob.glob("sales_data_*.csv")  # baca semua file dengan pola nama ini
    all_data = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file)
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce', format="%m/%d/%y %H:%M")
        df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
        df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
        df['Sales'] = df['Quantity Ordered'] * df['Price Each']
        all_data = pd.concat([all_data, df], ignore_index=True)

    return all_data

# Load data
df = load_data()

# Profil & Judul
st.title("Sales Analysis 2019")
st.markdown("""
*Nama:* Onky Pradana  
*Project:* Analisis Penjualan Tahun 2019  
*Kontak:* freddycull27@gmail.com
""")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
col2.metric("Total Orders", df['Order ID'].nunique())
col3.metric("Unique Products", df['Product'].nunique())

st.markdown("---")

# Pilihan filter bulan
months = sorted(df_all['month'].unique())
selected_month = st.selectbox("Pilih Bulan", months)
df_filtered = df_all[df_all['month'] == selected_month]

st.subheader(f"Data Penjualan - {selected_month}")
st.dataframe(df_filtered)

# Grafik 1: Tren Penjualan Bulanan
df['Month'] = df['Order Date'].dt.month
monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()
fig1 = px.line(monthly_sales, x='Month', y='Sales', markers=True, title="Monthly Sales Trend")
st.plotly_chart(fig1, use_container_width=True)

# Grafik 2: Top 10 Produk
top_products = df.groupby('Product')['Sales'].sum().nlargest(10).reset_index()
fig2 = px.bar(top_products, x='Sales', y='Product', orientation='h', title="Top 10 Products by Sales")
st.plotly_chart(fig2, use_container_width=True)

# Grafik 3: Penjualan per Kota
df['City'] = df['Purchase Address'].apply(lambda x: x.split(',')[1] if pd.notnull(x) else None)
city_sales = df.groupby('City')['Sales'].sum().reset_index()
fig3 = px.bar(city_sales, x='City', y='Sales', title="Sales by City")
st.plotly_chart(fig3, use_container_width=True)

# Preview Data
st.markdown("---")
st.subheader("Preview Dataset")
st.dataframe(df.head())

# Tombol download
st.download_button(
    "Download data terfilter (CSV)",
    df.to_csv(index=False),
    file_name="filtered_sales.csv"
)
