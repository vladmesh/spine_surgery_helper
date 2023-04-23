import math
from typing import Any

from enums import ParameterType


class PatientParameter:
    def __init__(self, par_id, par_type, value):
        self.par_id = par_id
        self.par_type = par_type
        self.value = value


class PatientParameters:
    def __init__(self, patient_id=None, parameters=None):
        self.patient_id = patient_id
        if parameters is None:
            self.parameters = []
        else:
            self.parameters = parameters
        self.calculated_params_restore = [5, 6, 13, 16, 17, 15]
        self.calculated_params_control = [16, 17, 15]

    def calculate_restore(self):
        for par in self.calculated_params_restore:
            self._calculate_parameter_restore(par)
        for par in self.get_parameters_by_type(ParameterType.BROKEN_KT):
            if par.par_id not in self.calculated_params_restore:
                self.add_parameter(par.par_id, ParameterType.DEFAULT_KT, par.value)

    def _calculate_parameter_restore(self, par):
        needed_params = {
            5: [2, 3, 7],
            6: [2, 4, 8],
            13: [2, 14],
            15: [11, 16, 17],
            16: [1, 2, 3, 7, 9],
            17: [2, 4, 6, 10]
        }
        for needed_param in needed_params[par]:
            if self.get_parameter_value(needed_param, ParameterType.BROKEN_KT) == '':
                print('Для расчёта параметра', par, 'необходимо ввести параметр', needed_param)
                return
        calc_params = [self.get_parameter_value(x, ParameterType.BROKEN_KT) for x in needed_params[par]]
        if par == 5:
            par_2, par_3, par_7 = calc_params
            answer = (par_3 + par_7) / par_2
            self.add_parameter(5, ParameterType.DEFAULT_KT, answer)
        elif par == 6:
            par_2, par_4, par_8 = calc_params
            answer = (par_4 + par_8) / par_2
            self.add_parameter(6, ParameterType.DEFAULT_KT, answer)
        elif par == 13:
            par_2, par_14 = calc_params
            answer = (par_2 + par_14) / par_2
            self.add_parameter(13, ParameterType.DEFAULT_KT, answer)
        elif par == 15:
            par_11, par_16, par_17 = calc_params
            answer = math.asin((par_16 - par_17) / par_11)
            self.add_parameter(15, ParameterType.DEFAULT_KT, answer)
        elif par == 16:
            par_1, par_2, par_3, par_7, par_9 = calc_params
            answer = (par_3 + par_7) / par_2 + par_1 + par_9
            self.add_parameter(16, ParameterType.DEFAULT_KT, answer)
        elif par == 17:
            par_2, par_4, par_6, par_10 = calc_params
            answer = (par_4 + par_6) / par_2 + par_10
            self.add_parameter(17, ParameterType.DEFAULT_KT, answer)
        else:
            raise ValueError('Неверный параметр')

    def calculate_control(self):
        for par in self.calculated_params_control:
            self._calculate_parameter_control(par)

    def _calculate_parameter_control(self, par):
        needed_params = {
            15: [(11, ParameterType.DEFAULT_KT), (16, ParameterType.INTEROPERATION_KT),
                 (17, ParameterType.INTEROPERATION_KT)],
            16: [(16, ParameterType.INTEROPERATION_RG), (11, ParameterType.INTEROPERATION_RG),
                 (11, ParameterType.DEFAULT_KT)],
            17: [(17, ParameterType.INTEROPERATION_KT), (11, ParameterType.INTEROPERATION_KT),
                 (11, ParameterType.DEFAULT_KT)]
        }

        for n_p in needed_params[par]:
            if self.get_parameter_value(n_p[0], n_p[1]) == '':
                print(f'Для расчёта параметра {par} необходим параметр {n_p[0]}_{n_p[1]}')
                return
        calc_params = [self.get_parameter_value(x[0], x[1]) for x in needed_params[par]]
        if par == 15:
            par_11_1, par_16_3, par_17_3 = calc_params
            answer = math.asin((par_16_3 - par_17_3) / par_11_1)
            self.add_parameter(15, ParameterType.INTEROPERATION_KT, answer)
        elif par == 16:
            par_16_2, par_11_2, par_11_1 = calc_params
            answer = par_16_2 / par_11_2 / par_11_1
            self.add_parameter(16, ParameterType.INTEROPERATION_KT, answer)
        elif par == 17:
            par_17_2, par_11_2, par_11_1 = calc_params
            answer = par_17_2 / par_11_2 / par_11_1
            self.add_parameter(17, ParameterType.INTEROPERATION_KT, answer)
        else:
            raise ValueError('Неверный параметр')

    def add_parameter(self, par_id, par_type: ParameterType, value):
        try:
            value = round(float(value), 2)
        except ValueError:
            raise ValueError('Значение параметра должно быть числом')
        par = self.get_parameter(par_id, par_type)
        if par is None:
            self.parameters.append(PatientParameter(par_id, par_type, value))
        else:
            raise ValueError('Параметр с таким id и типом уже существует')

    def get_parameter(self, par_id, par_type: ParameterType) -> Any | None:
        for par in self.parameters:
            if par.par_id == par_id and par.par_type == par_type:
                return par
        return None

    def get_parameter_value(self, par_id, par_type: ParameterType):
        par = self.get_parameter(par_id, par_type)
        if par is None:
            return ''
        return par.value

    def get_parameters(self):
        return self.parameters

    def get_patient_id(self):
        return self.patient_id

    def get_parameters_by_type(self, par_type):
        result = []
        for par in self.parameters:
            if par.par_type == par_type:
                result.append(par)
        return result

    def get_parameters_by_types(self, par_types):
        result = []
        for par in self.parameters:
            if par.par_type in par_types:
                result.append(par)
        return result
