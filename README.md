# Tugas 1 - Sistem Pencarian Data Buku Perpustakaan Digital

**Nama:** Falih Darmawan  
**NIM:** 12550110298  
**Prodi:** Teknik Informatika, UIN Sultan Syarif Kasim Riau

Implementasi manual **Linear Search** (O(n)) dan **Binary Search** (O(log n)) untuk mencari buku berdasarkan judul,
lengkap dengan penghitungan jumlah perbandingan, pengukuran waktu eksekusi, tabel, dan grafik untuk n = 100, 1.000, 10.000.

## Dataset
`google_books_dataset.csv` (15.147 baris, 21 kolom). Kolom yang dipakai: `book_id`, `title`, `authors`,
`categories`, `average_rating`, `list_price`. Setelah 8 baris tanpa judul dibuang dan judul ganda dihapus,
tersisa 13.087 judul unik. Simpan file CSV di folder yang sama dengan `pencarian_buku.py`.

## Menjalankan
```
pip install -r requirements.txt
python pencarian_buku.py
python pencarian_buku.py --cari "Memorials"
python pencarian_buku.py --uji-saja --ulangan 1000
```
Keluaran: tabel di terminal, `hasil_pengujian.csv`, dan `grafik_pengujian.png`.

Tidak memakai `list.index()`, `in`, atau library pencarian untuk algoritma pencarian.
