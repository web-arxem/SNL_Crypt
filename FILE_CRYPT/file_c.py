import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import ctypes
import sys

# Генерация и сохранение ключа
def generate_and_save_key():
    key = get_random_bytes(32)  # AES-256 требует ключ длиной 32 байта
    with open("FILE_CRYPT\\file_c.dll", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Информация", "Ключ сгенерирован и сохранён в папку программы под названием file_c.dll")

# Загрузка ключа из файла
def load_key():
    try:
        with open("FILE_CRYPT\\file_c.dll", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл с ключом не найден. Проверьте, существует ли файл file_c.dll")
        exit(1)

# Шифрование файла
def encrypt_file(filename):
    key = load_key()
    cipher = AES.new(key, AES.MODE_CBC)  # Используем режим CBC

    with open(filename, "rb") as file:
        file_data = file.read()

    # Добавление паддинга и шифрование данных
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))

    # Конкатенируем вектор и зашифрованные данные
    with open(filename, "wb") as file:
        file.write(cipher.iv + encrypted_data)  # Сохраняем IV перед зашифрованными данными
    messagebox.showinfo("Успех", f"Файл {os.path.basename(filename)} зашифрован.")

# Дешифрование файла
def decrypt_file(filename):
    key = load_key()

    with open(filename, "rb") as file:
        iv = file.read(16)  # Первый 16 байт - вектор инициализации
        encrypted_data = file.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)  # Инициализация с IV
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    with open(filename, "wb") as file:
        file.write(decrypted_data)
    messagebox.showinfo("Успех", f"Файл {os.path.basename(filename)} расшифрован.")

# Открытие диалогового окна для выбора файла
def browse_file():
    return filedialog.askopenfilename()

# Проверка прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Основная логика программы
def run_program():
    # Проверяем наличие ключа, если он не существует, генерируем его
    if not os.path.exists("FILE_CRYPT\\file_c.dll"):
        if not is_admin():
            # Перезапустить этот скрипт с правами администратора
            messagebox.showinfo("Информация", "Перезапуск с правами администратора...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()
        generate_and_save_key()

    # Создание главного окна
    window = tk.Tk()
    window.title("Шифрование и расшифрование файлов")
    window.geometry("400x200")
    window.iconbitmap("IMG\\logo.ico")

    # Кнопка для шифрования
    btn_encrypt = tk.Button(window, text="Зашифровать файл", command=lambda: encrypt_file(browse_file()))
    btn_encrypt.pack(pady=10)

    # Кнопка для расшифрования
    btn_decrypt = tk.Button(window, text="Расшифровать файл", command=lambda: decrypt_file(browse_file()))
    btn_decrypt.pack(pady=10)

    # Кнопка выхода
    btn_exit = tk.Button(window, text="Выход", command=window.quit)
    btn_exit.pack(pady=10)

    # Запуск интерфейса
    window.mainloop()

# Запуск программы
if __name__ == "__main__":
    run_program()
