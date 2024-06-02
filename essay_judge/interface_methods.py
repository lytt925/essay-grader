import tkinter as tk
from tkinter import filedialog
import threading
import os
from essay_judge.mail import Mail, send_mail
from essay_judge.process_essay import grade_batch
from essay_judge.records import save_to_json


def add_methods(cls):
    def validate_input(self, filepath, instruction):
        # Validate filepath and instructions
        if not filepath or instruction == "請在這裡輸入評分標準\n\n" or instruction == "":
            self.toggle_inputs(True)
            return False
        return True

    def start_grading_thread(self, filepath, instruction, grade_one=False):
        # Start the thread for grading
        process_thread = threading.Thread(
            target=self.grade_all_thread, args=(filepath, instruction, grade_one))
        process_thread.start()

    def grade_all(self):
        self.toggle_inputs(False)
        filepath = self.entry_filepath.get()
        instruction = self.text_instruction.get("1.0", tk.END).strip()
        if self.validate_input(filepath, instruction):
            self.start_grading_thread(filepath, instruction)

    def grade_one(self):
        self.toggle_inputs(False)
        current_id = self.name_dropdown.get()
        if current_id:
            filepath = self.essay_collections[current_id]['filename']
            instruction = self.text_instruction.get("1.0", tk.END).strip()
            if self.validate_input(filepath, instruction):
                self.start_grading_thread(filepath, instruction, True)

    def browse_dir(self):
        initial_directory = self.last_selected_directory if self.last_selected_directory else os.path.expanduser(
            '~/Desktop/course1122/ComputationalLinguistics/Final Project/essay-local/essay-judge/essays')
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

            files = os.listdir(os.path.expanduser(dirpath))
            for file in files:
                if file.endswith(".docx"):
                    [id, filename] = file.split("_")
                    essay_collection = {
                        "filename": os.path.join(os.path.expanduser(dirpath), file),
                        "original_text": "",
                        "grade_content": ""
                    }
                    if id not in self.essay_collections:
                        self.essay_collections[id] = essay_collection

            self.name_dropdown['values'] = list(self.essay_collections.keys())
            self.name_dropdown.current(0)

        # focus back to the window
        self.focus_force()

    def next_essay(self):
        if len(self.essay_collections.keys()) == 0:
            return
        current_index = self.name_dropdown.current()
        next_index = (current_index + 1) % len(self.essay_collections.keys())
        self.name_dropdown.current(next_index)
        if (current_index != next_index):
            self.update_result_area()
            self.update_essay_text()

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
        # self.button_next.config(state='normal' if state else 'disabled')
        # self.name_dropdown.config(state='normal' if state else 'disabled')
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

    def grade_all_thread(self, filepath, instruction, grade_one=False):
        # Get the length of the essay_collections
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = len(
            self.essay_collections) if not grade_one else 1
        for result in grade_batch(filepath, instruction):
            print(result)
            self.essay_collections[result["id"]
                                   ]['original_text'] = result["original_text"]
            self.essay_collections[result["id"]
                                   ]['grade_content'] = result["grade_content"]
            self.after(0, self.update_result_area)
            self.progress_bar['value'] += 1

        new_records = {
            "dirpath": self.entry_filepath.get(),
            "instruction": self.text_instruction.get("1.0", tk.END).strip(),
            "essay_collections": self.essay_collections
        }
        self.after(0, self.toggle_inputs, True)
        save_to_json('./results/data.json', new_records)

    def open_confirmation(self):
        # Create a top-level window for the confirmation dialog
        confirmation_window = tk.Toplevel(self)
        confirmation_window.title("Confirm Send Mail")
        confirmation_window.geometry("300x200")

        # Message Label
        label = tk.Label(confirmation_window,
                         text="Are you sure you want to send the email?")
        label.pack(pady=10, fill=tk.X)

        to = "To: " + self.name_dropdown.get() + "@ntu.edu.tw"
        subject = 'Email Subject: ' + self.entry_emailsubject.get()

        # Email Address Label
        self.label_confirm_to = tk.Label(
            confirmation_window, text=to, anchor="w")
        # Fill in the X direction
        self.label_confirm_to.pack(fill=tk.X, padx=15, pady=5)

        self.label_confirm_subject = tk.Label(
            confirmation_window, text=subject, anchor="w")
        self.label_confirm_subject.pack(
            fill=tk.X, padx=15, pady=5)  # Fill in the X direction

        # Send Button
        send_btn = tk.Button(confirmation_window, text="Send",
                             command=lambda: self.send_action(confirmation_window))
        send_btn.pack(side="left", padx=10, pady=10)

        # Cancel Button
        cancel_btn = tk.Button(
            confirmation_window, text="Cancel", command=confirmation_window.destroy)
        cancel_btn.pack(side="right", padx=10, pady=10)

    # Method to update the essay text when a new essay is selected
    def update_essay_text(self, event=None):
        if hasattr(self, 'essay_window'):
            current_id = self.name_dropdown.get()
            original_text = self.essay_collections[current_id]['original_text']
            self.essay_text.config(state=tk.NORMAL)
            self.essay_text.delete(1.0, tk.END)
            self.essay_text.insert(tk.END, original_text)
            self.essay_text.config(state=tk.DISABLED)

    def view_essay(self):
        # remove the existing window if it exists
        if hasattr(self, 'essay_window'):
            if self.essay_window.winfo_exists():
                return

        # Create a top-level window for viewing the essay
        self.essay_window = tk.Toplevel(self)
        self.essay_window.title("View Essay")
        self.essay_window.geometry("600x400+600+0")

        # Text widget to display the essay
        self.essay_text = tk.Text(self.essay_window, wrap=tk.WORD)
        self.essay_text.pack(expand=True, fill=tk.BOTH)

        # Initially populate the text widget with the current essay's text
        current_id = self.name_dropdown.get()
        if current_id not in self.essay_collections:
            return
        original_text = self.essay_collections[current_id]['original_text']
        self.essay_text.insert(tk.END, original_text)
        self.essay_text.config(state=tk.DISABLED)

    def send_action(self, confirmation_window):
        # Disable all inputs and the grade button
        self.toggle_inputs(False)
        email = self.name_dropdown.get() + "@ntu.edu.tw"
        mail_subject = self.entry_emailsubject.get()
        original_text = self.essay_collections[self.name_dropdown.get(
        )]['original_text']
        result = self.text_result.get("1.0", tk.END).strip()
        mail_content = f"""
        <strong>原文：</strong> <br>
        {original_text}
        <br><br>
        <strong>評語：</strong> <br>
        {result}
        """
        mail = Mail(to=email,
                    subject=mail_subject,
                    content=mail_content)

        send_thread = threading.Thread(
            target=self.tk_send_mail_thread, args=(mail,))
        send_thread.start()
        confirmation_window.destroy()

    def tk_send_mail_thread(self, mail):
        res = send_mail(mail)
        print("OK:", res)
        self.after(0, self.toggle_inputs, True)
        return {"message": "Email sent successfully"}

    cls.grade_all = grade_all
    cls.grade_one = grade_one
    cls.validate_input = validate_input
    cls.start_grading_thread = start_grading_thread
    cls.browse_dir = browse_dir
    cls.next_essay = next_essay
    cls.browse_file = browse_file
    cls.toggle_inputs = toggle_inputs
    cls.update_result_area = update_result_area
    cls.grade_all_thread = grade_all_thread
    cls.send_action = send_action
    cls.tk_send_mail_thread = tk_send_mail_thread
    cls.on_essay_select = on_essay_select
    cls.open_confirmation = open_confirmation
    cls.view_essay = view_essay
    cls.update_essay_text = update_essay_text

    return cls
