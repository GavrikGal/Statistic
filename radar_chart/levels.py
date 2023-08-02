import matplotlib

from radarplot.services.levels_plot import RadarDataLevels, RadarLevelsPlotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 2 (Поменяли стекло)\LVDS ГП'

# TODO: Добавить возможность расчета из другой папки со сравнением на соответствующих графиках
# DIR2_NAME


if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('TkAgg')

    df_new = RadarDataLevels(DIR_NAME)

    plotter = RadarLevelsPlotter(df_new)
    plotter.show()
    plotter.save(DIR_NAME + '_plot.png')
