"""
Tugas 1 - Sistem Pencarian Data Buku Perpustakaan Digital
Nama : Falih Darmawan
NIM  : 12550110298
Prodi: Teknik Informatika, UIN Sultan Syarif Kasim Riau

Program ini mengimplementasikan Linear Search dan Binary Search secara manual
(tanpa list.index(), `in`, atau library pencarian), menghitung jumlah operasi
perbandingan, mengukur waktu eksekusi, dan menampilkan hasil pengujian.

Cara pakai:
    python pencarian_buku.py --csv books.csv            # demo + pengujian
    python pencarian_buku.py --csv books.csv --cari "Judul Buku"
    python pencarian_buku.py --csv books.csv --uji-saja
"""

import argparse
import csv
import random
import time
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# 1. MODEL INPUT
# ---------------------------------------------------------------------------
@dataclass
class Buku:
    """Satu baris data buku dari dataset (elemen yang dicari)."""
    judul: str
    penulis: str
    kategori: str
    rating: float
    harga: float
    # Kunci pencarian yang sudah dinormalisasi (huruf kecil, tanpa spasi tepi)
    kunci_judul: str = field(init=False, repr=False)

    def __post_init__(self):
        self.kunci_judul = normalisasi(self.judul)


@dataclass
class PermintaanPencarian:
    """Masukan dari petugas perpustakaan."""
    kata_kunci: str          # judul buku yang dicari
    kriteria: str = "judul"  # kriteria pencarian


# ---------------------------------------------------------------------------
# 2. MODEL OUTPUT
# ---------------------------------------------------------------------------
@dataclass
class HasilPencarian:
    """Keluaran satu kali pemanggilan algoritma pencarian."""
    algoritma: str
    kata_kunci: str
    ditemukan: bool
    indeks: int                    # -1 jika tidak ditemukan
    buku: Optional[Buku]           # None jika tidak ditemukan
    jumlah_perbandingan: int
    waktu_ms: float


@dataclass
class HasilPengujian:
    """Satu baris hasil pengujian (dipakai untuk tabel & grafik)."""
    n: int
    algoritma: str
    skenario: str
    jumlah_operasi: int
    waktu_ms: float


# ---------------------------------------------------------------------------
# Fungsi bantu
# ---------------------------------------------------------------------------
def normalisasi(teks: str) -> str:
    return teks.strip().lower()


NAMA_KOLOM = {
    "judul": ["title", "book title", "book_title", "judul", "name", "book_name"],
    "penulis": ["author", "authors", "book author", "penulis"],
    "kategori": ["category", "categories", "genre", "kategori"],
    "rating": ["rating", "avg_rating", "average_rating", "stars"],
    "harga": ["price", "harga", "price_usd"],
}


def ke_float(teks: str) -> float:
    """Ubah teks seperti '$12.99' menjadi 12.99; 0.0 jika gagal."""
    bersih = ""
    for ch in str(teks):
        if ch.isdigit() or ch == ".":
            bersih += ch
    try:
        return float(bersih)
    except ValueError:
        return 0.0


def cari_kolom(header: List[str], kandidat: List[str]) -> Optional[str]:
    for nama in header:
        for k in kandidat:
            if normalisasi(nama) == k:
                return nama
    return None


# ---------------------------------------------------------------------------
# 3. MEMBACA DATASET & MENYIMPAN KE STRUKTUR DATA (list of Buku)
# ---------------------------------------------------------------------------
def baca_dataset(path_csv: str) -> List[Buku]:
    """Baca CSV -> list[Buku] terurut berdasarkan judul dan tanpa judul ganda.

    Pengurutan (sorted) dan penghapusan duplikat adalah tahap PRA-PROSES,
    bukan bagian dari algoritma pencarian yang dianalisis. Data terurut
    dibutuhkan oleh Binary Search; Linear Search memakai data yang sama
    agar kedua algoritma dibandingkan pada data yang identik.
    """
    mentah: List[Buku] = []
    with open(path_csv, newline="", encoding="utf-8-sig") as f:
        pembaca = csv.DictReader(f)
        header = pembaca.fieldnames or []
        k_judul = cari_kolom(header, NAMA_KOLOM["judul"])
        if k_judul is None:
            raise ValueError(f"Kolom judul tidak ditemukan. Header: {header}")
        k_penulis = cari_kolom(header, NAMA_KOLOM["penulis"])
        k_kategori = cari_kolom(header, NAMA_KOLOM["kategori"])
        k_rating = cari_kolom(header, NAMA_KOLOM["rating"])
        k_harga = cari_kolom(header, NAMA_KOLOM["harga"])

        for baris in pembaca:
            judul = (baris.get(k_judul) or "").strip()
            if judul == "":
                continue
            mentah.append(Buku(
                judul=judul,
                penulis=(baris.get(k_penulis) or "-").strip() if k_penulis else "-",
                kategori=(baris.get(k_kategori) or "-").strip() if k_kategori else "-",
                rating=ke_float(baris.get(k_rating, "")) if k_rating else 0.0,
                harga=ke_float(baris.get(k_harga, "")) if k_harga else 0.0,
            ))

    mentah.sort(key=lambda b: b.kunci_judul)
    unik: List[Buku] = []
    for b in mentah:  # hapus duplikat dengan membandingkan tetangga
        if len(unik) == 0 or unik[-1].kunci_judul != b.kunci_judul:
            unik.append(b)
    return unik


