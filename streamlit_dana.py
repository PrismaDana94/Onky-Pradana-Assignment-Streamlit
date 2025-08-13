# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import re

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
    if not files:
        return pd.DataFrame()
    all_frames = []
    for file in files:
        try:
            df = pd.read_csv(file)
        except Exception:
            # fallback encoding jika diperlukan
            df = pd.read_csv(file, encoding='latin1')
        # parsing tanggal permissive
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce', infer_datetime_format=True)
        else:
            df['Order Date'] = pd.NaT
        # numeric columns (jika ada)
        df['Quantity Ordered'] = pd.to_numeric(df.get('Quantity Ordered'), errors='coerce')
        df['Price Each'] = pd.to_numeric(df.get('Price Each'), errors='coerce')
        df['Sales'] = df['Quantity Ordered'] * df['Price Each']
        all_frames.append(df)
    return pd.concat(all_frames, ignore_index=True) if all_frames else pd.DataFrame()

# ========================
# Load data
# ========================
df = load_data()

if df.empty:
    st.error("Data tidak ditemukan atau file 'sales_data_*.csv' kosong. Pastikan file tersedia di folder kerja.")
    st.stop()

# ========================
# Ekstrak kolom waktu & bulan
# ========================
df['Month'] = df['Order Date'].dt.month
df['Month Name'] = df['Order Date'].dt.strftime('%B')  # bisa NaN bila Order Date invalid

# ========================
# Fungsi robust untuk ekstrak City (State)
# ========================
def extract_city_state(address):
    if pd.notnull(address):
        parts = address.split(',')
        if len(parts) >= 3:  # format normal
            city = parts[1].strip()
            state = parts[2].strip().split(' ')[0]
            return f"{city} ({state})"
    return None

df_clean['City'] = df_clean['Purchase Address'].apply(extract_city_state)
print(df_clean[['Purchase Address', 'City']].head())

    # 1) pola umum: "... , City, ST 12345" atau "... , City, ST"
    m = re.search(r',\s*([^,]+),\s*([A-Za-z]{2})\b', addr)
    if m:
        city = m.group(1).strip()
        state = m.group(2).strip().upper()
        return f"{city} ({state})"

    # 2) pola "City, ST" (tanpa street)
    m = re.search(r'^\s*([^,]+),\s*([A-Za-z]{2})\b', addr)
    if m:
        city = m.group(1).strip()
        state = m.group(2).strip().upper()
        return f"{city} ({state})"

    # 3) pola tanpa koma: "City ST ZIP" -> capture City & ST
    m = re.search(r'([A-Za-z\s]+)\s+([A-Za-z]{2})\s+\d{5}', addr)
    if m:
        city = m.group(1).strip()
        state = m.group(2).strip().upper()
        return f"{city} ({state})"

    # 4) fallback: split by comma atau titik, gunakan bagian kedua dari belakang jika memungkinkan
    parts = [p.strip() for p in re.split(r',|\.', addr) if p.strip()]
    if len(parts) >= 3:
        city = parts[-2]
        state_token = parts[-1].split()[0]
        if len(state_token) <= 3:
            return f"{city} ({state_token.upper()})"
        return city
    if len(parts) == 2:
        # kemungkinan "City, State" atau "Street, City"
        first, second = parts
        second_tok = second.split()[0]
        if len(second_tok) <= 3:
            return f"{first} ({second_tok.upper()})"
        return second

    # 5) terakhir, kembalikan string (lebih baik daripada error)
    return addr

# ========================
# Buat kolom City
# ========================
if 'Purchase Address' in df.columns:
    df['City'] = df['Purchase Address'].apply(extract_city_state)
elif 'City' in df.columns and 'State' in df.columns:
    df['City'] = df['City'].astype(str).str.strip() + " (" + df['State'].astype(str).str.strip() + ")"
else:
    df['City'] = None

# ========================
# Urutan nama bulan (kategori terurut)
# ========================
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
if df['Month Name'].notna().any():
    df['Month Name'] = pd.Categorical(df['Month Name'], categories=month_order, ordered=True)

# ========================
# Sidebar Filter
# ========================
st.sidebar.header("Filter Data")

# tampilkan bulan yang ada (tetap urut berdasarkan month_order)
present_months = [m for m in month_order if m in list(df['Month Name'].dropna().unique())]
if not present_months:
    # fallback: gunakan angka bulan jika Month Name tidak tersedia
    present_months = sorted(df['Month'].dropna().unique())

selected_month = st.sidebar.multiselect("Pilih Bulan", present_months, default=present_months)

cities_all = sorted([c for c in df['City'].dropna().unique()])
selected_city = st.sidebar.multiselect("Pilih Kota", cities_all, default=cities_all)

products_all = sorted(df['Product'].dropna().unique()) if 'Product' in df.columns else []
selected_product = st.sidebar.multiselect("Pilih Produk", products_all, default=products_all)

# ========================
# Terapkan filter (safe copy)
# ========================
mask = df['Month Name'].isin(selected_month) if isinstance(selected_month[0], str) or selected_month else df['Month Name'].isin(selected_month)
mask &= df['City'].isin(selected_city)
if products_all:
    mask &= df['Product'].isin(selected_product)

df_filtered = df[mask].copy()

if df_filtered.empty:
    st.warning("Tidak ada data setelah diterapkan filter. Coba ubah pilihan filter.")
    st.dataframe(df_filtered.head())
    st.stop()

# ========================
# Skema warna konsisten untuk kota (berdasarkan seluruh dataset)
# ========================
city_colors = px.colors.qualitative.Plotly
unique_cities = sorted(df['City'].dropna().unique())
city_color_map = {city: city_colors[i % len(city_colors)] for i, city in enumerate(unique_cities)}

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
total_sales = df_filtered['Sales'].sum() if 'Sales' in df_filtered.columns else 0
total_orders = df_filtered['Order ID'].nunique() if 'Order ID' in df_filtered.columns else df_filtered.shape[0]
unique_products = df_filtered['Product'].nunique() if 'Product' in df_filtered.columns else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Unique Products", unique_products)

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
if 'Product' in df_filtered.columns:
    top_products = df_filtered.groupby('Product')['Sales'].sum().nlargest(10).reset_index()
    fig2 = px.bar(top_products, x='Sales', y='Product', orientation='h', title="Top 10 Products by Sales")
    st.plotly_chart(fig2, use_container_width=True)

# ========================
# Grafik 3: Penjualan per Kota
# ========================
city_sales = df_filtered.groupby('City')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
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
if 'Product' in df_filtered.columns:
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
# Preview Data & Download
# ========================
st.markdown("---")
st.subheader("Preview Dataset (Filtered)")
st.dataframe(df_filtered.head())

st.download_button(
    "Download data terfilter (CSV)",
    df_filtered.to_csv(index=False),
    file_name="filtered_sales.csv"
)
