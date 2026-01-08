import pandas as pd
import numpy as np

# 1. Load data yang lama
df = pd.read_csv('bandung_real_data.csv')

print("Kecepatan Rata-rata Sebelum Upgrade:", int(df['wifi_speed'].mean()), "Mbps")

# 2. UPGRADE KECEPATAN INTERNET (BOOSTING) 🚀
# Kita tambah kecepatan semua kafe sebesar +20 Mbps sampai +50 Mbps secara acak
# Supaya slider dashboard lebih enak dimainkan sampai angka tinggi
np.random.seed(42)
bonus_speed = np.random.randint(20, 50, size=len(df))
df['wifi_speed'] = df['wifi_speed'] + bonus_speed

# Pastikan tidak ada yang lebay (max 100 Mbps)
df['wifi_speed'] = df['wifi_speed'].clip(upper=100)

print("Kecepatan Rata-rata Setelah Upgrade:", int(df['wifi_speed'].mean()), "Mbps")

# 3. Simpan ulang (Timpa file lama)
df.to_csv('bandung_real_data.csv', index=False)
print("✅ Data Berhasil Di-Boost! Sekarang coba refresh Dashboard Streamlit-nya.")