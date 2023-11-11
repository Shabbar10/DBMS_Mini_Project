import customtkinter as ctk
from PIL import Image

class App(ctk.CTk):
    def __init__(self, dimensions):
        super().__init__()

        center_x = int((self.winfo_screenwidth() - dimensions[0]) / 2)
        center_y = int((self.winfo_screenheight() - dimensions[1]) / 2)

        self.geometry(f'{dimensions[0]}x{dimensions[1]}+{center_x}+{center_y}')
        self.title('Hospital Management System')
        self.minsize(dimensions[0], dimensions[1])

        left_frame = Left_User_Frame(self)
        left_frame.place(relx=0, rely=0, relwidth=0.69, relheight=1)

        self.mainloop()

class Left_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#333333')
        self.create_widgets()
    
    def create_widgets(self):
        self.mute_image = ctk.CTkImage(Image.open('mute.png'), size=(30,30))
        self.mute_label = ctk.CTkLabel(self, text='', image=self.mute_image)
        
        # self.profile_pic = ctk.CTkImage(None)

        self.welcome_label = ctk.CTkLabel(self, text='Welcome, whoever')

        # Layout
        self.mute_label.place(x=5, y=5)
        self.welcome_label.place(relx=0.5, rely=0.9, anchor='center')

class Left_User_Frame(Left_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.profile_pic = ctk.CTkImage(Image.open('Saurab.png'), size=(298,451))
        self.profile_label = ctk.CTkLabel(self, image=self.profile_pic, text='')
        self.profile_label.place(relx=0.5, rely=0.5, anchor='center')

window = App((1280,720))
