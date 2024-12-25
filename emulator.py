import os
import tarfile
import json
import datetime
from tkinter import Tk, Text, Entry, Button


class ShellEmulator:
    def __init__(self, fs_path):
        self.current_directory = '/'
        self.log = []
        self.base_path = os.path.abspath('virtual_fs')
        self.load_virtual_fs(fs_path)

    def load_virtual_fs(self, fs_path):
        with tarfile.open(fs_path, 'r') as tar:
            tar.extractall(self.base_path)

    def run_command(self, command):
        if command.startswith('ls'):
            return self.ls()
        elif command.startswith('cd '):
            return self.cd(command[3:].strip())
        elif command == 'pwd':
            return self.pwd()
        elif command.startswith('touch '):
            return self.touch(command[6:].strip())
        elif command == 'exit':
            return 'exit'
        else:
            return 'Unknown command'

    def ls(self):
        path = os.path.join(self.base_path, self.current_directory.lstrip('/'))
        try:
            files = os.listdir(path)
            files = [f + '/' if os.path.isdir(os.path.join(path, f)) else f for f in files]
            self.log_action(f'ls in {self.current_directory}')
            return "\n".join(sorted(files))
        except FileNotFoundError:
            return 'Directory not found'

    def cd(self, new_dir):
        if new_dir == '..':
            self.current_directory = os.path.dirname(self.current_directory)
            self.current_directory = '/' if self.current_directory == '' else self.current_directory
            self.log_action(f'cd to {self.current_directory}')
            return ''

        potential_path = os.path.join(self.base_path, self.current_directory.lstrip('/'), new_dir)
        if os.path.isdir(potential_path):
            self.current_directory = os.path.relpath(potential_path, self.base_path)
            self.current_directory = '/' + self.current_directory.replace(os.path.sep, '/')
            self.log_action(f'cd to {self.current_directory}')
            return ''
        else:
            return 'Directory not found'

    def pwd(self):
        self.log_action(f'pwd {self.current_directory}')
        return self.current_directory

    def touch(self, filename):
        file_path = os.path.join(self.base_path, self.current_directory.lstrip('/'), filename)
        with open(file_path, 'a'):
            pass
        self.log_action(f'touch {filename} in {self.current_directory}')
        return ''

    def log_action(self, action):
        self.log.append({
            'action': action,
            'timestamp': datetime.datetime.now().isoformat()
        })

    def save_log(self, log_path):
        with open(log_path, 'w') as log_file:
            json.dump(self.log, log_file, indent=4)


def main():
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Config file not found.")
        return

    emulator = ShellEmulator(config.get("virtual_fs_path", ''))

    root = Tk()
    root.title("Shell Emulator")
    output_area = Text(root, height=15, width=50)
    output_area.pack()

    def execute_command():
        command = command_entry.get()
        result = emulator.run_command(command)
        output_area.insert('end', f'{command}\n{result}\n\n')
        command_entry.delete(0, 'end')
        if command == 'exit':
            root.destroy()

    command_entry = Entry(root, width=50)
    command_entry.pack()

    execute_button = Button(root, text="Execute", command=execute_command)
    execute_button.pack()

    root.mainloop()

    emulator.save_log(config.get("log_path", 'log.json'))


if __name__ == "__main__":
    main()