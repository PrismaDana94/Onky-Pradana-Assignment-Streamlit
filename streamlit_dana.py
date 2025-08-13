import streamlit as st
import pandas as pd
import glob
import os

st.title(" Sales Dashboard 2019")

# Load semua CSV
all_files = glob.glob(os.path.join(".", "sales_data_*.csv"))
df_list = []

for file in all_files:
    df = pd.read_csv(file)
    df["month"] = os.path.basename(file).replace("sales_data_", "").replace("_2019.csv", "")
    df_list.append(df)

# Gabungkan semua data
df_all = pd.concat(df_list, ignore_index=True)

# Tampilkan data awal
st.subheader("Data Penjualan Gabungan")
st.dataframe(df_all.head())

# Pilihan filter bulan
months = sorted(df_all['month'].unique())
selected_month = st.selectbox("Pilih Bulan", months)
df_filtered = df_all[df_all['month'] == selected_month]

st.subheader(f"Data Penjualan - {selected_month}")
st.dataframe(df_filtered)

# Grafik 
if "Total" in df_filtered.columns:
    st.subheader(f"Total Penjualan - {selected_month}")
    st.bar_chart(df_filtered["Total"])

st.caption("Dashboard by Streamlit")
