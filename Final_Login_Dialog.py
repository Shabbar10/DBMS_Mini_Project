import customtkinter as ctk

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


class canva(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness = 0, bg = 'black')
        self.pack(expand=True, fill='both')
        self.center_frame = frame(self).place(relx = 0.5, rely=0.5, anchor='center')


class frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", border_color="cyan", border_width=1,  height= 300, width= 300)

        #1 Login Label
        login_label = ctk.CTkLabel(self, text="Login", font=("Helvetica", 20, "bold"), text_color="white") 

        # Entry widgets
        self.username_entry = ctk.CTkEntry(self, placeholder_text="username", placeholder_text_color="grey", fg_color="transparent", border_color="#0492C2")
        self.pswd_entry = ctk.CTkEntry(self, placeholder_text="password", placeholder_text_color="grey", fg_color="transparent", border_color="#0492C2", show="🖕🏻")
        self.user_entry_rel_width = 0.7
        self.pwd_entry_rel_width = 0.7
        
        self.username_entry.bind('<FocusIn>', self.animate_user_entry)
        self.username_entry.bind('<FocusOut>', self.deanimate_user_entry)
        
        self.pswd_entry.bind('<FocusIn>', self.animate_pwd_entry)
        self.pswd_entry.bind('<FocusOut>', self.deanimate_pwd_entry)

        # Error labels
        user_error = ctk.CTkLabel(self, text="", text_color="red", font=("Helvetica", 15))
        pswd_error = ctk.CTkLabel(self, text="", text_color="red", font=("Helvetica", 15))

        # Enter button
        submit = ctk.CTkButton(self, text="Submit", border_color="#0492C2",corner_radius=20,  font=("Helvetica", 15), text_color="white", command=lambda e: self.login())

        # Placing Widgets
        login_label.place(relx=0.5, rely=0.1, anchor='center')
        self.username_entry.place(relx=0.5, rely=0.4,relheight = 0.1, relwidth=self.user_entry_rel_width, anchor='center')
        self.pswd_entry.place(relx=0.5, rely=0.6,relheight = 0.1, relwidth=self.pwd_entry_rel_width, anchor='center')
        submit.place(relx=0.5, rely=0.82, anchor='center', relwidth=0.4)

        user_error.place(relx= 0.5, rely=0.5, anchor='center')
        pswd_error.place(relx= 0.7, rely=0.5, anchor='center')

    def animate_user_entry(self, event):
        self.user_entry_rel_width += 0.016
        if self.user_entry_rel_width <= 0.9:
            self.username_entry.place(relx=0.5, rely=0.4, relheight = 0.1, relwidth=self.user_entry_rel_width, anchor='center')
            home.after(1, lambda: self.animate_user_entry(event))
   
    def deanimate_user_entry(self, event):
        self.user_entry_rel_width -= 0.016
        if self.user_entry_rel_width >= 0.7:
            self.username_entry.place(relx=0.5, rely=0.4, relheight = 0.1, relwidth=self.user_entry_rel_width, anchor='center')
            home.after(1, lambda: self.deanimate_user_entry(event))

    def animate_pwd_entry(self, event):
        self.pwd_entry_rel_width += 0.016
        if self.pwd_entry_rel_width <= 0.9:
            self.pswd_entry.place(relx=0.5, rely=0.6, relheight = 0.1, relwidth=self.pwd_entry_rel_width, anchor='center')
            home.after(1, lambda: self.animate_pwd_entry(event))
   
    def deanimate_pwd_entry(self, event):
        self.pwd_entry_rel_width -= 0.016
        if self.pwd_entry_rel_width >= 0.7:
            self.pswd_entry.place(relx=0.5, rely=0.6, relheight = 0.1, relwidth=self.pwd_entry_rel_width, anchor='center')
            home.after(1, lambda: self.deanimate_pwd_entry(event))

    def login(self, uname, pswd ):
        print(f'Username: {uname}\nPassword: {pswd}\n')
        if uname != self.username:
                self.username_entry.delete(0, 'end')
                self.pswd_entry.delete(0, 'end')
                
                self.user_error.configure(text="User does not exist")
        
        elif uname == self.username:
                self.user_error.configure(text="User Found", text_color="green") 
                if pswd != self.password:
                    self.pswd_entry.delete(0, 'end')
                    self.pswd_error.configure(text="Incorrect Password")
                else:
                    self.pswd_error.configure(text="Password matched! Signing in", text_color="green")
        else:
                self.pswd_entry.delete(0, 'end')
                self.pswd_error.configure(text="")
                self.user_error.configure(text="")

home = login_window(300, 300)
home.mainloop()