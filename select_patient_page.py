import tkinter as tk

from db_helper import DBHelper


class SelectPatient(tk.Toplevel):
    def __init__(self, next_page):
        super().__init__()
        self.title("Выбор пациента")

        self.db_helper = DBHelper()

        self.patients = self.db_helper.get_patients()

        self.patients_listbox = tk.Listbox(self, selectmode='single')
        self.patients_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.next_page = next_page

        for patient in self.patients:
            self.patients_listbox.insert(tk.END, f"{patient[1]}")

        select_button = tk.Button(self, text="Выбрать", command=self.select)
        select_button.grid(row=1, column=0, padx=10, pady=10)

        delete_button = tk.Button(self, text="Удалить", command=self.delete)
        delete_button.grid(row=2, column=0, padx=10, pady=10)

    def reload_patients(self):
        self.patients = self.db_helper.get_patients()
        self.patients_listbox.delete(0, tk.END)
        for patient in self.patients:
            self.patients_listbox.insert(tk.END, f"{patient[1]}")

    def select(self):
        selected_patient = self.patients_listbox.curselection()
        self.next_page(self.patients[selected_patient[0]][0])

    def delete(self):
        selected_patient_idx = self.patients_listbox.curselection()[0]
        self.selected_patient_id = self.patients[selected_patient_idx][0]
        self.db_helper.delete_patient(self.selected_patient_id)
        self.patients_listbox.delete(selected_patient_idx)
        self.reload_patients()
