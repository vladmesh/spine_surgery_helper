import math
import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog

from db_helper import DBHelper
from enums import ParameterType
from patient_parameters import PatientParameters, PatientParameter


class CalculateRestorePage(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Расчёты по восстановлению исходной анатомии позвоночника")
        self.db_helper = DBHelper()

        self.parameters = self.db_helper.get_parameters()

        self.saved = False

        self.entries = {}
        self.result_entries = {}
        self.calculated_parameters = [5, 6, 13, 15, 16, 17, 18, 19, 20]

        label = tk.Label(self, text=f"Параметры сломанного отдела позвоночника")
        label.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        label = tk.Label(self, text=f"Расчётные параметры исходной анатомии позвоночника")
        label.grid(row=0, column=1, sticky='w', padx=10, pady=5)

        for i, (number, description) in enumerate(self.parameters):
            label = tk.Label(self, text=f"{number} – {description}")
            label.grid(row=i + 1, column=2, sticky='w', padx=10, pady=5)

            if number not in (18, 19, 20):
                entry = tk.Entry(self)
                entry.grid(row=i + 1, column=0, padx=10, pady=5)
                self.entries[number] = entry

            if number in self.calculated_parameters:
                result_entry = tk.Entry(self, state='readonly')
                result_entry.grid(row=i + 1, column=1, padx=10, pady=5)
                self.result_entries[number] = result_entry

        calculate_button = tk.Button(self, text="Рассчитать", command=self.calculate)
        calculate_button.grid(row=len(self.parameters) + 1, column=0, padx=10, pady=10)

        self.save_button = tk.Button(self, text="Сохранить", command=self.save)
        self.save_button.grid(row=len(self.parameters) + 1, column=1, padx=10, pady=10)
        self.save_button.config(state='disabled')

        return_button = tk.Button(self, text="Вернуться", command=self._return)
        return_button.grid(row=len(self.parameters) + 1, column=2, padx=10, pady=10)

    def _return(self):
        if not self.saved:
            answer = tk.messagebox.askyesno("Внимание", "Вы не сохранили результаты расчётов. Выйти без сохранения?")
            if answer:
                self.destroy()
        else:
            self.destroy()

    def _write_answer(self, number, answer):
        entry = self.result_entries[number]
        entry.config(state='normal')
        entry.delete(0, tk.END)
        if answer != '':
            answer = round(float(answer), 2)
        entry.insert(0, str(answer))
        entry.config(state='readonly')

    def _get_params_or_none(self, *numbers):
        answer = []
        for number in numbers:
            try:
                answer.append(float(self.result_entries[number].get()))
            except ValueError:
                return None
        return answer

    def calculate(self):
        self.save_button.config(state='normal')
        self.patient_parameters = PatientParameters()
        for idx in range(1, 18):
            str_value = self.entries[idx].get()
            if str_value == '':
                continue
            try:
                float_value = float(str_value)
            except ValueError:
                print(f"Неверный формат значения параметра {idx}")
                continue
            self.patient_parameters.add_parameter(idx, ParameterType.BROKEN_KT, float_value)
        self.patient_parameters.calculate_restore()
        for idx in self.calculated_parameters:
            self._write_answer(idx, self.patient_parameters.get_parameter_value(idx, ParameterType.DEFAULT_KT))

    def save(self):
        name = None
        while name is None:
            name = tkinter.simpledialog.askstring("Сохранение", "Введите имя пользователя:")
            patient = self.db_helper.get_patient_by_name(name)
            if patient is not None:
                answer = tk.messagebox.askyesno("Внимание", "Пользователь с таким именем уже существует. Перезаписать?")
                if not answer:
                    name = None
                else:
                    self.db_helper.delete_parameters_by_patient_id(patient[0])
            if patient is None:
                self.db_helper.add_patient(name)
                patient = self.db_helper.get_patient_by_name(name)
            self.patient_parameters.patient_id = patient[0]
            self.db_helper.write_patient_parameters(self.patient_parameters, (ParameterType.BROKEN_KT,
                                                                              ParameterType.DEFAULT_KT))

        self.saved = True
