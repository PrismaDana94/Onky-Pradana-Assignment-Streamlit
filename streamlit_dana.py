# streamlit_dana.py

import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 1. PROFIL SINGKAT
# =========================
st.set_page_config(page_title="Dana's Interactive Portfolio", layout="wide")

st.title(" Dana's Interactive Data Portfolio")
st.markdown("""
**Nama:** Dana  
**Bio:** Data enthusiast dengan latar belakang akuntansi, fokus pada analisis data, visualisasi, dan machine learning.  
**Kontak:** [Email](mailto:emailkamu@example.com) | [LinkedIn](www.linkedin.com/in/prisma-dana) | [GitHub](https://github.com/PrismaDana94)  
""")

# =========================
# 2. JUDUL / TOPIK PROYEK
# =========================
st.header(" Analisis Penjualan & Perilaku Pelanggan")
st.markdown("""
Proyek ini menganalisis data penjualan untuk mengidentifikasi tren, performa produk, dan perbedaan penjualan antar kota.
Visualisasi interaktif membantu mempermudah eksplorasi data.
""")

# =========================
# 3. LOAD DATA
# =========================
@st.cache_data
def load_data():
    # Ganti dengan path CSV kamu
    df = pd.read_csv("sales_data.csv")
    # Ekstrak kota
    df['City'] = df['Purchase Address'].apply(lambda x: x.split(',')[1].strip() + " (" + x.split(',')[2].split(' ')[1] + ")")
    # Konversi tanggal
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Month'] = df['Order Date'].dt.month
    return df

df_clean = load_data()

# =========================
# 4. FILTER INTERAKTIF
# =========================
st.sidebar.header("Filter Data")
selected_month = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=sorted(df_clean['Month'].unique()),
    default=sorted(df_clean['Month'].unique())
)

selected_city = st.sidebar.multiselect(
    "Pilih Kota:",
    options=sorted(df_clean['City'].unique()),
    default=sorted(df_clean['City'].unique())
)

filtered_df = df_clean[
    (df_clean['Month'].isin(selected_month)) &
    (df_clean['City'].isin(selected_city))
]

# =========================
# 5. VISUALISASI & INSIGHT
# =========================

# Total Penjualan per Bulan
st.subheader("📈 Total Penjualan per Bulan")
sales_per_month = filtered_df.groupby('Month')['Sales'].sum().reset_index()
fig_month = px.line(sales_per_month, x='Month', y='Sales', markers=True)
st.plotly_chart(fig_month, use_container_width=True)
st.markdown("**Insight:** Terlihat fluktuasi penjualan sepanjang tahun, dengan puncak pada bulan tertentu yang bisa dikaitkan dengan musim liburan atau event promo.")

# Penjualan per Kota
st.subheader("🌆 Penjualan per Kota")
sales_per_city = filtered_df.groupby('City')['Sales'].sum().reset_index()
fig_city = px.bar(sales_per_city, x='City', y='Sales', color='Sales', title="Penjualan Berdasarkan Kota")
st.plotly_chart(fig_city, use_container_width=True)
st.markdown("**Insight:** Kota dengan populasi dan pusat ekonomi besar seperti San Francisco dan Los Angeles memiliki penjualan tertinggi.")

# Produk Terlaris
st.subheader("🏆 Produk Terlaris")
top_products = filtered_df.groupby('Product')['Quantity Ordered'].sum().reset_index().sort_values(by='Quantity Ordered', ascending=False).head(10)
fig_products = px.bar(top_products, x='Product', y='Quantity Ordered', color='Quantity Ordered')
st.plotly_chart(fig_products, use_container_width=True)
st.markdown("**Insight:** Produk dengan harga terjangkau dan kebutuhan tinggi seperti kabel charger menempati posisi teratas dalam jumlah penjualan.")

# =========================
# 6. CATATAN PENUTUP
# =========================
st.markdown("---")
st.markdown("""
**Tools yang digunakan:**  
- Python (Pandas, Plotly, Streamlit)  
- GitHub untuk version control  
- Streamlit Community Cloud untuk deployment  

Aplikasi ini dirancang untuk eksplorasi data penjualan secara interaktif, membantu dalam pengambilan keputusan bisnis berbasis data.
""")
