from Crypto.Cipher import AES
import base64
import tkinter as tk
from tkinter import messagebox
import hashlib

# Функция для расшифрования текста
def decrypt_text(key, ciphertext):
    data = base64.b64decode(ciphertext)
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_text.decode()

# Генерация ключа на основе пользовательского пароля
def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

# Функция для ручного дешифрования
def manual_decrypt():
    encrypted_text_level2 = entry_encrypted_text.get("1.0", tk.END).strip()
    password = entry_password.get()
    key2_input = entry_key2.get()

    if not encrypted_text_level2 or not password or not key2_input:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля!")
        return

    try:
        # Декодируем второй ключ из Base64
        key2 = base64.b64decode(key2_input)

        # Генерируем первый ключ на основе пароля
        key1 = generate_key(password)

        # Дешифруем текст: сначала вторым, затем первым ключом
        decrypted_text_level1 = decrypt_text(key2, encrypted_text_level2)
        decrypted_text = decrypt_text(key1, decrypted_text_level1)

        # Выводим расшифрованный текст в поле результата
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, decrypted_text)
        messagebox.showinfo("Успешно", "Текст успешно расшифрован!")
        
    except Exception as e:
        messagebox.showerror("Ошибка", "Не удалось расшифровать текст. Проверьте данные и попробуйте снова.")

# Создание окна
root = tk.Tk()
root.title("SNLCrypt Дешифровка")
root.geometry("600x400")
# Установка иконки окна
root.iconbitmap("IMG\\logo.ico")

# Поля для ввода зашифрованного текста, пароля и второго ключа
tk.Label(root, text="Введите зашифрованный текст (Base64):").pack()
entry_encrypted_text = tk.Text(root, height=5, width=60)
entry_encrypted_text.pack(pady=5)

tk.Label(root, text="Введите пароль для дешифровки:").pack()
entry_password = tk.Entry(root, show="*", width=60)
entry_password.pack(pady=5)

tk.Label(root, text="Введите второй ключ (Base64):").pack()
entry_key2 = tk.Entry(root, width=60)
entry_key2.pack(pady=5)

# Кнопка для расшифрования
decrypt_button = tk.Button(root, text="Расшифровать", command=manual_decrypt)
decrypt_button.pack(pady=10)

# Поле для отображения результата
tk.Label(root, text="Расшифрованный текст:").pack()
result_text = tk.Text(root, height=5, width=60)
result_text.pack(pady=5)

# Запуск основного цикла
root.mainloop()
