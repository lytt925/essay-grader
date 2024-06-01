import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import os
from essay_judge.mail import Mail, send_mail
from essay_judge.interface_methods import add_methods
from essay_judge.records import load_from_json
from tkinter import ttk


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Essay Grader")
        self.geometry("1200x600")
        self.create_panes()
        self.last_selected_directory = None
        self.essay_collections = {}
        self.load_history()

    def load_history(self):
        historys = load_from_json('data.json')
        if len(historys) == 0:
            return
        self.history = historys[-1]

        self.last_selected_directory = self.history['dirpath']
        self.entry_filepath.insert(0, self.last_selected_directory)
        instruction = self.history['instruction']
        self.text_instruction.delete("1.0", tk.END)
        self.text_instruction.insert(tk.END, instruction)

        for id, essay_collection in self.history['essay_collections'].items():
            # check if the file still exists
            if os.path.exists(essay_collection['filename']):
                self.essay_collections[id] = essay_collection

        # update the dropdown
        self.name_dropdown['values'] = list(self.essay_collections.keys())
        self.name_dropdown.current(0)

        # update the result
        self.update_result_area()

    def create_panes(self):
        self.pane = tk.PanedWindow(
            self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.pane.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.pane)
        self.pane.add(self.left_frame, minsize=610)

        self.right_frame = tk.Frame(self.pane)
        self.pane.add(self.right_frame, minsize=610)

        self.setup_left_frame()
        self.setup_right_frame()

    def setup_left_frame(self):
        self.left_frame.grid_columnconfigure(1, weight=1)
        self.left_frame.rowconfigure(2, weight=1)

        self.label_filepath = tk.Label(self.left_frame, text="Folder Path")
        self.label_filepath.grid(
            row=0, column=0, sticky="ew", padx=(2, 2), pady=5)
        self.entry_filepath = tk.Entry(self.left_frame)
        self.entry_filepath.grid(
            row=0, column=1, sticky="ew", padx=(2, 2), pady=5)
        self.button_browse = tk.Button(
            self.left_frame, text="Browse", command=self.browse_dir)
        self.button_browse.grid(
            row=0, column=2, sticky="ew", padx=(2, 15), pady=5)

        # Instruction Widgets
        self.label_instruction = tk.Label(self.left_frame, text="Instruction:")
        self.label_instruction.grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        self.text_instruction = tk.Text(
            self.left_frame, height=10, wrap=tk.WORD, font=("Arial", 14), padx=10, pady=10)
        self.text_instruction.insert(tk.END, "請在這裡輸入評分標準\n\n")
        self.text_instruction.grid(
            row=2, column=0, columnspan=3, sticky="nsew", padx=(10, 15), pady=5)

        self.progress_bar = ttk.Progressbar(
            self.left_frame, orient="horizontal", length=200, mode='determinate')
        self.progress_bar.grid(row=3, column=0, columnspan=3, padx=(
            20, 25), pady=(3, 3), sticky="ew")
        self.button_grade = tk.Button(
            self.left_frame, text="Grade All", command=self.grade_all)
        self.button_grade.grid(row=4, column=1, columnspan=1, pady=20)

    def setup_right_frame(self):
        # Configure column weights
        self.right_frame.columnconfigure(0, weight=0)
        self.right_frame.columnconfigure(1, weight=0)
        self.right_frame.columnconfigure(2, weight=1)
        self.right_frame.rowconfigure(3, weight=1)

        self.label_name = tk.Label(self.right_frame, text="Name")
        self.label_name.grid(row=0, column=0, padx=(10, 2), pady=5, sticky="w")
        self.name_dropdown = ttk.Combobox(
            self.right_frame, values=[], width=35, state="readonly")
        self.name_dropdown.grid(
            row=0, column=1, padx=(2, 10), pady=5, sticky="w")
        self.name_dropdown.bind("<<ComboboxSelected>>", self.on_essay_select)

        self.button_next = tk.Button(
            self.right_frame, text="Next", command=self.next_essay)
        self.button_next.grid(
            row=0, column=2, padx=(2, 10), pady=5, sticky="w")

        # Email Subject
        self.label_emailsubject = tk.Label(
            self.right_frame, text="Email Subject")
        self.label_emailsubject.grid(
            row=1, column=0, sticky="w", padx=(10, 2), pady=5)
        self.entry_emailsubject = tk.Entry(self.right_frame)
        self.entry_emailsubject.grid(
            row=1, column=1, sticky="ew", padx=(2, 2), pady=5)

        # Result Widgets
        self.label_result = tk.Label(self.right_frame, text="Result:")
        self.label_result.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.text_result = tk.Text(
            self.right_frame, height=10, wrap=tk.WORD, font=("Arial", 12), padx=8, pady=8)
        self.text_result.grid(row=3, column=0, columnspan=3,
                              sticky="nsew", padx=10, pady=5)

        self.button_view = tk.Button(self.right_frame, text="View Essay")
        self.button_view.grid(row=4, column=0, padx=(
            20, 10), pady=20, sticky="ew")
        self.button_regrade = tk.Button(
            self.right_frame, text="Regrade", command=self.grade_one)
        self.button_regrade.grid(
            row=4, column=1, padx=(2, 10), pady=5, sticky="w")

        # self.button_regrade = tk.Button(self.right_frame, text="Grade this", command=self.grade_one)
        # self.button_regrade.grid(row=4, column=0, padx=(20, 10), pady=20, sticky="ew")

        self.button_send = tk.Button(
            self.right_frame, text="Send Mail", command=self.open_confirmation)
        self.button_send.grid(row=4, column=1, columnspan=2,
                              padx=(10, 20), pady=20, sticky="e")


add_methods(Interface)

if __name__ == "__main__":
    app = Interface()
    app.mainloop()