# ---------------------------------------------------------------------------
# 4. LINEAR SEARCH  -> O(n)
# ---------------------------------------------------------------------------
def linear_search(data: List[Buku], permintaan: PermintaanPencarian) -> HasilPencarian:
    kunci = normalisasi(permintaan.kata_kunci)
    perbandingan = 0
    mulai = time.perf_counter()
    for i in range(len(data)):
        perbandingan += 1                      # 1 perbandingan kunci per elemen
        if data[i].kunci_judul == kunci:
            waktu = (time.perf_counter() - mulai) * 1000
            return HasilPencarian("Linear Search", permintaan.kata_kunci, True,
                                  i, data[i], perbandingan, waktu)
    waktu = (time.perf_counter() - mulai) * 1000
    return HasilPencarian("Linear Search", permintaan.kata_kunci, False,
                          -1, None, perbandingan, waktu)


# ---------------------------------------------------------------------------
# 5. BINARY SEARCH  -> O(log n)   (data HARUS terurut berdasarkan judul)
# ---------------------------------------------------------------------------
def binary_search(data: List[Buku], permintaan: PermintaanPencarian) -> HasilPencarian:
    kunci = normalisasi(permintaan.kata_kunci)
    kiri, kanan = 0, len(data) - 1
    perbandingan = 0
    mulai = time.perf_counter()
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        perbandingan += 1                      # 1 perbandingan kunci per iterasi
        if data[tengah].kunci_judul == kunci:
            waktu = (time.perf_counter() - mulai) * 1000
            return HasilPencarian("Binary Search", permintaan.kata_kunci, True,
                                  tengah, data[tengah], perbandingan, waktu)
        elif data[tengah].kunci_judul < kunci:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    waktu = (time.perf_counter() - mulai) * 1000
    return HasilPencarian("Binary Search", permintaan.kata_kunci, False,
                          -1, None, perbandingan, waktu)


# ---------------------------------------------------------------------------
# 6 & 7. TAMPILAN HASIL (ditemukan / tidak ditemukan)
# ---------------------------------------------------------------------------
def tampilkan_hasil(h: HasilPencarian) -> None:
    print(f"=== {h.algoritma} ===")
    print(f"Kata kunci (judul) : {h.kata_kunci}")
    if h.ditemukan:
        b = h.buku
        print("Status             : DITEMUKAN")
        print(f"Indeks             : {h.indeks}")
        print(f"Judul              : {b.judul}")
        print(f"Penulis            : {b.penulis}")
        print(f"Kategori           : {b.kategori}")
        print(f"Rating             : {b.rating}")
        print(f"Harga              : {b.harga}")
    else:
        print("Status             : TIDAK DITEMUKAN")
        print(f"Informasi          : Buku dengan judul '{h.kata_kunci}' tidak ada dalam data.")
    print(f"Jumlah perbandingan: {h.jumlah_perbandingan}")
    print(f"Waktu eksekusi     : {h.waktu_ms:.6f} ms\n")


# ---------------------------------------------------------------------------
# 8, 9. PENGUJIAN (n = 100, 1.000, 10.000) + PENGUKURAN WAKTU
# ---------------------------------------------------------------------------
JUDUL_TIDAK_ADA = "~~~ Judul Buku Yang Tidak Ada ~~~"   # urut setelah semua judul


def rata_waktu_ms(fungsi, data, permintaan, ulangan: int) -> float:
    mulai = time.perf_counter()
    for _ in range(ulangan):
        fungsi(data, permintaan)
    return (time.perf_counter() - mulai) * 1000 / ulangan


