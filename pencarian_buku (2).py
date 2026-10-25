"""Tugas DAA: Sistem Pencarian Buku dengan Linear Search dan Binary Search.

Jalankan: python pencarian_buku_diperbaiki.py
Pilih dataset 2 untuk memakai google_books_dataset.xlsx di folder Downloads.
"""
from pathlib import Path
from io import StringIO
import csv
import time
import pandas as pd

FOLDER_PROGRAM = Path(__file__).resolve().parent
FILE_SAMPEL = FOLDER_PROGRAM / "sample_buku.csv"
FILE_CSV = Path.home() / "Downloads" / "google_books_dataset.csv"
FILE_EXCEL = Path.home() / "Downloads" / "google_books_dataset.xlsx"
KOLOM = ["book_id", "title", "authors", "categories", "published_date"]


def baca_dataset(path):
    """Baca CSV normal, atau Excel yang ternyata berisi baris CSV dalam satu kolom."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    if path.suffix.lower() == ".xlsx":
        df = pd.read_excel(path, header=None, dtype=str)
        # File yang dibuka dan disimpan dari teks CSV kadang berisi seluruh
        # baris CSV di kolom pertama. Kenali header yang memuat book_id,title.
        first = str(df.iloc[0, 0]) if not df.empty else ""
        if len(df.columns) == 1 and ("book_id,title" in first.lower() or first.lower().startswith("book_id")):
            text_csv = "\n".join(df.iloc[:, 0].dropna().astype(str).tolist())
            df = pd.read_csv(StringIO(text_csv), dtype=str, on_bad_lines="skip", engine="python")
        else:
            df.columns = [str(c).strip().lower() for c in df.iloc[0]]
            df = df.iloc[1:].reset_index(drop=True)
    else:
        # Dataset asli menggunakan koma sebagai pemisah.
        df = pd.read_csv(path, encoding="utf-8-sig", dtype=str, on_bad_lines="skip", engine="python")

    df.columns = [str(c).strip().lower() for c in df.columns]
    if "title" not in df.columns:
        raise ValueError("Kolom 'title' tidak ditemukan. Pastikan file dataset benar.")

    for col in KOLOM:
        if col not in df.columns:
            df[col] = ""
    df = df[KOLOM].fillna("")
    df["title"] = df["title"].astype(str).str.strip()
    df = df[df["title"] != ""]

    books = []
    for _, row in df.iterrows():
        books.append({
            "book_id": row["book_id"].strip() or "Tidak diketahui",
            "title": row["title"].strip(),
            "author": row["authors"].strip() or "Tidak diketahui",
            "category": row["categories"].strip() or "Tidak diketahui",
            "published_date": row["published_date"].strip() or "Tidak diketahui",
        })
    return books


def linear_search(books, keyword):
    count = 0
    target = keyword.strip().casefold()
    for book in books:
        count += 1
        if book["title"].casefold() == target:
            return book, count
    return None, count


def binary_search(sorted_books, keyword):
    left, right, count = 0, len(sorted_books) - 1, 0
    target = keyword.strip().casefold()
    while left <= right:
        mid = (left + right) // 2
        count += 1
        title = sorted_books[mid]["title"].casefold()
        if title == target:
            return sorted_books[mid], count
        if title < target:
            left = mid + 1
        else:
            right = mid - 1
    return None, count


def tampilkan_hasil(nama, result, comparisons, elapsed):
    print(f"\n--- {nama} ---")
    if result:
        print("Status          : Buku ditemukan")
        print("ID buku         :", result["book_id"])
        print("Judul           :", result["title"])
        print("Penulis         :", result["author"])
        print("Kategori        :", result["category"])
        print("Tanggal terbit  :", result["published_date"])
    else:
        print("Status          : Buku tidak ditemukan")
    print("Jumlah perbandingan:", comparisons)
    print(f"Waktu pencarian : {elapsed:.8f} detik")


def benchmark(books):
    print("\n=== PENGUJIAN PERFORMA ===")
    print("Waktu bergantung pada komputer; pengurutan Binary Search tidak dihitung dalam waktu pencarian.")
    print(f"{'n':>7} | {'Algoritma':<14} | {'Kasus':<18} | {'Perbandingan':>13} | {'Waktu (detik)':>14}")
    print("-" * 79)
    for n in (100, 1000, 10000):
        if len(books) < n:
            print(f"n={n} dilewati: dataset hanya berisi {len(books)} buku.")
            continue
        data = books[:n]
        sorted_data = sorted(data, key=lambda b: b["title"].casefold())
        cases_linear = [
            ("Posisi awal", data[0]["title"]),
            ("Posisi tengah", data[n // 2]["title"]),
            ("Posisi akhir", data[-1]["title"]),
            ("Tidak ditemukan", "__JUDUL_TIDAK_ADA_DAA__"),
        ]
        cases_binary = [
            ("Posisi awal", sorted_data[0]["title"]),
            ("Posisi tengah", sorted_data[n // 2]["title"]),
            ("Posisi akhir", sorted_data[-1]["title"]),
            ("Tidak ditemukan", "__JUDUL_TIDAK_ADA_DAA__"),
        ]
        for label, target in cases_linear:
            start = time.perf_counter()
            _, count = linear_search(data, target)
            elapsed = time.perf_counter() - start
            print(f"{n:7} | {'Linear Search':<14} | {label:<18} | {count:13} | {elapsed:14.8f}")
        for label, target in cases_binary:
            start = time.perf_counter()
            _, count = binary_search(sorted_data, target)
            elapsed = time.perf_counter() - start
            print(f"{n:7} | {'Binary Search':<14} | {label:<18} | {count:13} | {elapsed:14.8f}")


def main():
    print("=" * 44)
    print(" SISTEM PENCARIAN BUKU PERPUSTAKAAN")
    print("=" * 44)
    print("1. Dataset sampel (sample_buku.csv)")
    print("2. Dataset utama Kaggle (file di Downloads)")
    print("3. Uji performa dataset utama")
    pilihan = input("Pilih menu (1/2/3): ").strip()

    if pilihan == "1":
        path = FILE_SAMPEL
    elif pilihan in ("2", "3"):
        # Prioritaskan CSV asli jika ada; jika tidak, pakai file Excel.
        path = FILE_CSV if FILE_CSV.exists() else FILE_EXCEL
    else:
        print("Pilihan tidak valid.")
        return

    try:
        books = baca_dataset(path)
    except Exception as exc:
        print("\nGagal membaca dataset:", exc)
        print("Lokasi yang dicoba:", path)
        print("Pastikan file bernama google_books_dataset.csv atau google_books_dataset.xlsx ada di folder Downloads.")
        return

    print(f"\nDataset berhasil dibaca: {len(books):,} buku")
    print("File:", path)
    if not books:
        print("Tidak ada data buku yang valid.")
        return

    if pilihan == "3":
        benchmark(books)
        return

    keyword = input("Masukkan judul buku secara lengkap: ").strip()
    if not keyword:
        print("Judul tidak boleh kosong.")
        return

    start = time.perf_counter()
    result_l, count_l = linear_search(books, keyword)
    time_l = time.perf_counter() - start

    sorted_books = sorted(books, key=lambda b: b["title"].casefold())
    start = time.perf_counter()
    result_b, count_b = binary_search(sorted_books, keyword)
    time_b = time.perf_counter() - start

    tampilkan_hasil("LINEAR SEARCH", result_l, count_l, time_l)
    tampilkan_hasil("BINARY SEARCH", result_b, count_b, time_b)
    print("\nCatatan: Binary Search hanya benar jika data sudah diurutkan berdasarkan judul.")


if __name__ == "__main__":
    main()
