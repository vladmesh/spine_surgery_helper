import tkinter as tk

from db_helper import DBHelper
from enums import ParameterType


class InterOperationalControlPage(tk.Toplevel):
    def __init__(self, patient_id):
        super().__init__()
        self.title("Интраоперационный контроль за восстановлением исходной анатомии позвоночника")

        self.resizable(True, True)

        self.db_helper = DBHelper()


        self.input_entries = {}
        self.calc_entries = {}
        self.prev_entries = {}

        self.patient_parameters = None
        self.patient_id = patient_id
        self.generate()

    def _return(self):
        self.destroy()


    def generate(self):
        self.patient_parameters = self.db_helper.get_patient_parameters(self.patient_id)
        parameters = self.db_helper.get_parameters()
        label = tk.Label(self, text="Интраоперационные параметры\nдля ввода")
        label.grid(row=0, column=0, sticky='w', padx=10, pady=5)

        label = tk.Label(self, text="Расчётные интраоперационные\nпараметры")
        label.grid(row=0, column=1, sticky='w', padx=10, pady=5)

        label = tk.Label(self, text="Расчётные параметры исходной\nанатомии позвоночника")
        label.grid(row=0, column=2, sticky='w', padx=10, pady=5)

        i = 1
        for idx in (11, 15, 16, 17):
            label_text = f"{idx} - {parameters[idx - 1][1]}"
            label = tk.Label(self, text=label_text)
            label.grid(row=i, column=3, sticky='w', padx=10, pady=5)

            entry = tk.Entry(self)
            entry.grid(row=i, column=2, padx=10, pady=5)
            entry.insert(0, self.patient_parameters.get_parameter_value_str(idx, ParameterType.DEFAULT_KT))
            entry.config(state='readonly')
            self.prev_entries[idx] = entry

            if idx != 11:
                entry = tk.Entry(self)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.config(state='readonly')
                self.calc_entries[idx] = entry

            if idx != 15:
                entry = tk.Entry(self)
                entry.grid(row=i, column=0, padx=10, pady=5)
                self.input_entries[idx] = entry
            i += 1

        self.return_button = tk.Button(self, text="Вернуться", command=self._return)
        self.return_button.grid(row=12, column=0, padx=10, pady=10)

        self.calculate_button = tk.Button(self, text="Рассчитать", command=self.calculate)
        self.calculate_button.grid(row=12, column=1, padx=10, pady=10)

        self.save_button = tk.Button(self, text="Сохранить", command=self.save)
        self.save_button.grid(row=12, column=2, padx=10, pady=10)
        self.save_button.config(state='disabled')

    def calculate(self):
        self.patient_parameters.delete_parameters_by_type(ParameterType.INTEROPERATION_INPUT)
        for idx in self.input_entries:
            self.patient_parameters.add_parameter(idx, ParameterType.INTEROPERATION_INPUT, self.input_entries[idx].get())
        self.patient_parameters.calculate_control()
        for idx in self.calc_entries:
            self.calc_entries[idx].config(state='normal')
            self.calc_entries[idx].delete(0, tk.END)
            self.calc_entries[idx].insert(0, self.patient_parameters.get_parameter_value_str(idx,
                                                                                         ParameterType.INTEROPERATION_CALCULATED))
            self.calc_entries[idx].config(state='readonly')

        self.save_button.config(state='normal')

    def save(self):
        self.db_helper.write_patient_parameters(self.patient_parameters, (ParameterType.INTEROPERATION_CALCULATED,
                                                                          ParameterType.INTEROPERATION_INPUT))
        self.save_button.config(state='disabled')
