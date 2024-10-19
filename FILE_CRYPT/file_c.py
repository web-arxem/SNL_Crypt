import os
from tkinter import Tk, filedialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import ctypes
import sys
import subprocess
import time

# Генерация и сохранение ключа
def generate_and_save_key():
    key = get_random_bytes(32)  # AES-256 требует ключ длиной 32 байта
    with open("FILE_CRYPT\\file_c.dll", "wb") as key_file:
        key_file.write(key)
    print("Ключ сгенерирован и сохранён в папку программы под названием file_c.dll")
    time.sleep(2)
    ossystem("ggg")

# Загрузка ключа из файла
def load_key():
    try:
        with open("FILE_CRYPT\\file_c.dll", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("Файл с ключом не найден. Проверьте, существует ли файл file_c.dll")
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

# Открытие диалогового окна для выбора файла
def browse_file():
    root = Tk()
    root.withdraw()  # Скрыть главное окно
    filename = filedialog.askopenfilename()  # Выбор файла
    return filename

# Проверка прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Основная логика программы
if __name__ == "__main__":
    # Проверяем наличие ключа, если он не существует, генерируем его
    if not os.path.exists("FILE_CRYPT\\file_c.dll"):
        if not is_admin():
            # Перезапустить этот скрипт с правами администратора
            print("Перезапуск с правами администратора...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()
        generate_and_save_key()

    while True:
        action = input("Выберите действие: 1 - зашифровать, 2 - расшифровать, 0 - выйти: ").lower()
        if action == '1':
            filepath = browse_file()
            if filepath:
                encrypt_file(filepath)
                print(f"Файл {os.path.basename(filepath)} зашифрован.")
        elif action == '2':
            filepath = browse_file()
            if filepath:
                decrypt_file(filepath)
                print(f"Файл {os.path.basename(filepath)} расшифрован.")
        elif action == '0':
            print("Выход из программы.")
            os.system("cls")
            subprocess.run("snl_crypt.exe", shell=True)
            break  # Добавлено для корректного выхода из цикла
        else:
            print("Неверный ввод, попробуйте снова.")
