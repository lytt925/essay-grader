import tkinter as tk
from tkinter import filedialog
import threading
import os
from essay_judge.mail import Mail, send_mail
from essay_judge.process_essay import  grade_batch


def add_methods(cls):
    def grade_all(self):
        # Disable all inputs and the grade button
        self.toggle_inputs(False)
        filepath = self.entry_filepath.get()
        instruction = self.text_instruction.get("1.0", tk.END).strip()
        if not filepath or instruction == "請在這裡輸入評分標準\n\n" or instruction == "":
            self.toggle_inputs(True)
            return

        process_thread = threading.Thread(target=self.grade_all_thread, args=(filepath, instruction))
        process_thread.start()

    def browse_dir(self):
        initial_directory = self.last_selected_directory if self.last_selected_directory else os.path.expanduser('~/Desktop/course1122/ComputationalLinguistics/Final Project/essay-local/essay-judge/essays')
        dirpath = filedialog.askdirectory(
            title="Select a directory",
            initialdir=initial_directory
        )
        if dirpath:
            # Get the user's home directory path
            home = os.path.expanduser('~')
            # Check if the file path starts with the user's home directory path
            if dirpath.startswith(home):
                # Create a relative path using '~' instead of the full home directory path
                dirpath = '~' + dirpath[len(home):]
            self.entry_filepath.delete(0, 'end')
            self.entry_filepath.insert(0, dirpath)
            self.last_selected_directory = dirpath
        
            self.essay_collections = {}
            files = os.listdir(os.path.expanduser(dirpath))
            for file in files:
                if file.endswith(".docx"):
                    [id, filename] = file.split("_")
                    essay_collection = {
                        "filename": os.path.join(os.path.expanduser(dirpath), file),
                        "grade_content": ""
                    }
                    self.essay_collections[id] = essay_collection
            
            self.name_dropdown['values'] = list(self.essay_collections.keys())
            self.name_dropdown.current(0)
    
    def next_essay(self):
        current_index = self.name_dropdown.current()
        if len(self.essay_collection) == 0:
            return
        next_index = (current_index + 1) % len(self.essay_collection)
        self.name_dropdown.current(next_index)

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All files", "*.*")]
        )
        if filepath:
            self.entry_filepath.delete(0, 'end')
            self.entry_filepath.insert(0, filepath)

    def toggle_inputs(self, state):
        # State is True to enable, False to disable
        self.entry_filepath.config(state='normal' if state else 'disabled')
        self.text_instruction.config(state='normal' if state else 'disabled')
        self.button_browse.config(state='normal' if state else 'disabled')
        self.button_grade.config(state='normal' if state else 'disabled')
        self.button_regrade.config(state='normal' if state else 'disabled')
        self.button_next.config(state='normal' if state else 'disabled')
        self.name_dropdown.config(state='normal' if state else 'disabled')
        self.button_send.config(state='normal' if state else 'disabled')

    # Change combobox value and update result area
    def on_essay_select(self, event):
        print("Selected:", self.name_dropdown.get())
        self.update_result_area()

    def update_result_area(self):
        # get current combobox value
        current_id = self.name_dropdown.get()
        content = self.essay_collections[current_id]['grade_content']
        self.text_result.delete('1.0', tk.END)  # Clear existing content
        self.text_result.insert('1.0', content)  # Insert new content

    def grade_all_thread(self, filepath, instruction):
        results = grade_batch(filepath, instruction)
        for result in results:
            self.essay_collections[result["id"]]['grade_content'] = result["grade_content"]
        self.after(0, self.toggle_inputs, True)
        self.after(0, self.update_result_area)

    def send_action(self):
        # Disable all inputs and the grade button
        self.toggle_inputs(False)
        email = self.email_entry.get()
        mail_subject = self.mail_subject_entry.get()
        result = self.result_text.get("1.0", tk.END).strip()
        mail = Mail(to=email, subject=mail_subject, content="評語：\n\n" + result)

        send_thread = threading.Thread(target=self.tk_send_mail_thread, args=(mail,))
        send_thread.start()

    def tk_send_mail_thread(self, mail):
        res = send_mail(mail)
        print("OK:", res)
        # Use root.after to safely update GUI from a non-main thread
        self.root.after(0, self.toggle_inputs, True)
        return {"message": "Email sent successfully"}


    cls.grade_all = grade_all
    cls.browse_dir = browse_dir
    cls.next_essay = next_essay
    cls.browse_file = browse_file
    cls.toggle_inputs = toggle_inputs
    cls.update_result_area = update_result_area
    cls.grade_all_thread = grade_all_thread
    cls.send_action = send_action
    cls.tk_send_mail_thread = tk_send_mail_thread
    cls.on_essay_select = on_essay_select

    return cls


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Input Form")
        self.root.geometry("800x500")  # Set the size of the window

        self.frame = tk.Frame(self.root, pady=10)
        self.frame.pack(padx=15, pady=20, fill='both', expand=True)
        self.frame.grid_columnconfigure(1, weight=1)  # This makes the middle column expandable
        self.frame.grid_rowconfigure(3, weight=1)  # Allow the row with the instructions to expand
        self.frame.grid_rowconfigure(5, weight=1)  # Allow the row with the result to expand

        self.last_selected_directory = None

        self.setup_widgets()

    def setup_widgets(self):
        # File Path
        tk.Label(self.frame, text="File Path:").grid(row=0, column=0, sticky='w')
        self.filepath_entry = tk.Entry(self.frame, width=20)
        self.filepath_entry.grid(row=0, column=1, sticky='we')
        self.browse_button = tk.Button(self.frame, text="Browse", command=self.browse_dir)
        self.browse_button.grid(row=0, column=2)

        # Email
        tk.Label(self.frame, text="Email:").grid(row=1, column=0, sticky='w')
        self.email_entry = tk.Entry(self.frame, width=50)
        self.email_entry.grid(row=1, column=1, columnspan=2, sticky='we')

        # Mail Subject
        tk.Label(self.frame, text="Mail Subject:").grid(row=2, column=0, sticky='w')
        self.mail_subject_entry = tk.Entry(self.frame, width=50)
        self.mail_subject_entry.grid(row=2, column=1, columnspan=2, sticky='we')

        # Instructions
        tk.Label(self.frame, text="Instructions:").grid(row=3, column=0, sticky='nw')
        self.instruction_text = tk.Text(self.frame, height=6, padx=8, pady=8)
        self.instruction_text.grid(row=3, column=1, sticky='nswe')
        self.grade_button = tk.Button(self.frame, text="Grade", command=self.grade)
        self.grade_button.grid(row=3, column=2, sticky='ne', columnspan=5)

        # Result Area
        tk.Label(self.frame, text="Result:").grid(row=5, column=0, sticky='nw')
        self.result_text = tk.Text(self.frame, height=10, padx=8, pady=8)
        self.result_text.grid(row=5, column=1, columnspan=2, sticky='nswe')

        # Send Mail Button
        self.send_button = tk.Button(self.frame, text="Send Mail", command=self.send_action)
        self.send_button.grid(row=6, column=1, columnspan=2)


    def grade(self):
        # Disable all inputs and the grade button
        self.toggle_inputs(False)
        filepath = self.filepath_entry.get()
        instruction = self.instruction_text.get("1.0", tk.END).strip()

        process_thread = threading.Thread(target=self.grade_thread, args=(filepath, instruction))
        process_thread.start()

    def browse_dir(self):
        initial_directory = self.last_selected_directory if self.last_selected_directory else os.path.expanduser('~/Documents')
        dirpath = filedialog.askdirectory(
            title="Select a directory",
            initialdir=initial_directory
        )
        if dirpath:
            self.filepath_entry.delete(0, 'end')
            self.filepath_entry.insert(0, dirpath)
            self.last_selected_directory = dirpath

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All files", "*.*")]
        )
        if filepath:
            self.filepath_entry.delete(0, 'end')
            self.filepath_entry.insert(0, filepath)

    def toggle_inputs(self, state):
        # State is True to enable, False to disable
        self.filepath_entry.config(state='normal' if state else 'disabled')
        self.email_entry.config(state='normal' if state else 'disabled')
        self.mail_subject_entry.config(state='normal' if state else 'disabled')
        self.instruction_text.config(state='normal' if state else 'disabled')
        self.browse_button.config(state='normal' if state else 'disabled')
        self.grade_button.config(state='normal' if state else 'disabled')

    def update_result_area(self, content):
        self.result_text.delete('1.0', tk.END)  # Clear existing content
        self.result_text.insert('1.0', content)  # Insert new content

    def grade_thread(self, filepath, instruction):
        results = process_essay_batch(filepath, instruction)
        # Use root.after to safely update GUI from a non-main thread
        self.root.after(0, self.toggle_inputs, True)
        self.root.after(0, self.update_result_area, results[0]["content"])

    def send_action(self):
        # Disable all inputs and the grade button
        self.toggle_inputs(False)
        email = self.email_entry.get()
        mail_subject = self.mail_subject_entry.get()
        result = self.result_text.get("1.0", tk.END).strip()
        mail = Mail(to=email, subject=mail_subject, content="評語：\n\n" + result)

        send_thread = threading.Thread(target=self.tk_send_mail_thread, args=(mail,))
        send_thread.start()

    def tk_send_mail_thread(self, mail):
        res = send_mail(mail)
        print("OK:", res)
        # Use root.after to safely update GUI from a non-main thread
        self.root.after(0, self.toggle_inputs, True)
        return {"message": "Email sent successfully"}


def main():
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
