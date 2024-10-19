import os
import time
import numpy as np
from PIL import Image
import subprocess
import platform

def image_to_ascii(image_path, width=100):
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # Преобразуем в черно-белое
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width / 2)
        img = img.resize((width, new_height))

        pixels = np.array(img)

        chars = "@%#*+=-:. "
        ascii_image = ""

        for row in pixels:
            for pixel in row:
                index = pixel // 25  
                if index >= len(chars):  
                    index = len(chars) - 1
                ascii_image += chars[index]
            ascii_image += "\n"

        return ascii_image
    except Exception as e:
        return str(e)

def center_text(text):
    """Центрирует текст в консоли."""
    if platform.system() == "Windows":
        columns = os.get_terminal_size()[0]
    else:
        rows, columns = os.popen('stty size', 'r').read().split()
        columns = int(columns)

    lines = text.split('\n')
    centered_text = ""
    
    for line in lines:
        centered_line = line.center(columns)
        centered_text += centered_line + "\n"
    
    return centered_text

def main(image_path):
    while True:
        print("\nВыбор действия:")
        print("1. Запустить шифрование диска")
        print("2. Запустить дешифровку диска")
        print("3. Выход")

        choice = input("Выберите действие (1, 2 или 3): ")

        if choice in {'1', '2'}:
            os.system("cls")
            # Вывод ASCII-арта сразу после выбора действия
            ascii_art = image_to_ascii(image_path)
            centered_art = center_text(ascii_art)
            print(centered_art)

            print(f"\nЗапуск программы {'шифрования' if choice == '1' else 'дешифрования'}...")
            time.sleep(4)  # Задержка перед запуском
            if platform.system() == "Windows": # Определение системы и ввод команды очистки
                os.system("cls")
            else:
                os.system("clear")
            subprocess.run(['DISK_CRYPT\\D_CRYPT.exe' if choice == '1' else 'DISK_CRYPT\\D_DECRYPT.exe'], shell=True)  # Запуск выбранного файла
            break  # Выход из цикла после выполнения
        elif choice == '3':
            print("Выход из программы.")
            
            return  # Выход из функции main
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")

if __name__ == "__main__":
    image_path = 'IMG\\SNL_DISK_CRYPT.png'  # Выбор изображения
    main(image_path)
