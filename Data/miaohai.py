from fileinput import filename
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import pandas as pd
import time,datetime

finalname = BASE_DIR+'/Data/Price/福州麦芽田.csv'
data = pd.read_csv(finalname, usecols=['code'])
print(data)
