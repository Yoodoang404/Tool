import random
import time
import os

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
    BLINK = '\033[5m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def garis():
    print(Warna.BIRU + "="*50 + Warna.ENDC)

def slot_banner():
    garis()
    print(Warna.TEBAL + Warna.HEADER + Warna.BLINK + "      🐅 RED TIGER SLOT GAME 🐅      " + Warna.ENDC)
    garis()
    print(Warna.KUNING + Warna.TEBAL + "Menangkan " + Warna.HIJAU + "JACKPOT" + Warna.KUNING + " dengan 3 simbol sama!")
    print("Menang juga jika 2 simbol sama (" + Warna.CYAN + "setengah payout" + Warna.KUNING + ")!\n" + Warna.ENDC)

# Sederhana: data akun hanya disimpan di memori (tidak ke file)
users_db = {}

def register():
    clear_screen()
    garis()
    print(Warna.TEBAL + Warna.HEADER + "         REGISTRASI AKUN         " + Warna.ENDC)
    garis()
    while True:
        username = input(Warna.CYAN + "Buat username: " + Warna.ENDC).strip()
        if not username:
            print(Warna.MERAH + "Username tidak boleh kosong." + Warna.ENDC)
            continue
        if username in users_db:
            print(Warna.MERAH + "Username sudah terdaftar. Pilih username lain." + Warna.ENDC)
            continue
        break
    while True:
        password = input(Warna.CYAN + "Buat password: " + Warna.ENDC)
        if not password:
            print(Warna.MERAH + "Password tidak boleh kosong." + Warna.ENDC)
            continue
        break
    users_db[username] = {"password": password, "balance": 1000}
    print(Warna.HIJAU + "Registrasi berhasil! Silakan login." + Warna.ENDC)
    time.sleep(1.5)
    return

def login():
    clear_screen()
    garis()
    print(Warna.TEBAL + Warna.HEADER + "            LOGIN AKUN           " + Warna.ENDC)
    garis()
    for _ in range(3):
        username = input(Warna.CYAN + "Username: " + Warna.ENDC).strip()
        password = input(Warna.CYAN + "Password: " + Warna.ENDC)
        user = users_db.get(username)
        if user and user["password"] == password:
            print(Warna.HIJAU + "Login berhasil! Selamat datang, " + username + "!" + Warna.ENDC)
            time.sleep(1.2)
            return username
        else:
            print(Warna.MERAH + "Username atau password salah." + Warna.ENDC)
    print(Warna.MERAH + "Terlalu banyak percobaan gagal. Keluar..." + Warna.ENDC)
    time.sleep(1.5)
    return None

