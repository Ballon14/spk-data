# 📊 SPK-DATA REPOSITORY | The Engine of Decision Making 🧠

[![GitHub stars](https://img.shields.io/github/stars/Ballon14/spk-data.svg?style=social)](https://github.com/Ballon14/spk-data)
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/Ballon14/spk-data/blob/main/LICENSE)

Selamat datang di **`spk-data`**! Repositori ini adalah sumber tunggal dan terstruktur untuk semua data yang dibutuhkan dalam implementasi **Sistem Pendukung Keputusan (SPK)**.

Kami menyediakan data mentah yang rapi, siap digunakan untuk pemodelan, analisis, dan simulasi keputusan menggunakan berbagai metode SPK.

---

## ⚙️ Struktur Data (Data Architecture)

Repositori ini berfokus pada penyediaan file data (biasanya dalam format **`.csv`**, **`.json`**, atau **`.xlsx`**) yang merupakan inti dari setiap proses SPK. Struktur utama data terdiri dari tiga komponen kunci:

### 1. Kriteria & Bobot (Criteria & Weights)

Ini adalah daftar faktor atau atribut yang akan digunakan untuk mengevaluasi semua opsi. Setiap kriteria memiliki **bobot** (nilai kepentingan) yang menunjukkan seberapa signifikan kriteria tersebut dalam hasil akhir keputusan.

| File Contoh | Fungsi |
| :--- | :--- |
| `kriteria.csv` | **ID_Kriteria, Nama, Tipe (Benefit/Cost), Bobot** |

### 2. Alternatif (Alternatives)

Ini adalah daftar opsi atau pilihan yang sedang dievaluasi oleh sistem.

| File Contoh | Fungsi |
| :--- | :--- |
| `alternatif.csv` | **ID_Alternatif, Nama_Opsi** |

### 3. Nilai Evaluasi (Scoring Matrix)

Ini adalah *Decision Matrix* (Matriks Keputusan) yang berisi penilaian dari setiap **Alternatif** terhadap setiap **Kriteria**. Ini adalah data yang akan diproses oleh algoritma SPK.

| File Contoh | Fungsi |
| :--- | :--- |
| `evaluasi.csv` | **ID_Alternatif, ID_Kriteria, Nilai_Score** |

---

### 🖼️ Ilustrasi Struktur Data Matriks Keputusan

Berikut adalah visualisasi bagaimana data di repositori ini membentuk **Matriks Keputusan** yang siap diolah:

> [attachment_0](attachment)

---

## 🚀 Pemanfaatan Data (Usage & Integration)

Data di repositori ini telah dirancang agar mudah diintegrasikan dengan proyek-proyek yang mengimplementasikan metode SPK, seperti:

1.  **AHP** (Analytic Hierarchy Process)
2.  **SAW** (Simple Additive Weighting)
3.  **TOPSIS** (Technique for Order Preference by Similarity to Ideal Solution)
4.  **WPM** (Weighted Product Model)

### Alur Integrasi Umum

Anda dapat menggunakan data ini dengan alur sebagai berikut:

1.  **Kloning Repositori:** Dapatkan semua data terbaru.
    ```bash
    git clone [https://github.com/Ballon14/spk-data.git](https://github.com/Ballon14/spk-data.git)
    ```
2.  **Load Data:** Muat file CSV/JSON ke dalam *environment* pemrograman Anda (Python, R, dsb.).
3.  **Normalisasi & Pemodelan:** Proses data berdasarkan metode SPK yang Anda gunakan.
4.  **Hasil:** Dapatkan rekomendasi keputusan.

### 📈 Alur Proses Sistem Pendukung Keputusan

Data dari repositori ini berfungsi sebagai input kritis pada fase awal proses SPK:

> [attachment_1](attachment)

---

## 🤝 Kontribusi (Contribution)

Kami menyambut kontribusi data baru yang relevan, perbaikan skema, atau pembersihan data!

1.  *Fork* repositori ini.
2.  Buat *branch* fitur baru: `git checkout -b fitur/data-pembaharuan`
3.  Tambahkan atau ubah file data Anda.
4.  *Commit* perubahan Anda: `git commit -m 'feat: menambahkan dataset penilaian pemasok'`
5.  *Push* ke *branch* Anda, dan ajukan **Pull Request (PR)**.

## 📜 Lisensi

Repositori ini dirilis di bawah Lisensi **MIT**. Anda bebas menggunakan, memodifikasi, dan mendistribusikan data ini untuk tujuan komersial maupun non-komersial.

Lihat file [`LICENSE`](./LICENSE) untuk detail lengkap.
