from Crypto.Cipher import AES
import base64
import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Ваш код, который требует прав администратора
    pass
else:
    # Перезапуск программы с правами администратора
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# Ваш основной код программы
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

# Путь к файлу
file_path = 'C:\\encryption.snlcrypt'

# Чтение зашифрованного текста и ключа из файла
encrypted_text, key_b64 = read_from_file(file_path)

# Декодирование ключа из формата base64
key = base64.b64decode(key_b64)

# Расшифровываем текст и выводим результат
decrypted_text = decrypt_text(key, encrypted_text)
print("Расшифрованный текст:", decrypted_text)

# Добавляем ожидание нажатия клавиши Enter перед завершением программы
input("Нажмите Enter для завершения программы...")
