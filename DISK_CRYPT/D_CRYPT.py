import os
import base64
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from tqdm import tqdm

def double_base64_encode(data):
    first_encoded = base64.b64encode(data)
    second_encoded = base64.b64encode(first_encoded)
    return second_encoded

def double_aes_encrypt(data, key):
    cipher1 = AES.new(key, AES.MODE_CBC)
    ciphertext1 = cipher1.encrypt(pad(data, AES.block_size))

    cipher2 = AES.new(key, AES.MODE_CBC)
    ciphertext2 = cipher2.iv + cipher2.encrypt(pad(ciphertext1, AES.block_size))
    return cipher1.iv + ciphertext2

def encrypt_with_password(data, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(pad(data, AES.block_size))
    return salt + ciphertext

def get_available_drives():
    drives = []
    for drive in range(ord('C'), ord('Z') + 1):
        drive_letter = f"{chr(drive)}:\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives

def select_drive():
    drives = get_available_drives()
    print("Выберите диск для шифрования:")
    for i, drive in enumerate(drives):
        print(f"{i}: {drive}")
    choice = int(input("Введите номер диска: "))
    return drives[choice]

def process_files(directory, password):
    log_entries = []

    # Подсчет количества файлов
    total_files = sum(len(files) for _, _, files in os.walk(directory))

    start_time = datetime.now()

    with tqdm(total=total_files, desc="Шифрование файлов") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'rb') as f:
                        data = f.read()

                    # Генерация уникального ключа для каждого файла
                    encryption_key = get_random_bytes(32)

                    encoded_data = double_base64_encode(data)
                    encrypted_data = double_aes_encrypt(encoded_data, encryption_key)

                    with open(file_path, 'wb') as f:
                        f.write(encrypted_data)

                    os.rename(file_path, file_path + '.SDE')

                    log_entries.append(f"{file_path}, {encryption_key.hex()}")

                except (PermissionError, OSError) as e:
                    print(f"Ошибка доступа к файлу {file_path}: {e}")

                pbar.update(1)
                elapsed_time = datetime.now() - start_time
                remaining_time = elapsed_time / (pbar.n + 1) * (total_files - pbar.n + 1)
                pbar.set_postfix(ETA=str(remaining_time).split('.')[0])

    log_data = "\n".join(log_entries).encode()
    encrypted_log_data = encrypt_with_password(log_data, password)

    timestamp = datetime.now().strftime("%H %M %S %d %m %Y")
    log_file_name = f"{timestamp}.enc"

    log_file_path = os.path.join(directory, log_file_name)
    with open(log_file_path, 'wb') as f:
        f.write(encrypted_log_data)

    print(f"Лог файл создан и зашифрован: {log_file_path}")

# Пример использования
selected_drive = select_drive()

user_password = input("Введите пароль для лог файла: ")

process_files(selected_drive, user_password)
