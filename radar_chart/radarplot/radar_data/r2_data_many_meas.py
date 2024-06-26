import math

import pandas as pd

from .base_many_meas_data import BaseManyMeasData

COVERAGE_FACTOR = 2   # Коэффициент охвата. При расчете расширенной неопределенности


class RadarDataR2ManyMeas(BaseManyMeasData):
    """Класс данных для круговых диаграмм зон R2 по углам"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные о зонах R2 (на всех углах измерения) для отображения их на круговых диаграммах

        :param dir_path: путь к папке со списком файлов данных
        """
        BaseManyMeasData.__init__(self, dir_path)

    def make_data(self) -> pd.DataFrame:
        """
        Читает имя каждого файла из списка self.files парсит в нем угол, на котором проводились измерения,
        результат рассчитанной зоны R2, номер измерений и т.д.
        Из этих данных формирует ДатаСерию для всех положений (углов) измерений

        :return: ДатаСерия с углами, в качестве индексов,
                 и R2 с нижней и верхней границей доверительного интервала, в качестве значений
        """

        # Пустой датасет для необработанных данных с именами столбцов
        raw_data = pd.DataFrame(columns=["meas_name", "interface", "polarisation", "angle", "r2", "rounding"])

        # Перебрать все файлы в списке и распарсить из путей данные по измерениям
        for file in self.files:
            meas_name = self._get_meas_name(file)
            interface = self._get_interface(file)
            polarisation = self._get_polarisation(file)
            filename = self._get_filename(file)
            angle = self.get_angle_from_filename(filename)
            r2 = self.get_r2_from_filename(filename)

            # Неопределенность дискретности округления Навигатором
            # расцениваем как прямоугольное распределение вероятностей. Поэтому
            rounding_uncertainty = ((r2 - self._calc_lower_r2(r2)) / 2) / (3 ** 0.5)

            # Принимаем за величину R2 значение в середине интервала от R2(min) до R2(max)
            r2 = r2 - (r2 - self._calc_lower_r2(r2)) / 2

            new_row = {'meas_name': meas_name, 'interface': interface,
                       'polarisation': polarisation, 'angle': angle, 'r2': r2,
                       'rounding': rounding_uncertainty}
            raw_data.loc[len(raw_data)] = new_row

        grouped_max_in_polarisation = raw_data.groupby(['meas_name', 'angle'],
                                                       as_index=False).max()[['angle', 'r2', 'rounding']]

        max_in_polarisation = pd.DataFrame(grouped_max_in_polarisation)

        grouped_r2_angle = max_in_polarisation.groupby('angle', as_index=False)['r2'].agg(['mean', 'std', 'count'])
        grouped_rounding_angle = max_in_polarisation.groupby('angle', as_index=False)['rounding'].mean()

        count = grouped_r2_angle['count'].max()

        # Выборочное стандартное отклонение среднего
        grouped_r2_angle['uncertainty'] = grouped_r2_angle['std'] / math.sqrt(count)

        # Суммарная неопределенность с коэффициентом охвата COVERAGE_FACTOR
        grouped_r2_angle['total_uncertainty'] = COVERAGE_FACTOR * (grouped_r2_angle['uncertainty'] ** 2 +
                                                                   grouped_rounding_angle['rounding'] ** 2) ** 0.5

        data = pd.DataFrame(columns=["angle", "main", "lower"])
        data['angle'] = grouped_r2_angle['angle']
        data['main'] = grouped_r2_angle['mean']
        data['lower'] = grouped_r2_angle['mean'] - grouped_r2_angle['total_uncertainty']
        data['upper'] = grouped_r2_angle['mean'] + grouped_r2_angle['total_uncertainty']

        # Установить углы в качестве индексов и отсортировать датафрей по индексам
        data = data.set_index('angle').sort_index()

        # Добавить в конец ДатаСерии данные начальной точки, чтобы график замкнулся
        data = pd.concat([data, data[:0]])

        return data

    @staticmethod
    def _calc_lower_r2(r2: float) -> float:
        """Вычисляет нижний уровень неопределенности зоны R2"""

        if r2 <= 10:
            return r2 - 1
        else:
            return r2 - 5
