import matplotlib

from radarplot.levels_plot import RadarDataLevels, RadarLevelsPlotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 2 (Поменяли стекло)\DVI ГП'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
DIR2_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\DVI ГП'


if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('TkAgg')

    data1 = RadarDataLevels(DIR_NAME)
    if DIR2_NAME is not None:
        data2 = RadarDataLevels(DIR2_NAME)
    else:
        data2 = None

    plotter = RadarLevelsPlotter(data1, data2)
    plotter.show()
    plotter.save(DIR_NAME + '_plot.png')
