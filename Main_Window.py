import customtkinter as ctk
from PIL import Image
import pygame
from pymysql import err

import Admin_Fns as af
from datetime import datetime


is_muted = False


class App(ctk.CTkToplevel):
    def __init__(self, dimensions, connection):
        super().__init__()

        self.connection = connection
        user = self.connection.user.decode('utf-8')

        center_x = int((self.winfo_screenwidth() - dimensions[0]) / 2)
        center_y = int((self.winfo_screenheight() - dimensions[1]) / 2)

        self.geometry(f'{dimensions[0]}x{dimensions[1]}+{center_x}+{center_y}')
        self.title('Hospital Management System')
        self.minsize(dimensions[0], dimensions[1])

        if user == 'root':
            self.left_frame = Left_Admin_Frame(self)
            right_frame = Right_Admin_Frame(self, self.connection)
        else:
            self.left_frame = Left_User_Frame(self)
            right_frame = Right_User_Frame(self, self.connection)

        self.left_frame.place(relx=0, rely=0, relwidth=0.69, relheight=1)
        right_frame.place(relx=0.69, rely=0, relwidth=0.31, relheight=1)


class Left_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#0f0f0f')
        self.create_widgets()
        # self.play_music()
    
    def create_widgets(self):
        self.mute_image = ctk.CTkImage(Image.open('mute1.png'), size=(18,18))
        self.mute_label = ctk.CTkLabel(self, text='', image=self.mute_image)
        self.mute_button = ctk.CTkButton(self, image=self.mute_image, text='', fg_color='transparent', command=lambda e=None: self.toggle_mute(e), width=15, hover=False)

        self.welcome_label = ctk.CTkLabel(self, text='Welcome, whoever')

        title_label = ctk.CTkLabel(self, text='United States of Smash', font=('Consolas', 35, "bold"))

        self.logout_button = ctk.CTkButton(self)

        logo = ctk.CTkImage(Image.open('logo.png'), size=(130, 130))
        self.logo_label = ctk.CTkLabel(self, text='', image=logo)

        # Layout
        self.mute_button.place(x=5, y=5)
        self.welcome_label.place(relx=0.5, rely=0.88, anchor='center')
        # self.logo_label.place(relx=0.985, rely=0.015, anchor='ne')
        self.logo_label.place(relx=1, rely=0, anchor='ne')
        title_label.place(relx=0.5, rely=0.04, anchor='center')

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("Gogeta.mp3")
        pygame.mixer.music.play(-1) # Loop indefinitely

    # def stop_music(self):
    #     pygame.mixer.music.stop()

    def toggle_mute(self, event):
        global is_muted
        if is_muted:
            pygame.mixer.music.set_volume(1.0)
            self.mute_image = ctk.CTkImage(Image.open('mute1.png'), size=(18,18))
            is_muted = False
        else:
            pygame.mixer.music.set_volume(0.0)
            self.mute_image = ctk.CTkImage(Image.open('mute2.png'), size=(18,18))
            is_muted = True

        self.mute_label = ctk.CTkLabel(self, text='', image=self.mute_image)
        self.mute_button = ctk.CTkButton(self, image=self.mute_image, text='', fg_color='transparent', command=lambda e=None: self.toggle_mute(e), width=15)
        self.mute_button.place(x=5, y=5)


