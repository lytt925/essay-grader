import tkinter as tk
from tkinter import filedialog
from .main import process_essay

def submit():
    # Get values from the GUI
    filepath = filepath_entry.get()
    email = email_entry.get()
    mail_subject = mail_subject_entry.get()  # Get the mail subject from the new entry field
    instruction = instruction_text.get("1.0", tk.END).strip()  # Get text from Text widget

    # Print the values to the console
    print("File Path:", filepath)
    print("Email:", email)
    print("Mail Subject:", mail_subject)  # Print the mail subject
    print("Instructions:", instruction)

    # Add your logic here to process the input values (e.g., send an email)
    process_essay(email, mail_subject, filepath, instruction)


def browse_file():
    filepath = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All files", "*.*")]
    )
    if filepath:
        filepath_entry.delete(0, 'end')  # Clear any existing text in the entry
        filepath_entry.insert(0, filepath)  # Insert the selected file path

def main():
    root = tk.Tk()
    root.title("Input Form")
    root.geometry("500x300")  # Set the size of the window

    global filepath_entry, email_entry, mail_subject_entry, instruction_text

    frame = tk.Frame(root, pady=10)
    frame.pack(expand=True)

    # File path entry with browse button
    tk.Label(frame, text="File Path:").pack(anchor='w')
    filepath_entry = tk.Entry(frame, width=50)
    filepath_entry.pack(fill='x', expand=True)
    browse_button = tk.Button(frame, text="Browse", command=browse_file)
    browse_button.pack()

    # Email entry
    tk.Label(frame, text="Email:").pack(anchor='w')
    email_entry = tk.Entry(frame, width=50)
    email_entry.pack(fill='x', expand=True)

    # Mail Subject entry
    tk.Label(frame, text="Mail Subject:").pack(anchor='w')
    mail_subject_entry = tk.Entry(frame, width=50)
    mail_subject_entry.pack(fill='x', expand=True)

    # Instruction entry (now using a Text widget for multiline input)
    tk.Label(frame, text="Instructions:").pack(anchor='w')
    instruction_text = tk.Text(frame, height=5)
    instruction_text.pack(fill='x', expand=True)

    # Submit button
    submit_button = tk.Button(frame, text="Submit", command=submit)
    submit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
