import customtkinter as ctk
import pymysql

class Insert(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.update()

        center_x = int((self.winfo_screenwidth() - 800) / 2)
        center_y = int((self.winfo_screenheight() - 600) / 2)

        self.geometry(f'800x600+{center_x}+{center_y}')
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        menu = ctk.CTkTabview(self)
        hospital = menu.add('Hospital')
        employee = menu.add('Employee')
        
        menu.pack()