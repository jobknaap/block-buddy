#!/usr/bin/pyton3

import tkinter as tk
from info import InfoWindow

class MainWindow(tk.Tk):
    background_color = "light blue"
    def __init__(self):
        super().__init__()

        self.title("Home Screen")
        self.geometry("800x480")
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        self.configure(background = self.background_color)

        self.align_center = tk.Label(self, text="|", font=('Arial', 36), background=self.background_color)
        self.align_center.place(x=400)

        self.title_label = tk.Label(self, text="BlockBuddy", font=('Ariel', 36), background=self.background_color)
        self.title_label.place(x=280, y=100)

        self.info_button = tk.Button(self, text="i", font=('Arial', 30), width=2, command=self.open_info_window)
        self.info_button.place(x=710, y=10)

        self.create_button = tk.Button(self, text="Create", font=('Arial',36))
        self.create_button.place(x=185, y=240)

        self.return_button = tk.Button(self, text="Return", font=('Arial', 36))
        self.return_button.place(x=460, y=240)

    def open_info_window(self):
        self.withdraw()
        info_window = InfoWindow(self)
        info_window.protocol("WM_DELETE_WINDOW", lambda: self.open_info_window_close(info_window))

    def on_info_window_close(self, info_window):
        info_window.destroy()
        self.deiconify()

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()