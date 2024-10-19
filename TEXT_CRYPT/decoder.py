from Crypto.Cipher import AES
import base64
import tkinter as tk
from tkinter import filedialog
import os
import subprocess

# Определение функции для расшифрования текста
def decrypt_text(key, ciphertext):
    data = base64.b64decode(ciphertext.encode())
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_text.decode()

# Открыть диалоговое окно для выбора пути сохранения файла
root = tk.Tk()
root.withdraw()

file_path = filedialog.asksaveasfilename(defaultextension='.snldecrypt', filetypes=[('SNLDecrypt files', '*.snldecrypt')])

# Проверка, что пользователь выбрал путь сохранения файла
if file_path:
    # Ввод зашифрованного текста и ключа для дешифрования
    encrypted_text = input("Введите зашифрованный текст для дешифровки: ")
    key = input("Введите ключ шифрования для дешифровки (введите ключ в base64): ")
    key = base64.b64decode(key)

    # Расшифровываем текст и выводим результат
    decrypted_text = decrypt_text(key, encrypted_text)
    print("Расшифрованный текст:", decrypted_text)

    # Записать результат в выбранный файл
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'Расшифрованный текст: {decrypted_text}')

    print(f'Данные сохранены в файле: {file_path}')
else:
    print('Путь сохранения файла не выбран')

# Добавляем ожидание нажатия клавиши Enter перед завершением программы
input("Нажмите Enter для завершения программы...")


# Чтение зашифрованного текста и ключа из файла
encrypted_text, key_b64 = read_from_file(file_path)

# Декодирование ключа из формата base64
key = base64.b64decode(key_b64)

# Расшифровываем текст и выводим результат
decrypted_text = decrypt_text(key, encrypted_text)
print("Расшифрованный текст:", decrypted_text)

# Добавляем ожидание нажатия клавиши Enter перед завершением программы
os.system("cls")
subprocess.run("snl_crypt.exe", shell=True)
