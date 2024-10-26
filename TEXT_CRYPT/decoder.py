from Crypto.Cipher import AES
import base64
import tkinter as tk
import os
import hashlib
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

# Создаем диалоговое окно для выбора файла
root = tk.Tk()
root.withdraw()

# Ввод зашифрованного текста и ключа для дешифрования
encrypted_text = input("Введите зашифрованный текст для дешифровки: ")
key1_input_b64 = input("Введите ключ шифрования для дешифровки (введите ключ в base64): ")
key1_input = base64.b64decode(key1_input_b64)

# Ввод пароля для генерации ключа
password = input("Введите пароль для генерации второго ключа: ")
key1_generated = hashlib.sha256(password.encode()).digest()

# Проверка соответствия первого ключа
if key1_input != key1_generated:
    print("Ошибка: неверный пароль!")
else:
    # Ввод второго ключа
    key2_input_b64 = input("Введите второй ключ шифрования для дешифровки (введите ключ в base64): ")
    key2_input = base64.b64decode(key2_input_b64)

    # Расшифровываем текст
    try:
        decrypted_text_level1 = decrypt_text(key2_input, encrypted_text)
        decrypted_text = decrypt_text(key1_input, decrypted_text_level1)
        print("Расшифрованный текст:", decrypted_text)
    except Exception as e:
        print("Ошибка расшифровки:", str(e))
        exit()

    # Вопрос о сохранении расшифрованного текста
    save_file = input("Хотите сохранить расшифрованный текст в файл? (да/нет): ").strip().lower()
    
    if save_file == 'да':
        # Открываем диалоговое окно для выбора пути сохранения файла .snldecrypt
        save_path = filedialog.asksaveasfilename(defaultextension='.snldecrypt', filetypes=[("SNL Decrypt Files", "*.snldecrypt")])
        
        # Проверка, что пользователь выбрал путь сохранения файла
        if save_path:  # Проверяем, что путь сохранения был выбран
            # Записываем результат в выбранный файл
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(f'Расшифрованный текст: {decrypted_text}')
            print(f'Данные сохранены в файле: {save_path}')
        else:
            print("Сохранение файла отменено.")
    else:
        print("Файл не сохранен.")

# Добавляем ожидание нажатия клавиши Enter перед завершением программы
input("Нажмите Enter для завершения программы...")
os.system("cls")
subprocess.run("snl_crypt.exe", shell=True)
