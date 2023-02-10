import tkinter as tk



def popup_action(event, popup, entry):
    # get the text from the entry
    input_text = entry.get()

    # destroy the popup
    popup.destroy()

    # bind the <Return> back to the main entry
    root.bind("<Return>", lambda event, entry=entry: main_action(event, entry))

def main_action(event, entry):
    # do something with the input text
    input_text = entry.get()
    print(input_text)

# create the main window
root = tk.Tk()
root.title("Main Window")

# create the main entry
entry = tk.Entry(root)
entry.pack()

# bind the <Return> to the main entry
root.bind("<Return>", lambda event, entry=entry: main_action(event, entry))

# create the Login button
button = tk.Button(root, text="Login", command=lambda: switch_bindings(root, entry))
button.pack()