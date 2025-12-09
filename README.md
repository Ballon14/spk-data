# 🎯 SPK SAW - Sistem Pendukung Keputusan Package NodeJS

Aplikasi web untuk analisis dan ranking package NodeJS menggunakan metode **Simple Additive Weighting (SAW)** - Decision Support System yang modern dan interaktif.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![Tailwind CSS](https://img.shields.io/badge/tailwindcss-3.0-06B6D4.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📋 Daftar Isi

- [Tentang Project](#-tentang-project)
- [Fitur Utama](#-fitur-utama)
- [Kriteria Penilaian](#-kriteria-penilaian)
- [Requirements](#-requirements)
- [Instalasi](#-instalasi)
- [Cara Menjalankan](#-cara-menjalankan)
- [Penggunaan](#-penggunaan)
- [Struktur Project](#-struktur-project)
- [Teknologi](#-teknologi)
- [Troubleshooting](#-troubleshooting)

## 🎓 Tentang Project

Sistem Pendukung Keputusan (SPK) ini dirancang untuk membantu developer dalam memilih package NodeJS terbaik berdasarkan multiple criteria. Aplikasi menggunakan metode **Simple Additive Weighting (SAW)** untuk melakukan normalisasi dan perhitungan score dari setiap package.

### Metode SAW

SAW adalah metode penjumlahan terbobot yang menggunakan rating kinerja pada setiap alternatif di semua kriteria. Metode ini membutuhkan proses normalisasi matriks keputusan (X) ke suatu skala yang dapat diperbandingkan dengan semua rating alternatif yang ada.

**Formula:**

```
SAW Score = Σ(Wi × Ri)
```

Dimana:
- `Wi` = Bobot kriteria ke-i
- `Ri` = Rating kinerja ternormalisasi

## ✨ Fitur Utama

### 🎨 **UI Modern dengan Tailwind CSS**
- ✅ Gradient background yang eye-catching
- ✅ Glass morphism effects
- ✅ Smooth animations dan transitions
- ✅ Fully responsive (Mobile, Tablet, Desktop)

### ⚡ **Interactive Features**
- 📊 Real-time total bobot calculator
- 🔄 Automatic validation
- ⏳ Loading states dengan spinner
- 🎯 Visual feedback untuk user input

### 🏆 **Premium Table Results**
- 🥇 Medali Gold untuk Rank 1
- 🥈 Medali Silver untuk Rank 2
- 🥉 Medali Bronze untuk Rank 3
- 🌈 Color-coded rows untuk readability
- 📱 Horizontal scroll untuk mobile

### 📈 **Data Analysis**
- 📦 139+ packages NodeJS ter-update
- 🔢 5 kriteria penilaian komprehensif
- ⚖️ Customizable weights
- 📊 Normalized scoring system

## 📊 Kriteria Penilaian

Sistem mengevaluasi package berdasarkan 5 kriteria utama:

| No | Kriteria | Sumber Data | Bobot Default | Tipe | Keterangan |
|----|----------|-------------|---------------|------|------------|
| 1 | 🛡️ **Keamanan** | `days_since_publish` | 0.46 (46%) | Cost | Semakin baru (kecil) semakin aman |
| 2 | 🔗 **Interoperabilitas** | `interoperability_score` | 0.26 (26%) | Benefit | Semakin tinggi semakin baik |
| 3 | ⚡ **Efisiensi** | `package_size_kb` | 0.15 (15%) | Cost | Semakin kecil semakin efisien |
| 4 | 📚 **Dokumentasi** | `readme_length` | 0.09 (9%) | Benefit | Semakin lengkap semakin baik |
| 5 | ⭐ **Popularitas** | `github_stars` | 0.04 (4%) | Benefit | Semakin banyak semakin populer |

**Total Bobot:** 0.46 + 0.26 + 0.15 + 0.09 + 0.04 = **1.00** ✓

### Normalisasi Data

#### Kriteria Benefit (Higher is Better)
Untuk `interoperability_score`, `readme_length`, `github_stars`:
```
normalized_value = (value - min) / (max - min)
```

#### Kriteria Cost (Lower is Better)
Untuk `days_since_publish`, `package_size_kb`:
```
normalized_value = (max - value) / (max - min)
```

## 🔧 Requirements

### Software Requirements

- **Python**: 3.8 atau lebih tinggi
- **pip**: Package installer untuk Python
- **Web Browser**: Chrome, Firefox, Safari, atau Edge (versi terbaru)

### Python Libraries

```
Flask==3.0.0
pandas==2.1.0
numpy==1.24.0
```

## 📥 Instalasi

### 1. Clone atau Download Project

```bash
# Clone repository (jika menggunakan git)
git clone <repository-url>
cd spk-1

# Atau extract file ZIP ke folder
unzip spk-1.zip
cd spk-1
```

### 2. Install Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**macOS:**
```bash
brew install python3
```

**Windows:**
- Download installer dari [python.org](https://www.python.org/downloads/)
- Jalankan installer dan centang "Add Python to PATH"

### 3. Verifikasi Instalasi Python

```bash
python3 --version
# Output: Python 3.8.x atau lebih tinggi

pip3 --version
# Output: pip xx.x.x
```

### 4. Install Dependencies

```bash
# Install semua library yang dibutuhkan
pip3 install flask pandas numpy

# Atau gunakan requirements.txt (jika tersedia)
pip3 install -r requirements.txt
```

### 5. Verifikasi File Dataset

Pastikan file dataset ada di folder project:
```bash
ls Dataset_10_Desember.csv
```

File harus berisi data packages dengan kolom:
- `name`
- `days_since_publish`
- `interoperability_score`
- `package_size_kb`
- `readme_length`
- `github_stars`
- dan kolom lainnya

## 🚀 Cara Menjalankan

### Metode 1: Menjalankan Langsung

```bash
# Navigate ke folder project
cd /path/to/spk-1

# Jalankan aplikasi
python3 main.py
```

### Metode 2: Menjalankan dengan Virtual Environment (Recommended)

```bash
# 1. Buat virtual environment
python3 -m venv venv

# 2. Aktifkan virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install flask pandas numpy

# 4. Jalankan aplikasi
python main.py

# 5. Untuk deactivate (setelah selesai)
deactivate
```

### Output yang Diharapkan

```
* Serving Flask app 'main'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
```

### Akses Aplikasi

1. Buka web browser
2. Navigasi ke: **http://127.0.0.1:5000** atau **http://localhost:5000**
3. Aplikasi siap digunakan! 🎉

## 📖 Penggunaan

### Langkah 1: Input Bobot Kriteria

1. Buka aplikasi di browser
2. Lihat section **"Input Bobot Kriteria"**
3. Masukkan bobot untuk setiap kriteria (0.00 - 1.00)
4. Pastikan **Total Bobot = 1.00** (akan terlihat di indicator)

**Contoh:**
- Keamanan: 0.46
- Interoperabilitas: 0.26
- Efisiensi: 0.15
- Dokumentasi: 0.09
- Popularitas: 0.04

### Langkah 2: Hitung Ranking

1. Klik tombol **"Hitung Ranking SAW"**
2. Tunggu loading animation
3. Hasil akan muncul di bawah form

### Langkah 3: Analisis Hasil

Tabel hasil menampilkan:
- **Rank**: Peringkat package (1 = terbaik)
- **Package Name**: Nama package NodeJS
- **Score SAW**: Skor akhir (0.0000 - 1.0000)
- **Kriteria Values**: Nilai asli untuk setiap kriteria

**Top 3 Packages:**
- 🥇 **Rank 1**: Gold badge + highlight
- 🥈 **Rank 2**: Silver badge + highlight
- 🥉 **Rank 3**: Bronze badge + highlight

### Tips Penggunaan

1. **Customize Weights**: Sesuaikan bobot berdasarkan prioritas Anda
2. **Compare Top Packages**: Fokus pada top 10 untuk keputusan terbaik
3. **Check Criteria**: Lihat nilai individual untuk insight mendalam
4. **Real-time Feedback**: Monitor total bobot saat input

## 📁 Struktur Project

```
spk-1/
│
├── main.py                          # Aplikasi Flask utama
├── Dataset_10_Desember.csv          # Dataset packages NodeJS (TSV format)
├── README.md                        # Dokumentasi lengkap (file ini)
│
└── (optional files)
    ├── requirements.txt             # List dependencies Python
    └── .gitignore                   # Git ignore file
```

### File Penting

#### `main.py`
File utama aplikasi Flask yang berisi:
- **Backend Logic**: Normalisasi data, perhitungan SAW
- **API Endpoints**: `/` (home), `/rank` (POST)
- **Frontend Templates**: HTML dengan Tailwind CSS

#### `Dataset_10_Desember.csv`
Dataset packages NodeJS dengan delimiter TAB (`\t`) berisi:
- 139 packages NodeJS
- Data ter-update (Desember 2025)
- Multiple metrics per package

## 🛠️ Teknologi

### Backend
- **Flask 3.0+**: Lightweight Python web framework
- **Pandas**: Data manipulation dan analysis
- **NumPy**: Numerical computing untuk perhitungan SAW

### Frontend
- **Tailwind CSS 3.0**: Utility-first CSS framework (via CDN)
- **Vanilla JavaScript**: Interactivity tanpa dependencies
- **Google Fonts (Inter)**: Modern typography
- **Custom CSS**: Animations dan special effects

### Data Format
- **CSV/TSV**: Tab-separated values dataset
- **JSON**: API response format

## 🐛 Troubleshooting

### Error: "Address already in use"

**Problem**: Port 5000 sudah digunakan aplikasi lain

**Solusi 1** - Stop aplikasi sebelumnya:
```bash
# Linux/macOS
pkill -f "python main.py"

# Windows
# Tutup process Python dari Task Manager
```

**Solusi 2** - Gunakan port berbeda:
```python
# Edit main.py baris terakhir
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Ganti 5000 ke 5001
```

### Error: "ModuleNotFoundError: No module named 'flask'"

**Problem**: Library belum terinstall

**Solusi**:
```bash
pip3 install flask pandas numpy
```

### Error: "FileNotFoundError: Dataset_10_Desember.csv"

**Problem**: File dataset tidak ditemukan

**Solusi**:
1. Pastikan file `Dataset_10_Desember.csv` ada di folder yang sama dengan `main.py`
2. Cek nama file (case-sensitive)
3. Verifikasi current working directory

### Error: "ParserError: Error tokenizing data"

**Problem**: Format CSV tidak sesuai

**Solusi**:
1. Pastikan delimiter adalah TAB (`\t`), bukan comma
2. Buka CSV dengan text editor untuk verifikasi format
3. Pastikan tidak ada data corrupt

### Browser Tidak Terbuka

**Solusi**:
1. Pastikan ada output `Running on http://127.0.0.1:5000`
2. Manual buka browser dan ketik URL
3. Try http://localhost:5000 jika 127.0.0.1 tidak work
4. Clear browser cache jika tampilan tidak update

### Tabel Tidak Muncul

**Solusi**:
1. Buka Developer Console (F12)
2. Check error di Console tab
3. Verify API response di Network tab
4. Pastikan bobot total = 1.00

### Tampilan Berantakan

**Solusi**:
1. Pastikan koneksi internet aktif (Tailwind via CDN)
2. Clear browser cache (Ctrl + Shift + Delete)
3. Try browser berbeda
4. Disable browser extensions yang mungkin interfere

## 📊 Contoh Hasil

### Sample Top 5 Packages:

| Rank | Package Name | Score SAW | Keamanan | Interop | Efisiensi |
|------|--------------|-----------|----------|---------|-----------|
| 🥇 1 | @testing-library/react | 0.8452 | 251 | 100 | 6.59 |
| 🥈 2 | axios | 0.7995 | 34 | 90 | 36.81 |
| 🥉 3 | bee-queue | 0.7647 | 1 | 100 | 0.00 |
| 4 | express-session | 0.7640 | 145 | 100 | 21.69 |
| 5 | enquirer | 0.7587 | 865 | 100 | 74.01 |

## 📝 Catatan Penting

1. **Development Mode**: Aplikasi berjalan dalam debug mode, tidak untuk production
2. **Data Accuracy**: Dataset ter-update per Desember 2025
3. **Bobot Custom**: User dapat customize bobot sesuai kebutuhan
4. **Browser Compatibility**: Tested di Chrome, Firefox, Safari, Edge

## 🔒 Keamanan

- ⚠️ Ini adalah development server, JANGAN deploy ke production tanpa proper WSGI server
- 🔐 Untuk production, gunakan: Gunicorn, uWSGI, atau similar
- 🌐 Untuk public access, pertimbangkan authentication dan HTTPS

## 📄 Lisensi

Project ini dibuat untuk tujuan edukasi dan analisis data.

## 👨‍💻 Developer

Developed with ❤️ untuk analisis package NodeJS

---

## 🚀 Quick Start Cheat Sheet

```bash
# 1. Install dependencies
pip3 install flask pandas numpy

# 2. Run application
python3 main.py

# 3. Open browser
# Navigate to: http://127.0.0.1:5000

# 4. Input weights (total = 1.00)
# 5. Click "Hitung Ranking SAW"
# 6. Analyze results!
```

---

**Selamat menggunakan SPK SAW! 🎉**

Jika ada pertanyaan atau issues, silakan buat issue di repository atau hubungi developer.
