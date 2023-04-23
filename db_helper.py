import sqlite3
from patient_parameters import PatientParameters


class DBHelper:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )""")
        parameters = [
            (1, 'передняя высота межпозвоночного диска над телом вышележащего позвонка'),
            (2, 'задняя высота межпозвоночного диска над телом вышележащего позвонка'),
            (3, 'передняя высота вышележащего тела позвонка'),
            (4, 'задняя высота вышележащего тела позвонка'),
            (5, 'передняя высота тела повреждённого позвонка'),
            (6, 'задняя высота тела повреждённого позвонка'),
            (7, 'передняя высота нижележащего тела позвонка'),
            (8, 'задняя высота нижележащего тела позвонка'),
            (9, 'передняя высота межпозвоночного диска под телом нижележащего позвонка'),
            (10, 'задняя высота межпозвоночного диска под телом нижележащего позвонка'),
            (11, 'размер верхней кортикальной пластинки тела нижележащего позвонка'),
            (12, 'минимальный размер позвоночного канала на уровне тела вышележащего позвонка'),
            (13, 'минимальный размер позвоночного канала на уровне тела повреждённого позвонка'),
            (14, 'минимальный размер позвоночного канала на уровне тела нижележащего позвонка'),
            (15, 'угол сегментарной деформации, образованный нижней кортикальной пластинкой тела вышележащего '
                 'позвонка и верхней кортикальной пластинкой тела нижележащего позвонка'),
            (16, 'переднее межтеловое расстояние (от переднего края нижней кортикальной пластинки тела вышележащего '
                 'позвонка до переднего края верхней кортикальной пластинки тела нижележащего позвонка)'),
            (17, 'Заднее межтеловое расстояние (от заднего края нижней кортикальной пластинки тела '
                 'вышележащего позвонка до заднего края верхней кортикальной пластинки тела нижележащего позвонка)')
        ]
        if self.count_parameters() == 0:
            for i in parameters:
                self.cursor.execute("INSERT INTO parameters VALUES (?, ?)", i)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS patient_parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            parameter_id INTEGER,
            type INTEGER CHECK ( type IN (1, 2, 3, 4) ),
            value REAL,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (parameter_id) REFERENCES parameters(id)
        )""")
        self.connection.commit()

    def count_parameters(self):
        self.cursor.execute("SELECT COUNT(*) FROM parameters")
        return self.cursor.fetchone()[0]

    def add_patient(self, name):
        self.cursor.execute("INSERT INTO patients VALUES (NULL, ?)", (name,))
        self.connection.commit()

    def write_patient_parameters(self, patient_parameters: PatientParameters, types: tuple):
        self.delete_parameters_by_patient_id_and_types(patient_parameters.patient_id, types)
        for par in patient_parameters.get_parameters_by_types(types):
            self.cursor.execute("INSERT INTO patient_parameters VALUES (NULL, ?, ?, ?, ?)",
                                (patient_parameters.patient_id, par.par_id, par.par_type, par.value))
        self.connection.commit()

    def get_patient_parameters_by_parameter_type(self, patient_id, parameter_type) -> PatientParameters:
        self.cursor.execute("SELECT parameter_id, value FROM patient_parameters WHERE patient_id=? AND type=?",
                            (patient_id, parameter_type))
        patient_parameters = PatientParameters(patient_id)
        for par in self.cursor.fetchall():
            patient_parameters.add_parameter(par[0], parameter_type, par[1])
        return patient_parameters

    def get_patient_parameters(self, patient_id) -> PatientParameters:
        self.cursor.execute("SELECT id, type, value FROM patient_parameters WHERE patient_id=?",
                            (patient_id,))
        patient_parameters = PatientParameters(patient_id)
        for par in self.cursor.fetchall():
            patient_parameters.add_parameter(par[0], par[1], par[2])
        return patient_parameters

    def get_patients(self):
        self.cursor.execute("SELECT id, name FROM patients")
        return self.cursor.fetchall()

    def get_patient_by_name(self, patient_name):
        self.cursor.execute("SELECT id, name FROM patients WHERE name=?", (patient_name,))
        return self.cursor.fetchone()

    def get_parameters(self):
        self.cursor.execute("SELECT id, name FROM parameters")
        return self.cursor.fetchall()

    def delete_parameters_by_patient_id(self, patient_id):
        self.cursor.execute("DELETE FROM patient_parameters WHERE patient_id=?", (patient_id,))
        self.connection.commit()

    def delete_parameters_by_patient_id_and_types(self, patient_id, types):
        types = (int(x) for x in types)
        self.cursor.execute("DELETE FROM patient_parameters WHERE patient_id=? AND type IN ({})".format(
            ','.join(['?'] * len(types))), (patient_id,) + types)
        self.connection.commit()
