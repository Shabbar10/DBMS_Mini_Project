import customtkinter as ctk
from PIL import Image
import pygame
from pymysql import err

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
        elif user == 'guest':
            self.left_frame = Left_User_Frame(self)
            right_frame = Right_User_Frame(self, self.connection)

        self.left_frame.place(relx=0, rely=0, relwidth=0.69, relheight=1)
        right_frame.place(relx=0.69, rely=0, relwidth=0.31, relheight=1)


class Left_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#333333')
        self.create_widgets()
        self.play_music()
    
    def create_widgets(self):
        self.mute_image = ctk.CTkImage(Image.open('mute.png'), size=(30,30))
        self.mute_label = ctk.CTkLabel(self, text='', image=self.mute_image)
        self.mute_button = ctk.CTkButton(self, image=self.mute_image, text='', fg_color='transparent', command=lambda e=None: self.toggle_mute(e), width=15)

        self.welcome_label = ctk.CTkLabel(self, text='Welcome, whoever')

        self.logout_button = ctk.CTkButton(self)

        # Layout
        self.mute_button.place(x=5, y=5)
        self.welcome_label.place(relx=0.5, rely=0.88, anchor='center')

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("Vega.mp3")
        pygame.mixer.music.play(-1) # Loop indefinitely

    # def stop_music(self):
    #     pygame.mixer.music.stop()

    def toggle_mute(self, event):
        global is_muted
        if is_muted:
            pygame.mixer.music.set_volume(1.0)
            self.mute_image = ctk.CTkImage(Image.open('mute.png'), size=(30,30))
            is_muted = False
        else:
            pygame.mixer.music.set_volume(0.0)
            self.mute_image = ctk.CTkImage(Image.open('sound.png'), size=(30,30))
            is_muted = True

        self.mute_label = ctk.CTkLabel(self, text='', image=self.mute_image)
        self.mute_button = ctk.CTkButton(self, image=self.mute_image, text='', fg_color='transparent', command=lambda e=None: self.toggle_mute(e), width=15)
        self.mute_button.place(x=5, y=5)


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

        self.profile_pic = ctk.CTkImage(Image.open('Saurab.png'), size=(378,504))
        self.profile_label = ctk.CTkLabel(self, image=self.profile_pic, text='')
        self.profile_label.place(relx=0.5, rely=0.43, anchor='center')

        self.welcome_label.configure(text='Welcome, Admin', font=('Consolas', 20, "bold"))


class Right_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        self.insert_button = ctk.CTkButton(self, text='Insert Record(s)', corner_radius=13, font=('Helvetica', 16), fg_color='transparent', border_width=3, border_color='#00FFFF')
        self.view_button = ctk.CTkButton(self, text='View Record(s)', corner_radius=13, font=('Helvetica', 16), fg_color='transparent', border_width=3, border_color='#00FFFF')
        self.delete_button = ctk.CTkButton(self, text='Delete Record(s)', corner_radius=13, font=('Helvetica', 16), fg_color='transparent', border_width=3, border_color='#00FFFF')
        self.update_button = ctk.CTkButton(self, text='Update Record(s)', corner_radius=13, font=('Helvetica', 16), fg_color='transparent', border_width=3, border_color='#00FFFF')

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


