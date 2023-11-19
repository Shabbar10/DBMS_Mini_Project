import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from datetime import datetime

class Insert(ctk.CTkToplevel):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

        self.update()

        center_x = int((self.winfo_screenwidth() - 600) / 2)
        center_y = int((self.winfo_screenheight() - 350) / 2)

        self.geometry(f'700x350+{center_x}+{center_y}')
        self.title('Admin Insert')
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        self.tabs = ctk.CTkTabview(self, command=lambda e=None: self.change_size(e))
        self.hospital = self.tabs.add('Hospital')

        self.employee = self.tabs.add('Employee')
        self.emp_frame = ctk.CTkFrame(self.employee)
        
        self.doc_nurse_frame = ctk.CTkFrame(self.employee)
        self.employee_tabs = ctk.CTkTabview(self.doc_nurse_frame)
        self.doc = self.employee_tabs.add('Doctor')
        self.nurse = self.employee_tabs.add('Nurse')

        self.room = self.tabs.add('Room')
        self.patient = self.tabs.add('Patient')
        self.patient_records = self.tabs.add('Patient Record')
        self.treatment = self.tabs.add('Treatment')
        self.cares_for = self.tabs.add('Assigned Nurse')

        self.error_img = ctk.CTkImage(Image.open('error.png'))
        self.done_img = ctk.CTkImage(Image.open('done.png'))

        self.hospital_form()
        self.employee_form()
        self.doctor_form()
        self.nurse_form()
        self.room_form()
        self.patient_form()
        self.patient_records_form()
        self.treatment_form()
        self.assigned_nurse_form()

        # Layout
        self.tabs.pack(expand=True, fill='both')
        self.employee_tabs.pack(expand=True, fill='both')
        self.emp_frame.pack(side='left', expand=True, fill='both')
        self.doc_nurse_frame.pack(side='left', expand=True, fill='both')

    def hospital_form(self):
        self.id_list = list()
        self.get_branch_id()        
        # Define grid
        self.hospital.columnconfigure(0, weight=1)
        self.hospital.columnconfigure(1, weight=2)
        self.hospital.rowconfigure((0,1,3),weight=1)
        self.hospital.rowconfigure(2,weight=1) # For address textbox
        self.hospital.rowconfigure(4,weight=1) # For Submit button

        # Textvariables
        branch_id_var = ctk.StringVar()
        branch_name_var = ctk.StringVar()

        # Labels
        branch_id_label = ctk.CTkLabel(self.hospital, text='Branch ID', font=('Helvetica', 14))
        branch_name_label = ctk.CTkLabel(self.hospital, text='Branch Name', font=('Helvetica', 14))
        address_label = ctk.CTkLabel(self.hospital, text='Address', font=('Helvetica', 14))
        self.h_error_label = ctk.CTkLabel(self.hospital, text=' ', text_color='red', font=('Helvetica', 14))
        # Entries
        self.h_branch_id_entry = ctk.CTkEntry(self.hospital, textvariable=branch_id_var,
                                               validatecommand = lambda  : self.check_entry(self.id_list,
                                                                                            self.h_branch_id_entry.get(),
                                                                                            self.h_branch_id_entry,
                                                                                            self.h_error_label,
                                                                                            submit_button), validate = "focusout")
        
        self.h_branch_name_entry = ctk.CTkEntry(self.hospital, textvariable=branch_name_var,
                                                 validatecommand = lambda: self.not_null(submit_button,self.h_branch_name_entry,
                                                                                          self.h_error_label ),
                                                                                         validate = "focusout")
                                                                                                                                     
        self.h_address_textbox = ctk.CTkTextbox(self.hospital, font=('Helvetica', 14), fg_color='#343638', height=100, width=370, border_color='#565b5e', border_width=2, activate_scrollbars=False)

        # Submit button
        submit_button = ctk.CTkButton(self.hospital, text='Submit', command=lambda: self.commit_data('Hospital', ('Branch_ID', 'Branch_Name', 'Address'), (int(branch_id_var.get()), branch_name_var.get(), self.address_textbox.get('1.0', ctk.END))), fg_color='#144870', text_color='black', hover_color='cyan')

        # Layout
        branch_id_label.grid(column=0, row=0, sticky='e')
        branch_name_label.grid(column=0, row=1, sticky='e')
        address_label.grid(column=0, row=2, sticky='e')
        self.h_error_label.grid(column=0, row=3, columnspan = 2, sticky = 'ns')

        self.h_branch_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        self.h_branch_name_entry.grid(column=1, row=1, sticky='ew', padx=50)
        self.h_address_textbox.grid(column=1, row=2, sticky='ew', padx=50)

        submit_button.grid(column=0, row=4, columnspan=2)

    def employee_form(self):
        # Define grid
        self.emp_frame.columnconfigure(0, weight=1)
        self.emp_frame.columnconfigure(1, weight=2)
        self.emp_frame.rowconfigure((0,1,2,3,4,5,6),weight=1)

        # Textvariables
        emp_name_var = ctk.StringVar()
        salary_var = ctk.StringVar()
        doj_var = ctk.StringVar()
        mgr_id_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()

        # Labels
        emp_name_label = ctk.CTkLabel(self.emp_frame, text='Employee Name', font=('Helvetica', 14))
        salary_label = ctk.CTkLabel(self.emp_frame, text='Salary', font=('Helvetica', 14))
        doj_label = ctk.CTkLabel(self.emp_frame, text='DoJ', font=('Helvetica', 14))
        mgr_id_label = ctk.CTkLabel(self.emp_frame, text='Manager ID', font=('Helvetica', 14))
        branch_id_label = ctk.CTkLabel(self.emp_frame, text='Branch ID', font=('Helvetica', 14))
        e_error_label = ctk.CTkLabel(self.emp_frame, text='', font=('Helvetica', 14), text_color= 'red')

        # Entries
        self.e_emp_name_entry = ctk.CTkEntry(self.emp_frame, textvariable=emp_name_var, validatecommand = lambda: self.not_null(submit_button,self.e_emp_name_entry,
                                                                                          e_error_label ),
                                                                                         validate = "focusout")
        self.e_salary_entry = ctk.CTkEntry(self.emp_frame, textvariable=salary_var)
        self.e_doj_entry = ctk.CTkEntry(self.emp_frame, textvariable=doj_var, validatecommand = lambda : self.validate_date(doj_var.get(),self.e_doj_entry,
                                                                                                                              e_error_label,
                                                                                                                               submit_button ), validate = "focusout")

        # Comboboxes
        cursor = self.connection.cursor()

        cursor.execute('SELECT Emp_ID FROM Employee;')
        results = cursor.fetchall()
        emp_id_list = []

        for eid in results:
            emp_id_list.append(str(eid[0]))

        cursor.execute('SELECT Branch_ID FROM Hospital;')
        results = cursor.fetchall()
        branch_id_list = []

        for bid in results:
            branch_id_list.append(str(bid[0]))

        mgr_id_combo = ctk.CTkComboBox(self.emp_frame, values=emp_id_list, variable=mgr_id_var, state = 'readonly')
        branch_id_combo = ctk.CTkComboBox(self.emp_frame, values=branch_id_list, variable=branch_id_var, state = 'readonly')

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.emp_frame, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Employee', ('Emp_Name', 'Salary', 'DOJ', 'MGR_ID', 'Branch_ID'), (emp_name_var.get(), int(salary_var.get()), doj_var.get(), int(mgr_id_var.get()), int(branch_id_var.get()))), 
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')

        # Layout
        emp_name_label.grid(column=0, row=0, sticky='e')
        salary_label.grid(column=0, row=1, sticky='e')
        doj_label.grid(column=0, row=2, sticky='e')
        mgr_id_label.grid(column=0, row=3, sticky='e')
        branch_id_label.grid(column=0, row=4, sticky='e')
        e_error_label.grid(column=0, row=5, sticky='ns', columnspan=2)

        self.e_emp_name_entry.grid(column=1, row=0, sticky='ew', padx=50)
        self.e_salary_entry.grid(column=1, row=1, sticky='ew', padx=50)
        self.e_doj_entry.grid(column=1, row=2, sticky='ew', padx=50)
        mgr_id_combo.grid(column=1, row=3, sticky='ew', padx=50)
        branch_id_combo.grid(column=1, row=4, sticky='ew', padx=50)

        submit_button.grid(column=0, row=6, columnspan=2)

    def doctor_form(self):
        # Define the grid
        self.doc.columnconfigure(0, weight=1)
        self.doc.columnconfigure(1, weight=2)
        self.doc.rowconfigure((0,1,), weight=1)
        self.doc.rowconfigure(2, weight=4)

        # Textvariables
        emp_id_var = ctk.StringVar()
        qualification_var = ctk.StringVar()

        # Labels
        emp_id_label = ctk.CTkLabel(self.doc, text='Employee ID', font=('Helvetica', 14))
        qualification_label = ctk.CTkLabel(self.doc, text='Qualification', font=('Helvetica', 14))

        # Entry
        self.d_qualification_entry = ctk.CTkEntry(self.doc, textvariable=qualification_var)

        # Combobox
        cursor = self.connection.cursor()

        cursor.execute('SELECT Emp_ID from Employee;')
        results = cursor.fetchall()
        emp_id_list = []

        for eid in results:
            emp_id_list.append(str(eid[0]))

        emp_id_combo = ctk.CTkComboBox(self.doc, values=emp_id_list, variable=emp_id_var, state = 'readonly')

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.doc, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Doctor', ('Emp_ID', 'Qualification'), (int(emp_id_var.get()), qualification_var.get())), 
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')

        # Layout
        emp_id_label.grid(column=0, row=0, sticky='e', padx=15)
        qualification_label.grid(column=0, row=1, sticky='e', padx=15)

        emp_id_combo.grid(column=1, row=0, sticky='ew')
        self.d_qualification_entry.grid(column=1, row=1, sticky='ew')

        submit_button.grid(column=0, row=2, columnspan=2, sticky='s', pady='0 27')

    def nurse_form(self):
        # Define the grid
        self.nurse.columnconfigure(0, weight=1)
        self.nurse.columnconfigure(1, weight=2)
        self.nurse.rowconfigure((0,1), weight=1)
        self.nurse.rowconfigure(2, weight=4)

        # Textvariables
        emp_id_var = ctk.StringVar()
        role_var = ctk.StringVar()

        # Labels
        emp_id_label = ctk.CTkLabel(self.nurse, text='Employee ID', font=('Helvetica', 14))
        role_label = ctk.CTkLabel(self.nurse, text='Role', font=('Helvetica', 14))

        # Entry
        self.n_role_entry = ctk.CTkEntry(self.nurse, textvariable=role_var)

        # Combobox
        cursor = self.connection.cursor()

        cursor.execute('SELECT Emp_ID from Employee;')
        results = cursor.fetchall()
        emp_id_list = []

        for eid in results:
            emp_id_list.append(str(eid[0]))

        emp_id_combo = ctk.CTkComboBox(self.nurse, values=emp_id_list, variable=emp_id_var, state = 'readonly')

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.nurse, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Nurse', ('Emp_ID', 'Roles'), (int(emp_id_var.get()), role_var.get())), 
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')

        # Layout
        emp_id_label.grid(column=0, row=0, sticky='e', padx=15)
        role_label.grid(column=0, row=1, sticky='e', padx=15)

        emp_id_combo.grid(column=1, row=0, sticky='ew')
        self.n_role_entry.grid(column=1, row=1, sticky='ew')

        submit_button.grid(column=0, row=2, columnspan=2, sticky='s', pady='0 27')

    def room_form(self):
        # Define the grid
        self.room.columnconfigure(0, weight=1)
        self.room.columnconfigure(1, weight=2)
        self.room.rowconfigure((0,1,2,3,4,5,6), weight=1)

        # Textvariables
        room_no_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()
        room_type_var = ctk.StringVar()
        capactiy_var = ctk.StringVar(value = '0')
        available_var = ctk.StringVar(value = '0')

        # Labels
        room_no_label = ctk.CTkLabel(self.room, text='Room No', font=('Helvetica', 14))
        branch_id_label = ctk.CTkLabel(self.room, text='Branch ID', font=('Helvetica', 14))
        room_type_label = ctk.CTkLabel(self.room, text='Room Type', font=('Helvetica', 14))
        capactiy_label = ctk.CTkLabel(self.room, text='Capacity', font=('Helvetica', 14))
        available_label = ctk.CTkLabel(self.room, text='Availability', font=('Helvetica', 14))
        err_label = ctk.CTkLabel(self.room, text='', font=('Helvetica', 14), text_color='red')

        # Entries
        self.r_room_no_entry = ctk.CTkEntry(self.room)
        self.r_room_type_entry = ctk.CTkEntry(self.room)
        self.r_capactiy_entry = ctk.CTkEntry(self.room, textvariable= capactiy_var)
        self.r_available_entry = ctk.CTkEntry(self.room, textvariable= available_var)

        # Combobox
        cursor = self.connection.cursor()

        cursor.execute('SELECT Branch_ID from Hospital;')
        results = cursor.fetchall()
        branch_id_list = []

        for bid in results:
            branch_id_list.append(str(bid[0]))

        branch_id_combo = ctk.CTkComboBox(self.room, values=branch_id_list, variable=branch_id_var, state = 'readonly')

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.room, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Room', ('Room_no', 'Branch_ID', 'R_Type', 'Capacity', 'Available'), (int(room_no_var.get()), int(branch_id_var.get())), room_type_var.get(), int(capactiy_var.get()), int(available_var.get())), 
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')

        self.r_available_entry.configure(validatecommand = lambda : self.room_details( int(self.r_capactiy_entry.get()),
                                                                                                      int(self.r_available_entry.get()),
                                                                                                      self.r_available_entry,
                                                                                                      err_label,
                                                                                                      submit_button), validate = "focus")
        # Layout
        room_no_label.grid(column=0, row=0, sticky='e')
        branch_id_label.grid(column=0, row=1, sticky='e')
        room_type_label.grid(column=0, row=4, sticky='e')
        capactiy_label.grid(column=0, row=2, sticky='e')
        available_label.grid(column=0, row=3, sticky='e')
        err_label.grid(column=0, row=5, sticky='ns', columnspan = 2)

        self.r_room_no_entry.grid(column=1, row=0, sticky='ew', padx=50)
        branch_id_combo.grid(column=1, row=1, sticky='ew', padx=50)
        self.r_room_type_entry.grid(column=1, row=4, sticky='ew', padx=50)
        self.r_capactiy_entry.grid(column=1, row=2, sticky='ew', padx=50)
        self.r_available_entry.grid(column=1, row=3, sticky='ew', padx=50)

        submit_button.grid(column=0, row=6, columnspan=2)

    def patient_form(self):
        # Define grid
        self.patient.columnconfigure(0, weight=1)
        self.patient.columnconfigure(1, weight=2)
        self.patient.rowconfigure((0,1,2,4,5,6,7), weight=1, uniform='a')
        self.patient.rowconfigure(3, weight=3)

        # Textvariables
        p_name_var = ctk.StringVar()
        dob_var = ctk.StringVar(value='yyyy-mm-dd')
        sex_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()
        room_no_var = ctk.StringVar()

        # Labels
        p_name_label = ctk.CTkLabel(self.patient, text='Name', font=('Helvetica', 14))
        dob_label = ctk.CTkLabel(self.patient, text='DOB', font=('Helvetica', 14))
        sex_label = ctk.CTkLabel(self.patient, text='Sex', font=('Helvetica', 14))
        address_label = ctk.CTkLabel(self.patient, text='Address', font=('Helvetica', 14))
        branch_id_label = ctk.CTkLabel(self.patient, text='Branch ID', font=('Helvetica', 14))
        room_no_label = ctk.CTkLabel(self.patient, text='Room No.', font=('Helvetica', 14))
        self.error_label = ctk.CTkLabel(self.patient, text='', text_color='red', font=('Helvetica', 14))

        # Entries
        p_name_entry = ctk.CTkEntry(self.patient, textvariable=p_name_var)
        dob_entry = ctk.CTkEntry(self.patient, textvariable=dob_var)
        sex_entry = ctk.CTkEntry(self.patient, textvariable=sex_var)
        address_textbox = ctk.CTkTextbox(self.patient, font=('Helvetica', 14), fg_color='#343638', height=30, border_color='#565b5e', border_width=2, activate_scrollbars=False)

        # Comboboxes
        cursor = self.connection.cursor()

        cursor.execute('SELECT Branch_ID, Room_no FROM Room GROUP BY Branch_ID, Room_no;')
        results = cursor.fetchall()

        branch_id_list = []
        my_dict = {}

        for record in results:
            if str(record[0]) not in branch_id_list:
                branch_id_list.append(str(record[0]))

        for bid in branch_id_list:
            cursor.execute(f'SELECT Room_no FROM Room WHERE Branch_ID = {bid}')
            stuff = cursor.fetchall()
            room_no_list = []
            for s in stuff:
                room_no_list.append(str(s[0]))
                
            my_dict[bid] = room_no_list

        branch_id_combo = ctk.CTkComboBox(self.patient, values=branch_id_list, variable=branch_id_var, state = 'readonly')
        room_no_combo = ctk.CTkComboBox(self.patient, values=room_no_list, variable=room_no_var, state = 'readonly')

        cursor.close()

        # Submit Button
        submit_button = ctk.CTkButton(self.patient, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Patient', ('P_Name', 'DOB', 'Sex', 'Address', 'Branch_ID', 'Room_no'), (p_name_var.get(), dob_var.get()), sex_var.get(), address_textbox.get('1.0', ctk.END), int(branch_id_var.get()), int(room_no_var.get())), 
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')

        dob_entry.configure(validatecommand = lambda : self.validate_dob(dob_var.get(),dob_entry,self.error_label,submit_button), validate = "focusout")
        p_name_entry.configure(validatecommand = lambda: self.not_null(submit_button,
                                                                       p_name_entry,
                                                                       self.error_label
                                                                       ), validate = "focus")
        # Layout
        p_name_label.grid(column=0, row=0, sticky='e')
        dob_label.grid(column=0, row=1, sticky='e')
        sex_label.grid(column=0, row=2, sticky='e')
        address_label.grid(column=0, row=3, sticky='e')
        branch_id_label.grid(column=0, row=4, sticky='e')
        room_no_label.grid(column=0, row=5, sticky='e')
        self.error_label.grid(column=0, row=6, sticky='ns', columnspan = 2)

        p_name_entry.grid(column=1, row=0, sticky='ew', padx=50)
        dob_entry.grid(column=1, row=1, sticky='ew', padx=50)
        sex_entry.grid(column=1, row=2, sticky='ew', padx=50)
        address_textbox.grid(column=1, row=3, sticky='nsew', padx=50)
        branch_id_combo.grid(column=1, row=4, sticky='ew', padx=50)
        room_no_combo.grid(column=1, row=5, sticky='ew', padx=50)
        submit_button.grid(column=0, row=7, columnspan=2)

    def patient_records_form(self):
        # Define the grid
        self.patient_records.columnconfigure(0, weight=1)
        self.patient_records.columnconfigure(1, weight=2)
        self.patient_records.rowconfigure((0,1,2,3,4), weight=1)

        # Textvariables
        pid_var = ctk.StringVar()
        treatment_var = ctk.StringVar()
        date_var = ctk.StringVar(value='yyyy/mm/dd')
        bill_var = ctk.StringVar()

        # Labels
        pid_label = ctk.CTkLabel(self.patient_records, text='Patient ID', font=('Helvetica', 14))
        treatment_label = ctk.CTkLabel(self.patient_records, text='Treatment Type', font=('Helvetica', 14))
        date_label = ctk.CTkLabel(self.patient_records, text='Date', font=('Helvetica', 14))
        bill_label = ctk.CTkLabel(self.patient_records, text='Bill', font=('Helvetica', 14))

        # Entries
        self.pr_treatment_entry = ctk.CTkEntry(self.patient_records, textvariable=treatment_var)
        self.pr_date_entry = ctk.CTkEntry(self.patient_records, textvariable=date_var)
        self.pr_bill_entry = ctk.CTkEntry(self.patient_records, textvariable=bill_var)

        # Combobox
        cursor = self.connection.cursor()

        cursor.execute('SELECT PID FROM Patient;')
        results = cursor.fetchall()
        patient_id_list = []

        for pid in results:
            patient_id_list.append(str(pid[0]))

        patient_id_combo = ctk.CTkComboBox(self.patient_records, values=patient_id_list, variable=pid_var, state = 'readonly')

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.patient_records, 
                                      text='Submit', 
                                      command=lambda e=None: self.commit_data('Patient_Records', ['PID', 'Treatment_Type', 'Date', 'Bill'], [int(pid_var.get()), treatment_var.get(), date_var.get(), int(bill_var.get())]),
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')
        
        # Layout
        pid_label.grid(column=0, row=0, sticky='e')
        treatment_label.grid(column=0, row=1, sticky='e')
        date_label.grid(column=0, row=2, sticky='e')
        bill_label.grid(column=0, row=3, sticky='e')

        patient_id_combo.grid(column=1, row=0, sticky='ew', padx=50)
        self.pr_treatment_entry.grid(column=1, row=1, sticky='ew', padx=50)
        self.pr_date_entry.grid(column=1, row=2, sticky='ew', padx=50)
        self.pr_bill_entry.grid(column=1, row=3, sticky='ew', padx=50)

        submit_button.grid(column=0, row=4, columnspan=2)

    def treatment_form(self):
        # Define the grid
        self.treatment.columnconfigure(0, weight=1)
        self.treatment.columnconfigure(1, weight=2)
        self.treatment.rowconfigure((0,1,2,3,4), weight=1)

        # Textvariables
        doc_id_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()
        date_start_var = ctk.StringVar()
        date_end_var = ctk.StringVar()

        # Labels
        doc_id_label = ctk.CTkLabel(self.treatment, text='Doctor ID', font=('Helvetica', 14))
        patient_id_label = ctk.CTkLabel(self.treatment, text='Patient ID', font=('Helvetica', 14))
        date_start_label = ctk.CTkLabel(self.treatment, text='Start date', font=('Helvetica', 14))
        date_end_label = ctk.CTkLabel(self.treatment, text='End date', font=('Helvetica', 14))

        # Entries
        self.t_date_start_entry = ctk.CTkEntry(self.treatment, textvariable=date_start_var)
        self.t_date_end_entry = ctk.CTkEntry(self.treatment, textvariable=date_end_var)

        # Comboboxes
        cursor = self.connection.cursor()

        cursor.execute('SELECT Emp_ID FROM Doctor;')
        results = cursor.fetchall()
        doc_id_list = []

        for eid in results:
            doc_id_list.append(str(eid[0]))

        cursor.execute('SELECT PID FROM Patient;')
        results = cursor.fetchall()
        patient_id_list = []

        for pid in results:
            patient_id_list.append(str(pid[0]))

        doc_id_combo = ctk.CTkComboBox(self.treatment, values=doc_id_list, variable=doc_id_var, state = 'readonly')
        patient_id_combo = ctk.CTkComboBox(self.treatment, values=patient_id_list, variable=patient_id_var, state = 'readonly')

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.treatment, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Treatment', ('Emp_ID', 'PID', 'Date_Start', 'Date_end'), (int(doc_id_var.get()), int(patient_id_var.get()), date_start_var.get(), date_end_var.get())),
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')
        
        # Layout
        doc_id_label.grid(column=0, row=0, sticky='e')
        patient_id_label.grid(column=0, row=1, sticky='e')
        date_start_label.grid(column=0, row=2, sticky='e')
        date_end_label.grid(column=0, row=3, sticky='e')

        doc_id_combo.grid(column=1, row=0, sticky='ew', padx=50)
        patient_id_combo.grid(column=1, row=1, sticky='ew', padx=50)
        self.t_date_start_entry.grid(column=1, row=2, sticky='ew', padx=50)
        self.t_date_end_entry.grid(column=1, row=3, sticky='ew', padx=50)

        submit_button.grid(column=0, row=4, columnspan=2)

    def assigned_nurse_form(self):
        # Define the grid
        self.cares_for.columnconfigure(0, weight=1)
        self.cares_for.columnconfigure(1, weight=2)
        self.cares_for.rowconfigure((0,1,2,3), weight=1)

        # Textvariables
        nurse_id_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()
        shift_var = ctk.StringVar()

        # Labels
        nurse_id_label = ctk.CTkLabel(self.cares_for, text='Nurse ID', font=('Helvetica', 14))
        patient_id_label = ctk.CTkLabel(self.cares_for, text='Patient ID', font=('Helvetica', 14))
        shift_label = ctk.CTkLabel(self.cares_for, text='Shift', font=('Helvetica', 14))

        # Comboboxes
        cursor = self.connection.cursor()

        cursor.execute('SELECT Emp_ID From Nurse;')
        results = cursor.fetchall()
        nurse_id_list = []

        for nid in results:
            nurse_id_list.append(str(nid[0]))

        cursor.execute('SELECT PID From Patient;')
        results = cursor.fetchall()
        patient_id_list = []

        for pid in results:
            patient_id_list.append(str(pid[0]))

        nurse_id_combo = ctk.CTkComboBox(self.cares_for, values=nurse_id_list, variable=nurse_id_var, state = 'readonly')
        patient_id_combo = ctk.CTkComboBox(self.cares_for, values=patient_id_list, variable=patient_id_var, state = 'readonly')
        shift_combo = ctk.CTkComboBox(self.cares_for, values=['Morning', 'Evening'], variable=shift_var, state = 'readonly')

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.cares_for, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Cares_for', ('Emp_ID', 'PID', 'Shift'), (int(nurse_id_var.get()), int(patient_id_var.get()), shift_var.get())),
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')
        
        # Layout
        nurse_id_label.grid(column=0, row=0, sticky='e')
        patient_id_label.grid(column=0, row=1, sticky='e')
        shift_label.grid(column=0, row=2, sticky='e')

        nurse_id_combo.grid(column=1, row=0, sticky='ew', padx=50)
        patient_id_combo.grid(column=1, row=1, sticky='ew', padx=50)
        shift_combo.grid(column=1, row=2, sticky='ew', padx=50)

        submit_button.grid(column=0, row=3, columnspan=2)

    def commit_data(self, table, cols, values):
        cursor = self.connection.cursor()
        format_specifier = '%s'
        for i in range(len(cols) - 1):
            if i == range(len(cols) - 1):
                format_specifier += ' %s'
            else:
                format_specifier += ', %s'

        query = "INSERT INTO {}({}) values ({})".format(table, ', '.join(cols), format_specifier)

        cursor.execute(query, values)
        self.connection.commit()
        self.after(1500, self.destroy)

    def change_size(self, event):
        center_x = int((self.winfo_screenwidth() - 700) / 2)

        if self.tabs.get() == 'Hospital':
            center_y = int((self.winfo_screenheight() - 350) / 2)
            print('Hospital')
            self.geometry(f'700x350+{center_x}+{center_y}')

        elif self.tabs.get() == 'Employee':
            center_y = int((self.winfo_screenheight() - 650) / 2)
            print('Employee')
            self.geometry(f'700x650+{center_x}+{center_y}')

        elif self.tabs.get() == 'Room':
            center_y = int((self.winfo_screenheight() - 350) / 2)
            print('Room')
            self.geometry(f'700x350+{center_x}+{center_y}')

        elif self.tabs.get() == 'Patient':
            center_y = int((self.winfo_screenheight() - 450) / 2)
            print('Patient')
            self.geometry(f'700x450+{center_x}+{center_y}')
        
        elif self.tabs.get() == 'Patient Record':
            center_y = int((self.winfo_screenheight() - 350) / 2)
            print('Patient Records')
            self.geometry(f'700x350+{center_x}+{center_y}')

        elif self.tabs.get() == 'Treatment':
            center_y = int((self.winfo_screenheight() - 350) / 2)
            print('Hospital')
            self.geometry(f'700x350+{center_x}+{center_y}')

        elif self.tabs.get() == 'Assigned Nurse':
            center_y = int((self.winfo_screenheight() - 350) / 2)
            print('Hospital')
            self.geometry(f'700x350+{center_x}+{center_y}')

    def not_null(self, submit, err_widget, label):
        input = err_widget.get()
        if  len(input) == 0:
            err_widget.configure(border_color = 'red')
            label.configure(text=' Name cannot be empty', text_color = 'red', image = self.error_img, compound = 'left')
            submit.configure(state = 'disabled')
            return False
        
        elif input.isdigit():
            err_widget.configure(border_color = 'red')
            label.configure(text=' Name cannot be a number ', text_color = 'red', image = self.error_img, compound = 'left')
            submit.configure(state = 'disabled')

            return False
        else:
                err_widget.configure(border_color = 'green')
            # self.submit_button.configure(state = 'normal')
                label.configure(text = ' ', text_color = 'green', image = self.done_img, compound = 'left')
                return True
    
    def check_entry(self, check_list, target, err_widget, label, submit):
        if len(target) == 0:
                err_widget.configure(border_color = 'red')
                label.configure(text = ' Entry cannot be NULL', text_color = 'red', image = self.error_img, compound = 'left')
                submit.configure(state = 'disabled')
                return False
        
        else:
                for i in check_list:
                    if target != i:
                        check = True
                    elif target == i:
                        check = False
                        break
            
                if check == False:
                        err_widget.configure(border_color = 'red')
                        label.configure(text = ' Duplicate entry', text_color = 'red', image = self.error_img, compound = 'left')
                        submit.configure(state = 'disabled')

                        return False

                elif check == True:
                        err_widget.configure(border_color = 'green')
                        label.configure(text = ' ', text_color = 'green', image = self.done_img, compound = 'left')
                        submit.configure(state = 'normal')
                        return True

        self.id_list.clear()
        self.get_branch_id()

    def get_branch_id(self):
                self.id_list.clear()
                self.cursor1 = self.connection.cursor()
                self.cursor1.execute('select distinct Branch_ID from Room')
                result = self.cursor1.fetchall()
                self.id_list = [str(i[0]) for i in result]

    def get_room_id(self, b_id):
        self.room_list.clear()
        self.db_dict = {}
        for i in self.id_list:
            self.cursor1.execute('select Room_no from Room where Branch_ID = %s', (i))
            self.r1  = self.cursor1.fetchall()
            for room in self.r1:
                self.db_dict.setdefault(str(i), []).append(str(room[0]))


        for key in self.db_dict.keys():
            for value in self.db_dict[key]:
                if key == b_id:
                    self.room_list.append(str(value))

        self.room_no_var.set(value= self.room_list[0])
        self.room_no_entry.configure(values = self.room_list, variable = self.room_no_var)        

    def room_details(self, capacity, available, err_widget, err_label, submit):
       submit.configure(state = 'disabled')
       
       if available > capacity:
           err_widget.configure(border_color = 'red')
           err_label.configure(text = ' Availability cannot exceed capacity', text_color = 'red', image = self.error_img, compound = 'left')
           submit.configure(state = 'disabled')
           return False
         
       elif available <= capacity:
           submit.configure(state = 'normal')
           err_widget.configure(border_color = 'green')
           err_label.configure(text = ' ', text_color = 'red', image = self.done_img, compound = 'left')
           return True

    def validate_date(self, input_date, err_widget, err_label, submit):
        try:
            if input_date != datetime.strptime(input_date, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
          
        except ValueError:
            err_widget.configure(border_color = 'red')
            err_label.configure(text = ' Invalid Date Format\n Valid Format : yyyy/mm/dd', text_color = 'red', image = self.error_img, compound = 'left')
            submit.configure(state='disabled')
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
    

class View(ctk.CTkToplevel):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

        self.update()

        center_x = int((self.winfo_screenwidth() - 550) / 2)
        center_y = int((self.winfo_screenheight() - 350) / 2)

        self.geometry(f'550x350+{center_x}+{center_y}')
        self.title('Admin View')
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        self.choice_frame = ctk.CTkFrame(self)
        self.view_frame = ctk.CTkFrame(self, fg_color='#f0f0f0')

        # Choice Tabs
        self.tabs = ctk.CTkTabview(self.choice_frame)
        self.hospital = self.tabs.add('Hospital')

        self.employee = self.tabs.add('Employee')
        self.emp_frame = ctk.CTkFrame(self.employee)
        self.doc_nurse_frame = ctk.CTkFrame(self.employee)
        self.doc_nurse_tabs = ctk.CTkTabview(self.doc_nurse_frame)
        self.doc = self.doc_nurse_tabs.add('Doctor')
        self.nurse = self.doc_nurse_tabs.add('Nurse')

        self.room = self.tabs.add('Room')
        self.patient = self.tabs.add('Patient')
        self.patient_records = self.tabs.add('Patient Record')
        self.treatment = self.tabs.add('Treatment')
        self.cares_for = self.tabs.add('Assigned Nurse')

        self.hospital_choice()
        self.employee_choice()
        self.doc_choice()
        self.nurse_choice()
        self.room_choice()
        self.patient_choice()
        self.patient_records_choice()
        self.treatment_choice()
        self.assigned_nurse_choice()

        # Layout
        self.choice_frame.pack(expand=True, fill='both')
        self.tabs.pack(expand=True, fill='both')
        self.emp_frame.pack(expand=True, fill='both', side='left')
        self.doc_nurse_tabs.pack(expand=True, fill='both')
        self.doc_nurse_frame.pack(expand=True, fill='both', side='left')

    def hospital_choice(self):
        # Define the grid
        self.hospital.columnconfigure(0, weight=1, uniform='a')
        self.hospital.columnconfigure(1, weight=2)
        self.hospital.rowconfigure((0,1,2,3), weight=1, uniform='a')

        # Variables
        branch_id_var = ctk.StringVar()
        branch_name_var = ctk.StringVar()
        address_var = ctk.StringVar()

        # Textvariables
        branch_id_where = ctk.StringVar()
        branch_name_where = ctk.StringVar()
        address_where = ctk.StringVar()

        # Checkboxes
        branch_id_check = ctk.CTkCheckBox(self.hospital, text='Branch ID', variable=branch_id_var, onvalue='Branch_ID', offvalue='', command=lambda: self.toggle_entry(branch_id_var.get(), branch_id_entry))
        branch_name_check = ctk.CTkCheckBox(self.hospital, text='Branch Name', variable=branch_name_var, onvalue='Branch_Name', offvalue='', command=lambda: self.toggle_entry(branch_name_var.get(), branch_name_entry))
        address_check = ctk.CTkCheckBox(self.hospital, text='Address', variable=address_var, onvalue='Address', offvalue='', command=lambda: self.toggle_entry(address_var.get(), address_entry))

        # Entries
        branch_id_entry = ctk.CTkEntry(self.hospital, textvariable=branch_id_where, state='disabled')
        branch_name_entry = ctk.CTkEntry(self.hospital, textvariable=branch_name_where, state='disabled')
        address_entry = ctk.CTkEntry(self.hospital, textvariable=address_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.hospital,
                                         text='Show',
                                         command=lambda e=None: self.fetch_records('Hospital', (branch_id_var.get(), branch_name_var.get(), address_var.get()), (branch_id_where.get(), branch_name_where.get(), address_where.get())))

        # Layout
        branch_id_check.grid(column=0, row=0, sticky='w')
        branch_name_check.grid(column=0, row=1, sticky='w')
        address_check.grid(column=0, row=2, sticky='w')

        branch_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        branch_name_entry.grid(column=1, row=1, sticky='ew', padx=50)
        address_entry.grid(column=1, row=2, sticky='ew', padx=50)

        show_button.grid(column=0, row=3, columnspan=2)

    def employee_choice(self):
        # Define the grid
        self.emp_frame.columnconfigure(0, weight=1)
        self.emp_frame.columnconfigure(1, weight=2)
        self.emp_frame.rowconfigure((0,1,2,3,4,5,6), weight=1)

        # Variables
        emp_id_var = ctk.StringVar()
        emp_name_var = ctk.StringVar()
        salary_var = ctk.StringVar()
        doj_var = ctk.StringVar()
        mgr_id_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()

        # Textvariables
        emp_id_where = ctk.StringVar()
        emp_name_where = ctk.StringVar()
        salary_where = ctk.StringVar()
        doj_where = ctk.StringVar()
        mgr_id_where = ctk.StringVar()
        branch_id_where = ctk.StringVar()

        # Checkboxes
        emp_id_check = ctk.CTkCheckBox(self.emp_frame, text='Employee ID', variable=emp_id_var, onvalue='Emp_ID', offvalue='', command=lambda: self.toggle_entry(emp_id_var.get(), emp_id_entry))
        emp_name_check = ctk.CTkCheckBox(self.emp_frame, text='Employee Name', variable=emp_name_var, onvalue='Emp_Name', offvalue='', command=lambda: self.toggle_entry(emp_name_var.get(), emp_name_entry))
        salary_check = ctk.CTkCheckBox(self.emp_frame, text='Salary', variable=salary_var, onvalue='Salary', offvalue='', command=lambda: self.toggle_entry(salary_var.get(), salary_entry))
        doj_check = ctk.CTkCheckBox(self.emp_frame, text='DOJ', variable=doj_var, onvalue='DOJ', offvalue='', command=lambda: self.toggle_entry(doj_var.get(), doj_entry))
        mgr_id_check = ctk.CTkCheckBox(self.emp_frame, text='Manager ID', variable=mgr_id_var, onvalue='MGR_ID', offvalue='', command=lambda: self.toggle_entry(mgr_id_var.get(), mgr_id_entry))
        branch_id_check = ctk.CTkCheckBox(self.emp_frame, text='Branch ID', variable=branch_id_var, onvalue='Branch_ID', offvalue='', command=lambda: self.toggle_entry(branch_id_var.get(), branch_id_entry))

        # Entries
        emp_id_entry = ctk.CTkEntry(self.emp_frame, textvariable=emp_id_where, state='disabled')
        emp_name_entry = ctk.CTkEntry(self.emp_frame, textvariable=emp_name_where, state='disabled')
        salary_entry = ctk.CTkEntry(self.emp_frame, textvariable=salary_where, state='disabled')
        doj_entry = ctk.CTkEntry(self.emp_frame, textvariable=doj_where, state='disabled')
        mgr_id_entry = ctk.CTkEntry(self.emp_frame, textvariable=mgr_id_where, state='disabled')
        branch_id_entry = ctk.CTkEntry(self.emp_frame, textvariable=branch_id_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.emp_frame,
                                         text='Show',
                                         command=lambda e=None: self.fetch_records('Employee', (emp_id_var.get(), emp_name_var.get(), salary_var.get(), doj_var.get(), mgr_id_var.get(), branch_id_var.get()), (emp_id_where.get(), emp_name_where.get(), salary_where.get(), doj_where.get(), mgr_id_where.get(), branch_id_where.get())))
        
        # Layout
        emp_id_check.grid(column=0, row=0, sticky='w')
        emp_name_check.grid(column=0, row=1, sticky='w')
        salary_check.grid(column=0, row=2, sticky='w')
        doj_check.grid(column=0, row=3, sticky='w')
        mgr_id_check.grid(column=0, row=4, sticky='w')
        branch_id_check.grid(column=0, row=5, sticky='w')

        emp_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        emp_name_entry.grid(column=1, row=1, sticky='ew', padx=50)
        salary_entry.grid(column=1, row=2, sticky='ew', padx=50)
        doj_entry.grid(column=1, row=3, sticky='ew', padx=50)
        mgr_id_entry.grid(column=1, row=4, sticky='ew', padx=50)
        branch_id_entry.grid(column=1, row=5, sticky='ew', padx=50)

        show_button.grid(column=0, row=6, columnspan=2)

    def doc_choice(self):
        # Define the grid
        self.doc.columnconfigure(0, weight=1)
        self.doc.columnconfigure(1, weight=2)
        self.doc.rowconfigure((0,1,2), weight=1)

        # Variables
        emp_id_var = ctk.StringVar()
        qualification_var = ctk.StringVar()

        # Textvariables
        emp_id_where = ctk.StringVar()
        qualification_where = ctk.StringVar()

        # Checkboxes
        emp_id_check = ctk.CTkCheckBox(self.doc, text='Doctor ID', variable=emp_id_var, onvalue='Emp_ID', offvalue='', command=lambda: self.toggle_entry(emp_id_var.get(), emp_id_entry))
        qualification_check = ctk.CTkCheckBox(self.doc, text='Qualification', variable=emp_id_var, onvalue='Qualification', offvalue='', command=lambda: self.toggle_entry(qualification_var.get(), qualification_entry))

        # Entries
        emp_id_entry = ctk.CTkEntry(self.doc, textvariable=emp_id_where, state='disabled')
        qualification_entry = ctk.CTkEntry(self.doc, textvariable=qualification_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.doc,
                                         text='Show',
                                         command=lambda e=None: self.fetch_records('Doctor', (emp_id_var.get(), qualification_var.get()), (emp_id_where.get(), qualification_where.get())))

        # Layout
        emp_id_check.grid(column=0, row=0, sticky='w')
        qualification_check.grid(column=0, row=1, sticky='w')

        emp_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        qualification_entry.grid(column=1, row=1, sticky='ew', padx=50)

        show_button.grid(column=0, row=2, columnspan=2)

    def nurse_choice(self):
        # Define the grid
        self.nurse.columnconfigure(0, weight=1)
        self.nurse.columnconfigure(1, weight=2)
        self.nurse.rowconfigure((0,1,2), weight=1)

        # Variables
        emp_id_var = ctk.StringVar()
        role_var = ctk.StringVar()

        # Textvariables
        emp_id_where = ctk.StringVar()
        role_where = ctk.StringVar()

        # Checkboxes
        emp_id_check = ctk.CTkCheckBox(self.nurse, text='Nurse ID', variable=emp_id_var, onvalue='Emp_ID', offvalue='', command=lambda: self.toggle_entry(emp_id_var.get(), emp_id_entry))
        role_check = ctk.CTkCheckBox(self.nurse, text='Qualification', variable=emp_id_var, onvalue='Role', offvalue='', command=lambda: self.toggle_entry(role_var.get(), role_entry))

        # Entries
        emp_id_entry = ctk.CTkEntry(self.nurse, textvariable=emp_id_where, state='disabled')
        role_entry = ctk.CTkEntry(self.nurse, textvariable=role_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.nurse,
                                         text='Show',
                                         command=lambda e=None: self.fetch_records('Nurse', (emp_id_var.get(), role_var.get()), (emp_id_where.get(), role_where.get())))

        # Layout
        emp_id_check.grid(column=0, row=0, sticky='w')
        role_check.grid(column=0, row=1, sticky='w')

        emp_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        role_entry.grid(column=1, row=1, sticky='ew', padx=50)

        show_button.grid(column=0, row=2, columnspan=2)

    def room_choice(self):
        # Define the grid
        self.room.columnconfigure(0, weight=1)
        self.room.columnconfigure(1, weight=2)
        self.room.rowconfigure((0,1,2,3,4,5), weight=1)

        # Variables
        room_no_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()
        room_type_var = ctk.StringVar()
        capacity_var = ctk.StringVar()
        availability_var = ctk.StringVar()

        # Textvariables
        room_no_where = ctk.StringVar()
        branch_id_where = ctk.StringVar()
        room_type_where = ctk.StringVar()
        capacity_where = ctk.StringVar()
        availability_where = ctk.StringVar()

        # Checkboxes
        room_no_check = ctk.CTkCheckBox(self.room, text='Room No', variable=room_no_var, onvalue='Room_no', offvalue='', command=lambda: self.toggle_entry(room_no_var.get(), room_no_entry))
        branch_id_check = ctk.CTkCheckBox(self.room, text='Branch ID', variable=branch_id_var, onvalue='Branch_ID', offvalue='', command=lambda: self.toggle_entry(branch_id_var.get(), branch_id_entry))
        room_type_check = ctk.CTkCheckBox(self.room, text='Room Type', variable=room_type_var, onvalue='R_Type', offvalue='', command=lambda: self.toggle_entry(room_type_var.get(), room_type_entry))
        capacity_check = ctk.CTkCheckBox(self.room, text='Capacity', variable=capacity_var, onvalue='Capacity', offvalue='', command=lambda: self.toggle_entry(capacity_var.get(), capacity_entry))
        availability_check = ctk.CTkCheckBox(self.room, text='Available', variable=availability_var, onvalue='Available', offvalue='', command=lambda: self.toggle_entry(availability_var.get(), availability_entry))

        # Entries
        room_no_entry = ctk.CTkEntry(self.room, textvariable=room_no_where, state='disabled')
        branch_id_entry = ctk.CTkEntry(self.room, textvariable=branch_id_where, state='disabled')
        room_type_entry = ctk.CTkEntry(self.room, textvariable=room_type_where, state='disabled')
        capacity_entry = ctk.CTkEntry(self.room, textvariable=capacity_where, state='disabled')
        availability_entry = ctk.CTkEntry(self.room, textvariable=availability_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.room,
                                         text='Show',
                                         command=lambda e=None: self.fetch_records('Room', (room_no_var.get(), branch_id_var.get(), room_type_var.get(), capacity_var.get(), availability_var.get()), (room_no_where.get(), branch_id_where.get(), room_type_where.get(), capacity_where.get(), availability_where.get())))

        # Layout
        room_no_check.grid(column=0, row=0, sticky='w')
        branch_id_check.grid(column=0, row=1, sticky='w')
        room_type_check.grid(column=0, row=2, sticky='w')
        capacity_check.grid(column=0, row=3, sticky='w')
        availability_check.grid(column=0, row=4, sticky='w')

        room_no_entry.grid(column=1, row=0, sticky='ew', padx=50)
        branch_id_entry.grid(column=1, row=1, sticky='ew', padx=50)
        room_type_entry.grid(column=1, row=2, sticky='ew', padx=50)
        capacity_entry.grid(column=1, row=3, sticky='ew', padx=50)
        availability_entry.grid(column=1, row=4, sticky='ew', padx=50)

        show_button.grid(column=0, row=5, columnspan=2)

    def patient_choice(self):
        # Define the grid
        self.patient.columnconfigure(0, weight=1)
        self.patient.columnconfigure(1, weight=2)
        self.patient.rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        # Variables
        patient_id_var = ctk.StringVar()
        patient_name_var = ctk.StringVar()
        dob_var = ctk.StringVar()
        sex_var = ctk.StringVar()
        address_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()
        room_no_var = ctk.StringVar()

        # Textvariables
        patient_id_where = ctk.StringVar()
        patient_name_where = ctk.StringVar()
        dob_where = ctk.StringVar()
        sex_where = ctk.StringVar()
        address_where = ctk.StringVar()
        branch_id_where = ctk.StringVar()
        room_no_where = ctk.StringVar()

        # Checkboxes
        patient_id_check = ctk.CTkCheckBox(self.patient, text='Patient ID', variable=patient_id_var, onvalue='PID', offvalue='', command=lambda: self.toggle_entry(patient_id_var.get(), patient_id_entry))
        patient_name_check = ctk.CTkCheckBox(self.patient, text='Patient Name', variable=patient_name_var, onvalue='P_Name', offvalue='', command=lambda: self.toggle_entry(patient_name_var.get(), patient_name_entry))
        dob_check = ctk.CTkCheckBox(self.patient, text='DOB', variable=dob_var, onvalue='DOB', offvalue='', command=lambda: self.toggle_entry(dob_var.get(), dob_entry))
        sex_check = ctk.CTkCheckBox(self.patient, text='Sex', variable=sex_var, onvalue='Sex', offvalue='', command=lambda: self.toggle_entry(sex_var.get(), sex_entry))
        address_check = ctk.CTkCheckBox(self.patient, text='Address', variable=address_var, onvalue='Address', offvalue='', command=lambda: self.toggle_entry(address_var.get(), address_entry))
        branch_id_check = ctk.CTkCheckBox(self.patient, text='Branch ID', variable=branch_id_var, onvalue='Branch_ID', offvalue='', command=lambda: self.toggle_entry(branch_id_var.get(), branch_id_entry))
        room_no_check = ctk.CTkCheckBox(self.patient, text='Room No', variable=room_no_var, onvalue='Room_no', offvalue='', command=lambda: self.toggle_entry(room_no_var.get(), room_no_entry))

        # Entries
        patient_id_entry = ctk.CTkEntry(self.patient, textvariable=patient_id_where, state='disabled')
        patient_name_entry = ctk.CTkEntry(self.patient, textvariable=patient_name_where, state='disabled')
        dob_entry = ctk.CTkEntry(self.patient, textvariable=dob_where, state='disabled')
        sex_entry = ctk.CTkEntry(self.patient, textvariable=sex_where, state='disabled')
        address_entry = ctk.CTkEntry(self.patient, textvariable=address_where, state='disabled')
        branch_id_entry = ctk.CTkEntry(self.patient, textvariable=branch_id_where, state='disabled')
        room_no_entry = ctk.CTkEntry(self.patient, textvariable=room_no_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.patient,
                                    text='Show',
                                    command=lambda e=None: self.fetch_records('Patient', (patient_id_var.get(), patient_name_var.get(), dob_var.get(), sex_var.get(), address_var.get(), branch_id_var.get(), room_no_var.get()), (patient_id_where.get(), patient_name_where.get(), dob_where.get(), sex_where.get(), address_where.get(), branch_id_where.get(), room_no_where.get())))

        # Layout
        patient_id_check.grid(column=0, row=0, sticky='w')
        patient_name_check.grid(column=0, row=1, sticky='w')
        dob_check.grid(column=0, row=2, sticky='w')
        sex_check.grid(column=0, row=3, sticky='w')
        address_check.grid(column=0, row=4, sticky='w')
        branch_id_check.grid(column=0, row=5, sticky='w')
        room_no_check.grid(column=0, row=6, sticky='w')

        patient_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        patient_name_entry.grid(column=1, row=1, sticky='ew', padx=50)
        dob_entry.grid(column=1, row=2, sticky='ew', padx=50)
        sex_entry.grid(column=1, row=3, sticky='ew', padx=50)
        address_entry.grid(column=1, row=4, sticky='ew', padx=50)
        branch_id_entry.grid(column=1, row=5, sticky='ew', padx=50)
        room_no_entry.grid(column=1, row=6, sticky='ew', padx=50)

        show_button.grid(column=0, row=7, columnspan=2)

    def patient_records_choice(self):
        # Define the grid
        self.patient_records.columnconfigure(0, weight=1)
        self.patient_records.columnconfigure(1, weight=2)
        self.patient_records.rowconfigure((0,1,2,3,4,5), weight=1)

        # Variables
        record_no_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()
        treatment_var = ctk.StringVar()
        date_var = ctk.StringVar()
        bill_var = ctk.StringVar()

        # Textvariables
        record_no_where = ctk.StringVar()
        patient_id_where = ctk.StringVar()
        treatment_where = ctk.StringVar()
        date_where = ctk.StringVar()
        bill_where = ctk.StringVar()

        # Checkboxes
        record_no_check = ctk.CTkCheckBox(self.patient_records, text='Record No', variable=record_no_var, onvalue='Record_no', offvalue='', command=lambda: self.toggle_entry(record_no_var.get(), record_no_entry))
        patient_id_check = ctk.CTkCheckBox(self.patient_records, text='Patient ID', variable=patient_id_var, onvalue='PID', offvalue='', command=lambda: self.toggle_entry(patient_id_var.get(), patient_id_entry))
        treatment_check = ctk.CTkCheckBox(self.patient_records, text='Treatment', variable=treatment_var, onvalue='Treatment_Type', offvalue='', command=lambda: self.toggle_entry(treatment_var.get(), treatment_entry))
        date_check = ctk.CTkCheckBox(self.patient_records, text='Date', variable=date_var, onvalue='Date', offvalue='', command=lambda: self.toggle_entry(date_var.get(), date_entry))
        bill_check = ctk.CTkCheckBox(self.patient_records, text='Bill', variable=bill_var, onvalue='Bill', offvalue='', command=lambda: self.toggle_entry(bill_var.get(), bill_entry))

        # Entries
        record_no_entry = ctk.CTkEntry(self.patient_records, textvariable=record_no_where, state='disabled')
        patient_id_entry = ctk.CTkEntry(self.patient_records, textvariable=patient_id_where, state='disabled')
        treatment_entry = ctk.CTkEntry(self.patient_records, textvariable=treatment_where, state='disabled')
        date_entry = ctk.CTkEntry(self.patient_records, textvariable=date_where, state='disabled')
        bill_entry = ctk.CTkEntry(self.patient_records, textvariable=bill_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.patient_records,
                                    text='Show',
                                    command=lambda e=None: self.fetch_records('Patient_Records', (record_no_var.get(), patient_id_var.get(), treatment_var.get(), date_var.get(), bill_var.get()), (record_no_where.get(), patient_id_where.get(), treatment_where.get(), date_where.get(), bill_where.get())))

        # Layout
        record_no_check.grid(column=0, row=1, sticky='w')
        patient_id_check.grid(column=0, row=0, sticky='w')
        treatment_check.grid(column=0, row=2, sticky='w')
        date_check.grid(column=0, row=3, sticky='w')
        bill_check.grid(column=0, row=4, sticky='w')

        record_no_entry.grid(column=1, row=1, sticky='ew', padx=50)
        patient_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        treatment_entry.grid(column=1, row=2, sticky='ew', padx=50)
        date_entry.grid(column=1, row=3, sticky='ew', padx=50)
        bill_entry.grid(column=1, row=4, sticky='ew', padx=50)

        show_button.grid(column=0, row=5, columnspan=2)

    def treatment_choice(self):
        # Define the grid
        self.treatment.columnconfigure(0, weight=1)
        self.treatment.columnconfigure(1, weight=2)
        self.treatment.rowconfigure((0,1,2,3,4), weight=1)

        # Variables
        doc_id_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()
        date_start_var = ctk.StringVar()
        date_end_var = ctk.StringVar()

        # Textvariables
        doc_id_where = ctk.StringVar()
        patient_id_where = ctk.StringVar()
        date_start_where = ctk.StringVar()
        date_end_where = ctk.StringVar()

        # Checkboxes
        doc_id_check = ctk.CTkCheckBox(self.treatment, text='Doctor ID', variable=doc_id_var, onvalue='Emp_ID', offvalue='', command=lambda: self.toggle_entry(doc_id_var.get(), doc_id_entry))
        patient_id_check = ctk.CTkCheckBox(self.treatment, text='Patient ID', variable=patient_id_var, onvalue='PID', offvalue='', command=lambda: self.toggle_entry(patient_id_var.get(), patient_id_entry))
        date_start_check = ctk.CTkCheckBox(self.treatment, text='Date Start', variable=date_start_var, onvalue='Date_Start', offvalue='', command=lambda: self.toggle_entry(date_start_var.get(), date_start_entry))
        date_end_check = ctk.CTkCheckBox(self.treatment, text='Date End', variable=date_end_var, onvalue='Date_end', offvalue='', command=lambda: self.toggle_entry(date_end_var.get(), date_end_entry))

        # Entries
        doc_id_entry = ctk.CTkEntry(self.treatment, textvariable=doc_id_where, state='disabled')
        patient_id_entry = ctk.CTkEntry(self.treatment, textvariable=patient_id_where, state='disabled')
        date_start_entry = ctk.CTkEntry(self.treatment, textvariable=date_start_where, state='disabled')
        date_end_entry = ctk.CTkEntry(self.treatment, textvariable=date_end_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.treatment,
                                    text='Show',
                                    command=lambda e=None: self.fetch_records('Treatment', (doc_id_var.get(), patient_id_var.get(), date_start_var.get(), date_end_var.get()), (doc_id_where.get(), patient_id_where.get(), date_start_where.get(), date_end_where.get())))

        # Layout
        doc_id_check.grid(column=0, row=1, sticky='w')
        patient_id_check.grid(column=0, row=0, sticky='w')
        date_start_check.grid(column=0, row=2, sticky='w')
        date_end_check.grid(column=0, row=3, sticky='w')

        doc_id_entry.grid(column=1, row=1, sticky='ew', padx=50)
        patient_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        date_start_entry.grid(column=1, row=2, sticky='ew', padx=50)
        date_end_entry.grid(column=1, row=3, sticky='ew', padx=50)

        show_button.grid(column=0, row=4, columnspan=2)

    def assigned_nurse_choice(self):
        # Define the grid
        self.cares_for.columnconfigure(0, weight=1)
        self.cares_for.columnconfigure(1, weight=2)
        self.cares_for.rowconfigure((0,1,2,3), weight=1)

        # Variables
        nurse_id_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()
        shift_var = ctk.StringVar()

        # Textvariables
        nurse_id_where = ctk.StringVar()
        patient_id_where = ctk.StringVar()
        shift_where = ctk.StringVar()

        # Checkboxes
        nurse_id_check = ctk.CTkCheckBox(self.cares_for, text='Nurse ID', variable=nurse_id_var, onvalue='Emp_ID', offvalue='', command=lambda: self.toggle_entry(nurse_id_var.get(), nurse_id_entry))
        patient_id_check = ctk.CTkCheckBox(self.cares_for, text='Patient ID', variable=patient_id_var, onvalue='PID', offvalue='', command=lambda: self.toggle_entry(patient_id_var.get(), patient_id_entry))
        shift_check = ctk.CTkCheckBox(self.cares_for, text='Shift', variable=shift_var, onvalue='Shift', offvalue='', command=lambda: self.toggle_entry(shift_var.get(), shift_entry))

        # Entries
        nurse_id_entry = ctk.CTkEntry(self.cares_for, textvariable=nurse_id_where, state='disabled')
        patient_id_entry = ctk.CTkEntry(self.cares_for, textvariable=patient_id_where, state='disabled')
        shift_entry = ctk.CTkEntry(self.cares_for, textvariable=shift_where, state='disabled')

        # Show button
        show_button = ctk.CTkButton(self.cares_for,
                                    text='Show',
                                    command=lambda e=None: self.fetch_records('Cares_for', (nurse_id_var.get(), patient_id_var.get(), shift_var.get()), (nurse_id_where.get(), patient_id_where.get(), shift_where.get())))

        # Layout
        nurse_id_check.grid(column=0, row=1, sticky='w')
        patient_id_check.grid(column=0, row=0, sticky='w')
        shift_check.grid(column=0, row=2, sticky='w')

        nurse_id_entry.grid(column=1, row=1, sticky='ew', padx=50)
        patient_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        shift_entry.grid(column=1, row=2, sticky='ew', padx=50)

        show_button.grid(column=0, row=3, columnspan=2)

    def toggle_entry(self, where, entry):
        if where == '':
            entry.configure(state='disabled')
        else:
            entry.configure(state='normal')

    def check_zero(self, var_list):
        yes_count = 0
        for var in var_list:
            if var != '':
                yes_count += 1

        if yes_count == 0:
            return True
        else:
            return False

    def fetch_records(self, table, var_list, where_list):
        yes_count = 0
        for var in var_list:
            if var != '':
                yes_count += 1

        # cols = ''
        cols = []

        index = 0
        while yes_count > 0:
            if var_list[index] != '':
                yes_count -= 1
                cols.append(var_list[index])
            index += 1

        # for i in range(yes_count):
        #     if i == 0:
        #         cols += f'{var_list[i]}'
        #     else:
        #         cols += f', {var_list[i]}'

        conditions = []
        for i in range(yes_count):
            if where_list[i] != '':
                actual = f'{var_list[i]} {where_list[i]}'
                conditions.append(actual)

        query = "SELECT {} FROM {}".format(', '.join(cols), table)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        self.show_treeview(cols, results)

    def show_treeview(self, col_list, results):
        style = ttk.Style()

        # Configure the style for the Treeview widget
        style.theme_use("clam")  # Change the theme to 'clam' (you can try other themes)
        style.configure("Treeview",
                        background="#c2c2c2",  # Background color
                        foreground="black",    # Foreground color (text color)
                        rowheight=25,          # Row height
                        fieldbackground="#f0f0f0"  # Background color for fields
                        )
        style.map("Treeview",  # Map the Treeview widget with specific settings
                background=[('selected', '#0078D7')],  # Selected item background color
                foreground=[('selected', 'white')]    # Selected item text color
                )
        
        self.table = ttk.Treeview(self.view_frame, columns=col_list, show='headings', style='Treeview')

        for col in col_list:
            self.table.heading(f'{col}', text=f'{col.title()}')

        for row in results:
            self.table.insert('', ctk.END, values=row)

        self.table.pack(expand=True, fill='both')
        self.view_frame.pack(expand=True, fill='both')
        self.choice_frame.pack_forget()

        self.back_button = ctk.CTkButton(self.view_frame, text='Back', command=self.go_back)
        self.back_button.pack()

    def go_back(self):
        self.table.delete(*self.table.get_children())
        self.table.pack_forget()
        self.back_button.pack_forget()
        self.choice_frame.pack(expand=True, fill='both')
        self.view_frame.pack_forget()


class Delete(ctk.CTkToplevel):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

        self.update()

        center_x = int((self.winfo_screenwidth() - 1366) / 2)
        center_y = int((self.winfo_screenheight() - 500) / 2)

        self.geometry(f'1366x500+{center_x}+{center_y}')
        self.title('Admin View')
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        self.del_frame = ctk.CTkFrame(self)
        self.table_frame = ctk.CTkScrollableFrame(self, orientation='horizontal')
        
        # Tabs
        self.tabs = ctk.CTkTabview(self.del_frame, command=lambda e=None: self.choose_table())
        self.employee = self.tabs.add('Employee')
        self.room = self.tabs.add('Room')
        self.patient = self.tabs.add('Patient')
        self.patient_records = self.tabs.add('Patient Record')
        self.treatment = self.tabs.add('Treatment')
        self.cares_for = self.tabs.add('Assigned Nurse')

        self.table = ttk.Treeview(self.table_frame)

        self.employee_delete()
        self.show_table(['Emp_ID', 'Emp_Name', 'Salary', 'DOJ', 'MGR_ID', 'Branch_ID'], 'Employee')
        self.room_delete()
        self.patient_delete()
        self.patient_records_delete()
        self.treatment_delete()
        self.assigned_nurse_delete()

        # Layout
        self.del_frame.pack(expand=True, fill='both', side='left')
        self.table_frame.pack(expand=True, fill='both', side='left')
        self.tabs.pack(expand=True, fill='both')

    def employee_delete(self):
        # Define the grid
        self.employee.columnconfigure(0, weight=1)
        self.employee.columnconfigure(1, weight=2)
        self.employee.rowconfigure((0,1), weight=1)

        # Variable
        emp_id_var = ctk.StringVar()

        # Label
        emp_id_label = ctk.CTkLabel(self.employee, text='Employee ID', font=('Helvetica', 14))

        # Combobox
        cursor = self.connection.cursor()
        cursor.execute('SELECT Emp_ID FROM Employee')
        results = cursor.fetchall()
        emp_id_list = []

        for eid in results:
            emp_id_list.append(str(eid[0]))

        emp_id_combo = ctk.CTkComboBox(self.employee, values=emp_id_list, variable=emp_id_var, state='readonly')

        # Delete button
        del_button = ctk.CTkButton(self.employee, text='Delete', command=lambda: self.delete_record('Employee', ['Emp_ID', 'Emp_Name', 'Salary', 'DOJ', 'MGR_ID', 'Branch_ID'], f'Emp_ID = {emp_id_var.get()}'))

        # Layout
        emp_id_label.grid(column=0, row=0, sticky='e')
        emp_id_combo.grid(column=1, row=0, sticky='ew', padx=50)

        del_button.grid(column=0, row=1, columnspan=2)

    def room_delete(self):
        # Define the grid
        self.room.columnconfigure(0, weight=1)
        self.room.columnconfigure(1, weight=2)
        self.room.rowconfigure((0,1,2), weight=1)

        # Variable
        self.branch_id_var = ctk.StringVar()
        self.room_no_var = ctk.StringVar()

        # Label
        branch_id_label = ctk.CTkLabel(self.room, text='Branch ID', font=('Helvetica', 14))
        room_no_label = ctk.CTkLabel(self.room, text='Room No', font=('Helvetica', 14))

        # Combobox
        cursor = self.connection.cursor()

        cursor.execute('SELECT DISTINCT Branch_ID FROM Room')
        results = cursor.fetchall()
        self.branch_id_list = []

        for bid in results:
            self.branch_id_list.append(str(bid[0]))

        cursor.execute('SELECT Room_no FROM Room')
        results = cursor.fetchall()
        self.room_no_list = []

        for rno in results:
            self.room_no_list.append(str(rno[0]))

        branch_id_combo = ctk.CTkComboBox(self.room, values=self.branch_id_list, variable=self.branch_id_var, command= lambda x : self.get_room_id(self.branch_id_var.get(), room_no_combo), state = 'readonly')
        room_no_combo = ctk.CTkComboBox(self.room, values=self.room_no_list, variable=self.room_no_var, state = 'readonly')
        branch_id_combo = ctk.CTkComboBox(self.room, values=self.branch_id_list, variable=self.branch_id_var, command= lambda x : self.get_room_id(self.branch_id_var.get(), room_no_combo), state = 'readonly')
        room_no_combo = ctk.CTkComboBox(self.room, values=self.room_no_list, variable=self.room_no_var)

        # Delete button
        del_button = ctk.CTkButton(self.room, text='Delete', command=lambda: self.delete_record('Room', ['Room_no', 'Branch_ID', 'R_type', 'Capacity', 'Available'], f'Room_no = {self.room_no_var.get()} AND Branch_ID = {self.branch_id_var.get()}'))


        # Layout
        branch_id_label.grid(column=0, row=0, sticky='e')
        room_no_label.grid(column=0, row=1, sticky='e')

        branch_id_combo.grid(column=1, row=0, sticky='ew', padx=50)
        room_no_combo.grid(column=1, row=1, sticky='ew', padx=50)

        del_button.grid(column=0, row=2, columnspan=2)

    def patient_delete(self):
        # Define the grid
        self.patient.columnconfigure(0, weight=1)
        self.patient.columnconfigure(1, weight=2)
        self.patient.rowconfigure((0,1), weight=1)

        # Variable
        patient_id_var = ctk.StringVar()

        # Label
        patient_id_label = ctk.CTkLabel(self.patient, text='Patient ID', font=('Helvetica', 14))

        # Combobox
        cursor = self.connection.cursor()
        cursor.execute('SELECT Room_no FROM Room')
        results = cursor.fetchall()
        patient_id_list = []

        for rno in results:
            patient_id_list.append(str(rno[0]))

        patient_id_combo = ctk.CTkComboBox(self.patient, values=patient_id_list, variable=patient_id_var, state = 'readonly')

        # Delete button
        del_button = ctk.CTkButton(self.patient, text='Delete', command=lambda: self.delete_record('Room', ['PID', 'P_Name', 'DOB', 'Sex', 'Address', 'Branch_ID', 'Room_no'], f'Room_no = {patient_id_var.get()}'))

        # Layout
        patient_id_label.grid(column=0, row=0, sticky='e')
        patient_id_combo.grid(column=1, row=0, sticky='ew', padx=50)

        del_button.grid(column=0, row=1, columnspan=2)

    def patient_records_delete(self):
        # Define the grid
        self.patient_records.columnconfigure(0, weight=1)
        self.patient_records.columnconfigure(1, weight=2)
        self.patient_records.rowconfigure((0,1), weight=1)

        # Variable
        rec_no_var = ctk.StringVar()

        # Label
        rec_no_label = ctk.CTkLabel(self.patient_records, text='Record No', font=('Helvetica', 14))

        # Combobox
        cursor = self.connection.cursor()
        cursor.execute('SELECT Record_no FROM Patient_Records')
        results = cursor.fetchall()
        rec_no_list = []

        for rec in results:
            rec_no_list.append(str(rec[0]))

        rec_no_combo = ctk.CTkComboBox(self.patient_records, values=rec_no_list, variable=rec_no_var, state = 'readonly')

        # Delete button
        del_button = ctk.CTkButton(self.patient_records, text='Delete', command=lambda: self.delete_record('Patient_Records', ['Record_no', 'PID', 'Treatment_Type', 'Date', 'Bill'], f'Record_no = {rec_no_var.get()}'))

        # Layout
        rec_no_label.grid(column=0, row=0, sticky='e')
        rec_no_combo.grid(column=1, row=0, sticky='ew', padx=50)

        del_button.grid(column=0, row=1, columnspan=2)

    def treatment_delete(self):
        # Define the grid
        self.treatment.columnconfigure(0, weight=1)
        self.treatment.columnconfigure(1, weight=2)
        self.treatment.rowconfigure((0,1,2), weight=1)

        # Variable
        doc_id_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()

        # Label
        doc_id_label = ctk.CTkLabel(self.treatment, text='Doctor ID', font=('Helvetica', 14))
        patient_id_label = ctk.CTkLabel(self.treatment, text='Patient ID', font=('Helvetica', 14))

        # Combobox
        cursor = self.connection.cursor()
        # cursor.execute('SELECT Emp_ID FROM Treatment')
        # results = cursor.fetchall()
        self.doc_id_list = []

        # for did in results:
        #     self.doc_id_list.append(str(did[0]))

        cursor.execute('SELECT PID FROM Treatment')
        results = cursor.fetchall()
        patient_id_list = []

        for pid in results:
            patient_id_list.append(str(pid[0]))

        doc_id_combo = ctk.CTkComboBox(self.treatment, values=self.doc_id_list, variable=doc_id_var, state = 'readonly')
        patient_id_combo = ctk.CTkComboBox(self.treatment, values=patient_id_list, variable=patient_id_var, command= lambda : self.get_doc_id(patient_id_var.get()), state = 'readonly')

        # Delete button
        del_button = ctk.CTkButton(self.treatment, text='Delete', command=lambda: self.delete_record('Treatment', ['Emp_ID', 'PID', 'Date_Start', 'Date_end'], f'Emp_ID = {doc_id_var.get()} AND PID = {patient_id_var.get()}'))

        # Layout
        patient_id_label.grid(column=0, row=0, sticky='e')
        doc_id_label.grid(column=0, row=1, sticky='e')

        patient_id_combo.grid(column=1, row=0, sticky='ew', padx=50)
        doc_id_combo.grid(column=1, row=1, sticky='ew', padx=50)

        del_button.grid(column=0, row=2, columnspan=2)

    def assigned_nurse_delete(self):
        # Define the grid
        self.cares_for.columnconfigure(0, weight=1)
        self.cares_for.columnconfigure(1, weight=2)
        self.cares_for.rowconfigure((0,1,2), weight=1)

        # Variable
        nurse_id_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()

        # Label
        nurse_id_label = ctk.CTkLabel(self.cares_for, text='Nurse ID', font=('Helvetica', 14))
        patient_id_label = ctk.CTkLabel(self.cares_for, text='Patient ID', font=('Helvetica', 14))

        # Combobox
        cursor = self.connection.cursor()
        cursor.execute('SELECT Emp_ID FROM Cares_for')
        results = cursor.fetchall()
        self.nurse_id_list = list()

        for nid in results:
            self.nurse_id_list.append(str(nid[0]))

        cursor.execute('SELECT PID FROM Cares_for')
        results = cursor.fetchall()
        patient_id_list = []

        for pid in results:
            patient_id_list.append(str(pid[0]))

        nurse_id_combo = ctk.CTkComboBox(self.cares_for, values=self.nurse_id_list, variable=nurse_id_var, state = 'readonly')
        patient_id_combo = ctk.CTkComboBox(self.cares_for, values=patient_id_list, variable=patient_id_var, command = lambda x: self.get_nurse_id(patient_id_var.get()), state = 'readonly')

        # Delete button
        del_button = ctk.CTkButton(self.cares_for, text='Delete', command=lambda: self.delete_record('Cares_for', ['Emp_ID', 'PID', 'Shift'], f'Emp_ID = {nurse_id_var.get()} AND PID = {patient_id_var.get()}'))

        # Layout
        nurse_id_label.grid(column=0, row=1, sticky='e')
        patient_id_label.grid(column=0, row=0, sticky='e')

        nurse_id_combo.grid(column=1, row=1, sticky='ew', padx=50)
        patient_id_combo.grid(column=1, row=0, sticky='ew', padx=50)

        del_button.grid(column=0, row=2, columnspan=2)

    def choose_table(self):
        if self.tabs.get() == 'Employee':
            self.show_table(['Emp_ID', 'Emp_Name', 'Salary', 'DOJ', 'MGR_ID', 'Branch_ID'], 'Employee')

        elif self.tabs.get() == 'Room':
            self.show_table(['Room_no', 'Branch_ID', 'R_type', 'Capacity', 'Available'], 'Room')

        elif self.tabs.get() == 'Patient':
            self.show_table(['PID', 'P_Name', 'DOB', 'Sex', 'Address', 'Branch_ID', 'Room_no'], 'Patient')

        elif self.tabs.get() == 'Patient Record':
            self.show_table(['Record_no', 'PID', 'Treatment_Type', 'Date', 'Bill'], 'Patient_Records')

        elif self.tabs.get() == 'Treatment':
            self.show_table(['Emp_ID', 'PID', 'Date_Start', 'Date_end'], 'Treatment')

        elif self.tabs.get() == 'Assigned Nurse':
            self.show_table(['Emp_ID', 'PID', 'Shift'], 'Cares_for')

    def show_table(self, cols, table):
        self.table.delete(*self.table.get_children())
        self.table.pack_forget()
        style = ttk.Style()

        # Configure the style for the Treeview widget
        style.theme_use("clam")  # Change the theme to 'clam' (you can try other themes)
        style.configure("Treeview",
                        background="#c2c2c2",  # Background color
                        foreground="black",    # Foreground color (text color)
                        rowheight=25,          # Row height
                        fieldbackground="#f0f0f0"  # Background color for fields
                        )
        style.map("Treeview",  # Map the Treeview widget with specific settings
                background=[('selected', '#0078D7')],  # Selected item background color
                foreground=[('selected', 'white')]    # Selected item text color
                )
        
        self.table = ttk.Treeview(self.table_frame, columns=cols, show='headings', style='Treeview')

        query = 'SELECT {} FROM {}'.format(', '.join(cols), table)

        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        for col in cols:
            self.table.heading(f'{col}', text=f'{col.title()}')

        for row in results:
            self.table.insert('', ctk.END, values=row)

        # self.table_frame.pack(expand=True, fill='both')
        self.table.pack(expand=True, fill='both')

    def delete_record(self, table, cols, value):
        query = f'DELETE FROM {table} WHERE {value}'

        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        self.after(1500, self.destroy)

        # self.show_table(['Record_no', 'PID', 'Treatment_Type', 'Date', 'Bill'], 'Patient_Records')
        self.show_table(cols, table)

    def check_entry(self, check_list, target, err_widget, label, submit):
        if len(target) == 0:
                err_widget.configure(border_color = 'red')
                label.configure(text = ' Entry cannot be NULL', text_color = 'red', image = self.error_img, compound = 'left')
                submit.configure(state = 'disabled')
                return False
        
        else:
                for i in check_list:
                    if target != i:
                        check = True
                    elif target == i:
                        check = False
                        break
            
                if check == False:
                        err_widget.configure(border_color = 'red')
                        label.configure(text = ' Duplicate entry', text_color = 'red', image = self.error_img, compound = 'left')
                        submit.configure(state = 'disabled')

                        return False

                elif check == True:
                        err_widget.configure(border_color = 'green')
                        label.configure(text = ' ', text_color = 'green', image = self.done_img, compound = 'left')
                        submit.configure(state = 'normal')
                        return True

        self.id_list.clear()
        self.get_branch_id()

    def get_room_id(self, b_id, combo_widget):
        self.room_no_list.clear()
        self.db_dict = {}
        for i in self.branch_id_list:
            cursor1 = self.connection.cursor()
            cursor1.execute('select Room_no from Room where Branch_ID = %s', (i))

            self.r1  = cursor1.fetchall()
            for room in self.r1:
                self.db_dict.setdefault(str(i), []).append(str(room[0]))


        for key in self.db_dict.keys():
            for value in self.db_dict[key]:
                if key == b_id:
                    self.room_no_list.append(str(value))

        self.room_no_var.set(value= self.room_no_list[0])
        # self.room_no_entry.configure(values = self.room_list, variable = self.room_no_var)
        combo_widget.configure(values = self.room_no_list, variable = self.room_no_var)

    def get_doc_id(self, pid):
        self.doc_id_list.clear()
        cursor3 = self.connection.cursor()
        cursor3.execute(f'SELECT Emp_ID FROM Treatment where PID = {pid}')
        results = cursor3.fetchall()
        # doc_id_list = []

        for did in results:
            self.doc_id_list.append(str(did[0]))
    
    def get_nurse_id(self, pid):
        self.nurse_id_list.clear()
        cursor2 = self.connection.cursor()
        cursor2.execute(f'SELECT Emp_ID FROM Cares_for where PID = {pid}')
        results = cursor2.fetchall()
        # doc_id_list = []

        for did in results:
            self.nurse_id_list.append(str(did[0]))


class Update(ctk.CTkToplevel):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.cursor = self.connection.cursor()

        self.update()

        center_x = int((self.winfo_screenwidth() - 1366) / 2)
        center_y = int((self.winfo_screenheight() - 700) / 2)

        self.geometry(f'1366x700+{center_x}+{center_y}')
        self.title('Admin Update')
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        self.update_frame = ctk.CTkFrame(self)
        self.table_frame = ctk.CTkScrollableFrame(self, orientation='horizontal')

        # Tabs
        self.tabs = ctk.CTkTabview(self.update_frame, command=lambda e=None: self.choose_table())
        self.employee = self.tabs.add('Employee')
        self.room = self.tabs.add('Room')
        self.patient = self.tabs.add('Patient')
        self.patient_records = self.tabs.add('Patient Record')
        self.treatment = self.tabs.add('Treatment')
        self.cares_for = self.tabs.add('Assigned Nurse')

        self.table = ttk.Treeview(self.table_frame)

        self.error_img = ctk.CTkImage(Image.open('error.png'))
        self.done_img = ctk.CTkImage(Image.open('done.png'))

        self.employee_update()
        self.show_table(['Emp_ID', 'Emp_Name', 'Salary', 'DOJ', 'MGR_ID', 'Branch_ID'], 'Employee')
        self.room_update()
        self.patient_update()
        self.patient_records_update()
        self.treatment_update()
        self.assigned_nurse_update()

        # Layout
        self.update_frame.place(x=0, y=0, relwidth=0.4, relheight=1)
        self.table_frame.place(relx=0.4, y=0, relwidth=0.6, relheight=1)
        self.tabs.pack(expand=True, fill='both')

    def employee_update(self):
        # Define the grid
        self.employee.columnconfigure((0,1,2,3), weight=1)
        self.employee.rowconfigure(0, weight=3)
        self.employee.rowconfigure((1,2,3,4), weight=1)

        # Variables
        emp_id_var = ctk.StringVar()
        emp_name_var = ctk.StringVar()
        salary_var = ctk.StringVar()
        doj_var = ctk.StringVar()
        mgr_id_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()
        
        # Labels
        emp_id_label = ctk.CTkLabel(self.employee, text='Employee ID', font=('Helvetica', 14))
        emp_name_label = ctk.CTkLabel(self.employee, text='Employee Name', font=('Helvetica', 14))
        salary_label = ctk.CTkLabel(self.employee, text='Salary', font=('Helvetica', 14))
        doj_label = ctk.CTkLabel(self.employee, text='DOJ', font=('Helvetica', 14))
        mgr_id_label = ctk.CTkLabel(self.employee, text='Managager ID', font=('Helvetica', 14))
        branch_id_label = ctk.CTkLabel(self.employee, text='Branch ID', font=('Helvetica', 14))
        self.error_label = ctk.CTkLabel(self.employee, text='', font=('Helvetica', 14))

        # Comboboxes
        self.cursor.execute('SELECT Emp_ID FROM Employee')
        results = self.cursor.fetchall()
        emp_id_list = []
        mgr_id_list = []
        branch_id_list = []

        for row in results:
            emp_id_list.append(str(row[0]))

        mgr_id_list.append('0')
        self.cursor.execute('SELECT DISTINCT Emp_ID FROM Employee')
        results = self.cursor.fetchall()
        for row in results:
            mgr_id_list.append(str(row[0]))

        # mgr_id_list.remove('None')
            
        self.cursor.execute('SELECT DISTINCT Branch_ID FROM Employee')
        results = self.cursor.fetchall()
        for row in results:
            branch_id_list.append(str(row[0]))

        cols = ['Emp_Name', 'Salary', 'DOJ', 'MGR_ID', 'Branch_ID']

        emp_id_combo = ctk.CTkComboBox(self.employee, values=emp_id_list, variable=emp_id_var, state='readonly', command=lambda e=None: self.populate('Employee', 'Emp_ID', emp_id_var.get(), cols, [emp_name_var, salary_var, doj_var, mgr_id_var, branch_id_var]))
        mgr_id_combo = ctk.CTkComboBox(self.employee, values=mgr_id_list, variable=mgr_id_var, state='readonly')
        branch_id_combo = ctk.CTkComboBox(self.employee, values=branch_id_list, variable=branch_id_var, state='readonly')

        # Entries
        emp_name_entry = ctk.CTkEntry(self.employee, textvariable=emp_name_var)
        salary_entry = ctk.CTkEntry(self.employee, textvariable=salary_var)
        doj_entry = ctk.CTkEntry(self.employee, textvariable=doj_var)

        # Update button
        update_button = ctk.CTkButton(self.employee, text='Update', command=lambda e=None: self.update_record('Employee', cols, [emp_name_var.get(), salary_var.get(), doj_var.get(), mgr_id_var.get(), branch_id_var.get()], 'Emp_ID', emp_id_var.get(), self.error_label))


        emp_name_entry.configure(validatecommand = lambda : self.not_null(update_button, 
                                                                          emp_name_entry,
                                                                          self.error_label), validate = "focus")
        # Layout
        emp_id_label.grid(column=0, row=0, columnspan=2)
        emp_id_combo.grid(column=2, row=0, columnspan=2, sticky='ew', padx=50)

        emp_name_label.grid(column=0, row=1)
        salary_label.grid(column=2, row=1)
        doj_label.grid(column=0, row=2)
        mgr_id_label.grid(column=2, row=2)
        branch_id_label.grid(column=0, row=3)
        self.error_label.grid(column=1, row=4, columnspan=2)

        emp_name_entry.grid(column=1, row=1)
        salary_entry.grid(column=3, row=1)
        doj_entry.grid(column=1, row=2)
        mgr_id_combo.grid(column=3, row=2)
        branch_id_combo.grid(column=1, row=3)

        update_button.grid(column=0, row=5, columnspan=4)

    def room_update(self):
        # Define the grid
        self.room.columnconfigure((0,1,2,3), weight=1)
        self.room.rowconfigure((0,1), weight=3)
        self.room.rowconfigure((2,3,4,5), weight=1)

        # Variables
        branch_id_var = ctk.StringVar()
        room_no_var = ctk.StringVar()
        room_type_var = ctk.StringVar()
        capacity_var = ctk.StringVar()
        available_var = ctk.StringVar()

        # Labels
        branch_id_label = ctk.CTkLabel(self.room, text='Branch ID', font=('Helvetica', 14))
        room_no_label = ctk.CTkLabel(self.room, text='Room No', font=('Helvetica', 14))
        room_type_label = ctk.CTkLabel(self.room, text='Room Type', font=('Helvetica', 14))
        capacity_label = ctk.CTkLabel(self.room, text='Capacity', font=('Helvetica', 14))
        available_label = ctk.CTkLabel(self.room, text='Available', font=('Helvetica', 14))

        # Comboboxes
        branch_id_list = []
        room_no_list = []

        self.cursor.execute('SELECT DISTINCT Branch_ID FROM Room')
        results = self.cursor.fetchall()

        for bid in results:
            branch_id_list.append(str(bid[0]))

        self.cursor.execute('SELECT DISTINCT Room_no FROM Room')
        results = self.cursor.fetchall()

        for rno in results:
            room_no_list.append(str(rno[0]))

        cols = ['R_Type', 'Capacity', 'Available']

        branch_id_combo = ctk.CTkComboBox(self.room, values=branch_id_list, variable=branch_id_var)
        room_no_combo = ctk.CTkComboBox(self.room, values=room_no_list, variable=room_no_var)

        # Entries
        room_type_entry = ctk.CTkEntry(self.room, textvariable=room_type_var)
        capacity_entry = ctk.CTkEntry(self.room, textvariable=capacity_var)
        available_entry = ctk.CTkEntry(self.room, textvariable=available_var)

        # Update button
        update_button = ctk.CTkButton(self.room, text='Update', command=lambda e=None: self.update_record_composite('Room', cols, [room_type_var.get(), capacity_var.get(), available_var.get()], ['Branch_ID', 'Room_no'], [branch_id_var.get(), room_no_var.get()]))

        # Layout
        branch_id_label.grid(column=0, row=0, columnspan=2)
        room_no_label.grid(column=0, row=1, columnspan=2)

        branch_id_combo.grid(column=2, row=0, columnspan=2)
        room_no_combo.grid(column=2, row=1, columnspan=2)

        room_type_label.grid(column=0, row=2)
        capacity_label.grid(column=2, row=2)
        available_label.grid(column=0, row=3)
        self.error_label.grid(column=1, row=4, columnspan=2)

        room_type_entry.grid(column=1, row=2, sticky='ew', padx=50)
        capacity_entry.grid(column=3, row=2, sticky='ew', padx=50)
        available_entry.grid(column=1, row=3, sticky='ew', padx=50)

        update_button.grid(column=0, row=5, columnspan=4)

    def patient_update(self):
        # Define the grid
        self.patient.columnconfigure((0,1,2,3), weight=1)
        self.patient.rowconfigure(0, weight=3)
        self.patient.rowconfigure((1,2,3,4), weight=1)

        # Variables
        patient_id_var = ctk.StringVar()
        patient_name_var = ctk.StringVar()
        dob_var = ctk.StringVar()
        sex_var = ctk.StringVar()
        address_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()
        room_no_var = ctk.StringVar()

        # Labels
        patient_id_label = ctk.CTkLabel(self.patient, text='Patient ID', font=('Helvetica', 14))
        patient_name_label = ctk.CTkLabel(self.patient, text='Patient Name', font=('Helvetica', 14))
        dob_label = ctk.CTkLabel(self.patient, text='DOB', font=('Helvetica', 14))
        sex_label = ctk.CTkLabel(self.patient, text='Sex', font=('Helvetica', 14))
        address_label = ctk.CTkLabel(self.patient, text='Address', font=('Helvetica', 14))
        branch_id_label = ctk.CTkLabel(self.patient, text='Branch ID', font=('Helvetica', 14))
        room_no_label = ctk.CTkLabel(self.patient, text='Room No', font=('Helvetica', 14))
        self.error_label = ctk.CTkLabel(self.employee, text='', font=('Helvetica', 14))

        # Comboboxes
        patient_id_list = []
        branch_id_list = []
        room_no_list = []

        self.cursor.execute('SELECT DISTINCT PID FROM Patient')
        results = self.cursor.fetchall()

        for pid in results:
            patient_id_list.append(str(pid[0]))

        self.cursor.execute('SELECT DISTINCT Branch_ID FROM Patient')
        results = self.cursor.fetchall()

        for bid in results:
            branch_id_list.append(str(bid[0]))

        self.cursor.execute('SELECT DISTINCT Room_no FROM Patient')
        results = self.cursor.fetchall()

        for rno in results:
            room_no_list.append(str(rno[0]))

        cols = ['P_Name', 'DOB', 'Sex', 'Address', 'Branch_ID', 'Room_no']

        patient_id_combo = ctk.CTkComboBox(self.patient, values=patient_id_list, variable=patient_id_var, command=lambda e=None: self.populate('Patient', 'PID', patient_id_var.get(), cols, [patient_name_var, dob_var, sex_var, address_var, branch_id_var, room_no_var]))
        branch_id_combo = ctk.CTkComboBox(self.patient, values=branch_id_list, variable=branch_id_var)
        room_no_combo = ctk.CTkComboBox(self.patient, values=room_no_list, variable=room_no_var)

        # Entries
        patient_name_entry = ctk.CTkEntry(self.patient, textvariable=patient_name_var)
        dob_entry = ctk.CTkEntry(self.patient, textvariable=dob_var)
        sex_entry = ctk.CTkEntry(self.patient, textvariable=sex_var)
        address_entry = ctk.CTkEntry(self.patient, textvariable=address_var)

        # Update button
        update_button = ctk.CTkButton(self.patient, text='Update', command=lambda e=None: self.update_record('Patient', cols, [patient_name_var.get(), dob_var.get(), sex_var.get(), address_var.get()], 'PID', patient_id_var.get(), self.error_label))

        # Layout
        patient_id_label.grid(column=0, row=0, columnspan=2)
        patient_id_combo.grid(column=2, row=0, columnspan=2)

        patient_name_label.grid(column=0, row=1)
        dob_label.grid(column=2, row=1)
        sex_label.grid(column=0, row=2)
        address_label.grid(column=2, row=2)
        branch_id_label.grid(column=0, row=3)
        room_no_label.grid(column=2, row=3)

        patient_name_entry.grid(column=1, row=1, sticky='ew', padx=50)
        dob_entry.grid(column=3, row=1, sticky='ew', padx=50)
        sex_entry.grid(column=1, row=2, sticky='ew', padx=50)
        address_entry.grid(column=3, row=2, sticky='ew', padx=50)
        branch_id_combo.grid(column=1, row=3, sticky='ew', padx=50)
        room_no_combo.grid(column=3, row=3, sticky='ew', padx=50)

        update_button.grid(column=0, row=4, columnspan=4)

    def patient_records_update(self):
        # Define the grid
        self.patient_records.columnconfigure((0,1,2,3), weight=1)
        self.patient_records.rowconfigure(0, weight=3)
        self.patient_records.rowconfigure((1,2,3,4), weight=1)

        # Variables
        record_no_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()
        treatment_type_var = ctk.StringVar()
        date_var = ctk.StringVar()
        bill_var = ctk.StringVar()

        # Labels
        record_no_label = ctk.CTkLabel(self.patient_records, text='Record No', font=('Helvetica', 14))
        patient_id_label = ctk.CTkLabel(self.patient_records, text='Patient ID', font=('Helvetica', 14))
        treatment_type_label = ctk.CTkLabel(self.patient_records, text='Treatment Type', font=('Helvetica', 14))
        date_label = ctk.CTkLabel(self.patient_records, text='Date', font=('Helvetica', 14))
        bill_label = ctk.CTkLabel(self.patient_records, text='Bill', font=('Helvetica', 14))
        self.error_label = ctk.CTkLabel(self.employee, text='', font=('Helvetica', 14))

        # Comboboxes
        record_no_list = []
        patient_id_list = []

        self.cursor.execute('SELECT Record_no FROM Patient_Records')
        results = self.cursor.fetchall()

        for recno in results:
            record_no_list.append(str(recno[0]))

        self.cursor.execute('SELECT DISTINCT PID FROM Patient_Records')
        results = self.cursor.fetchall()

        for pid in results:
            patient_id_list.append(str(pid[0]))

        cols = ['PID', 'DOB', 'Treatment_Type', 'Date', 'Bill']

        record_no_combo = ctk.CTkComboBox(self.patient_records, values=record_no_list, variable=record_no_var, command=lambda e=None: self.populate('Patient_Records', 'Record_no', record_no_var.get(), cols, [patient_id_var, treatment_type_var, date_var, bill_var]))
        patient_id_combo = ctk.CTkComboBox(self.patient_records, values=patient_id_list, variable=patient_id_var)

        # Entries
        treatment_type_entry = ctk.CTkEntry(self.patient_records, textvariable=treatment_type_var)
        date_entry = ctk.CTkEntry(self.patient_records, textvariable=date_var)
        bill_entry = ctk.CTkEntry(self.patient_records, textvariable=bill_var)

        # Update button
        update_button = ctk.CTkButton(self.patient_records, text='Update', command=lambda e=None: self.update_record('Patient_Records', cols, [patient_id_var.get(), treatment_type_var.get(), date_var.get(), bill_var.get()], 'Record_no', record_no_var.get(), self.error_label))

        # Layout
        record_no_label.grid(column=0, row=0, columnspan=2)
        record_no_combo.grid(column=2, row=0, columnspan=2)

        patient_id_label.grid(column=0, row=1)
        treatment_type_label.grid(column=2, row=1)
        date_label.grid(column=0, row=2)
        bill_label.grid(column=2, row=2)
        self.error_label.grid(column=1, row=3, columnspan=2)

        treatment_type_entry.grid(column=3, row=1, sticky='ew', padx=50)
        date_entry.grid(column=1, row=2, sticky='ew', padx=50)
        bill_entry.grid(column=3, row=2, sticky='ew', padx=50)

        update_button.grid(column=0, row=4, columnspan=4)

    def treatment_update(self):
        # Define the grid
        self.treatment.columnconfigure((0,1,2,3), weight=1)
        self.treatment.rowconfigure(0, weight=3)
        self.treatment.rowconfigure((1,2,3,4), weight=1)

        # Variables
        emp_id_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()
        date_start_var = ctk.StringVar()
        date_end_var = ctk.StringVar()

        # Labels
        emp_id_label = ctk.CTkLabel(self.treatment, text='Record No', font=('Helvetica', 14))
        patient_id_label = ctk.CTkLabel(self.treatment, text='Patient ID', font=('Helvetica', 14))
        date_start_label = ctk.CTkLabel(self.treatment, text='Treatment Type', font=('Helvetica', 14))
        date_end_label = ctk.CTkLabel(self.treatment, text='Date', font=('Helvetica', 14))

        # Comboboxes
        emp_id_list = []
        patient_id_list = []

        self.cursor.execute('SELECT DISTINCT Emp_ID FROM Treatment')
        results = self.cursor.fetchall()

        for eid in results:
            emp_id_list.append(str(eid[0]))

        self.cursor.execute('SELECT DISTINCT PID FROM Patient_Records')
        results = self.cursor.fetchall()

        for pid in results:
            patient_id_list.append(str(pid[0]))

        cols = ['Date_Start', 'Date_end']

        # lambda e=None: self.populate('Patient_Records', 'Record_no', record_no_var.get(), cols, [patient_id_var, treatment_type_var, date_var, bill_var])
        emp_id_combo = ctk.CTkComboBox(self.treatment, values=emp_id_list, variable=emp_id_var, command=lambda e=None: self.enable_combo(patient_id_combo))
        patient_id_combo = ctk.CTkComboBox(self.treatment, values=patient_id_list, variable=patient_id_var, state='disabled', command=lambda e=None: self.populate_composite('Treatment', ['Emp_ID', 'PID'], [emp_id_var.get(), patient_id_var.get()], cols, [date_start_var, date_end_var]))

        # Entries
        date_start_entry = ctk.CTkEntry(self.treatment, textvariable=date_start_var)
        date_end_entry = ctk.CTkEntry(self.treatment, textvariable=date_end_var)

        # Update button
        update_button = ctk.CTkButton(self.treatment, text='Update', command=lambda e=None: self.update_record_composite('Treatment', cols, [date_start_var.get(), date_end_var.get()], ['Emp_ID', 'PID'], [emp_id_var.get(), patient_id_var.get()], self.error_label))

        # Layout
        emp_id_label.grid(column=0, row=0, columnspan=2)
        patient_id_label.grid(column=0, row=1, columnspan=2)

        emp_id_combo.grid(column=2, row=0, columnspan=2)
        patient_id_combo.grid(column=2, row=1, columnspan=2)

        date_start_label.grid(column=0, row=2)
        date_end_label.grid(column=2, row=2)
        self.error_label.grid(column=1, row=3, columnspan=2)

        date_start_entry.grid(column=1, row=2, sticky='ew', padx=50)
        date_end_entry.grid(column=3, row=2, sticky='ew', padx=50)

        update_button.grid(column=0, row=4, columnspan=4)

    def assigned_nurse_update(self):
        # Define the grid
        self.cares_for.columnconfigure((0,1,2,3), weight=1)
        self.cares_for.rowconfigure(0, weight=3)
        self.cares_for.rowconfigure((1,2,3,4), weight=1)

        # Variables
        emp_id_var = ctk.StringVar()
        patient_id_var = ctk.StringVar()
        shift_var = ctk.StringVar()

        # Labels
        emp_id_label = ctk.CTkLabel(self.cares_for, text='Record No', font=('Helvetica', 14))
        patient_id_label = ctk.CTkLabel(self.cares_for, text='Patient ID', font=('Helvetica', 14))
        shift_label = ctk.CTkLabel(self.cares_for, text='Treatment Type', font=('Helvetica', 14))

        # Comboboxes
        emp_id_list = []
        patient_id_list = []

        self.cursor.execute('SELECT DISTINCT Emp_ID FROM Treatment')
        results = self.cursor.fetchall()

        for eid in results:
            emp_id_list.append(str(eid[0]))

        self.cursor.execute('SELECT DISTINCT PID FROM Patient_Records')
        results = self.cursor.fetchall()

        for pid in results:
            patient_id_list.append(str(pid[0]))

        cols = ['Shift']

       
        emp_id_combo = ctk.CTkComboBox(self.cares_for, values=emp_id_list, variable=emp_id_var, command=lambda e=None: self.enable_combo(patient_id_combo))
        patient_id_combo = ctk.CTkComboBox(self.cares_for, values=patient_id_list, variable=patient_id_var, state='disabled', command=lambda e=None: self.populate_composite('Treatment', ['Emp_ID', 'PID'], [emp_id_var.get(), patient_id_var.get()], cols, [date_start_var, date_end_var]))
        shift_combo = ctk.CTkComboBox(self.cares_for, values=['Morning', 'Evening'], variable=shift_var, state='readonly')

        # Update button
        update_button = ctk.CTkButton(self.cares_for, text='Update', command=lambda e=None: self.update_record_composite('Cares_for', cols, shift_var.get(), ['Emp_ID', 'PID'], [emp_id_var.get(), patient_id_var.get()], self.error_label))

        # Layout
        emp_id_label.grid(column=0, row=0, columnspan=2)
        patient_id_label.grid(column=0, row=1, columnspan=2)

        emp_id_combo.grid(column=2, row=0, columnspan=2)
        patient_id_combo.grid(column=2, row=1, columnspan=2)

        shift_label.grid(column=0, row=2)
        self.error_label.grid(column=1, row=3, columnspan=2)

        shift_combo.grid(column=1, row=2, sticky='ew', padx=50)

        update_button.grid(column=0, row=4, columnspan=4)

    def enable_combo(self, widget):
        widget.configure(state='readonly')

    def populate(self, table, pk, pk_val, col_list, var_list):
        query = 'SELECT {} FROM {} WHERE {} = {}'.format(', '.join(col_list), table, pk, pk_val)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        
        index = 0
        for each in col_list:
            var_list[index].set(result[index])
            index += 1

    def populate_composite(self, table, pk, pk_val, col_list, var_list):
        query = 'SELECT {} FROM {} WHERE {} = {} AND {} = {}'.format(', '.join(col_list), table, pk[0], pk_val[0], pk[1], pk_val[1])
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        index = 0
        for each in col_list:
            var_list[index].set(result[index])
            index += 1

    def choose_table(self):
        if self.tabs.get() == 'Employee':
            self.show_table(['Emp_ID', 'Emp_Name', 'Salary', 'DOJ', 'MGR_ID', 'Branch_ID'], 'Employee')

        elif self.tabs.get() == 'Room':
            self.show_table(['Room_no', 'Branch_ID', 'R_type', 'Capacity', 'Available'], 'Room')

        elif self.tabs.get() == 'Patient':
            self.show_table(['PID', 'P_Name', 'DOB', 'Sex', 'Address', 'Branch_ID', 'Room_no'], 'Patient')

        elif self.tabs.get() == 'Patient Record':
            self.show_table(['Record_no', 'PID', 'Treatment_Type', 'Date', 'Bill'], 'Patient_Records')

        elif self.tabs.get() == 'Treatment':
            self.show_table(['Emp_ID', 'PID', 'Date_Start', 'Date_end'], 'Treatment')

        elif self.tabs.get() == 'Assigned Nurse':
            self.show_table(['Emp_ID', 'PID', 'Shift'], 'Cares_for')

    def show_table(self, cols, table):
        self.table.delete(*self.table.get_children())
        self.table.pack_forget()
        style = ttk.Style()

        # Configure the style for the Treeview widget
        style.theme_use("clam")  # Change the theme to 'clam' (you can try other themes)
        style.configure("Treeview",
                        background="#c2c2c2",  # Background color
                        foreground="black",    # Foreground color (text color)
                        rowheight=25,          # Row height
                        fieldbackground="#f0f0f0"  # Background color for fields
                        )
        style.map("Treeview",  # Map the Treeview widget with specific settings
                background=[('selected', '#0078D7')],  # Selected item background color
                foreground=[('selected', 'white')]    # Selected item text color
                )
        
        self.table = ttk.Treeview(self.table_frame, columns=cols, show='headings', style='Treeview')

        query = 'SELECT {} FROM {}'.format(', '.join(cols), table)

        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        for col in cols:
            self.table.heading(f'{col}', text=f'{col.title()}')

        for row in results:
            self.table.insert('', ctk.END, values=row)

        self.table.pack(expand=True, fill='both')

    def update_record(self, table, col_list, val_list, pk, pk_val, err_label):
        try:
            pairs = ' , '.join(["{}='{}'".format(col, val) for col, val in zip(col_list, val_list)])
            query = 'UPDATE {} SET {} WHERE {} = {}'.format(table, pairs, pk, pk_val)

            self.cursor.execute(query)
        except Exception :
               err_label.configure(text = ' ERROR', text_color = 'red', image = self.error_img, compound = 'left')
        else:
                self.connection.commit()

                temp = [pk]
                for each in col_list:
                    temp.append(each)

                self.show_table(temp, table)

    def update_record_composite(self, table, col_list, val_list, pk, pk_val, err_label):
        pairs = ' , '.join(["{}='{}'".format(col, val) for col, val in zip(col_list, val_list)])
        query = 'UPDATE {} SET {} WHERE {} = {} AND {} = {}'.format(table, pairs, pk[0], pk_val[0], pk[1], pk_val[1])

        self.cursor.execute(query)
        self.connection.commit()

        temp = [pk[0], pk[1]]
        for each in col_list:
            temp.append(each)

        self.show_table(temp, table)

    def validate_date(self, input_date, err_widget, err_label, submit):
        try:
            if input_date != datetime.strptime(input_date, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
          
        except ValueError:
            err_widget.configure(border_color = 'red')
            err_label.configure(text = ' Invalid Date Format\n Valid Format : yyyy/mm/dd', text_color = 'red', image = self.error_img, compound = 'left')
            submit.configure(state='disabled')
            return False
    
        else:
            err_widget.configure(border_color = 'green')
            err_label.configure(text = ' ', text_color = 'red', image = self.done_img, compound = 'left')
            submit.configure(state='normal')
            return True
        
    def not_null(self, submit, err_widget, label):
        input = err_widget.get()
        if  len(input) == 0:
            err_widget.configure(border_color = 'red')
            label.configure(text=' Name cannot be empty', text_color = 'red', image = self.error_img, compound = 'left')
            submit.configure(state = 'disabled')
            return False
        
        elif input.isdigit():
            err_widget.configure(border_color = 'red')
            label.configure(text=' Name cannot be a number ', text_color = 'red', image = self.error_img, compound = 'left')
            submit.configure(state = 'disabled')

            return False
        else:
                err_widget.configure(border_color = 'green')
            # self.submit_button.configure(state = 'normal')
                label.configure(text = ' ', text_color = 'green', image = self.done_img, compound = 'left')
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
            