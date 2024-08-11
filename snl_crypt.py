import subprocess
import os

print("Выберите, что запустить:")
print("1. шифровщик")
print("2. дешифровщик")
print("3. авто дешифровщик")
print("4. шифровщик-дешифровщик файлов")
#print("")
#print("0. выход")

choice = input("Введите номер для запуска: ")

if choice == "1":
    os.system("cls")
    subprocess.run("coder.exe", shell=True)
elif choice == "2":
    os.system("cls")
    subprocess.run("decoder.exe", shell=True)
elif choice == "3":
    os.system("cls")
    subprocess.run("auto_decoder.exe", shell=True)
elif choice == "4":
    os.system("cls")
    subprocess.run("file_c.exe", shell=True)
elif choice == "0":
    os.system("exit")
else:
    print("Ошибка. Пожалуйста, введите 1, 2, 3 или 4 для выбора.")
