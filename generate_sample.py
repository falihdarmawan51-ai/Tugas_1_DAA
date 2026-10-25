"""Membuat data SINTETIS (15.000 buku, 100 kategori) berstruktur mirip dataset Kaggle.
Hanya untuk uji coba bila dataset asli belum diunduh.
Dataset asli: https://www.kaggle.com/datasets/mihikaajayjadhav/books-dataset-15k-books-across-100-categories
"""
import csv, random

rng = random.Random(7)
kata = ["Rahasia", "Senja", "Algoritma", "Sejarah", "Dunia", "Cahaya", "Malam", "Samudra",
        "Petualangan", "Kota", "Hutan", "Mimpi", "Logika", "Data", "Bintang", "Perjalanan",
        "Warisan", "Bayangan", "Harmoni", "Pelajaran", "Kisah", "Legenda", "Rumah", "Waktu"]
nama = ["Ahmad", "Siti", "Budi", "Dewi", "Rizky", "Nadia", "Fajar", "Putri", "Andi", "Maya"]
marga = ["Pratama", "Lestari", "Hidayat", "Wijaya", "Saputra", "Nugroho", "Rahma", "Kusuma"]
kategori = [f"Kategori {i:03d}" for i in range(1, 101)]

with open("books_sample.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Title", "Author", "Category", "Rating", "Price"])
    for i in range(15000):
        judul = " ".join(rng.sample(kata, 3)) + f" Vol. {i + 1}"
        w.writerow([judul, f"{rng.choice(nama)} {rng.choice(marga)}",
                    rng.choice(kategori), round(rng.uniform(1, 5), 1),
                    round(rng.uniform(5, 80), 2)])
print("books_sample.csv dibuat")
