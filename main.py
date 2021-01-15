import os
import glob

import pandas as pd
import matplotlib.pyplot as plt

from src.static import COLUMNS

plt.rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'IPAPGothic']
plt.rcParams['figure.subplot.bottom'] = 0.4

excels = glob.glob('./excel/*.xlsx')

for excel in excels:
    df = pd.read_excel(excel)
    story_titles = df[COLUMNS[1]][1:].values
    story_counts = df[COLUMNS[0]][1:].values
    x_axis = range(1, len(df[COLUMNS[0]][1:].values) + 1)
    labels = list(map(lambda s: '%d話 %s' % (s[1], s[0]), zip(story_titles, story_counts)))
    basename = os.path.splitext(os.path.basename(excel))[0]
    plt.bar(x_axis, df[COLUMNS[2]][1:], width=0.5)
    plt.xticks(x_axis, labels, rotation=90, fontsize=8)
    plt.savefig('png/%s.png' % basename)
    plt.close()
