import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from tkinter.filedialog import askopenfilename, asksaveasfilename
from driver import GetStatus
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import threading
import time


class UI():
    
    def __init__(self):        
        # Create the main window
        self.root = tk.Tk()
        self.driver = GetStatus()
        
        # Set the window size and title
        self.root.geometry("550x550")
        self.root.resizable(False, False)
        self.root.title("WhatsApp Status")

        # try to set the window icon
        try:
            self.root.iconbitmap("logo.ico")
        except:
            try:
                self.root.iconbitmap("Project\logo.ico")
            except:
                pass
        

        # Create a frame for the title and login button
        self.header_frame = tk.Frame(self.root, bg="#25D366")
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        # Create a frame for the UI elements
        self.frame = tk.Frame(self.root, bg="#25D366", padx=2)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a label for the title text
        self.title_label = tk.Label(self.header_frame, text="WhatsApp Status", font=("Helvetica", 16), fg="white", bg="#25D366")
        self.title_label.pack(side=tk.LEFT, expand=True)

        # Create a login button
        self.style = ttk.Style()
        self.style.configure("Login.TButton", padding=3, relief="solid", borderwidth=3, font=("Helvetica", 12), background="#25D366")
        #self.login_button = ttk.Button(self.header_frame, text="Github repository", style="Login.TButton", command=lambda: self.login())
        #self.login_button.pack(side=tk.RIGHT)

        # Create a hyperlink label between the two buttons
        self.link_label = ttk.Button(self.header_frame, text="Github repository", style="Login.TButton")
        self.link_label.pack(side=tk.RIGHT)
        self.link_label.bind("<Button-1>", lambda event: self.driver.github())

        # Create a frame for the message list
        self.message_frame = tk.Frame(self.frame, bg="white")
        self.message_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrollbar for the message list
        self.message_scrollbar = tk.Scrollbar(self.message_frame)
        self.message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox for the messages
        self.message_list = tk.Listbox(self.message_frame, yscrollcommand=self.message_scrollbar.set)

        # Pack the message listbox and make it fill the frame
        self.message_list.pack(fill=tk.BOTH, expand=True)

        # Connect the scrollbar to the message listbox
        self.message_scrollbar.config(command=self.message_list.yview)

        # Create a frame for the input field
        self.input_frame = tk.Frame(self.frame, bg="#ece5dd")
        self.input_frame.pack(fill=tk.X, pady=10)

        # Create an entry widget for the input field
        self.input_entry = tk.Entry(self.input_frame, font=("Helvetica", 20))
        self.input_entry.pack(fill=tk.X, expand=True, padx=5, pady=3)

        # Bind the '<Return>' key to the input field
        self.input_entry.bind("<Return>", self.add_message)
       
        self.style = ttk.Style()
        self.style.configure("Round.TButton", padding=3, relief="solid", borderwidth=3, font=("Helvetica", 12), shape="circle")
        
        self.upload_button = ttk.Button(self.input_frame, text="Upload File", style="Round.TButton", command=self.upload_file)
        self.downloadall_button = ttk.Button(self.input_frame, text="Download File", style="Round.TButton", command=self.download_all)
        
        # Create a button to upload a CSV file
        self.upload_button.pack(side=tk.LEFT, pady=1, padx=1)

        # DOWNLOADS
        self.downloadall_button.pack(side=tk.RIGHT, pady=1, padx=1)
        
    def upload_file(self):
        file_path = askopenfilename()
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            self.data = pd.read_excel(file_path)

        arr = np.array(self.data.columns[0]) # convert to numpy array to avoid pandas elimination of duplicate values
        data_list = self.data[arr].tolist()
        
        self.resultCSV = {}

        for n in data_list:

            isDuplicate = False
            duplicateIndex = 0

            # Check duplicate values
            if n in self.resultCSV:
                isDuplicate = True
                # get the index of the duplicate value)
                duplicateIndex = list(self.resultCSV.keys()).index(n) 

            self.message_list.insert(tk.END, f"Checking {n}...")
            self.message_list.see(tk.END)
            self.root.update()

            if not isDuplicate:
                status = self.check(n)
            else:
                status = "Número duplicado."
                self.resultCSV[duplicateIndex] = status

            self.resultCSV[n] = status
            print(self.resultCSV[n])

            self.root.update()

        self.driver.login()

        self.message_list.insert(tk.END, "")
        self.message_list.insert(tk.END, f"Your verification is done for {len(data_list)} numbers.")
        self.message_list.insert(tk.END, "")
        self.message_list.insert(tk.END, "You can now download the results.")
        self.message_list.see(tk.END)
        self.root.update()


    def download_all(self):
        # add the results to the dataframe
        self.data['Status'] = self.resultCSV.values()
        file_path = asksaveasfilename(defaultextension='.csv', initialfile='Results.csv')
        self.data.to_csv(file_path, index=False)
    # LOGIN
    def checkOne(self): #switch_bindings
        # unbind the <Return> from the old entry
        self.input_entry.unbind("<Return>")

        # create the popup
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Single Check")
        self.popup.iconbitmap("Project\logo.ico")
        self.popup.geometry("200x100")
        self.popup.configure(bg='#25D366')
        self.popup.resizable(0, 0)

        # center the popup in the main window
        x = (self.root.winfo_screenwidth() - self.popup.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.popup.winfo_reqheight()) / 2
        self.popup.geometry("+%d+%d" % (x, y))

        # make the main window unclickable and unmovable
        self.popup.grab_set()

        frame = tk.Frame(self.popup, bd=2, relief=tk.SUNKEN, bg='#25D366')
        frame.pack(fill=tk.BOTH, expand=True)

        # create a label for the title
        title_label = tk.Label(frame, text="Username:", bg='#25D366', fg='white', font=("TkDefaultFont", 14))
        title_label.pack(pady=(10, 0))

        # create a new entry in the popup
        self.popup_entry = tk.Entry(frame, font=("TkDefaultFont", 14), bg='#fff', fg='black')
        self.popup_entry.pack()

        # bind the <Return> to the new entry
        self.popup.bind("<Return>", lambda event, entry=self.popup_entry: self.popup_action(event))

    def popup_action(self, event):
        # get the text from the entry
        popup_text = self.popup_entry.get()
        self.message_list.insert(tk.END, popup_text)

        # destroy the popup
        self.popup.destroy()

        # bind the <Return> back to the main entry
        self.root.bind("<Return>", lambda event, entry=self.input_entry: self.add_message(event))

    # Function to add message to the message list
    def add_message(self, event):
        # Get the text from the input field
        text = self.input_entry.get()
        self.check(text)

    def check(self, id):
        # For Brazil here it's 11, you can remove it but helps find errors beforehand. (can also be added a country code and use it)
        id = str(id)
        if(len(id) < 11): 
            self.message_list.insert(tk.END, f"{id}: ERROR! Not enough digits, verify the number and try again.")
        elif(len(id) > 11):
            self.message_list.insert(tk.END, f"{id}: ERROR! Too many digits, verify the number and try again.")
        else:
            
            number = "55" + id
            status = self.driver.run(number)

        return status

    def login(self):

        self.driver.login()
        # time.sleep(10)

        # # create the popup
        # self.popup = tk.Toplevel(self.root)
        # self.popup.title("Login")
        # self.popup.iconbitmap("Project\logo.ico")
        # self.popup.geometry("300x300")
        # self.popup.configure(bg='#25D366')
        # self.popup.resizable(0, 0)

        # # center the popup in the main window
        # x = (self.root.winfo_screenwidth() - self.popup.winfo_reqwidth()) / 2
        # y = (self.root.winfo_screenheight() - self.popup.winfo_reqheight()) / 2
        # self.popup.geometry("+%d+%d" % (x, y))

        # # make the main window unclickable and unmovable
        # self.popup.grab_set()

        # frame = tk.Frame(self.popup, bd=2, relief=tk.SUNKEN, bg='#25D366')
        # frame.pack(fill=tk.BOTH, expand=True)

        # image = Image.open("qr_code.png")
        # image = image.resize((300, 300), Image.ANTIALIAS)
        # image = ImageTk.PhotoImage(image)
            
        # self.canvas = tk.Canvas(frame, width=270, height=270)
        # self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        # self.canvas.pack(fill=tk.BOTH, expand=True)
