import math
import pandas as pd

from dataclasses import dataclass
from typing import List


@dataclass
class Line:
    color: str = 'gray'
    style: str = '-'
    width: float = 1.
    alpha: float = 1.


def make_unique_frequency_list(data_list: List[pd.DataFrame]) -> List[float]:
    """
    Формирует общий список частот из всех выборок
    :param data_list: список с выборками частот, из которого создать список
    не повторяющихся частот
    :return: список уникальных частот
    """
    frequency_set = set()

    # Каждую частоту из выборок добавить в set, который обеспечивает уникальность частот
    for frequencies in data_list:
        for freq in frequencies:

            frequency_set.add(freq)

    # Преобразуем set в list и возвращаем список уникальных частот
    return list(frequency_set)


def determine_max_y_tick(df_list: List[pd.DataFrame]) -> int:
    """
    Определяет максимальный предел шкалы графика уровней (max_y_tick) кратный 10 единицам
    исходя из максимальных уровней данных в выборках
    :param df_list: список выборок данных
    :return: максимальное значение шкалы графика кратное 10
    """
    y_max = max(df.max().max() for df in df_list)
    max_y_tick = int(math.ceil(y_max / 10) * 10)
    return max_y_tick
