import matplotlib

from utils.services import RadarData, RadarPlotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 2 (Поменяли стекло)\LVDS ВП'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
DIR2_NAME =r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\LVDS ВП'

if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('TkAgg')

    data1 = RadarData(DIR_NAME)
    if DIR2_NAME is not None:
        data2 = RadarData(DIR2_NAME)
    else:
        data2 = None

    plotter = RadarPlotter(data1, data2)
    plotter.show()
    plotter.save()
