import os
import tkinter as tk
from tkinter import LEFT
import tkinter.messagebox

from db_helper import DBHelper
from enums import ParameterType
import xlsxwriter


class InfoPage(tk.Toplevel):
    def __init__(self, patient_id):
        super().__init__()
        self.title("Сохранённые данные о пациентах")

        self.resizable(True, True)

        self.db_helper = DBHelper()
        self.patient_id = patient_id

        self.patient_parameters = None
        self.generate()


    def _return(self):
        self.destroy()

    def generate(self):
        self.patient_parameters = self.db_helper.get_patient_parameters(self.patient_id)
        parameters = self.db_helper.get_parameters()

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Create a frame inside the canvas which will be scrolled with it
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        label = tk.Label(self.scrollable_frame, text="Параметры сломанного\nотдела позвоночника\n на КТ", font=("Arial Bold", 7))
        label.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        label = tk.Label(self.scrollable_frame, text="Расчётные параметры\n исходной анатомии\n позвоночника", font=("Arial Bold", 7))
        label.grid(row=0, column=2, sticky='w', padx=5, pady=5)

        label = tk.Label(self.scrollable_frame, text="Интраоперационные параметры\n для ввода", font=("Arial Bold", 7))
        label.grid(row=0, column=3, sticky='w', padx=5, pady=5)

        label = tk.Label(self.scrollable_frame, text="Расчётные интраоперационные\n параметры", font=("Arial Bold", 7))
        label.grid(row=0, column=4, sticky='w', padx=5, pady=5)
        i = 1
        for parameter in parameters:
            label_text = f"{parameter[0]} - {parameter[1]}"
            label = tk.Label(self.scrollable_frame, text=label_text, font=("Arial Bold", 7), justify=LEFT)
            label.grid(row=i, column=0, sticky='w', padx=5, pady=5)

            entry = tk.Entry(self.scrollable_frame, width=9)
            entry.grid(row=i, column=1, padx=8, pady=5)
            entry.insert(0, self.patient_parameters.get_parameter_value_str(parameter[0], ParameterType.BROKEN_KT))
            entry.config(state='readonly')

            entry = tk.Entry(self.scrollable_frame, width=9)
            entry.grid(row=i, column=2, padx=8, pady=5)
            entry.insert(0, self.patient_parameters.get_parameter_value_str(parameter[0], ParameterType.DEFAULT_KT))
            entry.config(state='readonly')

            entry = tk.Entry(self.scrollable_frame, width=9)
            entry.grid(row=i, column=3, padx=8, pady=5)
            entry.insert(0,
                         self.patient_parameters.get_parameter_value_str(parameter[0], ParameterType.INTEROPERATION_INPUT))
            entry.config(state='readonly')

            entry = tk.Entry(self.scrollable_frame, width=9)
            entry.grid(row=i, column=4, padx=8, pady=5)
            entry.insert(0, self.patient_parameters.get_parameter_value_str(parameter[0],
                                                                        ParameterType.INTEROPERATION_CALCULATED))
            entry.config(state='readonly')

            i += 1

        self.to_excel_button = tk.Button(self.scrollable_frame, text="Экспорт", command=self.to_excel)
        self.to_excel_button.grid(row=i, column=0, padx=8, pady=8)

        self.send_mail_button = tk.Button(self.scrollable_frame, text="Отправить на почту", command=self.send_mail)
        self.send_mail_button.grid(row=i, column=1, padx=8, pady=8)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind('<Configure>', self._on_frame_configure)
        self.scrollable_frame.bind('<Enter>', self._bind_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbind_mousewheel)

    def to_excel(self):
        patient_name = self.db_helper.get_patient_name(self.patient_id)
        filename = f"Report_{patient_name}.xlsx"
        workbook = xlsxwriter.Workbook(filename)
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format({'text_wrap': True, 'bold': True, 'align': 'center', 'font': 'Times New Roman'})
        auto_wrap = workbook.add_format({'text_wrap': True, 'align': 'left', 'font': 'Times New Roman'})
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Фамилия И.О., год рождения:", bold)
        worksheet.write(0, 1, patient_name)
        worksheet.set_row(2, 4 * 18, cell_format)

        worksheet.write(2, 1, "Параметры сломанного отдела позвоночника")
        worksheet.write(2, 2, "Расчётные параметры исходной анатомии позвоночника")
        worksheet.write(2, 3, "Интраоперационные параметры для ввода")
        worksheet.write(2, 4, "Расчётные интраоперационные параметры")
        worksheet.set_column(1, 4, 18)
        worksheet.set_column(0, 0, 44, auto_wrap)

        parameters = self.db_helper.get_parameters()
        for i in range(1, len(parameters) + 1):
            worksheet.set_row(i + 2, 3 * 18)
        i = 3
        for parameter in parameters:
            worksheet.write(i, 0, f"{parameter[0]} - {parameter[1]}")
            worksheet.write(i, 1, self.patient_parameters.get_parameter_value(parameter[0], ParameterType.BROKEN_KT))
            worksheet.write(i, 2,
                            self.patient_parameters.get_parameter_value(parameter[0], ParameterType.DEFAULT_KT))
            worksheet.write(i, 3,
                            self.patient_parameters.get_parameter_value(parameter[0],
                                                                        ParameterType.INTEROPERATION_INPUT))
            worksheet.write(i, 4, self.patient_parameters.get_parameter_value(parameter[0],
                                                                              ParameterType.INTEROPERATION_CALCULATED))
            i += 1
        workbook.close()
        tk.messagebox.showinfo("Экспорт", f"Отчёт успешно экспортирован в файл {filename}")

    def send_mail(self):
        pass

    def _on_frame_configure(self, event=None):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if os.name == 'nt':
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def _bind_mousewheel(self, event):
        if os.name == 'nt':
            self.scrollable_frame.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.scrollable_frame.bind_all("<Button-4>", self._on_mousewheel)
            self.scrollable_frame.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        if os.name == 'nt':
            self.scrollable_frame.unbind_all("<MouseWheel>")
        else:
            self.scrollable_frame.unbind_all("<Button-4>")
            self.scrollable_frame.unbind_all("<Button-5>")
