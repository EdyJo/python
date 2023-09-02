from tkinter import *
import pyqrcode
import csv
from tkinter import filedialog

root = Tk()
root.title("Aplikasi Pembuat Kode QR")
width = 400
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

qrname = StringVar()
qr_result = StringVar()
data = []
current_data_index = 0

def load_data():
    global data, current_data_index
    try:
        with open("mahasiswa.csv", "r") as file:
            csv_reader = csv.reader(file, delimiter=';')
            next(csv_reader)
            data = [row for row in csv_reader]
            if data:
                current_data_index = 0
                show_current_data()
            else:
                qr_result.set("Data tidak ditemukan dalam file CSV.")
    except FileNotFoundError:
        qr_result.set("File 'mahasiswa.csv' tidak ditemukan.")

def show_current_data():
    global current_data_index
    if data:
        id = data[current_data_index][0]
        nama = data[current_data_index][1]
        nim = data[current_data_index][2]
        wa = data[current_data_index][3]
        qr_result.set(f"id: {id}\nNama: {nama}\nNIM: {nim}\nNo WA: {wa}")

def prev_data():
    global current_data_index
    if data and current_data_index > 0:
        current_data_index -= 1
        show_current_data()

def next_data():
    global current_data_index
    if data and current_data_index < len(data) - 1:
        current_data_index += 1
        show_current_data()

# Create QR Result Labels
lbl_id = Label(root, text="", font=('arial', 12))
lbl_id.pack()
lbl_nama = Label(root, text="", font=('arial', 12))
lbl_nama.pack()
lbl_nim = Label(root, text="", font=('arial', 12))
lbl_nim.pack()
lbl_wa = Label(root, text="", font=('arial', 12))
lbl_wa.pack()

def create_qr():
    global current_data_index
    if len(data) > 0:
        # id = data[current_data_index][0]
        nama = data[current_data_index][1]
        nim = data[current_data_index][2]
        # wa = data[current_data_index][3]
        qr_data = f"Nama: {nama}\nNIM: {nim}"
        # qr_data = f"Nama: {nama}\nNIM: {nim}\nNo WA: {wa}"
        qr = pyqrcode.create(qr_data)
        filename = f"{nim}_{nama}.png"  # Create the filename
        qr.png(filename, scale=8)
        qr_result.set(f"QR code berhasil dibuat {filename}")

Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)

# Load Data Button
btn_load_data = Button(root, text="Load Data", width=20, command=load_data)
btn_load_data.pack(pady=10)

# Previous Button
btn_prev = Button(Form, text="Prev", width=10, command=prev_data)
btn_prev.grid(row=1, column=0, padx=10)

# Next Button
btn_next = Button(Form, text="Next", width=10, command=next_data)
btn_next.grid(row=1, column=1, padx=10)

# Create QR Button
btn_create_qr = Button(Form, text="Create QR", width=20, command=create_qr)
btn_create_qr.grid(row=2, columnspan=2, pady=10)

# QR Result Display
lbl_qr_result = Label(root, textvariable=qr_result, font=('arial', 12), wraplength=350)
lbl_qr_result.pack(pady=20)

if __name__ == '__main__':
    load_data()
    root.mainloop()