class Left_User_Frame(Left_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.profile_pic = ctk.CTkImage(Image.open('Saurab.png'), size=(500,498))
        self.profile_label = ctk.CTkLabel(self, image=self.profile_pic, text='')
        self.user_img = ctk.CTkImage(Image.open('user.png'))

        self.profile_label.place(relx=0.5, rely=0.47, anchor='center')

        self.welcome_label.configure(text='  Welcome, User', font=('Futura', 20, "bold"), image = self.user_img, compound = 'left')


class Left_Admin_Frame(Left_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.profile_pic = ctk.CTkImage(Image.open('Saurab.png'), size=(500,498))
        self.profile_label = ctk.CTkLabel(self, image=self.profile_pic, text='')

        self.admin_img = ctk.CTkImage(Image.open('admin.png'))
        self.profile_label.place(relx=0.5, rely=0.47, anchor='center')

        self.welcome_label.configure(text=' Welcome, Admin', font=('Futura', 20, "bold"), image = self.admin_img, compound = 'left')


class Right_Frame(ctk.CTkFrame):
    def __init__(self, parent, connection):
        super().__init__(parent, fg_color='#171717', border_width=1, border_color='cyan')
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.get_branch_id()

        self.insert_img = ctk.CTkImage(Image.open('insert.png'))
        self.view_img = ctk.CTkImage(Image.open('view.png'))
        self.delete_img = ctk.CTkImage(Image.open('delete.png'))
        self.update_img = ctk.CTkImage(Image.open('update.png'))

        self.error_img = ctk.CTkImage(Image.open('error.png'))
        self.done_img = ctk.CTkImage(Image.open('done.png'))

        self.create_widgets()
        
    def create_widgets(self):
        self.insert_button = ctk.CTkButton(self, text='Insert Record(s)', corner_radius=13, font=('Helvetica', 16), bg_color= 'transparent',fg_color='black', border_width=1, border_color='#00FFFF', image= self.insert_img, compound= 'left')

        self.view_button = ctk.CTkButton(self, text='View Record(s)', corner_radius=13, font=('Helvetica', 16),bg_color= 'transparent', fg_color='black', border_width=1, border_color='#00FFFF', image= self.view_img, compound= 'left')

        self.delete_button = ctk.CTkButton(self, text='Delete Record(s)', corner_radius=13, font=('Helvetica', 16),bg_color= 'transparent', fg_color='black', border_width=1, border_color='#00FFFF', image= self.delete_img, compound='left')

        self.update_button = ctk.CTkButton(self, text='Update Record(s)', corner_radius=13, font=('Helvetica', 16),bg_color= 'transparent', fg_color='black', border_width=1, border_color='#00FFFF', image= self.update_img, compound= 'left')
        # Layout
        self.relative_w = 0.6
        self.relative_h = 0.11

        self.insert_button.place(relx = 0.5, rely = 0.2, relheight = self.relative_h, relwidth= self.relative_w, anchor ='center')
        self.view_button.place(relx = 0.5, rely = 0.4, relheight = self.relative_h, relwidth= self.relative_w, anchor ='center')
        self.delete_button.place(relx = 0.5, rely = 0.6, relheight = self.relative_h, relwidth= self.relative_w, anchor ='center')
        self.update_button.place(relx = 0.5, rely = 0.8, relheight = self.relative_h, relwidth= self.relative_w, anchor = 'center')

        # Events
        self.insert_button.bind('<Enter>', lambda e: self.expand_btn(e, self.insert_button, 0.2))
        self.insert_button.bind('<Leave>', lambda e: self.contract_btn(e, self.insert_button, 0.2))

        self.view_button.bind('<Enter>', lambda e: self.expand_btn(e, self.view_button, 0.4))
        self.view_button.bind('<Leave>', lambda e: self.contract_btn(e, self.view_button, 0.4))

        self.delete_button.bind('<Enter>', lambda e: self.expand_btn(e, self.delete_button, 0.6))
        self.delete_button.bind('<Leave>', lambda e: self.contract_btn(e, self.delete_button, 0.6))

        self.update_button.bind('<Enter>', lambda e: self.expand_btn(e, self.update_button, 0.8))
        self.update_button.bind('<Leave>', lambda e: self.contract_btn(e, self.update_button, 0.8))

    def expand_btn(self, event, button, rely):
        self.relative_h += 0.0005
        self.relative_w += 0.001
        if self.relative_h <= 0.12:
            button.place(relx = 0.5, rely = rely, relheight = self.relative_h, relwidth= self.relative_w, anchor ='center')
            self.after(2, lambda: self.expand_btn(event, button, rely))
    
    def contract_btn(self, event, button, rely):
        self.relative_h -= 0.0005
        self.relative_w -= 0.001
        if self.relative_h > 0.11:
            button.place(relx = 0.5, rely = rely, relheight = self.relative_h, relwidth= self.relative_w, anchor ='center')
            self.after(2, lambda: self.contract_btn(event, button, rely))

    def get_branch_id(self):
        self.id_list = list()
        
        cursor = self.connection.cursor()
        query = 'select distinct Branch_ID from Room'
        cursor.execute(query)
        result = cursor.fetchall()
        self.id_list = [str(i[0]) for i in result]


class Right_User_Frame(Right_Frame):
    def __init__(self, parent, connection):
        super().__init__(parent, connection)
        self.room_list = list()
        self.connection = connection

        # Disable buttons
        self.view_button.configure(state='disbaled', border_color='grey', fg_color='#1f1f1f')
        self.delete_button.configure(state='disbaled', border_color='grey', fg_color='#1f1f1f')
        self.update_button.configure(state='disbaled', border_color='grey', fg_color='#1f1f1f')

        # Setup command for insertion
        self.insert_button.configure(command=self.user_insert)
        self.view_button.configure(command=None)
        self.view_button.configure(command=None)
        self.view_button.configure(command=None)

    def user_insert(self):
        
        self.user_insert_window = ctk.CTkToplevel()
        self.user_insert_window.title('User Insert')
        self.update()

        center_x = int((self.winfo_screenwidth() - 300) / 2)
        center_y = int((self.winfo_screenheight() - 450) / 2)

        self.user_insert_window.geometry(f'300x450+{center_x}+{center_y}')
        self.user_insert_window.grab_set()

        # list of branches
        # Frame
        frame = ctk.CTkFrame(self.user_insert_window)
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Define grid
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)
        frame.rowconfigure((0,1,2,4,5,6,7), weight=1, uniform='a')
        frame.rowconfigure(3, weight=3)

        # Labels
        self.p_name_label = ctk.CTkLabel(frame, text='Name', font=('Helvetica', 14))
        self.dob_label = ctk.CTkLabel(frame, text='DOB', font=('Helvetica', 14))
        self.sex_label = ctk.CTkLabel(frame, text='Sex', font=('Helvetica', 14))
        self.address_label = ctk.CTkLabel(frame, text='Address', font=('Helvetica', 14))
        self.branch_id_label = ctk.CTkLabel(frame, text='Branch ID', font=('Helvetica', 14))
        self.room_no_label = ctk.CTkLabel(frame, text='Room No.', font=('Helvetica', 14))
        self.error_label = ctk.CTkLabel(frame, text='', text_color='red', font=('Helvetica', 14))

        # Submit Button
        self.submit_button = ctk.CTkButton(frame, text='Submit', command=self.commit_data, fg_color='#144870', text_color='black', hover_color='cyan')

        self.gender_list = ['M', 'F']
        # Textvariables
        self.p_name_var = ctk.StringVar()
        self.dob_var = ctk.StringVar(value='yyyy-mm-dd')
        self.sex_var = ctk.StringVar(value= self.gender_list[0] )
        self.address_var = ctk.StringVar()
        self.branch_id_var = ctk.StringVar( value = self.id_list[0])
        self.room_no_var = ctk.StringVar()

        # Entries
        self.p_name_entry = ctk.CTkEntry(frame, textvariable=self.p_name_var, validatecommand = self.not_null, validate = "focus")
        self.dob_entry = ctk.CTkEntry(frame, textvariable=self.dob_var)
        self.sex_entry = ctk.CTkComboBox(frame, values= self.gender_list, variable=self.sex_var, state='readonly')
        self.address_textbox = ctk.CTkTextbox(frame, font=('Helvetica', 14), fg_color='#343638', height=30, border_color='#565b5e', border_width=2, activate_scrollbars=False)
        # self.branch_id_entry = ctk.CTkEntry(frame, textvariable=self.branch_id_var)
         
        self.branch_id_entry = ctk.CTkComboBox(frame, values= self.id_list, variable= self.branch_id_var, state= 'readonly', command= lambda x : self.get_room_id(self.branch_id_var.get()))

        self.room_no_entry = ctk.CTkComboBox(frame, values= self.room_list, variable=self.room_no_var, state = 'readonly')


        self.dob_entry.configure(validatecommand = lambda : self.validate_dob(self.dob_var.get(),self.dob_entry,self.error_label,
                                                                                                                     self.submit_button), validate = "focusout")
        # Layout
                                                                                                                     
        self.p_name_label.grid(column=0, row=0, sticky='e')
        self.dob_label.grid(column=0, row=1, sticky='e')
        self.sex_label.grid(column=0, row=2, sticky='e')
        self.address_label.grid(column=0, row=3, sticky='e')
        self.branch_id_label.grid(column=0, row=4, sticky='e')
        self.room_no_label.grid(column=0, row=5, sticky='e')

        self.p_name_entry.grid(column=1, row=0, sticky='ew', padx=10)
        self.dob_entry.grid(column=1, row=1, sticky='ew', padx=10)
        self.sex_entry.grid(column=1, row=2, sticky='ew', padx=10)
        self.address_textbox.grid(column=1, row=3, sticky='nsew', padx=10)
        self.branch_id_entry.grid(column=1, row=4, sticky='ew', padx=10)
        self.room_no_entry.grid(column=1, row=5, sticky='ew', padx=10)

        self.error_label.grid(column=0, row=6, columnspan=2)

        self.submit_button.grid(column=0, row=7, columnspan=2)

        # Event
        self.dob_entry.bind('<Button-1>', lambda e: self.dob_entry.delete(0, ctk.END))

    
    def get_room_id(self, b_id):
        self.room_list.clear()
        self.db_dict = {}
        for i in self.id_list:
            self.cursor.execute('select Room_no from Room where Branch_ID = %s', (i))
            self.r1  = self.cursor.fetchall()
            for room in self.r1:
                self.db_dict.setdefault(str(i), []).append(str(room[0]))


        for key in self.db_dict.keys():
            for value in self.db_dict[key]:
                if key == b_id:
                    self.room_list.append(str(value))

        self.room_no_var.set(value= self.room_list[0])
        self.room_no_entry.configure(values = self.room_list, variable = self.room_no_var)

    def not_null(self):
        input = self.p_name_entry.get()
        if  len(input) == 0:
            self.p_name_entry.configure(border_color = 'red')
            self.error_label.configure(text = ' Name cannot be empty', text_color = 'red', image = self.error_img, compound = 'left')
            self.submit_button.configure(state = 'disabled')
            return False
        elif input.isdigit():
            self.p_name_entry.configure(border_color = 'red')
            self.error_label.configure(text = ' Name cannot be a number ', text_color = 'red', image = self.error_img, compound = 'left')
            self.submit_button.configure(state = 'disabled')

            return False
        else:
            self.p_name_entry.configure(border_color = 'green')
            self.submit_button.configure(state = 'normal')
            self.error_label.configure(text = ' ', text_color = 'green', image = self.done_img, compound = 'left')
            return True
        
    def commit_data(self):
        cursor = self.connection.cursor()
        query = 'INSERT INTO patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values (%s, %s, %s, %s, %s, %s)'
        self.address_var.set(self.address_textbox.get('1.0', ctk.END))
        try:
            values = (self.p_name_var.get(), self.dob_var.get(), self.sex_var.get(), self.address_var.get(), int(self.branch_id_var.get()), int(self.room_no_var.get()))
            cursor.execute(query, values)
        except err.MySQLError as e:
            if e.args[0] == 1644:
                self.room_no_entry.configure(border_color = 'red')
                # self.submit_button.configure(state = 'disbaled')
                self.error_label.configure(text = 'Room Occupied!', text_color = 'red', image = self.error_img, compound = 'left')
                
            if e.args[0] == 1048:
                if (self.p_name_entry.get()).isdigit():
                     self.p_name_entry.configure(border_color = 'red')
                     self.error_label.configure(text = ' Name cannot be a number ', text_color = 'red', image = self.error_img, compound = 'left')

                else:
                    self.p_name_entry.configure(border_color = 'red')
                    self.error_label.configure(text = ' Name cannot be empty', text_color = 'red', image = self.error_img, compound = 'left')
                    self.submit_button.configure(state = 'disabled')
        except Exception:
                    self.error_label.configure(text = ' ERROR', text_color = 'red', image = self.error_img, compound = 'left')

        else:
            self.p_name_entry.configure(border_color = 'green')
            self.submit_button.configure(state = 'normal')
            self.error_label.configure(text = ' ', text_color = 'green', image = self.done_img, compound = 'left')

            self.connection.commit()
            self.after(1500, self.user_insert_window.destroy)

    def validate_date(self, input_date, err_widget, err_label, submit):
        try:
            if input_date != datetime.strptime(input_date, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
          
            
        except ValueError:
            err_widget.configure(border_color = 'red')
            err_label.configure(text = ' Invalid Date Format\n Valid Format : yyyy/mm/dd', text_color = 'red', image = self.error_img, compound = 'left')
            return False
        
        else:
            err_widget.configure(border_color = 'green')
            err_label.configure(text = ' ', text_color = 'red', image = self.done_img, compound = 'left')
            submit.configure(state='normal')
            return True

    
    def validate_dob(self, date, err_widget, err_label, submit):

        if (self.validate_date(date, err_widget, err_label, submit)):

            err_widget.configure(border_color = 'green')
            err_label.configure(text = ' ', text_color = 'red', image = self.done_img, compound = 'left')
            submit.configure(state='normal')

            date_enter = datetime.strptime(date, "%Y-%m-%d")    
            curr = datetime.now()

            if date_enter.date() > curr.date():
                err_widget.configure(border_color = 'red')
                err_label.configure(text = "  Invalid Date of Birth",text_color = 'red', image = self.error_img, compound = 'left' )
                submit.configure(state = 'disabled')

                return False
            else:
                err_widget.configure(border_color = 'green')
                err_label.configure(text = " ",text_color = 'red', image = self.done_img, compound = 'left' )
                submit.configure(state = 'normal')
                return True
        

class Right_Admin_Frame(Right_Frame):
    def __init__(self, parent, connection):
        super().__init__(parent, connection)

        self.insert_button.configure(command=lambda: af.Insert(connection))
        self.view_button.configure(command=lambda: af.View(connection))
        self.delete_button.configure(command=lambda: af.Delete(connection))
        self.update_button.configure(command=lambda: af.Update(connection))
