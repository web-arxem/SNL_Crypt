import runpy
import traceback
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Перезапустить этот скрипт с правами администратора
    print("Перезапуск с правами администратора...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

def run_with_error_handling(file_path):
    try:
        runpy.run_path(file_path)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        last_trace = tb[-1]  # Получаем последнюю строку стека
        error_line = last_trace.lineno
        print(f"Ошибка в файле '{file_path}' на строке {error_line}: {e}")

if __name__ == "__main__":
    file_path = input("Введите путь к файлу .py, который нужно запустить: ")
    run_with_error_handling(file_path)