def jalankan_pengujian(semua: List[Buku], ukuran=(100, 1000, 10000),
                       ulangan: int = 200, seed: int = 42) -> List[HasilPengujian]:
    rng = random.Random(seed)
    hasil: List[HasilPengujian] = []
    for n in ukuran:
        if n > len(semua):
            print(f"[lewati] n={n} melebihi jumlah data ({len(semua)})")
            continue
        sampel = rng.sample(semua, n)
        sampel.sort(key=lambda b: b.kunci_judul)
        skenario = [
            ("Awal", sampel[0].judul),
            ("Tengah", sampel[(n - 1) // 2].judul),
            ("Akhir", sampel[n - 1].judul),
            ("Tidak ditemukan", JUDUL_TIDAK_ADA),
        ]
        for fungsi in (linear_search, binary_search):
            for nama, judul in skenario:
                p = PermintaanPencarian(judul)
                r = fungsi(sampel, p)
                waktu = rata_waktu_ms(fungsi, sampel, p, ulangan)
                hasil.append(HasilPengujian(n, r.algoritma, nama,
                                            r.jumlah_perbandingan, waktu))
    return hasil


def tampilkan_tabel(hasil: List[HasilPengujian]) -> None:
    print(f"{'n':>7} | {'Algoritma':<14} | {'Skenario':<16} | "
          f"{'Operasi':>8} | {'Waktu (ms)':>12}")
    print("-" * 70)
    for h in hasil:
        print(f"{h.n:>7} | {h.algoritma:<14} | {h.skenario:<16} | "
              f"{h.jumlah_operasi:>8} | {h.waktu_ms:>12.6f}")


def simpan_csv(hasil: List[HasilPengujian], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "algoritma", "skenario", "jumlah_operasi", "waktu_ms"])
        for h in hasil:
            w.writerow([h.n, h.algoritma, h.skenario, h.jumlah_operasi,
                        f"{h.waktu_ms:.6f}"])


def buat_grafik(hasil: List[HasilPengujian], path: str) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib tidak terpasang: grafik dilewati.")
        return
    skenario = ["Awal", "Tengah", "Akhir", "Tidak ditemukan"]
    fig, sumbu = plt.subplots(2, 4, figsize=(18, 8))
    for j, s in enumerate(skenario):
        for algo, gaya in (("Linear Search", "o-"), ("Binary Search", "s--")):
            titik = [h for h in hasil if h.algoritma == algo and h.skenario == s]
            xs = [h.n for h in titik]
            sumbu[0][j].plot(xs, [h.jumlah_operasi for h in titik], gaya, label=algo)
            sumbu[1][j].plot(xs, [h.waktu_ms for h in titik], gaya, label=algo)
        sumbu[0][j].set_title(f"Operasi - {s}")
        sumbu[1][j].set_title(f"Waktu (ms) - {s}")
        for baris in (0, 1):
            sumbu[baris][j].set_xscale("log")
            sumbu[baris][j].set_yscale("log")
            sumbu[baris][j].set_xlabel("n")
            sumbu[baris][j].grid(True, alpha=.3)
        sumbu[0][j].legend()
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    print(f"Grafik disimpan: {path}")


# ---------------------------------------------------------------------------
# PROGRAM UTAMA
# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Linear vs Binary Search - data buku")
    ap.add_argument("--csv", required=True, help="path file CSV dataset buku")
    ap.add_argument("--cari", help="judul buku yang dicari (opsional)")
    ap.add_argument("--uji-saja", action="store_true", help="lewati demo pencarian")
    ap.add_argument("--ulangan", type=int, default=200,
                    help="jumlah pengulangan untuk rata-rata waktu")
    args = ap.parse_args()

    buku = baca_dataset(args.csv)
    print(f"Jumlah buku (judul unik) yang dimuat: {len(buku)}\n")

    if args.cari:
        p = PermintaanPencarian(args.cari)
        tampilkan_hasil(linear_search(buku, p))
        tampilkan_hasil(binary_search(buku, p))
    elif not args.uji_saja:
        ada = PermintaanPencarian(buku[len(buku) // 2].judul)
        print(">>> DEMO: data ADA")
        tampilkan_hasil(linear_search(buku, ada))
        tampilkan_hasil(binary_search(buku, ada))
        print(">>> DEMO: data TIDAK ada")
        tidak = PermintaanPencarian("Buku Fiktif Yang Tidak Pernah Ada")
        tampilkan_hasil(linear_search(buku, tidak))
        tampilkan_hasil(binary_search(buku, tidak))

    print(">>> PENGUJIAN n = 100, 1.000, 10.000")
    hasil = jalankan_pengujian(buku, ulangan=args.ulangan)
    tampilkan_tabel(hasil)
    simpan_csv(hasil, "hasil_pengujian.csv")
    buat_grafik(hasil, "grafik_pengujian.png")


if __name__ == "__main__":
    main()
