import matplotlib

from radarplot.radar_data import RadarDataLevels
from radarplot.plotter import RadarLevelsPlotter


DIR_LIST = [
    # r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\LVDS ГП',
    # r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 4 (Стекло НВИТ...317)\LVDS ГП',
    r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 5 (Уплотнители в задней части корпуса + дораб LVDS)\TEST',
    r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 5 (Уплотнители в задней части корпуса + дораб LVDS)\TEST2',
    r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 5 (Уплотнители в задней части корпуса + дораб LVDS)\TEST3',
]


if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('QtAgg')

    data_list = list(map(RadarDataLevels, DIR_LIST))

    plotter = RadarLevelsPlotter(data_list, max_y_tick=60, col_count=2)
    # plotter.show()
    if len(data_list) < 2:
        plotter.save(DIR_LIST[-1] + ' [Уровни].png')
    else:
        plotter.save(DIR_LIST[-1] + ' [Сравнение уровней].png')
