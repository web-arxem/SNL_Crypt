from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib

# Функции для шифрования и расшифрования
def encrypt_text(key, text):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_text(key, ciphertext):
    data = base64.b64decode(ciphertext.encode())
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_text.decode()

# Генерация ключа на основе пользовательского пароля
def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

# Функция для записи данных в файл
def write_to_file(file_path, encrypted_data, key2):
    with open(file_path, 'w') as file:
        file.write(f'{encrypted_data}\n')
        file.write(base64.b64encode(key2).decode() + '\n')

# Функция для шифрования
def encrypt_and_save():
    text = entry_text.get("1.0", tk.END).strip()
    password = entry_password.get()
    
    if not text or not password:
        messagebox.showerror("Ошибка", "Введите текст и пароль!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension='.snlcrypt', filetypes=[('SNLCrypt files', '*.snlcrypt')])
    if not file_path:
        return
    
    # Генерация ключей: первый ключ на основе пароля, второй ключ случайный
    key1 = generate_key(password)
    key2 = get_random_bytes(32)
    
    encrypted_text_level1 = encrypt_text(key1, text)
    encrypted_text_level2 = encrypt_text(key2, encrypted_text_level1)
    
    # Проверка прав доступа и сохранение данных
    if os.access(os.path.dirname(file_path), os.W_OK):
        write_to_file(file_path, encrypted_text_level2, key2)
        messagebox.showinfo("Успешно", f"Файл успешно сохранен: {file_path}")
    else:
        messagebox.showerror("Ошибка", "Нет прав на запись в выбранную директорию.")

# Создание окна
root = tk.Tk()
root.title("SNLCrypt Шифрование")
root.geometry("500x400")
# Установка иконки окна
root.iconbitmap("IMG\\logo.ico")

# Поле для ввода текста
tk.Label(root, text="Введите текст для шифрования:").pack()
entry_text = tk.Text(root, height=5, width=50)
entry_text.pack()

# Поле для ввода пароля
tk.Label(root, text="Введите пароль для шифрования:").pack()
entry_password = tk.Entry(root, show="*", width=50)
entry_password.pack()

# Кнопка для шифрования и сохранения файла
encrypt_button = tk.Button(root, text="Зашифровать и сохранить", command=encrypt_and_save)
encrypt_button.pack(pady=10)

# Запуск основного цикла
root.mainloop()
