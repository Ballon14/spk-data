# 🚀 Quick Start Guide - SPK SAW

## Instalasi Cepat (5 Menit)

### 1️⃣ Install Python (Jika Belum Ada)
```bash
# Check Python version
python3 --version

# Jika belum ada, install:
# Ubuntu/Debian:
sudo apt install python3 python3-pip

# macOS:
brew install python3
```

### 2️⃣ Install Dependencies
```bash
# Navigate ke folder project
cd /path/to/spk-1

# Install semua library
pip3 install -r requirements.txt

# Atau manual:
pip3 install flask pandas numpy
```

### 3️⃣ Jalankan Aplikasi
```bash
python3 main.py
```

### 4️⃣ Buka Browser
```
http://127.0.0.1:5000
```

## ✅ Checklist Sebelum Mulai

- [ ] Python 3.8+ terinstall
- [ ] File `Dataset_10_Desember.csv` ada di folder
- [ ] Dependencies terinstall (Flask, Pandas, NumPy)
- [ ] Port 5000 tidak digunakan aplikasi lain

## 🎯 Cara Menggunakan

1. **Input Bobot** - Masukkan nilai 0.00-1.00 untuk setiap kriteria
2. **Pastikan Total = 1.00** - Akan otomatis ditampilkan
3. **Klik "Hitung Ranking SAW"** - Submit form
4. **Lihat Hasil** - Tabel ranking akan muncul

## ⚠️ Troubleshooting

### Port Already in Use
```bash
# Stop aplikasi sebelumnya
pkill -f "python main.py"
```

### Module Not Found
```bash
# Install ulang dependencies
pip3 install flask pandas numpy
```

### Dataset Not Found
```bash
# Pastikan file ada
ls Dataset_10_Desember.csv
# Harus di folder yang sama dengan main.py
```

## 📊 Kriteria Default

| Kriteria | Bobot | Icon |
|----------|-------|------|
| Keamanan | 0.46 | 🛡️ |
| Interoperabilitas | 0.26 | 🔗 |
| Efisiensi | 0.15 | ⚡ |
| Dokumentasi | 0.09 | 📚 |
| Popularitas | 0.04 | ⭐ |

**Total:** 1.00 ✓

## 💡 Tips

- Sesuaikan bobot sesuai prioritas Anda
- Total bobot HARUS 1.00
- Top 3 packages ditandai dengan medali 🥇🥈🥉
- Hover pada row untuk highlight

## 📖 Dokumentasi Lengkap

Baca `README.md` untuk dokumentasi detail!

---

**Happy Coding! 🎉**
