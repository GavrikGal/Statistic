import pandas as pd

from .base import BaseRadarData


class RadarDataR2(BaseRadarData):
    """Класс данных для круговых диаграмм зон R2 по углам"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные о зонах R2 (на всех углах измерения) для отображения их на круговых диаграммах

        :param dir_path: путь к папке со списком файлов данных
        """
        BaseRadarData.__init__(self, dir_path)

    def make_data(self) -> pd.DataFrame:
        """
        Читает имя каждого файла из списка self.files парсит в нем угол, на котором проводились измерения, и
        результат рассчитанной зоны R2. Из этих данных формирует ДатаСерию для всех положений (углов) измерений

        :return: ДатаСерия с углами, в качестве индексов, и R2, в качестве значений
        """

        data = pd.DataFrame(columns=["angle", "main", "lower"])
        # Перебрать названия всех файлов папки и выбрать из них угол,
        # на котором проводились измерения, и радиус зоны R2
        for i, filename in enumerate(self.files):
            angle = self.get_angle_from_filename(filename)
            r2 = self.get_r2_from_filename(filename)
            min_r2 = self._calc_lower_r2(r2)

            new_row = {'angle': angle, 'main': r2, 'lower': min_r2}
            data.loc[len(data)] = new_row

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

