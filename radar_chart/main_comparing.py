import matplotlib

from utils.services import RadarData


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 2 (Поменяли стекло)\LVDS ВП'

# TODO: Добавить возможность расчета из другой папки со сравнением на соответствующих графиках
DIR2_NAME =r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\LVDS ВП'


if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('TkAgg')

    data1 = RadarData(DIR_NAME)
    data2 = RadarData(DIR2_NAME)

