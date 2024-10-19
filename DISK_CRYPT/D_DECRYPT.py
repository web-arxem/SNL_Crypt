import os
import base64
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

def double_base64_decode(data):
    first_decoded = base64.b64decode(data)
    second_decoded = base64.b64decode(first_decoded)
    return second_decoded

def double_aes_decrypt(data, key):
    iv1 = data[:AES.block_size]
    iv2_ciphertext = data[AES.block_size:]

    iv2 = iv2_ciphertext[:AES.block_size]
    ciphertext2 = iv2_ciphertext[AES.block_size:]

    cipher2 = AES.new(key, AES.MODE_CBC, iv=iv2)
    decrypted_ciphertext1 = unpad(cipher2.decrypt(ciphertext2), AES.block_size)

    cipher1 = AES.new(key, AES.MODE_CBC, iv=iv1)
    original_data = unpad(cipher1.decrypt(decrypted_ciphertext1), AES.block_size)

    return original_data

def decrypt_with_password(data, password):
    salt = data[:16]
    ciphertext = data[16:]
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    iv = ciphertext[:AES.block_size]
    encrypted_data = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(encrypted_data), AES.block_size)

def read_log_file(log_file_path, password):
    with open(log_file_path, 'rb') as f:
        encrypted_log_data = f.read()

    print("Расшифровка лог-файла...")
    decrypted_log_data = decrypt_with_password(encrypted_log_data, password)

    log_entries = decrypted_log_data.decode().split('\n')

    file_keys = {}
    for entry in tqdm(log_entries, desc="Чтение лог-файла"):
        if entry.strip():
            file_path, key_hex = entry.split(', ')
            file_keys[file_path] = bytes.fromhex(key_hex)

    return file_keys

def process_files(file_keys):
    total_files = len(file_keys)

    start_time = datetime.now()

    with tqdm(total=total_files, desc="Дешифрование файлов") as pbar:
        for file_path, encryption_key in file_keys.items():
            try:
                with open(file_path + '.SDE', 'rb') as f:
                    encrypted_data = f.read()

                decrypted_data = double_aes_decrypt(encrypted_data, encryption_key)
                decoded_data = double_base64_decode(decrypted_data)

                with open(file_path, 'wb') as f:
                    f.write(decoded_data)

                os.remove(file_path + '.SDE')

            except (PermissionError, OSError) as e:
                print(f"Ошибка доступа к файлу {file_path}: {e}")

            pbar.update(1)
            elapsed_time = datetime.now() - start_time
            remaining_time = elapsed_time / (pbar.n + 1) * (total_files - pbar.n + 1)
            pbar.set_postfix(ETA=str(remaining_time).split('.')[0])

    print("Дешифрование завершено.")

# Пример использования
root = tk.Tk()
root.withdraw()  # Скрыть главное окно

log_file_path = filedialog.askopenfilename(title="Выберите лог-файл")
user_password = input("Введите пароль для лог-файла: ")

file_keys = read_log_file(log_file_path, user_password)
process_files(file_keys)

# Удаление лог-файла после успешной расшифровки
try:
    os.remove(log_file_path)
    print(f"Лог-файл {log_file_path} успешно удален.")
except OSError as e:
    print(f"Ошибка при удалении лог-файла: {e}")
