import cv2
from pyzbar.pyzbar import decode
import re
import sqlite3
from datetime import datetime

# Membuat atau menghubungkan ke database (file presensi.db)
connection = sqlite3.connect("presensi.db")
cursor = connection.cursor()

def read_qr_code():
    cap = cv2.VideoCapture(0)  # Mengakses webcam (0 adalah indeks kamera default)
    detected_qr_data = set()  # Menyimpan data QR yang telah terdeteksi
    
    while True:
        _, frame = cap.read()  # Membaca frame dari webcam
        decoded_objects = decode(frame)  # Mendekode objek dari frame
        
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')  # Mendapatkan data kode QR dalam bentuk teks
            
            if qr_data not in detected_qr_data:
                print(f"QR Code Data: {qr_data}")
                detected_qr_data.add(qr_data)  # Menambahkan data ke set detected_qr_data
                
                # Menggunakan ekspresi reguler untuk mengekstrak informasi               
                match = re.search(r"Nama: (.+)\nNIM: (.+)", qr_data)
                if match:
                    nama = match.group(1)
                    nim = match.group(2).strip()  # Menghapus spasi di awal dan akhir "nim"
                else:
                    # Penanganan jika format tidak sesuai
                    nama = "Tidak Diketahui"
                    nim = "N/A"
                
                # Memasukkan data ke dalam tabel presensi (catatan masuk)
                masuk_timestamp = datetime.now()
                cursor.execute("INSERT INTO presensi (nama, nim, waktu) VALUES (?, ?, ?)", (nama, nim, masuk_timestamp))
                connection.commit()
       
        cv2.imshow("Pembaca Kode QR", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Tekan 'q' untuk keluar dari aplikasi
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_qr_code()
