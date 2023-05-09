import tkinter as tk

from calculate_restore_page import CalculateRestorePage
from info_page import InfoPage
from interoperational_control_page import InterOperationalControlPage
from select_patient_page import SelectPatient


def open_page1():
    CalculateRestorePage()


def open_page2():
    SelectPatient(InterOperationalControlPage)


def open_page3():
    SelectPatient(InfoPage)


main_window = tk.Tk()
main_window.title("Помощник хирурга")

button1 = tk.Button(main_window, text="Расчёты по восстановлению исходной анатомии позвоночника", command=open_page1)
button1.pack(pady=10)

button2 = tk.Button(main_window, text="Интраоперационный контроль за восстановлением исходной анатомии позвоночника",
                    command=open_page2)
button2.pack(pady=10)

button3 = tk.Button(main_window, text="Сохранённые данные о пациентах", command=open_page3)
button3.pack(pady=10)

main_window.mainloop()
