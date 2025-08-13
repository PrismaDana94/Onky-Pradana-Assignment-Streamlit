# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import glob

# ========================
# Konfigurasi halaman
# ========================
st.set_page_config(page_title="Sales Analysis 2019", layout="wide")

# ========================
# Fungsi load & gabung semua CSV
# ========================
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

# ========================
# Load data
# ========================
df = load_data()

# ========================
# Tambah kolom Month, Month Name & City
# ========================
df['Month'] = df['Order Date'].dt.month
df['Month Name'] = df['Order Date'].dt.strftime('%B')

def get_city(address):
    if pd.notnull(address):
        parts = address.split(',')
        if len(parts) >= 3:
            city = parts[1].strip()
            state = parts[2].strip().split(' ')[0]
            return f"{city} ({state})"
    return None

df['City'] = df['Purchase Address'].apply(get_city)

# Urutan nama bulan untuk sort
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Pastikan kolom Month Name berformat kategori terurut
df['Month Name'] = pd.Categorical(df['Month Name'], categories=month_order, ordered=True)

# ========================
# Sidebar Filter
# ========================
st.sidebar.header("Filter Data")

months = list(df['Month Name'].cat.categories)
selected_month = st.sidebar.multiselect("Pilih Bulan", months, default=months)

cities = sorted(df['City'].dropna().unique())
selected_city = st.sidebar.multiselect("Pilih Kota", cities, default=cities)

products = sorted(df['Product'].dropna().unique())
selected_product = st.sidebar.multiselect("Pilih Produk", products, default=products)

# Terapkan filter
df_filtered = df[
    (df['Month Name'].isin(selected_month)) &
    (df['City'].isin(selected_city)) &
    (df['Product'].isin(selected_product))
].copy()

# ========================
# Skema warna konsisten untuk kota
# ========================
city_colors = px.colors.qualitative.Plotly
city_color_map = {city: city_colors[i % len(city_colors)] for i, city in enumerate(cities)}

# ========================
# Profil & Judul
# ========================
st.title("Sales Analysis 2019")
st.markdown("""
**Nama:** Onky Pradana  
**Project:** Analisis Penjualan Tahun 2019  
**Kontak:** freddycull27@gmail.com
""")

# ========================
# Metrics
# ========================
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.2f}")
col2.metric("Total Orders", df_filtered['Order ID'].nunique())
col3.metric("Unique Products", df_filtered['Product'].nunique())

st.markdown("---")

# ========================
# Grafik 1: Tren Penjualan Bulanan
# ========================
monthly_sales = (
    df_filtered.groupby('Month Name', observed=True)['Sales']
    .sum()
    .reset_index()
    .sort_values('Month Name')
)
fig1 = px.line(monthly_sales, x='Month Name', y='Sales', markers=True, title="Monthly Sales Trend")
st.plotly_chart(fig1, use_container_width=True)

# ========================
# Grafik 2: Top 10 Produk
# ========================
top_products = df_filtered.groupby('Product')['Sales'].sum().nlargest(10).reset_index()
fig2 = px.bar(top_products, x='Sales', y='Product', orientation='h', title="Top 10 Products by Sales")
st.plotly_chart(fig2, use_container_width=True)

# ========================
# Grafik 3: Penjualan per Kota
# ========================
city_sales = df_filtered.groupby('City')['Sales'].sum().reset_index()
fig3 = px.bar(city_sales, x='City', y='Sales', title="Sales by City",
              color='City', color_discrete_map=city_color_map)
st.plotly_chart(fig3, use_container_width=True)

# ========================
# Grafik 4: Sales per Jam
# ========================
df_filtered['Hour'] = df_filtered['Order Date'].dt.hour
hourly_sales = df_filtered.groupby('Hour')['Sales'].sum().reset_index()
fig_hour = px.line(hourly_sales, x='Hour', y='Sales', markers=True, title="Sales by Hour")
st.plotly_chart(fig_hour, use_container_width=True)

# ========================
# Grafik 5: Produk Terlaris di Filter Terpilih
# ========================
top_products_city = df_filtered.groupby('Product')['Sales'].sum().nlargest(5).reset_index()
fig_top_city = px.bar(top_products_city, x='Sales', y='Product', orientation='h',
                      title="Top 5 Products in Selected Filter")
st.plotly_chart(fig_top_city, use_container_width=True)

# ========================
# Grafik 6 (Stacked Bar Chart): Sales per Bulan per Kota
# ========================
fig_stacked = px.bar(
    df_filtered,
    x='Month Name',
    y='Sales',
    color='City',
    title="Sales by City per Month",
    barmode='stack',
    category_orders={"Month Name": month_order},
    color_discrete_map=city_color_map
)
st.plotly_chart(fig_stacked, use_container_width=True)

# ========================
# Preview Data
# ========================
st.markdown("---")
st.subheader("Preview Dataset (Filtered)")
st.dataframe(df_filtered.head())

# ========================
# Tombol download
# ========================
st.download_button(
    "Download data terfilter (CSV)",
    df_filtered.to_csv(index=False),
    file_name="filtered_sales.csv"
)

