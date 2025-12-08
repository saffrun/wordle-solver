
import pandas as pd
CSV = 'wordle.csv'

df = pd.read_csv(CSV)

#df.info()
#print(df.describe())
print(df['occurrence'].value_counts())
print(df['word'].str.len().value_counts())
print(df.isnull().sum())
print(df.columns)
