import pandas as pd

df = pd.read_csv('Data/HephaestusData.csv')

ind = df[df['name'] == 'V'].index.item()
print(df[df['name'] == 'V'].index.item())
print(df.at[ind, 'edge'])
