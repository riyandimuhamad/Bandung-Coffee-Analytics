import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Bandung Coffee Analytics", layout="wide")

st.title("☕ ICSAF Dashboard: Bandung Coffee Saturation")
st.markdown("---")

# ==========================================
# 2. LOAD DATA
# ==========================================
try:
    @st.cache_data
    def load_data():
        # GANTI NAMA FILE DI SINI JADI YANG BARU
        return pd.read_csv('bandung_final.csv') 
    
    df = load_data()
except:
    st.error("⚠️ File 'bandung_final.csv' belum dibuat! Jalankan fix_data.py dulu.")
    st.stop()

# ==========================================
# 3. SIDEBAR FILTER (DENGAN PROTEKSI)
# ==========================================
st.sidebar.header("🔍 Filter Data")

# Filter Tipe Bisnis
all_types = df['ownership_type'].unique()
filter_ownership = st.sidebar.multiselect(
    "Pilih Tipe Bisnis:",
    options=all_types,
    default=all_types # Default pilih semua
)

# Filter Wi-Fi
min_wifi = st.sidebar.slider("Minimum Kecepatan Wi-Fi (Mbps):", 0, 100, 10)

# LOGIKA PROTEKSI: Jika user hapus semua pilihan, anggap pilih semua (atau stop)
if not filter_ownership:
    st.warning("⚠️ Silakan pilih minimal satu Tipe Bisnis di sebelah kiri.")
    st.stop() # Berhenti di sini, jangan lanjut ke bawah biar gak error

# Terapkan Filter
filtered_df = df[
    (df['ownership_type'].isin(filter_ownership)) & 
    (df['wifi_speed'] >= min_wifi)
]

# LOGIKA PROTEKSI 2: Jika hasil filter kosong (misal Wi-Fi > 100Mbps padahal max cuma 90)
if filtered_df.empty:
    st.warning("❌ Tidak ada kafe yang sesuai dengan filter ini. Coba turunkan standar Wi-Fi nya bos!")
    st.stop()

# ==========================================
# 4. METRIK UTAMA (KPI)
# ==========================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Kafe Terpantau", f"{len(filtered_df)}")
col2.metric("Rata-rata Harga", f"Rp {int(filtered_df['avg_price'].mean()):,}")
col3.metric("Rata-rata Wi-Fi", f"{int(filtered_df['wifi_speed'].mean())} Mbps")
col4.metric("Avg Okupansi", f"{int(filtered_df['occupancy_rate'].mean())}%")

st.markdown("---")

# ==========================================
# 5. VISUALISASI PETA & CHART
# ==========================================
col_map, col_insight = st.columns([2, 1])

with col_map:
    st.subheader(f"📍 Peta Sebaran ({len(filtered_df)} Titik)")
    
    # Inisialisasi Peta (Pusat rata-rata dari data yang difilter)
    center_lat = filtered_df['latitude'].mean()
    center_lon = filtered_df['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    # Tambahkan Marker
    for index, row in filtered_df.iterrows():
        warna = 'gray'
        if 'Chain' in row['ownership_type']: warna = 'red'
        elif 'Specialty' in row['ownership_type']: warna = 'blue'
        elif 'Student' in row['ownership_type']: warna = 'green'
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=6,
            color=warna,
            fill=True,
            fill_color=warna,
            fill_opacity=0.7,
            popup=f"<b>{row['name']}</b><br>WiFi: {row['wifi_speed']} Mbps<br>Harga: {int(row['avg_price'])}"
        ).add_to(m)

    st_folium(m, use_container_width=True, height=500)

with col_insight:
    st.subheader("💡 Faktor Penentu")
    
    # Hitung Korelasi (Hanya jika variasi data cukup)
    if len(filtered_df) > 5:
        corr = filtered_df[['wifi_speed', 'avg_price', 'barista_s1_ratio', 'occupancy_rate']].corr()
        
        if 'occupancy_rate' in corr.columns:
            target_corr = corr['occupancy_rate'].drop('occupancy_rate').sort_values(ascending=False)
            
            # Plot
            fig, ax = plt.subplots(figsize=(4, 5))
            sns.barplot(x=target_corr.values, y=target_corr.index, palette='viridis', ax=ax)
            ax.set_xlabel("Korelasi ke Okupansi")
            ax.set_xlim(-1, 1) # Batas korelasi pasti -1 sampai 1
            st.pyplot(fig)
            
            top_factor = target_corr.index[0]
            st.success(f"Faktor Kunci: **{top_factor}**")
        else:
            st.info("Data kurang bervariasi untuk hitung korelasi.")
    else:
        st.warning("Data terlalu sedikit untuk analisis statistik.")
        
# ==========================================
# 6. RAW DATA
# ==========================================
with st.expander("Lihat Data Mentah"):
    st.dataframe(filtered_df)