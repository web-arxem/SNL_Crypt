from Crypto.Cipher import AES
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib

# Функция для расшифрования текста
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

# Функция для автоматического дешифрования
def auto_decrypt():
    file_path = filedialog.askopenfilename(defaultextension='.snlcrypt', filetypes=[('SNLCrypt files', '*.snlcrypt')])
    if not file_path:
        return
    
    password = entry_password.get()
    if not password:
        messagebox.showerror("Ошибка", "Введите пароль для дешифровки!")
        return

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            encrypted_text_level2 = lines[0].strip()
            key2 = base64.b64decode(lines[1].strip())

        # Создаем ключ дешифровки на основе пароля
        key1 = generate_key(password)
        
        # Расшифровываем сначала вторым, затем первым ключом
        decrypted_text_level1 = decrypt_text(key2, encrypted_text_level2)
        decrypted_text = decrypt_text(key1, decrypted_text_level1)

        # Успешное сообщение с запросом на сохранение
        save = messagebox.askyesno("Успешно", "Расшифровка завершена. Хотите сохранить результат в файл?")
        
        if save:
            save_path = filedialog.asksaveasfilename(defaultextension='.snldecrypt', filetypes=[('SNL_Crypt files', '*.snldecrypt')])
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(decrypted_text)
                messagebox.showinfo("Сохранено", f"Файл успешно сохранён: {save_path}")
        else:
            messagebox.showinfo("Информация", "Расшифрованный текст не был сохранён.")
            
    except Exception as e:
        messagebox.showerror("Ошибка", "Не удалось расшифровать файл. Проверьте пароль и попробуйте снова.")

# Создание окна
root = tk.Tk()
root.title("SNLCrypt Авто-Дешифровка")
root.geometry("500x200")
# Установка иконки окна
root.iconbitmap("IMG\\logo.ico")

# Поле для ввода пароля
tk.Label(root, text="Введите пароль для дешифровки:").pack()
entry_password = tk.Entry(root, show="*", width=50)
entry_password.pack(pady=10)

# Кнопка для расшифрования
decrypt_button = tk.Button(root, text="Загрузить и расшифровать", command=auto_decrypt)
decrypt_button.pack(pady=20)

# Запуск основного цикла
root.mainloop()
