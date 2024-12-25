import json
import os
from virtual_shell import VirtualShell
from gui import create_gui

# Загрузить конфигурацию из файла
with open('config.json', 'r') as f:
    config = json.load(f)

fs_path = config['filesystem_path']
log_path = config['log_file_path']

# Проверка, что файл существует
if not os.path.exists(fs_path):
    print(f"Error: The tar file '{fs_path}' does not exist.")
else:
    print(f"Tar file '{fs_path}' found. Proceeding with execution.")

# Инициализировать виртуальный шелл
shell = VirtualShell(fs_path, log_path)

# Запустить GUI
create_gui(shell)