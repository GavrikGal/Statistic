import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import re

import matplotlib


DIR_NAME = r'd:\Temp\ВМЦ-61.2ЖК 1903103\LVDS\ВП'


def get_angle(file_name):
    angle = re.findall(r'\((\d+)\)', file_name)[0]
    return angle


def read_data_frame(dir_name: str) -> pd.DataFrame:
    file_list = os.listdir(dir_name)
    data_set = pd.read_csv(os.path.join(dir_name, file_list[0]), sep='\t', encoding='cp1251', usecols=[1], skiprows=2,
                           names=['F, MHz'])
    angles = []
    for path in file_list:
        angle = get_angle(path)
        data_set[angle] = pd.read_csv(os.path.join(dir_name, path), sep='\t', encoding='cp1251', usecols=[2],
                                      skiprows=1)
        angles.append(int(angle))
    angles.sort()
    angles_str = [str(angle) for angle in angles]
    name_order = ['F, MHz']
    name_order.extend(angles_str)
    data_set = data_set[name_order]
    return data_set.transpose()


def get_max_y_lim(df: pd.DataFrame) -> int:
    max_y_value = df.transpose().max()[1:].max()
    return math.ceil(max_y_value / 10) * 10


def make_plot(df: pd.DataFrame) -> None:
    fig_cols = 3
    fig_rows = math.ceil(df.shape[1] / fig_cols)
    plt.figure(layout='constrained', figsize=(10, 19))
    max_y_lim = get_max_y_lim(df)

    angles = [int(v) for v in df.index.values[1:]]

    for col_n, data in df.items():
        axes = plt.subplot(fig_rows, fig_cols, col_n + 1, projection='polar')
        plt.plot(np.deg2rad(angles), data[1:], color='r', linewidth=1.8)
        plt.plot((np.deg2rad(angles[-1]), np.deg2rad(angles[0])), (data[-1], data[1]), color='r', linewidth=1.8)
        plt.ylim((0, max_y_lim))
        axes.tick_params(axis='both', which='major', labelsize=10)
        axes.set_yticks(np.arange(0, max_y_lim, 10))
        axes.set_yticks(np.arange(0, max_y_lim, 5), minor=True)
        axes.grid(which='minor', alpha=0.3)
        axes.grid(which='major', alpha=0.9)
        plt.title(f"Frequency - {data[0]} MHz ", loc='center')


if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('TkAgg')

    df = read_data_frame(DIR_NAME)
    make_plot(df)
    plt.savefig(DIR_NAME + '_plot.png', dpi=600)
    plt.show()

