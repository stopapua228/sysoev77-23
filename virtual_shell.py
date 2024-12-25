import os
import tarfile
import json
import datetime


class VirtualShell:
    def __init__(self, fs_archive, log_path):
        self.current_directory = '/'
        self.log = []
        self.base_path = os.path.join(os.getcwd(), 'temp_extracted')
        self.log_path = log_path

        # Загружать виртуальную файловую систему
        self.load_virtual_fs(fs_archive)

    def load_virtual_fs(self, fs_archive):
        if os.path.exists(self.base_path):
            # Очищаем директорию перед загрузкой
            for root, dirs, files in os.walk(self.base_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        with tarfile.open(fs_archive, 'r') as tar:
            tar.extractall(self.base_path)

    def ls(self):
        path = os.path.join(self.base_path, self.current_directory.lstrip('/'))
        try:
            files = os.listdir(path)
            # Добавим '/' к директориям для вывода
            files = [f + '/' if os.path.isdir(os.path.join(path, f)) else f for f in files]
            self.log_action(f'ls in {self.current_directory}')
            return sorted(files)
        except FileNotFoundError:
            return 'Directory not found'

    def cd(self, new_dir):
        if new_dir.startswith('/'):
            # Абсолютный путь
            potential_path = os.path.join(self.base_path, new_dir.lstrip('/'))
        else:
            # Относительный путь
            potential_path = os.path.join(self.base_path, self.current_directory.lstrip('/'), new_dir)

        if os.path.isdir(potential_path):
            rel_path = os.path.relpath(potential_path, self.base_path)
            self.current_directory = '/' + rel_path.replace(os.path.sep, '/') if rel_path != '.' else '/'
            self.log_action(f'cd to {self.current_directory}')
        else:
            raise FileNotFoundError(f'Directory not found: {new_dir}')

    def pwd(self):
        self.log_action(f'pwd {self.current_directory}')
        return self.current_directory

    def touch(self, filename):
        file_path = os.path.join(self.base_path, self.current_directory.lstrip('/'), filename)
        with open(file_path, 'a'):
            pass
        self.log_action(f'touch {filename} in {self.current_directory}')
        return ''

    def exit(self):
        self.log_action('exit')
        self.save_log()

    def log_action(self, action):
        self.log.append({
            'action': action,
            'timestamp': datetime.datetime.now().isoformat()
        })

    def save_log(self):
        with open(self.log_path, 'w') as log_file:
            json.dump(self.log, log_file, indent=4)