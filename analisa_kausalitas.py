import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ==========================================
# 1. GENERATE DATA INTERNAL (Biar Gak Error File)
# ==========================================
print("⚙️ Sedang meracik data simulasi di dalam memori...")
np.random.seed(42)
jumlah_data = 300

# Bikin Variabel Bebas (X)
wifi = np.random.randint(10, 100, jumlah_data)      # Kecepatan 10-100 Mbps
harga = np.random.randint(15000, 50000, jumlah_data) # Harga 15rb - 50rb
barista_s1 = np.random.uniform(0, 1, jumlah_data)    # Rasio Barista S1 (0% - 100%)
jarak_kampus = np.random.randint(100, 5000, jumlah_data) # Jarak 100m - 5km

# Bikin Variabel Target (Y) - Okupansi
# RUMUS KAUSALITAS RAHASIA:
# Kita set bahwa Wi-Fi punya pengaruh 50%, Harga 20%, Barista 20%, Jarak 10%
score = (wifi * 0.5) - (harga / 2000) + (barista_s1 * 30) - (jarak_kampus / 1000)
okupansi = np.interp(score + np.random.normal(0, 5, jumlah_data), [score.min(), score.max()], [10, 95])

# Bungkus jadi DataFrame
df = pd.DataFrame({
    'wifi_speed': wifi,
    'avg_price': harga,
    'barista_s1_ratio': barista_s1,
    'distance_to_campus': jarak_kampus,
    'occupancy_rate': okupansi
})

print(f"✅ Data siap! ({jumlah_data} sampel)")

# ==========================================
# 2. MACHINE LEARNING ENGINE (RANDOM FOREST)
# ==========================================
print("🧠 Sedang melatih 'Otak Buatan' (Random Forest)...")

# Tentukan X (Penyebab) dan Y (Akibat)
X = df[['wifi_speed', 'avg_price', 'barista_s1_ratio', 'distance_to_campus']]
y = df['occupancy_rate']

# Latih Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Hitung Seberapa Penting Tiap Faktor
importances = model.feature_importances_
feature_names = X.columns

# Buat Tabel Hasil
hasil_diagnosa = pd.DataFrame({'Faktor': feature_names, 'Pentingnya': importances})
hasil_diagnosa = hasil_diagnosa.sort_values(by='Pentingnya', ascending=False)

# ==========================================
# 3. VISUALISASI HASIL (OUTPUT AKHIR)
# ==========================================
print("📊 Menampilkan Grafik Diagnosa...")

plt.figure(figsize=(10, 6))
# Gunakan palet warna modern
colors = sns.color_palette("viridis", len(hasil_diagnosa))
bars = plt.barh(hasil_diagnosa['Faktor'], hasil_diagnosa['Pentingnya'], color=colors)

# Percantik Grafik
plt.xlabel('Tingkat Pengaruh (0.0 - 1.0)', fontsize=12)
plt.title('HASIL DIAGNOSA:\nApa Penyebab Utama Kafe Ramai?', fontsize=14, fontweight='bold')
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Tambahkan label angka di ujung batang
for index, value in enumerate(hasil_diagnosa['Pentingnya']):
    plt.text(value, index, f'{value:.2f}', va='center', fontweight='bold')

plt.gca().invert_yaxis() # Biar yang paling penting ada di atas
plt.tight_layout()
plt.show()

print("\n💡 INSIGHT BISNIS:")
top_factor = hasil_diagnosa.iloc[0]['Faktor']
print(f"Berdasarkan analisis data, faktor penentu utama adalah: {top_factor.upper()}")

# ... (kode sebelumnya biarkan saja) ...

# ==========================================
# 4. SIMPAN DATA UNTUK DASHBOARD (PENTING!)
# ==========================================
print("\n💾 Menyimpan data ke 'bandung_final.csv'...")
df.to_csv('bandung_final.csv', index=False) 

# Tambahkan kolom dummy untuk koordinat/nama biar peta Streamlit terbaca
# (Karena script analisa tadi cuma bikin angka, belum ada lokasi)
# Kita inject lokasi dummy:
df['latitude'] = np.random.uniform(-6.95, -6.85, len(df))
df['longitude'] = np.random.uniform(107.55, 107.75, len(df))

# Bikin nama kafe dummy
df['name'] = ["Kafe Data " + str(i) for i in range(len(df))]

# Bikin tipe bisnis dummy dari harga
conditions = [
    (df['avg_price'] > 40000),
    (df['wifi_speed'] > 70),
    (df['avg_price'] < 20000)
]
choices = ['Chain/Franchise', 'Local Specialty', 'Student Friendly']
df['ownership_type'] = np.select(conditions, choices, default='Local Standard')

# Simpan Final
df.to_csv('bandung_final.csv', index=False)
print("✅ DATA FINAL TERSIMPAN! Dashboard Streamlit sekarang pasti jalan.")