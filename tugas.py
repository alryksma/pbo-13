import mysql.connector

# Koneksi ke database
class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_all(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def hapus_data(self, table, condition_column, condition_value):
        query = f"DELETE FROM {table} WHERE {condition_column} = %s"
        values = (condition_value,)
        self.execute_query(query, values)

    def update_data(self, table, set_column, set_value, condition_column, condition_value):
        query = f"UPDATE {table} SET {set_column} = %s WHERE {condition_column} = %s"
        values = (set_value, condition_value)
        self.execute_query(query, values)

class Sosial:
    def __init__(self, nama, umur, tempatLahir):
        self.nama = nama
        self._umur = umur
        self.tempatLahir = tempatLahir

    def tambahData(self, db_manager):
        print("Tambah Data")
        nama = input("Nama: ")
        umur = int(input("Usia: "))
        tempatLahir = input("Tempat Lahir: ")

        # Menambah data ke database
        query = "INSERT INTO sosial (nama, umur, tempatLahir) VALUES (%s, %s, %s)"
        values = (nama, umur, tempatLahir)
        db_manager.execute_query(query, values)

    def tampil(self):
        print(
            f"Nama: {self.nama}\nUsia: {self._umur}\nTempat Lahir: {self.tempatLahir}"
        )

    def tambahTahunLahir(self, tahun):
        self._umur += tahun

    def isDewasa(self):
        return self._umur >= 18


class IdentitasNegara(Sosial):
    def __init__(self, nama, umur, tempatLahir, nik, noKK, pekerjaan, statusNikah, isAlive):
        super().__init__(nama, umur, tempatLahir)
        self.__nik = nik
        self.__noKK = noKK
        self._pekerjaan = pekerjaan
        self.statusNikah = statusNikah
        self.isAlive = isAlive

    def tampil(self):
        super().tampil()
        print(
            f"NIK: {self.__nik}\nNomor KK: {self.__noKK}\nPekerjaan: {self._pekerjaan}"
        )
        print(f"Status Nikah: {self.statusNikah}\nApakah Hidup: {self.isAlive}")

    def tambahData(self, db_manager):
        super().tambahData(db_manager)
        nik = int(input("Masukkan NIK: "))
        noKK = int(input("Masukkan Nomor KK: "))
        pekerjaan = input("Masukkan Pekerjaan: ")
        statusNikah = input("Masukkan Status Nikah (True or False): ")
        isAlive = input("Masukkan Status Hidup (True or False): ")

        # Menambah data ke database
        query = "INSERT INTO identitasnegara (nama, umur, tempatLahir, nik, noKK, pekerjaan, statusNikah, isAlive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.nama, self._umur, self.tempatLahir, nik, noKK, pekerjaan, statusNikah, isAlive)
        db_manager.execute_query(query, values)

    def tambahTahunLahir(self, tahun):
        super().tambahTahunLahir(tahun)

    def get_nik(self):
        return self.__nik


class CatatanTindakKriminal(IdentitasNegara):
    def __init__(self, nama, umur, tempatLahir, nik, noKK, pekerjaan, statusNikah, isAlive, jenisTindakKriminal, tanggalTindakKriminal, isSudahDipidana):
        super().__init__(nama, umur, tempatLahir, nik, noKK, pekerjaan, statusNikah, isAlive)
        self.jenisTindakKriminal = jenisTindakKriminal
        self._tanggalTindakKriminal = tanggalTindakKriminal
        self.__isSudahDipidana = isSudahDipidana
        self.__noKK = noKK  # Menambahkan atribut __noKK

    def tampil(self):
        super().tampil()
        print(f"Jenis Tindak Kriminal: {self.jenisTindakKriminal}")
        print(f"Tanggal Tindak Kriminal: {self._tanggalTindakKriminal}")
        print(f"Sudah Dipidana: {self.__isSudahDipidana}")

    def tambahData(self, db_manager):
        super().tambahData(db_manager)
        jenisTindakKriminal = input("Masukkan Jenis Tindak Kriminal: ")
        tanggalTindakKriminal = input("Masukkan Tanggal Tindak Kriminal: ")
        isSudahDipidana = input("Apakah Sudah Dipidana? (y/n): ")

        # Menambah data ke database
        query = "INSERT INTO catatantindakkriminal (nama, umur, tempatLahir, nik, noKK, pekerjaan, statusNikah, isAlive, jenisTindakKriminal, tanggalTindakKriminal, isSudahDipidana) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.nama, self._umur, self.tempatLahir, self.get_nik(), self.__noKK, self._pekerjaan, self.statusNikah, self.isAlive, jenisTindakKriminal, tanggalTindakKriminal, isSudahDipidana)
        db_manager.execute_query(query, values)


    def isDewasa(self):
        return super().isDewasa() and self._pekerjaan != "Pelajar"


# Membuat objek DatabaseManager
db_manager = DatabaseManager(host="localhost", user="root", password="", database="5220411242")

def looping(db_manager):
    # Looping untuk menambah data
    while True:
        print("\n1. Tambah Data Sosial")
        print("2. Tambah Data Identitas Negara")
        print("3. Tambah Data Catatan Tindak Kriminal")
        print("4. Tampilkan Semua Data")
        print("5. Hapus Data Berdasarkan NIK")
        print("6. Update Data Berdasarkan NIK")
        print("7. Keluar")

        pilihan = input("Pilih menu (1-7): ")

        if pilihan == "1":
            sosial = Sosial("", 0, "")
            sosial.tambahData(db_manager)
        elif pilihan == "2":
            identitasnegara = IdentitasNegara("", 0, "", 0, 0, "", False, False)
            identitasnegara.tambahData(db_manager)
        elif pilihan == "3":
            catatan_kriminal = CatatanTindakKriminal("", 0, "", 0, 0, "", False, False, "", "", False)
            catatan_kriminal.tambahData(db_manager)
        elif pilihan == "4":
            # Menampilkan semua data dari database
            query = "SELECT * FROM sosial"
            result = db_manager.fetch_all(query)
            for row in result:
                print(row)
        elif pilihan == "5":
            nik_hapus = input("Masukkan NIK untuk menghapus data: ")
            db_manager.hapus_data("identitasnegara", "nik", nik_hapus)
            print(f"Data dengan NIK {nik_hapus} telah dihapus.")
        elif pilihan == "6":
            nik_update = input("Masukkan NIK untuk memperbarui data: ")
            set_column = input("Masukkan nama kolom yang ingin diperbarui: ")
            set_value = input("Masukkan nilai baru: ")
            db_manager.update_data("identitasnegara", set_column, set_value, "nik", nik_update)
            print(f"Data dengan NIK {nik_update} telah diperbarui.")
        elif pilihan == "7":
            print("Terima kasih! Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih kembali.")


# Menjalankan fungsi looping
looping(db_manager)
