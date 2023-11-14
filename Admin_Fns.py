import customtkinter as ctk
import pymysql
from pymysql import err

class Insert(ctk.CTkToplevel):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

        self.update()

        center_x = int((self.winfo_screenwidth() - 600) / 2)
        center_y = int((self.winfo_screenheight() - 350) / 2)

        self.geometry(f'600x350+{center_x}+{center_y}')
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
        # Define grid
        self.hospital.columnconfigure(0, weight=1)
        self.hospital.columnconfigure(1, weight=2)
        self.hospital.rowconfigure((0,1,3),weight=1)
        self.hospital.rowconfigure(2,weight=1) # For address textbox

        # Textvariables
        branch_id_var = ctk.StringVar()
        branch_name_var = ctk.StringVar()

        # Labels
        branch_id_label = ctk.CTkLabel(self.hospital, text='Branch ID', font=('Helvetica', 14))
        branch_name_label = ctk.CTkLabel(self.hospital, text='Branch Name', font=('Helvetica', 14))
        address_label = ctk.CTkLabel(self.hospital, text='Address', font=('Helvetica', 14))

        # Entries
        self.h_branch_id_entry = ctk.CTkEntry(self.hospital, textvariable=branch_id_var)
        self.h_branch_name_entry = ctk.CTkEntry(self.hospital, textvariable=branch_name_var)
        self.h_address_textbox = ctk.CTkTextbox(self.hospital, font=('Helvetica', 14), fg_color='#343638', height=100, width=370, border_color='#565b5e', border_width=2, activate_scrollbars=False)

        # Submit button
        submit_button = ctk.CTkButton(self.hospital, text='Submit', command=lambda: self.commit_data('Hospital', ('Branch_ID', 'H_Name', 'Address'), (int(branch_id_var.get()), branch_name_var.get(), self.address_textbox.get('1.0', ctk.END))), fg_color='#144870', text_color='black', hover_color='cyan')

        # Layout
        branch_id_label.grid(column=0, row=0, sticky='e')
        branch_name_label.grid(column=0, row=1, sticky='e')
        address_label.grid(column=0, row=2, sticky='e')

        self.h_branch_id_entry.grid(column=1, row=0, sticky='ew', padx=50)
        self.h_branch_name_entry.grid(column=1, row=1, sticky='ew', padx=50)
        self.h_address_textbox.grid(column=1, row=2, sticky='ew', padx=50)

        submit_button.grid(column=0, row=3, columnspan=2)

    def employee_form(self):
        # Define grid
        self.emp_frame.columnconfigure(0, weight=1)
        self.emp_frame.columnconfigure(1, weight=2)
        self.emp_frame.rowconfigure((0,1,2,3,4,5),weight=1)

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

        # Entries
        self.e_emp_name_entry = ctk.CTkEntry(self.emp_frame, textvariable=emp_name_var)
        self.e_salary_entry = ctk.CTkEntry(self.emp_frame, textvariable=salary_var)
        self.e_doj_entry = ctk.CTkEntry(self.emp_frame, textvariable=doj_var)

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

        mgr_id_combo = ctk.CTkComboBox(self.emp_frame, values=emp_id_list, variable=mgr_id_var)
        branch_id_combo = ctk.CTkComboBox(self.emp_frame, values=branch_id_list, variable=branch_id_var)

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

        self.e_emp_name_entry.grid(column=1, row=0, sticky='ew', padx=50)
        self.e_salary_entry.grid(column=1, row=1, sticky='ew', padx=50)
        self.e_doj_entry.grid(column=1, row=2, sticky='ew', padx=50)
        mgr_id_combo.grid(column=1, row=3, sticky='ew', padx=50)
        branch_id_combo.grid(column=1, row=4, sticky='ew', padx=50)

        submit_button.grid(column=0, row=5, columnspan=2)

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

        emp_id_combo = ctk.CTkComboBox(self.doc, values=emp_id_list, variable=emp_id_var)

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
        self.nurse.rowconfigure((0,1,), weight=1)
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

        emp_id_combo = ctk.CTkComboBox(self.nurse, values=emp_id_list, variable=emp_id_var)

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
        self.room.rowconfigure((0,1,2,3,4,5), weight=1)

        # Textvariables
        room_no_var = ctk.StringVar()
        branch_id_var = ctk.StringVar()
        room_type_var = ctk.StringVar()
        capactiy_var = ctk.StringVar()
        available_var = ctk.StringVar()

        # Labels
        room_no_label = ctk.CTkLabel(self.room, text='Room No', font=('Helvetica', 14))
        branch_id_label = ctk.CTkLabel(self.room, text='Branch ID', font=('Helvetica', 14))
        room_type_label = ctk.CTkLabel(self.room, text='Room Type', font=('Helvetica', 14))
        capactiy_label = ctk.CTkLabel(self.room, text='Capacity', font=('Helvetica', 14))
        available_label = ctk.CTkLabel(self.room, text='Availability', font=('Helvetica', 14))

        # Entries
        self.r_room_no_entry = ctk.CTkEntry(self.room)
        self.r_room_type_entry = ctk.CTkEntry(self.room)
        self.r_capactiy_entry = ctk.CTkEntry(self.room)
        self.r_available_entry = ctk.CTkEntry(self.room)

        # Combobox
        cursor = self.connection.cursor()

        cursor.execute('SELECT Branch_ID from Hospital;')
        results = cursor.fetchall()
        branch_id_list = []

        for bid in results:
            branch_id_list.append(str(bid[0]))

        branch_id_combo = ctk.CTkComboBox(self.room, values=branch_id_list, variable=branch_id_var)

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.room, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Room', ('Room_no', 'Branch_ID', 'R_Type', 'Capacity', 'Available'), (int(room_no_var.get()), int(branch_id_var.get())), room_type_var.get(), int(capactiy_var.get()), int(available_var.get())), 
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')

        # Layout
        room_no_label.grid(column=0, row=0, sticky='e')
        branch_id_label.grid(column=0, row=1, sticky='e')
        room_type_label.grid(column=0, row=2, sticky='e')
        capactiy_label.grid(column=0, row=3, sticky='e')
        available_label.grid(column=0, row=4, sticky='e')

        self.r_room_no_entry.grid(column=1, row=0, sticky='ew', padx=50)
        branch_id_combo.grid(column=1, row=1, sticky='ew', padx=50)
        self.r_room_type_entry.grid(column=1, row=2, sticky='ew', padx=50)
        self.r_capactiy_entry.grid(column=1, row=3, sticky='ew', padx=50)
        self.r_available_entry.grid(column=1, row=4, sticky='ew', padx=50)

        submit_button.grid(column=0, row=5, columnspan=2)

    def patient_form(self):
        # Define grid
        self.patient.columnconfigure(0, weight=1)
        self.patient.columnconfigure(1, weight=2)
        self.patient.rowconfigure((0,1,2,4,5,6,7), weight=1, uniform='a')
        self.patient.rowconfigure(3, weight=3)

        # Textvariables
        p_name_var = ctk.StringVar()
        dob_var = ctk.StringVar(value='yyyy/mm/dd')
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

        

        # branch_id_list = []

        # for bid in results:
        #     branch_id_list.append(str(bid[0]))

        # cursor.execute('SELECT Room_no FROM Room;')
        # results = cursor.fetchall()
        # room_no_list = []

        # for rno in results:
        #     room_no_list.append(str(rno[0]))

        # for bid in branch_id_list:
        #     pass


        branch_id_combo = ctk.CTkComboBox(self.patient, values=branch_id_list, variable=branch_id_var)
        # room_no_combo = ctk.CTkComboBox(self.patient, values=room_no_list, variable=room_no_var)

        cursor.close()

        # Submit Button
        submit_button = ctk.CTkButton(self.patient, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Patient', ('P_Name', 'DOB', 'Sex', 'Address', 'Branch_ID', 'Room_no'), (p_name_var.get(), dob_var.get()), sex_var.get(), address_textbox.get('1.0', ctk.END), int(branch_id_var.get()), int(room_no_var.get())), 
                                      fg_color='#144870', 
                                      text_color='black', 
                                      hover_color='cyan')

        # Layout
        p_name_label.grid(column=0, row=0, sticky='e')
        dob_label.grid(column=0, row=1, sticky='e')
        sex_label.grid(column=0, row=2, sticky='e')
        address_label.grid(column=0, row=3, sticky='e')
        branch_id_label.grid(column=0, row=4, sticky='e')
        room_no_label.grid(column=0, row=5, sticky='e')

        p_name_entry.grid(column=1, row=0, sticky='ew', padx=50)
        dob_entry.grid(column=1, row=1, sticky='ew', padx=50)
        sex_entry.grid(column=1, row=2, sticky='ew', padx=50)
        address_textbox.grid(column=1, row=3, sticky='nsew', padx=50)
        branch_id_combo.grid(column=1, row=4, sticky='ew', padx=50)
        # room_no_combo.grid(column=1, row=5, sticky='ew', padx=50)

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

        patient_id_combo = ctk.CTkComboBox(self.patient_records, values=patient_id_list, variable=pid_var)

        cursor.close()

        # Submit button
        submit_button = ctk.CTkButton(self.patient_records, 
                                      text='Submit', 
                                      command=lambda: self.commit_data('Patient_Records', ('PID', 'Treatment_Type', 'Date', 'Bill'), (int(pid_var.get()), treatment_var.get()), date_var.get(), int(bill_var.get())), 
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

        doc_id_combo = ctk.CTkComboBox(self.treatment, values=doc_id_list, variable=doc_id_var)
        patient_id_combo = ctk.CTkComboBox(self.treatment, values=patient_id_list, variable=patient_id_var)

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

        nurse_id_combo = ctk.CTkComboBox(self.cares_for, values=nurse_id_list, variable=nurse_id_var)
        patient_id_combo = ctk.CTkComboBox(self.cares_for, values=patient_id_list, variable=patient_id_var)
        shift_combo = ctk.CTkComboBox(self.cares_for, values=['Morning', 'Evening'], variable=shift_var)

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

        self.update_comboboxes()

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
            pass

        elif self.tabs.get() == 'Assigned Nurse':
            pass


class View(ctk.CTkToplevel):
    def __init__(self, connection):
        super().__init__()


class Delete(ctk.CTkToplevel):
    def __init__(self, connection):
        super().__init__()


class Update(ctk.CTkToplevel):
    def __init__(self, connection):
        super().__init__()