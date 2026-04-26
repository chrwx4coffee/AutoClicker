import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui
from pynput import mouse

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("350x250")
        self.root.resizable(False, False)

        self.target_x = None
        self.target_y = None
        self.is_recording_location = False
        self.mouse_listener = None

        # Title
        title_label = tk.Label(root, text="Auto Clicker", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Coordinate Frame
        coord_frame = tk.Frame(root)
        coord_frame.pack(pady=5)

        self.coord_label = tk.Label(coord_frame, text="Konum: Seçilmedi", font=("Arial", 10))
        self.coord_label.pack(side=tk.LEFT, padx=10)

        self.select_btn = tk.Button(coord_frame, text="Konum Seç", command=self.start_location_selection, bg="lightblue")
        self.select_btn.pack(side=tk.LEFT)

        # Settings Frame
        settings_frame = tk.Frame(root)
        settings_frame.pack(pady=10)

        tk.Label(settings_frame, text="Tıklama Sayısı:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.count_entry = tk.Entry(settings_frame, width=10)
        self.count_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.count_entry.insert(0, "10")

        tk.Label(settings_frame, text="Gecikme (sn):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.delay_entry = tk.Entry(settings_frame, width=10)
        self.delay_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.delay_entry.insert(0, "1.0")

        # Start Button
        self.start_btn = tk.Button(root, text="Başlat", command=self.start_clicking, bg="lightgreen", font=("Arial", 12, "bold"))
        self.start_btn.pack(pady=5)

        # Status
        self.status_label = tk.Label(root, text="", fg="gray", font=("Arial", 9))
        self.status_label.pack()

    def start_location_selection(self):
        if self.is_recording_location:
            return

        self.is_recording_location = True
        self.select_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        # 3 saniyelik geri sayım başlat
        self.countdown(3)

    def countdown(self, seconds):
        if seconds > 0:
            self.status_label.config(text=f"Farenizi hedefe götürün... {seconds} saniye.", fg="blue")
            self.root.after(1000, self.countdown, seconds - 1)
        else:
            self.record_location()

    def record_location(self):
        # Mause imlecinin aktif ekran üstündeki konumunu yakala
        try:
            x, y = pyautogui.position()
            self.target_x = x
            self.target_y = y
        except Exception:
            pass
            
        self.is_recording_location = False
        self.update_location_ui()

    def update_location_ui(self):
        self.coord_label.config(text=f"Konum: X={int(self.target_x)}, Y={int(self.target_y)}")
        self.status_label.config(text="Konum başarıyla kaydedildi.", fg="green")
        self.select_btn.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.NORMAL)

    def start_clicking(self):
        if self.target_x is None or self.target_y is None:
            messagebox.showerror("Hata", "Lütfen önce bir konum seçin.")
            return

        try:
            click_count = int(self.count_entry.get())
            if click_count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir tıklama sayısı girin (ör: 10).")
            return

        try:
            delay = float(self.delay_entry.get())
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir gecikme süresi girin (ör: 0.5).")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.select_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Tıklama işlemi sürüyor...", fg="orange")

        # Run clicking process in a separate thread so UI doesn't freeze
        threading.Thread(target=self.click_thread, args=(click_count, delay), daemon=True).start()

    def click_thread(self, count, delay):
        # Optional: Add an initial short delay so user can release the mouse if needed
        time.sleep(1) 

        for i in range(count):
            try:
                pyautogui.click(self.target_x, self.target_y)
                time.sleep(delay)
            except Exception as e:
                print(f"Error during click: {e}")
                break

        self.root.after(0, self.finish_clicking)

    def finish_clicking(self):
        self.start_btn.config(state=tk.NORMAL)
        self.select_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Tıklama işlemi tamamlandı.", fg="green")
        messagebox.showinfo("Bitti", "Auto Clicker işlemi tamamlandı!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
