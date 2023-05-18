import os
import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import LEFT

from PIL import ImageTk, Image
from db_helper import DBHelper
from enums import ParameterType
from patient_parameters import PatientParameters


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
        self.obligatory_params = [1, 2, 3, 4, 5, 5, 7, 8, 9, 10, 11]

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)



        # Create a frame inside the canvas which will be scrolled with it
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        image = Image.open("images/img.png")
        image = image.resize((200, 250), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.scrollable_frame, image=image)
        image_label.image = image
        image_label.grid(row=6, column=3, rowspan=10, padx=10, pady=5)

        label = tk.Label(self.scrollable_frame, text=f"Параметры сломанного \n отдела позвоночника",
                         font=("Arial Bold", 8))
        label.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        label = tk.Label(self.scrollable_frame, text=f"Расчётные параметры \n исходной анатомии \n позвоночника",
                         font=("Arial Bold", 8))
        label.grid(row=0, column=1, sticky='w', padx=10, pady=5)

        for i, (number, description) in enumerate(self.parameters):
            label = tk.Label(self.scrollable_frame, text=f"{number} – {description}", justify=LEFT,
                             font=("Arial Bold", 8))
            label.grid(row=i + 1, column=2, sticky='w', padx=10, pady=5)

            if number not in (18, 19, 20):
                entry = tk.Entry(self.scrollable_frame)
                entry.grid(row=i + 1, column=0, padx=10, pady=5)
                self.entries[number] = entry

            if number in self.calculated_parameters:
                result_entry = tk.Entry(self.scrollable_frame, state='readonly', font=("Arial Bold", 8))
                result_entry.grid(row=i + 1, column=1, padx=10, pady=5)
                self.result_entries[number] = result_entry

        calculate_button = tk.Button(self.scrollable_frame, text="Рассчитать", command=self.calculate)
        calculate_button.grid(row=len(self.parameters) + 1, column=0, padx=10, pady=10)

        self.save_button = tk.Button(self.scrollable_frame, text="Сохранить", command=self.save)
        self.save_button.grid(row=len(self.parameters) + 1, column=1, padx=10, pady=10)
        self.save_button.config(state='disabled')

        return_button = tk.Button(self.scrollable_frame, text="Вернуться", command=self._return)
        return_button.grid(row=len(self.parameters) + 1, column=2, padx=10, pady=10)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind('<Configure>', self._on_frame_configure)
        if os.name == 'nt':
            self.scrollable_frame.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.scrollable_frame.bind_all("<Button-4>", self._on_mousewheel)
            self.scrollable_frame.bind_all("<Button-5>", self._on_mousewheel)


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
            answer = str(answer)
            answer = answer.replace('.', ',')
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
        for idx in self.obligatory_params:
            if self.entries[idx].get() == '':
                tk.messagebox.showerror("Ошибка", f"Параметр {idx} не заполнен")
                return
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