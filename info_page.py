import tkinter as tk

from db_helper import DBHelper
from enums import ParameterType
import xlsxwriter

class InfoPage(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Сохранённые данные о пациентах")

        self.resizable(True, True)

        self.db_helper = DBHelper()

        self.patients = self.db_helper.get_patients()

        self.patients_listbox = tk.Listbox(self, selectmode='single')
        self.patients_listbox.grid(row=0, column=0, padx=8, pady=8)

        for patient in self.patients:
            self.patients_listbox.insert(tk.END, f"{patient[1]}")

        self.select_button = tk.Button(self, text="Выбрать", command=self.select)
        self.select_button.grid(row=1, column=0, padx=8, pady=8)

        self.return_button = tk.Button(self, text="Вернуться", command=self._return)
        self.return_button.grid(row=2, column=0, padx=8, pady=8)


        self.patient_parameters = None

    def _return(self):
        self.destroy()

    def select(self):
        selected_patient_idx = self.patients_listbox.curselection()[0]
        self.selected_patient_id = self.patients[selected_patient_idx][0]
        self.patient_parameters = self.db_helper.get_patient_parameters(self.selected_patient_id)
        parameters = self.db_helper.get_parameters()
        self.patients_listbox.destroy()
        self.select_button.destroy()
        self.return_button.destroy()


        label = tk.Label(self, text="Параметры сломанного отдела позвоночника на КТ", font=("Arial Bold", 8))
        label.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        label = tk.Label(self, text="Интраоперационные параметры на Rg", font=("Arial Bold", 8))
        label.grid(row=0, column=2, sticky='w', padx=5, pady=5)

        label = tk.Label(self, text="Интраоперационные параметры на КТ", font=("Arial Bold", 8))
        label.grid(row=0, column=3, sticky='w', padx=5, pady=5)

        label = tk.Label(self, text="Параметры исходной анатомии позвоночника на КТ", font=("Arial Bold", 8))
        label.grid(row=0, column=4, sticky='w', padx=5, pady=5)
        i = 1
        for parameter in parameters:
            label_text = f"{parameter[0]} - {parameter[1]}"
            label = tk.Label(self, text=label_text, font=("Arial Bold", 8))
            label.grid(row=i, column=0, sticky='w', padx=5, pady=5)

            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=8, pady=5)
            entry.insert(0, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.BROKEN_KT))
            entry.config(state='readonly')

            entry = tk.Entry(self)
            entry.grid(row=i, column=2, padx=8, pady=5)
            entry.insert(0, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.INTEROPERATION_RG))
            entry.config(state='readonly')

            entry = tk.Entry(self)
            entry.grid(row=i, column=3, padx=8, pady=5)
            entry.insert(0, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.INTEROPERATION_KT))
            entry.config(state='readonly')

            entry = tk.Entry(self)
            entry.grid(row=i, column=4, padx=8, pady=5)
            entry.insert(0, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.DEFAULT_KT))
            entry.config(state='readonly')

            i += 1

        self.to_excel_button = tk.Button(self, text="Экспорт", command=self.to_excel)
        self.to_excel_button.grid(row=i, column=0, padx=8, pady=8)

        self.send_mail_button = tk.Button(self, text="Отправить на почту", command=self.send_mail)
        self.send_mail_button.grid(row=i, column=1, padx=8, pady=8)


    def to_excel(self):
        workbook = xlsxwriter.Workbook('Report.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 1, "Параметры сломанного отдела позвоночника на КТ")
        worksheet.write(0, 2, "Интраоперационные параметры на Rg")
        worksheet.write(0, 3, "Интраоперационные параметры на КТ")
        worksheet.write(0, 4, "Параметры исходной анатомии позвоночника на КТ")
        parameters = self.db_helper.get_parameters()
        i = 1
        for parameter in parameters:
            worksheet.write(i, 0, parameter[0])
            worksheet.write(i, 1, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.BROKEN_KT))
            worksheet.write(i, 2, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.INTEROPERATION_RG))
            worksheet.write(i, 3, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.INTEROPERATION_KT))
            worksheet.write(i, 4, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.DEFAULT_KT))
            i += 1
        workbook.close()

    def send_mail(self):
        pass
