import tkinter as tk

class InfoWindow(tk.Toplevel):
    background_color = "light blue"
    text_info = "With block buddy you can 'Create' your own custom buddy. You only\nhave to select which piece you want and the machine will deliver\nthe piees to you. After you got the pieces you can build your buddy\nyourself!!\n\nOnce you are done playing with your buddy you can 'return' your\nbuddy. Please take apart your buddy and follow the instructions\non the screen."

    def __init__(self, main_window):
        super().__init__(main_window)

        self.title("Info window")
        self.geometry("800x480")
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        self.configure(background=self.background_color)

        self.title_label = tk.Label(self, text="How does block buddy work?", font=('Arial', 30), background=self.background_color)
        self.title_label.place(x=150, y=50)

        self.info_text = tk.Label(self, text=self.text_info, justify="left", font=('Arial', 16), background=self.background_color)
        self.info_text.place(x=85, y=120)

        self.back_button = tk.Button(self, text="Back", font=('Arial', 30), command=self.back_to_main_window)
        self.back_button.place(x=600, y=350)

    def back_to_main_window(self):
        self.destroy()
        self.master.deiconify()

if __name__ == "__main__":
    info_window = InfoWindow(None)
    info_window.mainloop()
