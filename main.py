import os
import glob

import pandas as pd
import matplotlib.pyplot as plt

from src.static import COLUMNS

excels = glob.glob('./excel/*.xlsx')

for excel in excels:
    df = pd.read_excel(excel)
    basename = os.path.splitext(os.path.basename(excel))[0]
    plt.plot(df[COLUMNS[2]][1:])
    plt.savefig('png/%s.png' % basename)
    plt.close()
