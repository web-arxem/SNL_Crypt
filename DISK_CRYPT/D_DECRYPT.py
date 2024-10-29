import os
import base64
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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

    decrypted_log_data = decrypt_with_password(encrypted_log_data, password)
    log_entries = decrypted_log_data.decode().split('\n')

    file_keys = {}
    for entry in log_entries:
        if entry.strip():
            file_path, key_hex = entry.split(', ')
            file_keys[file_path] = bytes.fromhex(key_hex)

    return file_keys

def process_files(file_keys, output_text, progress_bar, current_file_label):
    total_files = len(file_keys)
    start_time = datetime.now()

    for index, (file_path, encryption_key) in enumerate(file_keys.items()):
        current_file_label.config(text=f"Дешифровка: {file_path}")  # Обновляем метку с текущим файлом

        try:
            with open(file_path + '.SDE', 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = double_aes_decrypt(encrypted_data, encryption_key)
            decoded_data = double_base64_decode(decrypted_data)

            with open(file_path, 'wb') as f:
                f.write(decoded_data)

            os.remove(file_path + '.SDE')

        except (PermissionError, OSError) as e:
            output_text.insert(tk.END, f"Ошибка доступа к файлу {file_path}: {e}\n")

        # Обновление прогресс-бара
        progress_bar['value'] = (index + 1) / total_files * 100
        elapsed_time = datetime.now() - start_time
        remaining_time = elapsed_time / (index + 1) * (total_files - (index + 1))
        output_text.insert(tk.END, f"Осталось времени: {str(remaining_time).split('.')[0]}\n")

    output_text.insert(tk.END, "Дешифрование завершено.\n")

def run_decryption(log_file_path, password):
    progress_window = tk.Toplevel()
    progress_window.title("Дешифровка в процессе")
    progress_window.geometry("400x200")

    current_file_label = tk.Label(progress_window, text="", font=("Arial", 12))
    current_file_label.pack(pady=5)

    progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack(pady=10)

    output_text = tk.Text(progress_window, wrap=tk.WORD, height=5)
    output_text.pack(pady=5)

    file_keys = read_log_file(log_file_path, password)
    process_files(file_keys, output_text, progress_bar, current_file_label)

    # Удаление лог-файла после успешной расшифровки
    try:
        os.remove(log_file_path)
        output_text.insert(tk.END, f"Лог-файл {log_file_path} успешно удален.\n")
    except OSError as e:
        output_text.insert(tk.END, f"Ошибка при удалении лог-файла: {e}\n")

def create_interface():
    root = tk.Tk()
    root.title("Дешифратор файлов")
    root.geometry("400x200")
    # Установка иконки окна
    root.iconbitmap("IMG\\logo_2.ico")

    # Выбор лог-файла
    log_file_path = filedialog.askopenfilename(title="Выберите лог-файл")

    # Ввод пароля
    password_label = tk.Label(root, text="Введите пароль для лог-файла:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(root, show='*', font=("Arial", 14))
    password_entry.pack(pady=5)

    # Кнопка для запуска расшифровки
    decrypt_button = tk.Button(root, text="Запустить дешифровку", font=("Arial", 14),
                                command=lambda: run_decryption(log_file_path, password_entry.get()))
    decrypt_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_interface()
