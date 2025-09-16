🛒 E-Commerce Sales Dashboard 2019

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen)](https://onky-pradana-assignment-app-sales2019.streamlit.app/)

📌 Project Overview

Proyek ini bertujuan untuk menganalisis data penjualan e-commerce sepanjang tahun 2019 dan membangun dashboard interaktif menggunakan Streamlit.
Dashboard ini memberikan insight terkait performa penjualan, tren bulanan, kontribusi kategori produk, dan analisis kota serta periode rush hour.Dashboard ini menganalisis seluruh transaksi e-commerce selama tahun 2019. Tujuannya untuk membantu tim bisnis memahami pola penjualan (time, product, city), menemukan produk & lokasi prioritas, serta mengidentifikasi jam belanja paling ramai untuk optimasi operasional dan pemasaran.

Statistik ringkas (dari dashboard):
- Total Sales (GMV): $34,492,035.97
- Total Orders: 178,437
- Unique Products: 19
- Average Order Value (AOV): ≈ $193.30

Tujuan utama:
1. Memahami pola penjualan sepanjang tahun 2019.
2. Mengidentifikasi bulan dan produk dengan penjualan tertinggi.
3. Menemukan jam "rush hour" untuk optimasi promosi & operasi (fulfillment & customer support).
4. Menyediakan visualisasi yang membantu pengambilan keputusan bisnis.
5. Sumber Data: Transaksi e-commerce sepanjang tahun 2019 (file CSV per bulan).

📊 Dataset
Jumlah file: 12 file, masing-masing mewakili satu bulan (sales_data_january_2019.csv s.d. sales_data_december_2019.csv).
Kolom utama:
1. order_id → ID unik untuk setiap transaksi
2. product_name → Nama produk yang terjual
3. city → Kota tempat transaksi terjadi
4. quantity → Jumlah produk terjual
5. price → Harga satuan produk
6. order_date → Tanggal dan waktu transaksi

📂 Contoh struktur folder:
- ├── sales_data_january_2019.csv
- ├── sales_data_february_2019.csv
- ├── ...
- ├── sales_data_december_2019.csv
- ├── streamlit_dana.py
- └── requirements.txt

🚀 Metodologi
1. Data Preparation
   - Menggabungkan 12 file CSV menjadi satu dataset.
   - Membersihkan data: menghapus duplikat & menangani missing values.
2. Exploratory Data Analysis (EDA)
   - Tren penjualan harian dan bulanan.
   - Analisis produk paling laris & kontribusi per kategori.
   - Identifikasi kota dengan penjualan tertinggi.
3. Dashboard Building dengan Streamlit
   - Membuat visualisasi interaktif (bar chart, line chart, pie chart).
   - Fitur filter berdasarkan bulan, kota, dan kategori produk.
4. Deployment
   Deploy menggunakan Streamlit Cloud agar bisa diakses secara publik.

📈 Dashboard Features
- ✅ Monthly Sales Trend – Visualisasi tren penjualan sepanjang 2019
- ✅ Top Products – Produk dengan penjualan tertinggi
- ✅ Analisis Kota – Kota dengan performa terbaik
- ✅ Rush Hour Analysis – Jam transaksi tersibuk
- ✅ Data Filtering – Filter dinamis berdasarkan bulan atau kota
- ✅ Insights & Recommendations – Kesimpulan dan rekomendasi bisnis
- ✅ Data Preview - Tabel transaksi agregat/raw untuk verifikasi
  
🔗 **Live App** → [Streamlit Dashboard](https://onky-pradana-assignment-app-sales2019.streamlit.app/)→ E-Commerce Sales Dashboard

🛠 Tech Stack
- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Streamlit – untuk membangun dashboard interaktif
- GitHub – version control & deployment
- Excel/CSV – sumber data penjualan

📌 Key Insights

1. Total GMV: $34,492,035.97 — ukuran bisnis cukup besar, fokus pada produk high-ticket.
2. Top product
   - Macbook Pro adalah kontributor GMV terbesar (≈ $8M, ~23% dari total GMV).
   - iPhone di posisi kedua (~$4.79M, ≈ 13.9%).
   - Kombinasi top-2 menyumbang ≈ 37% dari total GMV → ketergantungan signifikan pada beberapa SKU high-ticket.
3. Top cities
   - San Francisco (CA) paling tinggi (≈ $8.1M, ~23% dari GMV).
   - Los Angeles (CA) dan New York City (NY) juga kontributor besar (masing-masing ≈ 16% dan 14% estimasi).
     → Fokus pemasaran & inventory untuk region CA & NY memberi efek besar pada revenue.
4. Trend bulanan
   - Penjualan relatif naik dari Jan → Apr (Apr ≈ 3.3M).
   - Ada penurunan di paruh kedua (Jun–Sep), lalu lonjakan kuat di Oct (~3.7M) dan puncak di Dec (~4.5M).
     → Desember sebagai puncak (holiday peak), Oktober juga momentum penting (mungkin promo).
5. Rush hour (jam transaksi)
   - Dua periode puncak terlihat: 11:00–13:00 (siang) dan 19:00–21:00 (malam), dengan puncak tertinggi sekitar 19:00–20:00.
     → Ini relevan untuk penjadwalan kampanye iklan & staffing operational (CS/fulfillment).
6. Customer / Product concentration risk
   Karena persentase GMV tinggi tersentralisasi pada beberapa produk dan kota, risiko stok habis atau isu supply chain pada SKU tersebut dapat berdampak besar.
   
✅ Rekomendasi Actionable (singkat)
1. Inventory priority: pastikan stok Macbook Pro & iPhone mencukupi, khususnya untuk bulan Oct–Dec.
2. Promosi terjadwal: jalankan promosi/push ads saat 11:00–13:00 dan 19:00–21:00 untuk maksimal exposure.
3. Geo-targeting: alokasikan budget marketing lebih ke San Francisco & Los Angeles (karena kontribusi terbesar).
4. Diversifikasi produk: pertimbangkan strategi upsell/penawaran pada SKU mid-range agar ketergantungan top-2 berkurang.
5. Investigasi penurunan: cek penyebab penurunan pada Jun–Sep (kompetitor, stok, seasonality).
6. Laporan KPI bulanan: buat monitoring AOV, conversion rate, stockouts untuk SKU top 10.

📂 Project Structure
├── .devcontainer/             # Setup dev environment
├── README.md                   # Dokumentasi project
├── requirements.txt            # Library dependencies
├── sales_data_*.csv            # File data penjualan per bulan
└── streamlit_dana.py           # Script utama untuk dashboard


