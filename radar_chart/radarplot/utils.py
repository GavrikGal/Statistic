import pandas as pd

from typing import List


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
