from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os
import tkinter as tk
from tkinter import filedialog
import hashlib
import subprocess

# Открыть диалоговое окно для выбора пути сохранения файла
root = tk.Tk()
root.withdraw()

file_path = filedialog.asksaveasfilename(defaultextension='.snlcrypt', filetypes=[('SNLCrypt files', '*.snlcrypt')])

# Проверка, что пользователь выбрал путь сохранения файла
if file_path:
    # Функция для шифрования текста
    def encrypt_text(key, text):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(text.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    # Функция для расшифрования текста
    def decrypt_text(key, ciphertext):
        data = base64.b64decode(ciphertext.encode())
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_text.decode()  # вернем расшифрованный текст в виде строки

    # Функция для генерации ключа на основе пароля
    def generate_key(password):
        return hashlib.sha256(password.encode()).digest()

    # Функция для записи данных в файл
    def write_to_file(file_path, encrypted_data, encryption_keys):
        with open(file_path, 'w') as file:
            file.write(f'{encrypted_data}\n')
            for key in encryption_keys:
                file.write(f'{key}\n')

    # Ввод текста для шифрования
    text = input("Введите текст для шифрования: ")
    password = input("Введите пароль для шифрования: ")

    # Генерируем ключ на основе пароля
    key1 = generate_key(password)
    key2 = get_random_bytes(32)  # Генерация второго случайного ключа

    # Первый уровень шифрования
    encrypted_text_level1 = encrypt_text(key1, text)

    # Второй уровень шифрования
    encrypted_text_level2 = encrypt_text(key2, encrypted_text_level1)

    # Выводим оба ключа шифрования для дешифровки
    encryption_keys = [base64.b64encode(key1).decode(), base64.b64encode(key2).decode()]
    print("Ключи шифрования для дешифровки:", encryption_keys)

    # Проверяем, есть ли у пользователя права на запись в выбранную директорию
    if os.access(os.path.dirname(file_path), os.W_OK):
        # Записываем зашифрованный текст и ключи в один файл
        write_to_file(file_path, encrypted_text_level2, encryption_keys)
        print(f'Файл успешно сохранен: {file_path}')
    else:
        print("Ошибка: Нет прав на запись в выбранную директорию.")

    # Расшифровываем текст в обратном порядке
    decrypted_text_level1 = decrypt_text(key2, encrypted_text_level2)
    decrypted_text = decrypt_text(key1, decrypted_text_level1)
    print("Расшифрованный текст:", decrypted_text)

    # Добавляем ожидание нажатия клавиши Enter перед завершением программы
    input("Нажмите Enter для завершения программы...")
    os.system("cls")
    subprocess.run("snl_crypt.exe", shell=True)
else:
    print('Путь сохранения файла не выбран')
    os.system("cls")
    subprocess.run("snl_crypt.exe", shell=True)
