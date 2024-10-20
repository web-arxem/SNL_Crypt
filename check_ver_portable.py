import requests
import os
from tqdm import tqdm  # Прогресс-бар для удобного отслеживания прогресса
import time
import subprocess

def check_new_version(repo_owner, repo_name, current_version):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        latest_release = response.json()
        latest_version = latest_release["tag_name"]
        
        if latest_version != current_version:
            print(f"Доступна новая версия: {latest_version}")
            user_input = input("Хотите загрузить и установить новую версию? (да/нет): ").strip().lower()
            
            if user_input in ["да", "yes"]:
                # Ищем файл SNL_Crypt.exe среди файлов в "Assets"
                download_url = find_asset_url(latest_release, "SNL_Crypt.exe")
                
                if download_url:
                    download_and_install(download_url)
                else:
                    print("Не удалось найти файл SNL_Crypt.exe в последнем релизе.")
        else:
            print("Вы используете последнюю версию.")
            time.sleep(2)
            os.system("cls")
            subprocess.run(['snl_crypt.py'], shell=True)
    else:
        print("Не удалось получить информацию о последнем релизе.")

def find_asset_url(latest_release, target_filename):
    # Ищем в assets нужный файл
    for asset in latest_release.get("assets", []):
        if asset["name"] == target_filename:
            return asset["browser_download_url"]
    return None

def download_and_install(download_url):
    # Определяем путь для загрузки
    local_filename = download_url.split("/")[-1]
    
    # Получаем размер файла
    response = requests.head(download_url)
    file_size = int(response.headers.get('Content-Length', 0))
    
    # Скачиваем установочный файл с отображением прогресса
    print(f"Загружаю {local_filename} ...")
    
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            # Создаем прогресс-бар с помощью tqdm
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=local_filename, ncols=100) as progress_bar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # Фильтруем пустые куски данных
                        f.write(chunk)
                        progress_bar.update(len(chunk))  # Обновляем прогресс-бар
    
    print(f"Файл {local_filename} успешно загружен.")
    
    # Запускаем установщик
    print("Запускаю установщик...")
    os.startfile(local_filename)  # Запускает установочный файл на Windows

# Пример использования
check_new_version("web-arxem", "SNL_Crypt", "SNL_Crypt_V4_1")
