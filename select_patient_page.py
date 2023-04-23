import tkinter as tk

from db_helper import DBHelper


class SelectPatient(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Выбор пациента")

        self.db_helper = DBHelper()

        self.patients = self.db_helper.get_patients()

        self.patients_listbox = tk.Listbox(self, selectmode='single')
        self.patients_listbox.grid(row=0, column=0, padx=10, pady=10)

        for patient in self.patients:
            self.patients_listbox.insert(tk.END, f"{patient[1]}")

        select_button = tk.Button(self, text="Выбрать", command=self.select)
        select_button.grid(row=1, column=0, padx=10, pady=10)

    def select(self):
        selected_patient = self.patients_listbox.curselection()
        print(selected_patient)
