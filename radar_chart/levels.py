import matplotlib
import tkinter

from radar_chart.radarplot.levels.plotter import RadarLevelsPlotter
from radar_chart.radarplot.levels.data import RadarDataLevels


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\DVI ВП'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
DIR2_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 4 (Стекло НВИТ...317)\DVI ВП'


if __name__ == '__main__':
    matplotlib.get_backend()

    matplotlib.use('QtAgg')

    data_list = None

    data1 = RadarDataLevels(DIR_NAME)
    # print(40*'----')
    # print(data1.data)
    if DIR2_NAME is None:
        data2 = None
    else:
        data2 = RadarDataLevels(DIR2_NAME)
        data_list = [data1, data2]

    plotter = RadarLevelsPlotter(data1, data2, radar_data_list=data_list)
    # plotter.show()
    if DIR2_NAME is None:
        plotter.save(DIR_NAME + '_plot.png')
    else:
        plotter.save(DIR2_NAME + '_compare.png')
