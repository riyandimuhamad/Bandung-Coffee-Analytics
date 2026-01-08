import pandas as pd
import numpy as np

print("🔄 MEMULAI RESET DATA TOTAL (Factory Reset)...")

# 1. SETUP LOKASI BANDUNG (Gedung Sate)
lat_center = -6.9024
lon_center = 107.6188
jumlah_data = 200 # Kita buat 200 kafe langsung!

# 2. GENERATE KOORDINAT ACAK (Radius 5KM)
np.random.seed(42)
lats = lat_center + np.random.normal(0, 0.02, jumlah_data)
lons = lon_center + np.random.normal(0, 0.02, jumlah_data)

# 3. GENERATE NAMA KAFE (Biar terlihat real)
prefixes = ["Kopi", "Cafe", "Warung", "Kedai", "Studio", "Roastery"]
suffixes = ["Senja", "Bandung", "Jiwa", "Kenangan", "Hitam", "Luwak", "Pagi", "Malam", "Rindu", "Dago"]
names = [f"{np.random.choice(prefixes)} {np.random.choice(suffixes)} {i}" for i in range(jumlah_data)]

# 4. GENERATE TIPE BISNIS & ATRIBUT (LOGIKA LENGKAP)
types = ['Chain/Franchise', 'Local Specialty', 'Local Standard', 'Student Friendly']
weights = [0.25, 0.25, 0.30, 0.20] # Komposisi Beragam

ownerships = np.random.choice(types, size=jumlah_data, p=weights)

data = []
for i in range(jumlah_data):
    tipe = ownerships[i]
    
    # Atribut beda-beda tiap tipe
    if tipe == 'Chain/Franchise':
        wifi = int(np.random.normal(50, 10))
        price = int(np.random.normal(45000, 5000))
        s1 = 0.2
        color = 'red'
    elif tipe == 'Local Specialty':
        wifi = int(np.random.normal(85, 15)) # Ngebut
        price = int(np.random.normal(35000, 5000))
        s1 = 0.9
        color = 'blue'
    elif tipe == 'Student Friendly':
        wifi = int(np.random.normal(40, 10))
        price = int(np.random.normal(20000, 3000))
        s1 = 0.5
        color = 'green'
    else: # Local Standard
        wifi = int(np.random.normal(15, 5))
        price = int(np.random.normal(15000, 3000))
        s1 = 0.1
        color = 'gray'
    
    # Pastikan tidak minus
    wifi = max(5, wifi)
    
    # Hitung Okupansi
    score = (wifi * 0.6) - (price / 3000) + np.random.normal(0, 10)
    occupancy = int(np.interp(score, [-10, 60], [10, 95]))
    
    data.append([names[i], lats[i], lons[i], tipe, wifi, price, s1, occupancy])

# 5. BUAT DATAFRAME
df_new = pd.DataFrame(data, columns=['name', 'latitude', 'longitude', 'ownership_type', 'wifi_speed', 'avg_price', 'barista_s1_ratio', 'occupancy_rate'])

# 6. SIMPAN KE FILE YANG DIBACA DASHBOARD ('bandung_final.csv')
filename = 'bandung_final.csv'
df_new.to_csv(filename, index=False)

print(f"\n✅ SUKSES! {jumlah_data} Data baru telah dibuat di '{filename}'.")
print("Sekarang refresh Dashboard Streamlit Anda!")