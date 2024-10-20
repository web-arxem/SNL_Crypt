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
    os.system("cls")
    print("Выберите, что запустить:")
    print("1. Шифровщик")
    print("2. Дешифровщик")
    print("3. Авто дешифровщик")
    print("4. Шифровщик-дешифровщик файлов")
    print("5. Шифровщик-дешифровщик дисков")
    print("9. Проверить обновления программы")
    #print("")
    #print("0. выход")

    choice = input("Введите номер для запуска: ")

    if choice == "1":
        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        # Вывод ASCII-арта сразу после выбора действия
        ascii_art = image_to_ascii(image_path)
        centered_art = center_text(ascii_art)
        print(centered_art)

        print(f"\nЗапуск программы шифрования.")
        time.sleep(4)  # Задержка перед запуском

        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        subprocess.run(['TEXT_CRYPT\\coder.exe'], shell=True)  # Запуск выбранного файла
    elif choice == "2":
        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        # Вывод ASCII-арта сразу после выбора действия
        ascii_art = image_to_ascii(image_path)
        centered_art = center_text(ascii_art)
        print(centered_art)

        print(f"\nЗапуск программы дешифрования")
        time.sleep(4)  # Задержка перед запуском

        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        subprocess.run(['TEXT_CRYPT\\decoder.exe'], shell=True)  # Запуск выбранного файла
    elif choice == "3":
        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        # Вывод ASCII-арта сразу после выбора действия
        ascii_art = image_to_ascii(image_path)
        centered_art = center_text(ascii_art)
        print(centered_art)

        print(f"\nЗапуск программы авто-дешифрования")
        time.sleep(4)  # Задержка перед запуском

        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        subprocess.run(['TEXT_CRYPT\\auto_decoder.exe'], shell=True)  # Запуск выбранного файла
    elif choice == "4":
        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        # Вывод ASCII-арта сразу после выбора действия
        ascii_art = image_to_ascii(image_path)
        centered_art = center_text(ascii_art)
        print(centered_art)

        print(f"\nЗапуск программы шифрования-дешифрования файлов")
        time.sleep(4)  # Задержка перед запуском

        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        subprocess.run(['FILE_CRYPT\\file_c.exe'], shell=True)  # Запуск выбранного файла
    elif choice == "5":
        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        # Вывод ASCII-арта сразу после выбора действия
        ascii_art = image_to_ascii(image_path)
        centered_art = center_text(ascii_art)
        print(centered_art)

        print(f"\nЗапуск программы шифрования-дешифрования диска")
        time.sleep(4)  # Задержка перед запуском

        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        subprocess.run(['DISK_CRYPT\\SNL_DISK_CRYPT.exe'], shell=True)  # Запуск выбранного файла
    
    elif choice == "9":
        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        # Вывод ASCII-арта сразу после выбора действия
        ascii_art = image_to_ascii(image_path)
        centered_art = center_text(ascii_art)
        print(centered_art)

        print(f"\nЗапуск проверки обновлений")
        time.sleep(4)  # Задержка перед запуском

        if platform.system() == "Windows": # Определение системы и ввод команды очистки
            os.system("cls")
        else:
            os.system("clear")
        subprocess.run(['check_ver.exe'], shell=True)  # Запуск выбранного файла
    elif choice == "Crypt":
        #subprocess.run(['FILE_CRYPT\\fiIe_c.exe'], shell=True)
if __name__ == "__main__":
    image_path = 'IMG\\SNL_CRYPT.png'  # Выбор изображения
    main(image_path)
