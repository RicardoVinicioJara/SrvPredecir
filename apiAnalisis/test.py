import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder
from sklearn.compose import make_column_transformer
from sklearn import preprocessing


dfOriginal = pd.read_csv("mio.csv", sep=";")
df = pd.DataFrame(dfOriginal, columns= [dfOriginal.head()])
elect_color = dfOriginal.loc[dfOriginal['DNI'] == 105452171]
print(elect_color)