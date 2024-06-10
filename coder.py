from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
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

# Путь к файлу в корневой директории диска C
file_path = 'C:\\encryption.snlcrypt'

# Проверяем, есть ли у пользователя права на запись в корневую директорию диска C
if os.access('C:\\', os.W_OK):
    # Записываем зашифрованный текст и ключ в один файл
    write_to_file(file_path, encrypted_text, encryption_key)
    print(f'Файл успешно сохранен: {file_path}')
else:
    print("Ошибка: Нет прав на запись в корневую директорию диска C.")

# Расшифровываем текст и выводим результат
decrypted_text = decrypt_text(key, encrypted_text)
print("Расшифрованный текст:", decrypted_text)

# Добавляем ожидание нажатия клавиши Enter перед завершением программы
input("Нажмите Enter для завершения программы...")
