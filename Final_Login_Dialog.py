import customtkinter as ctk
import pymysql

class login_window(ctk.CTk):
    def __init__(self, width, height):
        super().__init__()

        center_x = int((self.winfo_screenwidth() - width) / 2)
        center_y = int((self.winfo_screenheight() - height) / 2)

        self.geometry(f'{width}x{height}+{center_x}+{center_y}')
        self.main_container = canva(self)
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Button-1>', lambda e: self.deanimate_all(e))
    
    def deanimate_all(self, event):
        self.main_container.center_frame.deanimate_user_entry(event)
        self.main_container.center_frame.deanimate_pwd_entry(event)


class canva(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness = 0, bg = 'black')
        self.pack(expand=True, fill='both')
        self.center_frame = frame(self)
        self.center_frame.place(relx = 0.5, rely=0.5, anchor='center', relwidth=1, relheight=1)


class frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", border_color="cyan", border_width=1,  height= 300, width= 300)

        # Login Label
        login_label = ctk.CTkLabel(self, text="Login", font=("Helvetica", 20, "bold"), text_color="white") 

        # Username/Password labels
        username_label = ctk.CTkLabel(self, text='Username', text_color='white', font=("Helvetica", 14))
        pwd_label = ctk.CTkLabel(self, text='Password', text_color='white', font=("Helvetica", 14))

        # Entry widgets
        self.username_var = ctk.StringVar()
        self.pwd_var = ctk.StringVar()

        self.username_entry = ctk.CTkEntry(self,
                                           placeholder_text="username", 
                                           placeholder_text_color="grey", 
                                           fg_color="transparent", 
                                           border_color="#0492C2", 
                                           textvariable=self.username_var)
        
        self.pswd_entry = ctk.CTkEntry(self, 
                                       placeholder_text="password", 
                                       placeholder_text_color="grey", 
                                       fg_color="transparent", 
                                       border_color="#0492C2", 
                                       show="🖕🏻", 
                                       textvariable=self.pwd_var)
        
        self.user_entry_rel_width = 0.4
        self.pwd_entry_rel_width = 0.4
        
        self.username_entry.bind('<FocusIn>', self.animate_user_entry)
        self.username_entry.bind('<FocusOut>', self.deanimate_user_entry)
        
        self.pswd_entry.bind('<FocusIn>', self.animate_pwd_entry)
        self.pswd_entry.bind('<FocusOut>', self.deanimate_pwd_entry)

        # Error labels
        self.error = ctk.CTkLabel(self, text="", text_color="red", font=("Helvetica", 15))

        # Enter button
        submit = ctk.CTkButton(self, 
                               text="Submit", 
                               border_color="#0492C2",
                               corner_radius=20,
                               font=("Helvetica", 15), 
                               text_color="white", 
                               command=self.establish_connection)

        # Placing Widgets
        login_label.place(relx=0.5, rely=0.1, anchor='center')

        username_label.place(relx=0.30, rely=0.395, anchor='center')
        pwd_label.place(relx=0.30, rely=0.595, anchor='center')

        self.username_entry.place(relx=0.65, rely=0.4,relheight = 0.1, relwidth=self.user_entry_rel_width, anchor='center')
        self.pswd_entry.place(relx=0.65, rely=0.6,relheight = 0.1, relwidth=self.pwd_entry_rel_width, anchor='center')

        submit.place(relx=0.5, rely=0.85, anchor='center', relwidth=0.4)

        self.error.place(relx= 0.5, rely=0.77, anchor='s')

        self.username_entry.bind('<Return>', lambda e: self.establish_connection())
        self.pswd_entry.bind('<Return>', lambda e: self.establish_connection())

    def animate_user_entry(self, event):
        self.user_entry_rel_width += 0.016
        if self.user_entry_rel_width <= 0.5:
            self.username_entry.place(relx=0.65, rely=0.4, relheight = 0.1, relwidth=self.user_entry_rel_width, anchor='center')
            home.after(1, lambda: self.animate_user_entry(event))
   
    def deanimate_user_entry(self, event):
        self.user_entry_rel_width -= 0.016
        if self.user_entry_rel_width >= 0.4:
            self.username_entry.place(relx=0.65, rely=0.4, relheight = 0.1, relwidth=self.user_entry_rel_width, anchor='center')
            home.after(1, lambda: self.deanimate_user_entry(event))

    def animate_pwd_entry(self, event):
        self.pwd_entry_rel_width += 0.016
        if self.pwd_entry_rel_width <= 0.5:
            self.pswd_entry.place(relx=0.65, rely=0.6, relheight = 0.1, relwidth=self.pwd_entry_rel_width, anchor='center')
            home.after(1, lambda: self.animate_pwd_entry(event))
   
    def deanimate_pwd_entry(self, event):
        self.pwd_entry_rel_width -= 0.016
        if self.pwd_entry_rel_width >= 0.4:
            self.pswd_entry.place(relx=0.65, rely=0.6, relheight = 0.1, relwidth=self.pwd_entry_rel_width, anchor='center')
            home.after(1, lambda: self.deanimate_pwd_entry(event))

    def establish_connection(self):
        host = 'localhost'
        user = self.username_var.get()
        pwd = self.pwd_var.get()
        database = 'empproject'
        connection = None
        try:
            connection = pymysql.connect(host=host, user=user, password=pwd, database=database)
        except pymysql.err.OperationalError:
            self.error.configure(text='')
            self.error.configure(text='Username/Password Invalid')
            self.username_entry.configure(border_color='red')
            self.pswd_entry.configure(border_color='red')
            print('Failure')
        else:
            self.error.configure(text='')
            print('Success')
            self.error.configure(text_color='green')
            self.error.configure(text='Login Successful')
            home.after(1500, home.destroy)

        return connection
        

home = login_window(400, 300)

# connection = frame(None).establish_connection()
# cursor = connection.cursor()

home.mainloop()