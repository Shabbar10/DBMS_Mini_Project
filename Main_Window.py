import customtkinter as ctk
from PIL import Image
import Final_Login_Dialog as login


connection = login.send_connection()
cursor = connection.cursor()
cursor.execute('SELECT * FROM employee;')
results = cursor.fetchall()
for i in results:
    print(i)


class App(ctk.CTk):
    def __init__(self, dimensions, user):
        super().__init__()
        # self.update()

        center_x = int((self.winfo_screenwidth() - dimensions[0]) / 2)
        center_y = int((self.winfo_screenheight() - dimensions[1]) / 2)

        self.geometry(f'{dimensions[0]}x{dimensions[1]}+{center_x}+{center_y}')
        self.title('Hospital Management System')
        self.minsize(dimensions[0], dimensions[1])

        print(f'\n\nThe user is {user}\n\n')

        if user == 'boom':
            left_frame = Left_Admin_Frame(self)
            right_frame = Right_Admin_Frame(self)
        else:
            left_frame = Left_User_Frame(self)
            right_frame = Right_User_Frame(self)

        left_frame.place(relx=0, rely=0, relwidth=0.69, relheight=1)
        right_frame.place(relx=0.69, rely=0, relwidth=0.31, relheight=1)

        self.mainloop()


class Left_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#333333')
        self.create_widgets()
    
    def create_widgets(self):
        self.mute_image = ctk.CTkImage(Image.open('mute.png'), size=(30,30))
        self.mute_label = ctk.CTkLabel(self, text='', image=self.mute_image)
        self.welcome_label = ctk.CTkLabel(self, text='Welcome, whoever')

        # Layout
        self.mute_label.place(x=5, y=5)
        self.welcome_label.place(relx=0.5, rely=0.88, anchor='center')


class Left_User_Frame(Left_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.profile_pic = ctk.CTkImage(Image.open('Saurab.png'), size=(298,451))
        self.profile_label = ctk.CTkLabel(self, image=self.profile_pic, text='')
        self.profile_label.place(relx=0.5, rely=0.5, anchor='center')

        self.welcome_label.configure(text='Welcome, User', font=('Consolas', 20, "bold"))


class Left_Admin_Frame(Left_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.profile_pic = ctk.CTkImage(Image.open('ACD293.png'), size=(378,504))
        self.profile_label = ctk.CTkLabel(self, image=self.profile_pic, text='')
        self.profile_label.place(relx=0.5, rely=0.43, anchor='center')

        self.welcome_label.configure(text='Welcome, Admin', font=('Consolas', 20, "bold"))


class Right_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Define the grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')
        self.create_widgets()

    def create_widgets(self):
        self.insert_button = ctk.CTkButton(self, text='Insert Record(s)', corner_radius=13, font=('Helvetica', 14), fg_color='transparent', border_width=3, border_color='#00FFFF')
        self.view_button = ctk.CTkButton(self, text='View Record(s)', corner_radius=13, font=('Helvetica', 14), fg_color='transparent', border_width=3, border_color='#00FFFF')
        self.delete_button = ctk.CTkButton(self, text='Delete Record(s)', corner_radius=13, font=('Helvetica', 14), fg_color='transparent', border_width=3, border_color='#00FFFF')
        self.update_button = ctk.CTkButton(self, text='Update Record(s)', corner_radius=13, font=('Helvetica', 14), fg_color='transparent', border_width=3, border_color='#00FFFF')

        # Layout
        self.insert_button.grid(column=0, row=0, sticky='ew', padx=80, ipady=25, ipadx=2)
        self.view_button.grid(column=0, row=1, sticky='ew', padx=80, ipady=25, ipadx=2)
        self.delete_button.grid(column=0, row=2, sticky='ew', padx=80, ipady=25, ipadx=2)
        self.update_button.grid(column=0, row=3, sticky='ew', padx=80, ipady=25, ipadx=2)

class Right_User_Frame(Right_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Disable buttons
        self.view_button.configure(state='disbaled', border_color='black', fg_color='#1f1f1f')
        self.delete_button.configure(state='disbaled', border_color='black', fg_color='#1f1f1f')
        self.update_button.configure(state='disbaled', border_color='black', fg_color='#1f1f1f')

        # Setup command for insertion
        # self.insert_button.configure(command=print('hi'))


class Right_Admin_Frame(Right_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Setup commands for all buttons


window = App((1280,720), connection.user.decode('utf-8'))