# Tugas 1 - Sistem Pencarian Data Buku Perpustakaan Digital

**Nama:** Falih Darmawan  
**NIM:** 12550110298  
**Prodi:** Teknik Informatika, UIN Sultan Syarif Kasim Riau

Implementasi manual **Linear Search** (O(n)) dan **Binary Search** (O(log n)) untuk mencari buku berdasarkan judul,
lengkap dengan penghitungan jumlah perbandingan, pengukuran waktu eksekusi, tabel, dan grafik untuk n = 100, 1.000, 10.000.

## Dataset
Unduh dari Kaggle: https://www.kaggle.com/datasets/mihikaajayjadhav/books-dataset-15k-books-across-100-categories
lalu simpan CSV-nya (mis. `books.csv`) di folder ini. Program mendeteksi kolom judul, penulis, kategori, rating, dan harga secara otomatis.

Jika dataset belum diunduh, `python generate_sample.py` membuat data sintetis `books_sample.csv` (hanya untuk uji coba).

## Menjalankan
```
python pencarian_buku.py --csv books.csv
python pencarian_buku.py --csv books.csv --cari "Judul Buku"
python pencarian_buku.py --csv books.csv --uji-saja --ulangan 1000
```
Keluaran: tabel di terminal, `hasil_pengujian.csv`, dan `grafik_pengujian.png`.

Tidak memakai `list.index()`, `in`, atau library pencarian untuk algoritma pencarian.