class Right_User_Frame(Right_Frame):
    def __init__(self, parent, connection):
        super().__init__(parent)

        self.connection = connection

        # Disable buttons
        self.view_button.configure(state='disbaled', border_color='black', fg_color='#1f1f1f')
        self.delete_button.configure(state='disbaled', border_color='black', fg_color='#1f1f1f')
        self.update_button.configure(state='disbaled', border_color='black', fg_color='#1f1f1f')

        # Setup command for insertion
        self.insert_button.configure(command=self.user_insert)

    def user_insert(self):
        self.user_insert_window = ctk.CTkToplevel()
        self.user_insert_window.title('User Insert')
        self.user_insert_window.geometry('300x450')
        self.user_insert_window.grab_set()

        # Frame
        frame = ctk.CTkFrame(self.user_insert_window)
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Define grid
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)
        frame.rowconfigure((0,1,2,4,5,6,7), weight=1, uniform='a')
        frame.rowconfigure(3, weight=3)

        # Labels
        p_name_label = ctk.CTkLabel(frame, text='Name', font=('Helvetica', 14))
        dob_label = ctk.CTkLabel(frame, text='DOB', font=('Helvetica', 14))
        sex_label = ctk.CTkLabel(frame, text='Sex', font=('Helvetica', 14))
        address_label = ctk.CTkLabel(frame, text='Address', font=('Helvetica', 14))
        branch_id_label = ctk.CTkLabel(frame, text='Branch ID', font=('Helvetica', 14))
        room_no_label = ctk.CTkLabel(frame, text='Room No.', font=('Helvetica', 14))
        self.error_label = ctk.CTkLabel(frame, text='', text_color='red', font=('Helvetica', 14))

        # Submit Button
        submit_button = ctk.CTkButton(frame, text='Submit', command=self.commit_data, fg_color='#144870', text_color='black', hover_color='cyan')

        # Textvariables
        self.p_name_var = ctk.StringVar()
        self.dob_var = ctk.StringVar(value='yyyy/mm/dd')
        self.sex_var = ctk.StringVar()
        self.address_var = ctk.StringVar()
        self.branch_id_var = ctk.StringVar()
        self.room_no_var = ctk.StringVar()

        # Entries
        p_name_entry = ctk.CTkEntry(frame, textvariable=self.p_name_var)
        dob_entry = ctk.CTkEntry(frame, textvariable=self.dob_var)
        sex_entry = ctk.CTkEntry(frame, textvariable=self.sex_var)
        self.address_textbox = ctk.CTkTextbox(frame, font=('Helvetica', 14), fg_color='#343638', height=30, border_color='#565b5e', border_width=2, activate_scrollbars=False)
        branch_id_entry = ctk.CTkEntry(frame, textvariable=self.branch_id_var)
        room_no_entry = ctk.CTkEntry(frame, textvariable=self.room_no_var)

        # Layout
        p_name_label.grid(column=0, row=0, sticky='e')
        dob_label.grid(column=0, row=1, sticky='e')
        sex_label.grid(column=0, row=2, sticky='e')
        address_label.grid(column=0, row=3, sticky='e')
        branch_id_label.grid(column=0, row=4, sticky='e')
        room_no_label.grid(column=0, row=5, sticky='e')

        p_name_entry.grid(column=1, row=0, sticky='ew', padx=10)
        dob_entry.grid(column=1, row=1, sticky='ew', padx=10)
        sex_entry.grid(column=1, row=2, sticky='ew', padx=10)
        self.address_textbox.grid(column=1, row=3, sticky='nsew', padx=10)
        branch_id_entry.grid(column=1, row=4, sticky='ew', padx=10)
        room_no_entry.grid(column=1, row=5, sticky='ew', padx=10)

        self.error_label.grid(column=0, row=6, columnspan=2)

        submit_button.grid(column=0, row=7, columnspan=2)

        # Event
        dob_entry.bind('<Button-1>', lambda e: dob_entry.delete(0, ctk.END))

    def commit_data(self):
        cursor = self.connection.cursor()
        query = 'INSERT INTO patient(P_name, DOB, Sex, Address, Branch_ID, Room_no) values (%s, %s, %s, %s, %s, %s)'
        self.address_var.set(self.address_textbox.get('1.0', ctk.END))
        try:
            values = (self.p_name_var.get(), self.dob_var.get(), self.sex_var.get(), self.address_var.get(), int(self.branch_id_var.get()), int(self.room_no_var.get()))
            cursor.execute(query, values)
        except err.DataError as e:
           print(f'ERROR1: {e}')
        except err.IntegrityError as e: # Handles NOT NULL (1048), Branch or room not found (1216)
            print(f'ERROR2: {e}')
            error_code = e.args[0]

            if error_code == 1048:
                pass

            self.error_label.configure(text='ERR hai laude')
        except err.OperationalError as e: # Handles Room is full (Capacity !> 0) (1644)
            print(f'ERROR3: {e}')
        except err.InternalError as e:
            print(f'ERROR4: {e}')
        except err.ProgrammingError as e:
            print(f'ERROR5: {e}')
        except err.NotSupportedError as e:
            print(f'ERROR6: {e}')
        except ValueError as e:
            print(f'ERROR7: {e}')
        except TypeError as e:
            print(f'ERROR8: {e}')
        except AttributeError as e:
            print(f'ERROR9: {e}')
        except Exception as e:
            print(f'ERROR10: {e}')
        else:
            self.connection.commit()
            self.error_label.configure(text='Entry Recorded', text_color='green')
            self.after(1500, self.user_insert_window.destroy)
        

'''
    except err.MySQLError as e:
            error_code = e.args[0]

            if error_code == 1644:                                          # Room availability <= 0
                print(f'ERROR: {error_code}')
            elif error_code == 1452:                                        # Branch ID or Room No not found
                print(f'ERROR: {error_code}')
            elif error_code == 1048:                                        # Not null violated
                print(f'ERROR: {error_code}')
            elif error_code == 3819:                                        # Check constraint violated
                print(f'ERROR: {error_code}')
            elif error_code == 1062:                                        # Duplicate entry
                print(f'ERROR: {error_code}')
            else:
                print(f'ERROR: {error_code}')
        else:
'''

class Right_Admin_Frame(Right_Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Setup commands for all buttons