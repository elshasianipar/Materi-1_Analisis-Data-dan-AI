import csv
from collections import defaultdict
from pathlib import Path

FILE = Path(__file__).parent / "data_penjualan.csv"

def baca_data():
    data = []
    with FILE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                nama = row["produk"].strip()
                tanggal = row["tanggal"].strip()
                jumlah = int(row["jumlah"])
                harga = float(row["harga_satuan"])
                if not nama or not tanggal or jumlah <= 0 or harga < 0:
                    raise ValueError
            except (ValueError, KeyError, AttributeError):
                print("Baris dilewati karena data kosong/tidak valid:", row)
                continue
            data.append((tanggal, nama, jumlah, harga))
    return data

def main():
    data = baca_data()
    if not data:
        print("Tidak ada data valid.")
        return
    produk, bulanan = defaultdict(float), defaultdict(float)
    total, unit = 0, 0
    for tanggal, nama, jumlah, harga in data:
        nilai = jumlah * harga
        total += nilai
        unit += jumlah
        produk[nama] += nilai
        bulanan[tanggal[:7]] += nilai
    print("=== RINGKASAN PENJUALAN ===")
    print("Transaksi valid:", len(data))
    print("Unit terjual:", unit)
    print(f"Total penjualan: Rp{total:,.0f}")
    print("\nPenjualan per produk:")
    for nama, nilai in sorted(produk.items(), key=lambda x: x[1], reverse=True):
        print(f"- {nama}: Rp{nilai:,.0f}")
    print("\nPenjualan per bulan:")
    for bulan, nilai in sorted(bulanan.items()):
        print(f"- {bulan}: Rp{nilai:,.0f}")
    print("\nProduk dengan nilai penjualan tertinggi:", max(produk, key=produk.get))

if __name__ == "__main__":
    main()
