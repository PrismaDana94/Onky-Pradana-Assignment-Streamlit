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
    if not files:
        return pd.DataFrame()
    all_frames = []
    for file in files:
        try:
            df = pd.read_csv(file)
        except Exception:
            df = pd.read_csv(file, encoding='latin1')
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce', infer_datetime_format=True)
        else:
            df['Order Date'] = pd.NaT
        df['Quantity Ordered'] = pd.to_numeric(df.get('Quantity Ordered'), errors='coerce')
        df['Price Each'] = pd.to_numeric(df.get('Price Each'), errors='coerce')
        df['Sales'] = df['Quantity Ordered'] * df['Price Each']
        all_frames.append(df)
    # gabung semua frame
    df = pd.concat(all_frames, ignore_index=True) if all_frames else pd.DataFrame()
    # --- Bersihkan kolom Product ---
    prod_cols = [c for c in df.columns if c.lower() == 'product']
    if prod_cols:
        # samakan nama kolom jadi 'Product'
        if prod_cols[0] != 'Product':
            df.rename(columns={prod_cols[0]: 'Product'}, inplace=True)
            
        # ubah ke string, strip spasi
        df['Product'] = df['Product'].astype(str).str.strip()
        
        # ubah placeholder jadi NA                                                                            
        placeholders = ['nan', 'none', 'n/a', 'na', '']
        mask_placeholder = df['Product'].str.lower().isin(placeholders)
        df.loc[mask_placeholder, 'Product'] = pd.NA
        
        # buang baris yang kebaca 'product' (header ganda)
        # df = df[~df['Product'].astype(str).str.lower().eq('product')]
        
        # buang baris tanpa product
        df = df.dropna(subset=['Product']).reset_index(drop=True)
        
    # kembalikan df yang sudah dibersihkan
    return df
                                                                                                                                                                                                                         
# ========================
# Load data
# ========================
df = load_data()

# === DEBUG START ===
# st.write("DEBUG RAW:", df.shape)
# st.write("DEBUG RAW Unique Products:", df['Product'].nunique())
# === DEBUG END ===

if df.empty:
    st.error("Data tidak ditemukan atau file 'sales_data_*.csv' kosong. Pastikan file tersedia di folder kerja.")
    st.stop()

# ========================
# Ekstrak kolom waktu & bulan
# ========================
df['Month'] = df['Order Date'].dt.month
df['Month Name'] = df['Order Date'].dt.strftime('%B')

# ========================
# Fungsi aman untuk ekstrak City
# ========================
def extract_city_state(address):
    """Ekstrak 'City (ST)' dari Purchase Address secara aman."""
    if pd.isna(address) or str(address).strip() == "":
        return None
    try:
        parts = [p.strip() for p in str(address).split(',')]
        if len(parts) >= 2:
            city = parts[1]
            state = ""
            if len(parts) >= 3:
                state_token = parts[2].split()
                if state_token:
                    state = state_token[0].upper()
            return f"{city} ({state})" if state else city
        return address
    except Exception:
        return None

if 'Purchase Address' in df.columns:
    df['City'] = df['Purchase Address'].apply(extract_city_state)
elif 'City' in df.columns and 'State' in df.columns:
    df['City'] = df['City'].astype(str).str.strip() + " (" + df['State'].astype(str).str.strip() + ")"
else:
    df['City'] = None

# ========================
# Urutan nama bulan
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

present_months = [m for m in month_order if m in list(df['Month Name'].dropna().unique())]
if not present_months:
    present_months = sorted(df['Month'].dropna().unique())

selected_month = st.sidebar.multiselect("Pilih Bulan", present_months, default=present_months)

cities_all = sorted([c for c in df['City'].dropna().unique()])
selected_city = st.sidebar.multiselect("Pilih Kota", cities_all, default=cities_all)

products_all = sorted(df['Product'].dropna().unique()) if 'Product' in df.columns else []
selected_product = st.sidebar.multiselect("Pilih Produk", products_all, default=products_all)

# ========================
# Terapkan filter
# ========================
mask = df['Month Name'].isin(selected_month) if selected_month else True
mask &= df['City'].isin(selected_city)
if products_all:
    mask &= df['Product'].isin(selected_product)

df_filtered = df[mask].copy()

raw_p  = df['Product'].astype(str).str.strip().str.lower().unique()
filt_p = df_filtered['Product'].astype(str).str.strip().str.lower().unique()
missing = sorted(set(raw_p) - set(filt_p))
st.write("Produk yang terbuang oleh filter:",missing)

# === DEBUG START ===
# st.write("DEBUG FILTERED:", df_filtered.shape)
# st.write("DEBUG FILTERED Unique Products:", df_filtered['Product'].nunique())
# === DEBUG END ===

if df_filtered.empty:
    st.warning("Tidak ada data setelah diterapkan filter. Coba ubah pilihan filter.")
    st.stop()

# ========================
# Warna konsisten untuk kota
# ========================
city_colors = px.colors.qualitative.Plotly
unique_cities = sorted(df['City'].dropna().unique())
city_color_map = {city: city_colors[i % len(city_colors)] for i, city in enumerate(unique_cities)}

# ========================
# Profil & Judul
# ========================
st.title("Sales Analysis 2019")
st.markdown("""
Nama: Onky Pradana  
Project: Analisis Penjualan Tahun 2019  
Kontak: freddycull27@gmail.com
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
# Grafik 6: Stacked Bar Sales per Bulan per Kota
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

# Semua produk tanpa filter
all_products = df['Product'].dropna().unique()

# Produk setelah filter
filtered_products = df_filtered['Product'].dropna().unique()

# Produk yang hilang
missing_products = set(all_products) - set(filtered_products)

print("Total produk tanpa filter:", len(all_products))
print("Total produk setelah filter:", len(filtered_products))
print("Produk yang hilang:", missing_products)

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
