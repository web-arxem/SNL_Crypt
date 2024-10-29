import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import requests

# Основное окно с интерфейсом tkinter
root = tk.Tk()
root.title("SNL_Crypt")
root.geometry("1280x720")

# Установка иконки окна
root.iconbitmap("IMG\\logo.ico")  # Укажите путь к иконке .ico

# Текущая версия программы
current_version = "SNL_Crypt_V6"

# URL для проверки обновлений
GITHUB_REPO = "https://api.github.com/repos/web-arxem/SNL_Crypt/releases/latest"

def run_program(program_name, message):
    messagebox.showinfo("Запуск", f"{message}")
    subprocess.run([program_name], shell=True)

def download_file(url, dest):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(dest, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            downloaded_size += len(data)
            file.write(data)
            progress_var.set(downloaded_size)
            progress_bar['maximum'] = total_size
            root.update_idletasks()  # Обновление интерфейса

def check_updates():
    try:
        response = requests.get(GITHUB_REPO)
        response.raise_for_status()  # Проверяем успешность запроса
        latest_release = response.json()
        new_version = latest_release['tag_name']
        download_url = latest_release['assets'][0]['browser_download_url']  # Ссылка на файл

        if new_version != current_version:
            messagebox.showinfo("Доступно обновление", "Ваша версия программы не позволяет правильно загрузить обновление.\nВы можете его загрузить на Github")
            
        else:
            messagebox.showinfo("Обновление", "Вы находитесь на последней версии.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Не удалось проверить обновления: {e}")

# Интерфейс
for i in range(2):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Создание верхнего левого фрейма (Шифровщик, Дешифровщик, Авто дешифровщик)
left_top_frame = tk.Frame(root, bg="white")
left_top_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

label_top_left = tk.Label(left_top_frame, text="Текст", font=("Arial", 20))
label_top_left.pack(pady=20)

button_encrypt = tk.Button(left_top_frame, text="Шифровщик", font=("Arial", 14),
                           command=lambda: run_program('TEXT_CRYPT\\coder.py', "Запуск программы шифрования"))
button_encrypt.pack(pady=10)

button_decrypt = tk.Button(left_top_frame, text="Дешифровщик", font=("Arial", 14),
                           command=lambda: run_program('TEXT_CRYPT\\decoder.py', "Запуск программы дешифрования"))
button_decrypt.pack(pady=10)

button_auto_decrypt = tk.Button(left_top_frame, text="Авто дешифровщик", font=("Arial", 14),
                                command=lambda: run_program('TEXT_CRYPT\\auto_decoder.py', "Запуск программы авто-дешифрования"))
button_auto_decrypt.pack(pady=10)

# Создание верхнего правого фрейма (Файлы)
right_top_frame = tk.Frame(root, bg="white")
right_top_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

label_top_right = tk.Label(right_top_frame, text="Файлы", font=("Arial", 20))
label_top_right.pack(pady=20)

button_file_encrypt = tk.Button(right_top_frame, text="Шифровщик-дешифровщик файлов", font=("Arial", 14),
                                command=lambda: run_program('FILE_CRYPT\\file_c.py', "Запуск программы шифрования-дешифрования файлов"))
button_file_encrypt.pack(pady=10)

# Создание нижнего левого фрейма (Диски)
left_bottom_frame = tk.Frame(root, bg="white")
left_bottom_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

label_bottom_left = tk.Label(left_bottom_frame, text="Диски", font=("Arial", 20))
label_bottom_left.pack(pady=20)

button_disk_encrypt = tk.Button(left_bottom_frame, text="Шифровщик-дешифровщик дисков", font=("Arial", 14),
                                command=lambda: run_program('DISK_CRYPT\\SNL_DISK_CRYPT.py', "Запуск программы шифрования-дешифрования диска"))
button_disk_encrypt.pack(pady=10)

# Создание нижнего правого фрейма (Версия программы)
right_bottom_frame = tk.Frame(root, bg="white")
right_bottom_frame.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)

version_label = tk.Label(right_bottom_frame, text=f"Текущая версия: {current_version}", font=("Arial", 12), fg="grey")
version_label.pack(pady=20)
version_label.bind("<Button-1>", lambda e: check_updates())  # Проверка обновлений при нажатии

# Логотип в левом нижнем углу
logo_img = Image.open("IMG\\logo.png")  # Укажите путь к логотипу .png
logo_img = logo_img.resize((60, 60), Image.LANCZOS)  # Изменение размера до 60x60
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(left_bottom_frame, image=logo_photo)
logo_label.pack(side='bottom', anchor='sw', padx=10, pady=10)

root.mainloop()
