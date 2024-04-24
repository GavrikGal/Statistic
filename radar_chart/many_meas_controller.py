import matplotlib

from radar_chart.radarplot.utils import Line
from radarplot.radar_data import RadarDataR2ManyMeas, RadarDataLevelsManyMeas
from radarplot.plotter import RadarR2Plotter, RadarLevelsPlotter


LINE_STYLES = [
    Line('tab:blue', '-', 1.1, 0.8),
    Line('tab:red', '-', 1.6, 0.8)
]

DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ЭВМ БК-ТЗ-4К\1. DVI [кабель - доработанный, нагрузка - монитор Asus]'
DIR_NAMES = [r'd:\WorkSpace\Python\pythonProject\Statistic\data\ЭВМ БК-ТЗ-4К\1. DVI [кабель - доработанный, нагрузка - монитор Asus]',
             r'd:\WorkSpace\Python\pythonProject\Statistic\data\ЭВМ БК-ТЗ-4К\9. VGA [кабель - НВИТ, нагрузка - БК-ТЗ-А1] (все частоты + фон)',
             r'd:\WorkSpace\Python\pythonProject\Statistic\data\ЭВМ БК-ТЗ-4К\10. DVI [кабель - доработанный, нагрузка - ВМЦ-61.2ЖК(крэмз 10м)] (все частоты + фон)']
# DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
# DIR2_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\Монитор без краски\Ток прошивки\LVDS max'

if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('QtAgg')

    for dir_name in DIR_NAMES:
        data1 = RadarDataR2ManyMeas(dir_name)
        data_list = [data1]
        output_file_name = dir_name + ' [График R2].png'

        # if DIR2_NAME is None:
        #     data_list = [data1]
        #     output_file_name = dir_name + ' [График R2].png'
        # else:
        #     data2 = RadarDataR2ManyMeas(DIR2_NAME)
        #     data_list = [data1, data2]
        #     output_file_name = DIR2_NAME + ' [Сравнение R2].png'

        plotter = RadarR2Plotter(data_list, max_y_tick=13, line_styles=LINE_STYLES)
        # plotter = RadarR2Plotter(data_list, max_y_tick=17)
        # plotter.show()
        plotter.save(output_file_name)

    level_dir_names = [DIR_NAMES[0]]

    for dir_name in DIR_NAMES:
        data1 = RadarDataLevelsManyMeas(dir_name)
        data_list = [data1]
        output_file_name = dir_name + ' [Уровни].png'

        # if DIR2_NAME is None:
        #     data_list = [data1]
        #     output_file_name = dir_name + ' [График R2].png'
        # else:
        #     data2 = RadarDataR2ManyMeas(DIR2_NAME)
        #     data_list = [data1, data2]
        #     output_file_name = DIR2_NAME + ' [Сравнение R2].png'

        plotter = RadarLevelsPlotter(data_list, col_count=5)
        # plotter = RadarR2Plotter(data_list, max_y_tick=17)
        # plotter.show()
        plotter.save(output_file_name)



    # data_list = list(map(RadarDataLevelsManyMeas, level_dir_names))
    #
    # plotter = RadarLevelsPlotter(data_list, col_count=5)
    # # plotter = RadarLevelsPlotter(data_list, max_y_tick=50, col_count=5)
    # # plotter.show()
    # if len(data_list) < 2:
    #     plotter.save(level_dir_names[-1] + ' [Уровни].png')
    # else:
    #     plotter.save(level_dir_names[-1] + ' [Сравнение уровней].png')
