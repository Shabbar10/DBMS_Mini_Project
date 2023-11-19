import customtkinter as ctk

def next():
    frame2.pack(expand=True, fill='both')
    frame1.pack_forget()

def back():
    frame1.pack(expand=True, fill='both')
    frame2.pack_forget()

window = ctk.CTk()

frame1 = ctk.CTkFrame(window)
label1 = ctk.CTkLabel(frame1, text='1')
button1 = ctk.CTkButton(frame1, text='Next', command=next)
label1.pack()
button1.pack()
frame1.pack(expand=True, fill='both')

frame2 = ctk.CTkFrame(window)
label2 = ctk.CTkLabel(frame2, text='2')
button2 = ctk.CTkButton(frame2, text='Back', command=back)
label2.pack()
button2.pack()

window.mainloop()