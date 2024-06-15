from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os
import tkinter as tk
from tkinter import filedialog

# Открыть диалоговое окно для выбора пути сохранения файла
root = tk.Tk()
root.withdraw()

file_path = filedialog.asksaveasfilename(defaultextension='.snlcrypt', filetypes=[('SNLCrypt files', '*.snlcrypt')])

# Проверка, что пользователь выбрал путь сохранения файла
if file_path:
    # Ваш код для обработки шифрования и сохранения файла здесь

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
        return decrypted_text.decode()

    # Функция для записи данных в файл
    def write_to_file(file_path, encrypted_data, encryption_key):
        with open(file_path, 'w') as file:
            file.write(f'{encrypted_data}\n{encryption_key}')

    # Генерируем случайный ключ
    key = get_random_bytes(32)

    # Ввод текста для шифрования
    text = input("Введите текст для шифрования: ")

    # Шифруем текст и выводим результат
    encrypted_text = encrypt_text(key, text)
    print("Зашифрованный текст:", encrypted_text)

    # Выводим ключ шифрования для дешифровки
    encryption_key = base64.b64encode(key).decode()
    print("Ключ шифрования для дешифровки:", encryption_key)

    # Проверяем, есть ли у пользователя права на запись в выбранную директорию
    if os.access(os.path.dirname(file_path), os.W_OK):
        # Записываем зашифрованный текст и ключ в один файл
        write_to_file(file_path, encrypted_text, encryption_key)
        print(f'Файл успешно сохранен: {file_path}')
    else:
        print("Ошибка: Нет прав на запись в выбранную директорию.")

    # Расшифровываем текст и выводим результат
    decrypted_text = decrypt_text(key, encrypted_text)
    print("Расшифрованный текст:", decrypted_text)

    # Добавляем ожидание нажатия клавиши Enter перед завершением программы
    input("Нажмите Enter для завершения программы...")
else:
    print('Путь сохранения файла не выбран')
