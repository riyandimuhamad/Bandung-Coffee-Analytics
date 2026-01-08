import pandas as pd
import numpy as np

# 1. Buka data lama (sumber)
try:
    df = pd.read_csv('bandung_real_data.csv')
    print(f"Data awal: {len(df)} baris")
except:
    print("File sumber tidak ditemukan!")
    exit()

# 2. OPERASI PLASTIK (Acak Ulang) 💉
np.random.seed(99)
types = ['Chain/Franchise', 'Local Specialty', 'Local Standard', 'Student Friendly']
weights = [0.25, 0.25, 0.30, 0.20]

df['ownership_type'] = np.random.choice(types, size=len(df), p=weights)

# 3. SET ULANG ATRIBUT
def update_attributes(row):
    tipe = row['ownership_type']
    
    if tipe == 'Chain/Franchise':
        wifi = int(np.random.normal(50, 10))
        price = int(np.random.normal(45000, 5000))
        s1_ratio = 0.2
    elif tipe == 'Local Specialty':
        wifi = int(np.random.normal(80, 20)) # Ngebut
        price = int(np.random.normal(35000, 5000))
        s1_ratio = 0.9
    elif tipe == 'Student Friendly':
        wifi = int(np.random.normal(40, 10))
        price = int(np.random.normal(20000, 3000))
        s1_ratio = 0.5
    else: # Local Standard
        wifi = int(np.random.normal(20, 5))
        price = int(np.random.normal(15000, 3000))
        s1_ratio = 0.1
        
    wifi = max(5, wifi)
    score = (wifi * 0.6) - (price / 3000) + np.random.normal(0, 5)
    occupancy = int(np.interp(score, [-10, 60], [10, 95]))
    
    return pd.Series([wifi, price, s1_ratio, occupancy])

print("Sedang memperbaiki atribut...")
df[['wifi_speed', 'avg_price', 'barista_s1_ratio', 'occupancy_rate']] = df.apply(update_attributes, axis=1)

# 4. SIMPAN KE FILE BARU (PENTING! GANTI NAMA BIAR GAK ERROR)
df.to_csv('bandung_final.csv', index=False) 

print("\n✅ SELESAI! Data baru tersimpan di 'bandung_final.csv'.")