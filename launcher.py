import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import threading

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker Launcher")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Title
        title_label = tk.Label(root, text="AutoClicker Seçici", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        subtitle_label = tk.Label(root, text="Lütfen başlatmak istediğiniz sürümü seçin:", font=("Arial", 10))
        subtitle_label.pack(pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # C++
        self.cpp_btn = tk.Button(btn_frame, text="C++ Sürümünü Başlat", width=25, bg="lightblue", command=self.launch_cpp)
        self.cpp_btn.pack(pady=5)

        # Python
        self.python_btn = tk.Button(btn_frame, text="Python Sürümünü Başlat", width=25, bg="lightgreen", command=self.launch_python)
        self.python_btn.pack(pady=5)

        # Go
        self.go_btn = tk.Button(btn_frame, text="Go Sürümünü Başlat", width=25, bg="lightyellow", command=self.launch_go)
        self.go_btn.pack(pady=5)

        # Java
        self.java_btn = tk.Button(btn_frame, text="Java Sürümünü Başlat", width=25, bg="lightpink", command=self.launch_java)
        self.java_btn.pack(pady=5)
        
        # Web/JS info
        self.js_btn = tk.Button(btn_frame, text="Web/JS (Bilgi)", width=25, bg="lightgray", command=self.info_js)
        self.js_btn.pack(pady=5)

    def launch_process(self, command, cwd=None):
        def run():
            try:
                subprocess.run(command, cwd=cwd, check=True)
            except Exception as e:
                messagebox.showerror("Hata", f"Uygulama başlatılırken hata oluştu:\n{e}")
        
        threading.Thread(target=run, daemon=True).start()

    def launch_cpp(self):
        # ./cpp-clicker/cpp-clicker
        self.launch_process(["./cpp-clicker"], cwd="cpp-clicker")

    def launch_python(self):
        # python main.py
        # We need to use the venv python if we are in it, or just system python. 
        # Using sys.executable is usually safer.
        import sys
        self.launch_process([sys.executable, "main.py"])

    def launch_go(self):
        # go run main.go
        self.launch_process(["go", "run", "main.go"], cwd="go-clicker")

    def launch_java(self):
        # java AutoClicker
        self.launch_process(["java", "AutoClicker"], cwd="java-clicker")

    def info_js(self):
        messagebox.showinfo("Bilgi", "Web/JS sürümü bir tarayıcı konsol betiğidir (web_autoclicker.js). Tarayıcınızda F12'ye basıp konsola yapıştırarak kullanabilirsiniz.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()
