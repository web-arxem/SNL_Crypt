from Crypto.Cipher import AES
import base64
import tkinter as tk
from tkinter import filedialog
import os
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
        encryption_key = file.readline().strip()
    return encrypted_data, encryption_key

# Создаем диалоговое окно для выбора файла
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(defaultextension='.snlcrypt', filetypes=[('SNLCrypt files', '*.snlcrypt')])

# Чтение зашифрованного текста и ключа из файла
encrypted_text, key_b64 = read_from_file(file_path)

# Декодирование ключа из формата base64
key = base64.b64decode(key_b64)

# Расшифровываем текст
decrypted_text = decrypt_text(key, encrypted_text)
print("Расшифрованный текст:", decrypted_text)

# Диалоговое окно для выбора пути сохранения файла .snldecrypt
save_path = filedialog.asksaveasfilename(defaultextension=".snldecrypt", filetypes=[("SNL Decrypt Files", "*.snldecrypt")])

# Сохраняем расшифрованный текст и ключ в файл .snldecrypt
with open(save_path, 'w', encoding='utf-8') as file:
    file.write(f'Расшифрованный текст: {decrypted_text}')

print("Файл успешно сохранен.")

input("Нажмите Enter для завершения ...")
os.system("cls")
subprocess.run("snl_crypt.exe", shell=True)