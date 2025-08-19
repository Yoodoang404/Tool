import math
import sys
import time

# ANSI escape codes for colors
class Warna:
    HEADER = '\033[95m'
    BIRU = '\033[94m'
    HIJAU = '\033[92m'
    KUNING = '\033[93m'
    MERAH = '\033[91m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    TEBAL = '\033[1m'
    UNDERLINE = '\033[4m'
    ABU = '\033[90m'

def tambah(x, y):
    return x + y

def kurang(x, y):
    return x - y

def kali(x, y):
    return x * y

def bagi(x, y):
    if y == 0:
        raise ValueError(f"{Warna.MERAH}Tidak bisa membagi dengan nol!{Warna.ENDC}")
    return x / y

def pangkat(x, y):
    return x ** y

def akar(x):
    if x < 0:
        raise ValueError(f"{Warna.MERAH}Tidak bisa menghitung akar dari bilangan negatif!{Warna.ENDC}")
    return math.sqrt(x)

def faktorial(x):
    if x < 0:
        raise ValueError(f"{Warna.MERAH}Tidak bisa menghitung faktorial dari bilangan negatif!{Warna.ENDC}")
    return math.factorial(x)

def tampilkan_menu():
    print(Warna.BIRU + "="*40 + Warna.ENDC)
    print(Warna.TEBAL + Warna.HEADER + "         KALKULATOR KEREN         " + Warna.ENDC)
    print(Warna.BIRU + "="*40 + Warna.ENDC)
    print(Warna.KUNING + "Pilih operasi yang diinginkan:" + Warna.ENDC)
    print(Warna.HIJAU + "1. Tambah (+)" + Warna.ENDC)
    print(Warna.HIJAU + "2. Kurang (-)" + Warna.ENDC)
    print(Warna.HIJAU + "3. Kali (*)" + Warna.ENDC)
    print(Warna.HIJAU + "4. Bagi (/)" + Warna.ENDC)
    print(Warna.HIJAU + "5. Pangkat (^)" + Warna.ENDC)
    print(Warna.HIJAU + "6. Akar (√)" + Warna.ENDC)
    print(Warna.HIJAU + "7. Faktorial (!)" + Warna.ENDC)
    print(Warna.MERAH + "8. Keluar" + Warna.ENDC)
    print(Warna.BIRU + "="*40 + Warna.ENDC)

def animasi_loading(teks="Menghitung"):
    for i in range(3):
        print(Warna.ABU + f"{teks}{'.' * (i+1)}" + Warna.ENDC, end='\r')
        time.sleep(0.3)
    print(" " * 20, end='\r')

while True:
    tampilkan_menu()
    try:
        pilihan = int(input(Warna.CYAN + "Masukkan pilihan (1-8): " + Warna.ENDC))
    except ValueError:
        print(Warna.MERAH + "Input harus berupa angka! Silakan coba lagi.\n" + Warna.ENDC)
        continue

    if pilihan == 8:
        print(Warna.KUNING + "Terima kasih telah menggunakan kalkulator ini. Sampai jumpa!" + Warna.ENDC)
        sys.exit(0)

    if pilihan in (1, 2, 3, 4, 5):
        try:
            x = float(input(Warna.CYAN + "Masukkan bilangan pertama: " + Warna.ENDC))
            y = float(input(Warna.CYAN + "Masukkan bilangan kedua: " + Warna.ENDC))
        except ValueError:
            print(Warna.MERAH + "Input harus berupa angka! Silakan coba lagi.\n" + Warna.ENDC)
            continue

        animasi_loading()
        try:
            if pilihan == 1:
                hasil = tambah(x, y)
                print(Warna.HIJAU + f"Hasil: {x} + {y} = {hasil}" + Warna.ENDC)
            elif pilihan == 2:
                hasil = kurang(x, y)
                print(Warna.HIJAU + f"Hasil: {x} - {y} = {hasil}" + Warna.ENDC)
            elif pilihan == 3:
                hasil = kali(x, y)
                print(Warna.HIJAU + f"Hasil: {x} * {y} = {hasil}" + Warna.ENDC)
            elif pilihan == 4:
                hasil = bagi(x, y)
                print(Warna.HIJAU + f"Hasil: {x} / {y} = {hasil}" + Warna.ENDC)
            elif pilihan == 5:
                hasil = pangkat(x, y)
                print(Warna.HIJAU + f"Hasil: {x} ^ {y} = {hasil}" + Warna.ENDC)
        except Exception as e:
            print(Warna.MERAH + f"Terjadi kesalahan: {e}" + Warna.ENDC)

    elif pilihan == 6:
        try:
            x = float(input(Warna.CYAN + "Masukkan bilangan yang ingin diakar: " + Warna.ENDC))
            animasi_loading()
            hasil = akar(x)
            print(Warna.HIJAU + f"Hasil: √{x} = {hasil}" + Warna.ENDC)
        except Exception as e:
            print(Warna.MERAH + f"Terjadi kesalahan: {e}" + Warna.ENDC)

    elif pilihan == 7:
        try:
            x = int(input(Warna.CYAN + "Masukkan bilangan bulat non-negatif: " + Warna.ENDC))
            animasi_loading()
            hasil = faktorial(x)
            print(Warna.HIJAU + f"Hasil: {x}! = {hasil}" + Warna.ENDC)
        except Exception as e:
            print(Warna.MERAH + f"Terjadi kesalahan: {e}" + Warna.ENDC)

    else:
        print(Warna.MERAH + "Pilihan tidak valid. Silakan coba lagi.\n" + Warna.ENDC)

    print(Warna.BIRU + "\n" + "-"*40 + "\n" + Warna.ENDC)
