import tkinter as tk

def create_gui(shell):
    def execute_command():
        command = command_entry.get()
        output.delete(1.0, tk.END)
        try:
            if command.startswith("ls"):
                result = shell.ls()
                output.insert(tk.END, "\n".join(result))
            elif command.startswith("cd"):
                _, path = command.split()
                shell.cd(path)
                output.insert(tk.END, f"Changed directory to {shell.pwd()}")
            elif command.startswith("pwd"):
                pwd = shell.pwd()
                output.insert(tk.END, pwd)
            elif command.startswith("touch"):
                _, filename = command.split()
                shell.touch(filename)
                output.insert(tk.END, f"Created file {filename}")
            elif command.startswith("exit"):
                shell.exit()
                root.destroy()
        except Exception as e:
            output.insert(tk.END, f"Error: {e}")

    root = tk.Tk()
    root.title("Virtual Shell Emulator")

    command_entry = tk.Entry(root, width=50)
    command_entry.pack()

    execute_button = tk.Button(root, text="Execute", command=execute_command)
    execute_button.pack()

    output = tk.Text(root, height=20, width=60)
    output.pack()

    root.mainloop()