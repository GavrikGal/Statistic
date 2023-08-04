import matplotlib

from radarplot.levels_plot import RadarDataLevels, RadarLevelsPlotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 2 (Поменяли стекло)\LVDS ВП'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
DIR2_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\LVDS ВП'


if __name__ == '__main__':
    matplotlib.get_backend()
    # matplotlib.use('TkAgg')

    data1 = RadarDataLevels(DIR_NAME)
    if DIR2_NAME is None:
        data2 = None
    else:
        data2 = RadarDataLevels(DIR2_NAME)

    plotter = RadarLevelsPlotter(data1, data2)
    plotter.show()
    if DIR2_NAME is None:
        plotter.save(DIR_NAME + '_plot.png')
    else:
        plotter.save(DIR2_NAME + '_compare.png')