class RedTigerGame:
    def __init__(self, username):
        self.username = username
        self.balance = users_db[username]["balance"]
        self.symbols = ['🍒', '🔔', '7️⃣', '💎', '🍋', '⭐', '🐅']  # Red Tiger = 🐅
        self.payouts = {
            '🍒': 2,
            '🔔': 5,
            '7️⃣': 10,
            '💎': 20,
            '🍋': 3,
            '⭐': 8,
            '🐅': 50  # Red Tiger jackpot
        }

    def animasi_spin(self):
        for _ in range(10):
            baris = [random.choice(self.symbols) for _ in range(3)]
            print(Warna.ABU + Warna.BLINK + " | ".join(baris) + Warna.ENDC, end='\r')
            time.sleep(0.10)
        print(" " * 30, end='\r')

    def animate_reels(self, final_result):
        # Animasi reels berhenti satu per satu dengan efek slow-down
        total_ticks_per_reel = [14, 18, 22]
        max_ticks = max(total_ticks_per_reel)
        for tick in range(max_ticks):
            display_symbols = []
            for col in range(3):
                if tick >= total_ticks_per_reel[col]:
                    symbol = final_result[col]
                    color = Warna.TEBAL + Warna.HIJAU if symbol == '🐅' else Warna.TEBAL + Warna.KUNING
                    display_symbols.append(color + symbol + Warna.ENDC)
                else:
                    blur_symbol = random.choice(self.symbols)
                    color = Warna.ABU if (tick % 2 == 0) else Warna.CYAN
                    display_symbols.append(color + blur_symbol + Warna.ENDC)
            print(" " * 50, end='\r')
            print(" | ".join(display_symbols), end='\r')
            time.sleep(0.05 + tick * 0.009)
        print(" " * 50, end='\r')
        locked_display = []
        for s in final_result:
            if s == '🐅':
                locked_display.append(Warna.TEBAL + Warna.HIJAU + Warna.BLINK + s + Warna.ENDC)
            else:
                locked_display.append(Warna.TEBAL + Warna.KUNING + s + Warna.ENDC)
        print(" | ".join(locked_display))

    def spin(self, bet):
        if bet > self.balance or bet <= 0:
            print(Warna.MERAH + f"Bet tidak valid. Saldo Anda: {self.balance}" + Warna.ENDC)
            return

        self.balance -= bet
        print(Warna.CYAN + f"\nMemutar slot dengan taruhan {bet}..." + Warna.ENDC)
        # Tentukan hasil akhir lebih dulu agar animasi bisa berhenti sesuai hasil
        result = [random.choice(self.symbols) for _ in range(3)]
        # Animasi spin dengan reels berhenti satu per satu
        self.animasi_spin()
        self.animate_reels(result)

        # Cek kemenangan 3 simbol sama
        if result.count(result[0]) == 3:
            win = bet * self.payouts[result[0]]
            self.balance += win
            print(Warna.HIJAU + Warna.TEBAL + Warna.BLINK + f"\n🎉 JACKPOT! {result[0]} x3! Menang {win}! 🎉" + Warna.ENDC)
        # Cek kemenangan 2 simbol sama
        elif result[0] == result[1] or result[0] == result[2] or result[1] == result[2]:
            # Cari simbol yang sama
            if result[0] == result[1] or result[0] == result[2]:
                symbol = result[0]
            else:
                symbol = result[1]
            win = int(bet * self.payouts[symbol] / 2)
            if win > 0:
                print(Warna.KUNING + Warna.TEBAL + f"\n✨ {symbol} x2! Menang {win}! ✨" + Warna.ENDC)
                self.balance += win
            else:
                print(Warna.MERAH + "\nBelum beruntung, coba lagi!" + Warna.ENDC)
        else:
            print(Warna.MERAH + "\nBelum beruntung, coba lagi!" + Warna.ENDC)

        print(Warna.KUNING + f"Saldo Anda sekarang: {self.balance}\n" + Warna.ENDC)
        garis()

    def main_menu(self):
        bet_options = [100, 200, 250, 300, 350, 400, 450, 500]
        while True:
            clear_screen()
            slot_banner()
            print(Warna.CYAN + f"User: {self.username}" + Warna.ENDC)
            print(Warna.CYAN + f"Saldo Anda: {self.balance}" + Warna.ENDC)
            print(Warna.BIRU + "-"*50 + Warna.ENDC)
            print(Warna.TEBAL + Warna.KUNING + "Pilih jumlah taruhan:" + Warna.ENDC)
            # Tampilkan opsi taruhan yang <= saldo
            available_bets = [val for val in bet_options if val <= self.balance]
            for idx, val in enumerate(available_bets, 1):
                print(Warna.CYAN + f"{idx}. {val}" + Warna.ENDC, end='   ')
                if idx % 4 == 0:
                    print()
            # Opsi maxbet
            if self.balance > 0 and self.balance not in available_bets:
                maxbet_idx = len(available_bets) + 1
                print(Warna.CYAN + f"{maxbet_idx}. MAXBET ({self.balance})" + Warna.ENDC, end='   ')
            else:
                maxbet_idx = None
            print(Warna.CYAN + f"\n0. Keluar" + Warna.ENDC)
            try:
                pilihan = input(Warna.TEBAL + "Masukkan nomor taruhan: " + Warna.ENDC).strip()
                if not pilihan.isdigit():
                    raise ValueError
                pilihan = int(pilihan)
            except ValueError:
                print(Warna.MERAH + "Input tidak valid." + Warna.ENDC)
                time.sleep(1.2)
                continue
            if pilihan == 0:
                print(Warna.KUNING + "\nTerima kasih telah bermain! Sampai jumpa!" + Warna.ENDC)
                break
            if 1 <= pilihan <= len(available_bets):
                bet = available_bets[pilihan-1]
            elif maxbet_idx is not None and pilihan == maxbet_idx:
                bet = self.balance
            else:
                print(Warna.MERAH + "Pilihan tidak valid." + Warna.ENDC)
                time.sleep(1.2)
                continue
            self.spin(bet)
            if self.balance <= 0:
                print(Warna.MERAH + Warna.TEBAL + "\nSaldo Anda habis. Game over!" + Warna.ENDC)
                break
            input(Warna.ABU + "Tekan Enter untuk lanjut..." + Warna.ENDC)
        # Simpan saldo user ke "database"
        users_db[self.username]["balance"] = self.balance

def main():
    while True:
        clear_screen()
        garis()
        print(Warna.TEBAL + Warna.HEADER + Warna.BLINK + "   SELAMAT DATANG DI RED TIGER SLOT   " + Warna.ENDC)
        garis()
        print(Warna.KUNING + "1. Registrasi Akun\n2. Login\n3. Keluar" + Warna.ENDC)
        try:
            pilihan = input(Warna.CYAN + "Pilih menu (1/2/3): " + Warna.ENDC).strip()
        except KeyboardInterrupt:
            print("\n" + Warna.KUNING + "Keluar..." + Warna.ENDC)
            break
        if pilihan == "1":
            register()
        elif pilihan == "2":
            username = login()
            if username:
                game = RedTigerGame(username)
                game.main_menu()
        elif pilihan == "3":
            print(Warna.KUNING + "Terima kasih! Sampai jumpa!" + Warna.ENDC)
            break
        else:
            print(Warna.MERAH + "Pilihan tidak valid." + Warna.ENDC)
            time.sleep(1.2)

if __name__ == "__main__":
    main()
