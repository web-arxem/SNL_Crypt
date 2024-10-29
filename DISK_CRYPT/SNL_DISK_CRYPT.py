import os
import time
import numpy as np
from PIL import Image
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox, scrolledtext

def run_disk_operation(operation):
    """Запускает соответствующую операцию шифрования или дешифрования."""
    operation_name = "шифрования" if operation == 'encrypt' else "дешифрования"

    # Запуск соответствующей программы
    exe_file = 'DISK_CRYPT\\D_CRYPT.py' if operation == 'encrypt' else 'DISK_CRYPT\\D_DECRYPT.py'
    subprocess.run([exe_file], shell=True)

def create_interface():
    """Создает графический интерфейс приложения."""
    # Основное окно
    root = tk.Tk()
    root.title("SNL Disk Crypt")
    root.geometry("500x300")
    #Установка иконки окна
    root.iconbitmap("IMG\\logo_2.ico")

    # Заголовок
    title_label = tk.Label(root, text="SNL Disk Crypt", font=("Arial", 24))
    title_label.pack(pady=10)

    # Кнопки для шифрования и дешифрования
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    encrypt_button = tk.Button(button_frame, text="Шифровать диск", font=("Arial", 14), command=lambda: run_disk_operation('encrypt'))
    encrypt_button.pack(side=tk.LEFT, padx=10)

    decrypt_button = tk.Button(button_frame, text="Дешифровать диск", font=("Arial", 14), command=lambda: run_disk_operation('decrypt'))
    decrypt_button.pack(side=tk.LEFT, padx=10)

    exit_button = tk.Button(button_frame, text="Выход", font=("Arial", 14), command=root.quit)
    exit_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_interface()
