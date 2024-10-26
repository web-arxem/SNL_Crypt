from Crypto.Cipher import AES
import base64
import tkinter as tk
from tkinter import filedialog
import os
import hashlib
import subprocess

# Функция для расшифрования текста
def decrypt_text(key, ciphertext):
    data = base64.b64decode(ciphertext.encode())
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_text.decode()  # вернем расшифрованный текст в виде строки

# Функция для чтения данных из файла
def read_from_file(file_path):
    with open(file_path, 'r') as file:
        encrypted_data = file.readline().strip()
        encryption_keys = [file.readline().strip(), file.readline().strip()]  # Читаем оба ключа
    return encrypted_data, encryption_keys

# Создаем диалоговое окно для выбора файла
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(defaultextension='.snlcrypt', filetypes=[('SNLCrypt files', '*.snlcrypt')])

# Чтение зашифрованного текста и ключей из файла
encrypted_text, keys_b64 = read_from_file(file_path)

# Декодирование ключей из формата base64
key1 = base64.b64decode(keys_b64[0])
key2 = base64.b64decode(keys_b64[1])

# Ввод пароля для расшифрования
password = input("Введите пароль для расшифрования: ")

# Генерируем ключ на основе пароля
key1_input = hashlib.sha256(password.encode()).digest()

# Проверка соответствия ключа
if key1 != key1_input:
    print("Ошибка: неверный пароль!")
else:
    # Расшифровываем текст в обратном порядке
    decrypted_text_level1 = decrypt_text(key2, encrypted_text)
    decrypted_text = decrypt_text(key1, decrypted_text_level1)
    print("Расшифрованный текст:", decrypted_text)

    # Вопрос о сохранении расшифрованного текста
    save_file = input("Хотите сохранить расшифрованный текст в файл? (да/нет): ").strip().lower()
    
    if save_file == 'да':
        # Диалоговое окно для выбора пути сохранения файла .snldecrypt
        save_path = filedialog.asksaveasfilename(defaultextension=".snldecrypt", filetypes=[("SNL Decrypt Files", "*.snldecrypt")])
        
        # Сохраняем расшифрованный текст в файл .snldecrypt
        if save_path:  # Проверяем, что путь сохранения был выбран
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(f'Расшифрованный текст: {decrypted_text}')
            print("Файл успешно сохранен.")
        else:
            print("Сохранение файла отменено.")
    else:
        print("Файл не сохранен.")

input("Нажмите Enter для завершения ...")
os.system("cls")
subprocess.run("snl_crypt.exe", shell=True)
