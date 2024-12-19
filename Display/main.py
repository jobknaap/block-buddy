import tkinter as tk
from tkinter import messagebox
import socket
import pathlib
import threading

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BlockBuddy")
        self.geometry("800x480")
        #self.attributes('-fullscreen', True)
        self.configure(background="light blue")

        # Container frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.path_to_image = pathlib.Path(__file__).parent.resolve() / "img"

        # Frames
        self.frames = {}
        for F in (HomePage, InfoPage, ErrorPage, ReturnPage, WaitStoragePage, CreatePage, WaitBuildPage, SuccesBuildpage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Socket Client script for Raspberry Pi
        # host = "mainrpi.local"
        # port = 9999
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.connect((host, port))
            
        self.show_frame(HomePage)

    # def send_message(self, message):
    #     self.client_socket.send(message.encode('utf-8')) # Send message to server

    # def listening(self, callback):
    #     threading.Thread(target=self.receive_data, args=(callback, ), daemon=True).start()

    # def receive_data(self, callback):
    #     response = self.client_socket.recv(1024).decode("utf-8")
    #     self.after(0, callback, response)

    def show_frame(self, controller):
            frame = self.frames[controller]
            frame.tkraise()

            # Call the on_show method when the frame is shown
            if hasattr(frame, 'on_show'):
                frame.on_show()

            # Call the on_hide method for other frames
            for other_frame in self.frames.values():
                if other_frame != frame and hasattr(other_frame, 'on_hide'):
                    other_frame.on_hide()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.controller = controller

        title_label = tk.Label(self, text="BlockBuddy", font=('Arial', 36), background="light blue")
        title_label.place(x=280, y=100)

        info_button = tk.Button(self, text="i", font=('Arial', 30), 
                                command=lambda: controller.show_frame(InfoPage))
        info_button.place(x=710, y=10)

        create_button = tk.Button(self, text="Create", font=('Arial', 36),
                                 command=lambda: controller.show_frame(CreatePage))
        create_button.place(x=185, y=240)

        return_button = tk.Button(self, text="Return", font=('Arial', 36),
                                 command=lambda: controller.show_frame(ReturnPage))
        return_button.place(x=460, y=240)

class InfoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.controller = controller

        text_info = "With block buddy you can 'Create' your own custom buddy. You only\nhave to select which piece you want and the machine will deliver\nthe pieces to you. After you got the pieces you can build your buddy\nyourself!!\n\nOnce you are done playing with your buddy you can 'return' your\nbuddy. Please take apart your buddy and follow the instructions\non the screen."

        title_label = tk.Label(self, text="How does block buddy work?", font=('Arial', 30), background="light blue")
        title_label.place(x=150, y=50)

        info_text = tk.Label(self, text=text_info, justify="left", font=('Arial', 16), background="light blue")
        info_text.place(x=85, y=120)

        back_button = tk.Button(self, text="Back", font=('Arial', 30),
                                command=lambda: controller.show_frame(HomePage))
        back_button.place(x=600, y=350)

class ErrorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.controller = controller

        title_label = tk.Label(self, text="Sorry something went\nwrong!", font=('Arial', 40), background="light blue")
        title_label.place(x=135, y=100)

        self.info_label = tk.Label(self, text="Error message: 508\nPlease contact us: 0612345678", font=('Arial', 20), background="light blue")
        self.info_label.place(x=185, y=250)

class ReturnPage(tk.Frame):
    piece_text = "Please place one piece at a time\non the conveyor belt facing upwards!"
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.controller = controller
        
        title_label = tk.Label(self, text=self.piece_text, font=('Arial', 32), background="light blue")
        title_label.place(x=60, y=50)

        info_label = tk.Label(self, text="Press \"Confirm\" once the piece is correctly placed.", font=('Arial', 20), background="light blue")
        info_label.place(x=110, y=200)

        confirm_button = tk.Button(self, text="Confirm", font=('Arial', 40),
                                command=lambda: self.controller.show_frame(WaitStoragePage))
        confirm_button.place(x=300, y=300)

        back_button = tk.Button(self, text="back", font=('Arial', 26),
                                command=lambda: self.controller.show_frame(HomePage))
        back_button.place(x=50, y=365)      
        
class WaitStoragePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.controller = controller

        self.is_visible = False # Track if the frame is visible
        
        title_label = tk.Label(self, text="Please wait while we store\nyour piece!", font=('Arial', 36), background="light blue")
        title_label.place(x=115, y=150)

    def succes_item(self): # When item is corectly stored a popup will show that it worked
        self.controller.show_frame(ReturnPage)
        messagebox.showinfo(title="Succes!", message="The item is correctly stored in the system!")

    def bad_item(self): # When an item is incorrect or wrongly placed it will pop up it didn't work
        self.controller.show_frame(ReturnPage)
        messagebox.showwarning(title="Failed!", message="The item is incorrectly placed or a non-existing item. Please try again!")

    def error(self): # When something is wrong with the system it will show te error message
        self.controller.show_frame(ErrorPage)

    def on_show(self): # When the frame is show it listens for a message to continue
        self.is_visible = True
        self.controller.send_message("2")
        self.handle_listen()
        
    def handle_listen(self):
        self.controller.listening(self.process_response)

    def process_response(self, result):
        if result == "0":
            self.bad_item()
        elif result == "1":
            self.succes_item()
        elif result == "2":
            self.error()
        
class CreatePage(tk.Frame):
        
    parts_img = {
    "10": "legs_blue.png",
    "11": "legs_red.png",
    "12": "legs_grey.png",
    "13": "body_blouse.png",
    "14": "body_red.png",
    "15": "body_blue.png",
    "16": "head_beard.png",
    "17": "head_woman.png",
    "18": "head_male.png",
    "19": "hat_blue.png",
    "20": "hat_red.png",
    "21": "hair_black.png"
}
   
    # Define the ranges for each row
    ranges = [(10, 12), (13, 15), (16, 18), (19, 21)]

    # 2d array for parts in the system
    active_parts_ID = [[] for _ in range(len(ranges))]

    hairI = 0
    headI = 0
    bodyI = 0
    legI = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.controller = controller

        self.is_visible = False  # Track if the frame is visible

        # Navigation
        back_button = tk.Button(self, text="Back", font=('Arial', 30),
                                command=lambda: controller.show_frame(HomePage))
        back_button.place(x=100, y=375)

        build_button = tk.Button(self, text="Build", font=('Arial', 30),
                                command=self.send_parts)
        build_button.place(x=600, y=375)

    def on_show(self): # When the frame is show it listens for a message to continue
        self.is_visible = True
        self.controller.send_message("1")
        self.handle_listen()
        
    def handle_listen(self):
        self.controller.listening(self.process_response)

    def process_response(self, result):
        self.fill_array(result)
    
    def fill_array(self, result):
        # Split result based on spaces
        list_result = result.split()

        # Convert each string to an integer
        list_result_int = [int(number) for number in list_result]

        # Distribute numbers into rows based on the ranges
        for number in list_result_int:
            for i, (start, end) in enumerate(self.ranges):
                if start <= number <= end:
                    self.active_parts_ID[i].append(number)
                    break
        
        self.place_buttons()
        self.place_images()

    def place_buttons(self):
        # Hair
        if len(self.active_parts_ID[3]) == 1:
            self.hair_next_button = tk.Button(self, text="next", font=('Arial', 25), command=self.next_hair, state=tk.DISABLED)
            self.hair_next_button.place(x=500, y= 25)
        else:
            self.hair_next_button = tk.Button(self, text="next", font=('Arial', 25), command=self.next_hair)
            self.hair_next_button.place(x=500, y= 25)

        self.hair_back_button = tk.Button(self, text="prev", font=('Arial', 25), state=tk.DISABLED, command=self.prev_hair)
        self.hair_back_button.place(x=220, y=25)

        # Head
        if len(self.active_parts_ID[2]) == 1:
            self.head_next_button  = tk.Button(self, text="next", font=('Arial', 25), command=self.next_head, state=tk.DISABLED)
            self.head_next_button.place(x=500, y=110)
        else:
            self.head_next_button  = tk.Button(self, text="next", font=('Arial', 25), command=self.next_head)
            self.head_next_button.place(x=500, y=110)

        self.head_back_button = tk.Button(self, text="prev", font=('Arial', 25), state=tk.DISABLED, command=self.prev_head)
        self.head_back_button.place(x=220, y=110)

        # Body
        if len(self.active_parts_ID[1]) == 1:
            self.body_next_button = tk.Button(self, text="next", font=('Arial', 25), command=self.next_body, state=tk.DISABLED)
            self.body_next_button.place(x=500, y=195)
        else:
            self.body_next_button = tk.Button(self, text="next", font=('Arial', 25), command=self.next_body)
            self.body_next_button.place(x=500, y=195)
        
        self.body_back_button = tk.Button(self, text="prev", font=('Arial', 25), state=tk.DISABLED, command=self.prev_body)
        self.body_back_button.place(x=220, y=195)

        # Leg
        if len(self.active_parts_ID[0]) == 1:
            self.leg_next_button = tk.Button(self, text="next", font=('Arial', 25), command=self.next_leg, state=tk.DISABLED)
            self.leg_next_button.place(x=500, y=280)
        else:
            self.leg_next_button = tk.Button(self, text="next", font=('Arial', 25), command=self.next_leg)
            self.leg_next_button.place(x=500, y=280)

        self.leg_back_button = tk.Button(self, text="prev", font=('Arial', 25), state=tk.DISABLED, command=self.prev_leg)
        self.leg_back_button.place(x=220, y=280)


    def place_images(self):
        if len(self.active_parts_ID[3]) > 0 and len(self.active_parts_ID[2]) > 0 and len(self.active_parts_ID[1]) > 0 and len(self.active_parts_ID[0]) > 0:
            self.hair_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[3][self.hairI])])
            self.hair_label = tk.Label(self, image=self.hair_image, background="light blue")
            self.hair_label.place(x=375, y=20)

            self.head_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[2][self.headI])])
            self.head_label = tk.Label(self, image=self.head_image, background="light blue")
            self.head_label.place(x=375, y=120)

            self.body_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[1][self.bodyI])])
            self.body_label = tk.Label(self, image=self.body_image, background="light blue")
            self.body_label.place(x=365, y=205)

            self.legs_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[0][self.hairI])])
            self.legs_label = tk.Label(self, image=self.legs_image, background="light blue")
            self.legs_label.place(x=375, y=280)
        else:
            self.controller.show_frame(HomePage)
            messagebox.showwarning(title="Failed!", message="Sorry there are not enough items in the machine!\nCome back later or return your buddy :)")

    def send_parts(self):      
        self.controller.send_message(str(self.active_parts_ID[3][self.hairI]) + " " +
                                     str(self.active_parts_ID[2][self.headI]) + " " +
                                     str(self.active_parts_ID[1][self.bodyI]) + " " +
                                     str(self.active_parts_ID[0][self.legI]))
        self.controller.show_frame(WaitBuildPage)

    def next_hair(self):
        if self.hairI < len(self.active_parts_ID[3]) - 1:
            self.hairI += 1
            next_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[3][self.hairI])])
            self.hair_label.config(image=next_image)
            self.hair_back_button.config(state=tk.ACTIVE)
            if self.hairI == len(self.active_parts_ID[3]) - 1:
                self.hair_next_button.config(state=tk.DISABLED)
            
    def prev_hair(self):
        if self.hairI > 0:
            self.hairI -= 1
            prev_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[3][self.hairI])])            
            self.hair_label.config(image=prev_image)
            self.hair_next_button.config(state=tk.ACTIVE)
            if self.hairI == 0:
                self.hair_back_button.config(state=tk.DISABLED)

    def next_head(self):
        if self.headI < len(self.active_parts_ID[2]) - 1:
            self.headI = (self.headI + 1)
            next_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[2][self.headI])])  
            self.head_label.config(image=next_image)
            self.head_back_button.config(state=tk.ACTIVE)
            if self.headI == len(self.active_parts_ID[2]) - 1:
                self.head_next_button.config(state=tk.DISABLED)

    def prev_head(self):
        if self.headI > 0:
            self.headI = (self.headI - 1)
            prev_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[2][self.headI])])
            self.head_label.config(image=prev_image)
            self.head_next_button.config(state=tk.ACTIVE)
            if self.headI == 0:
                self.head_back_button.config(state=tk.DISABLED)

    def next_body(self):
        if self.bodyI < len(self.active_parts_ID[1]) - 1:
            self.bodyI = (self.bodyI + 1)
            next_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[1][self.bodyI])])
            self.body_label.config(image=next_image)
            self.body_back_button.config(state=tk.ACTIVE)
            if self.bodyI == len(self.active_parts_ID[1]) - 1:
                self.body_next_button.config(state=tk.DISABLED)

    def prev_body(self):
        if self.bodyI > 0:
            self.bodyI = (self.bodyI - 1)
            prev_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[1][self.bodyI])])
            self.body_label.config(image=prev_image)
            self.body_next_button.config(state=tk.ACTIVE)
            if self.bodyI == 0:
                self.body_back_button.config(state=tk.DISABLED)

    def next_leg(self):
        if self.legI < len(self.active_parts_ID[0]) - 1:
            self.legI = (self.legI + 1)
            next_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[0][self.legI])])
            self.legs_label.config(image=next_image)
            self.leg_back_button.config(state=tk.ACTIVE)
            if self.legI == len(self.active_parts_ID[0]) - 1:
                self.leg_next_button.config(state=tk.DISABLED)

    def prev_leg(self):
        if self.legI > 0:
            self.legI = (self.legI - 1)
            prev_image = tk.PhotoImage(file=self.controller.path_to_image / self.parts_img[str(self.active_parts_ID[0][self.legI])])
            self.legs_label.config(image=prev_image)
            self.leg_next_button.config(state=tk.ACTIVE)
            if self.legI == 0:
                self.leg_back_button.config(state=tk.DISABLED)
            
class WaitBuildPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.controller = controller

        self.is_visible = False  # Track if the frame is visible
        
        title_label = tk.Label(self, text="Please wait while we create\nyour buddy!", font=('Arial', 36), background="light blue")
        title_label.place(x=115, y=150)

    def on_show(self): # When the frame is show it listens for a message to continue
        self.is_visible = True
        self.handle_listen()
        
    def handle_listen(self):
        self.controller.listening(self.process_response)

    def process_response(self, result):
        if result == "1":
            self.controller.show_frame(SuccesBuildpage)
        elif result == "2":
            self.controller.show_frame(ErrorPage)
        

class SuccesBuildpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.controller = controller

        self.is_visible = False

        title_label = tk.Label(self, text="Enjoy your buddy! Take\ngood care of it.", font=('Arial', 40), background="light blue")
        title_label.place(x=135, y=100)

        self.info_label = tk.Label(self, text="After 5 seconds you will return to the\nhome screen.", font=('Arial', 20), background="light blue")
        self.info_label.place(x=185, y=250)

    def on_show(self):
        self.is_visible = True
        self.after(5000, self.controller.show_frame, HomePage)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
