#import library
import pandas as pd
import numpy as np 
from mlxtend.frequent_patterns import apriori, association_rules
import warnings
warnings.filterwarnings('ignore')

#menampilkan dataset
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv("BreadBasket_DMS.csv")
print("\nRaw Dataset:")
print(df.head(),"\n")
print(df.tail())
print(df.shape)

#deteksi missing value
missing_values = ["NaN","NA"," ","NONE"]
df = pd.read_csv('BreadBasket_DMS.csv', na_values = missing_values)
print("\nTotal Missing value:")
print(df.isnull().sum())
print(df.shape)
totalRow = len(df.index)
missingCount = df.isnull().sum()
totalMissing = missingCount.sum()
total_mv = round(((totalMissing/totalRow) * 100), 2)
print(f"\nDataset BreadBasket_DMS Memiliki = {total_mv}% missing values\n")

#data cleaning dengan metode remove row
print("Dataset setelah proses cleaning:")
df.dropna(inplace = True)
df['Item'] = df['Item'].str.lower()
df_clean = df
print(df_clean.isnull().sum())
print(df_clean.shape)
print("\nTipe data tiap Atribut:")
print(df_clean.dtypes,"\n")

#data reduction untuk atribut Date dan Time
to_drop = ['Date',
           'Time']
df.drop(to_drop, inplace=True, axis=1)
print("Dataset setelah reduksi:")
print(df.head())
print(df.shape)
print("\nTipe data tiap Atribut:")
print(df.dtypes)

#menampilkan total terjualnya masing-masing item
total_items = df_clean['Item'].value_counts()
print("\nPenjualan masing-masing item: ")
print(total_items)
a1 = total_items.sum()
print(f"\nTotal Item yang Terjual: {a1:,} pcs")
print()

#mengelompokan data berdasarkan transaksi
trx_data = df_clean.groupby('Transaction').agg(','.join).reset_index()
print(f"Mengelompokan Data berdasarkan Transaksinya: \n{trx_data.head()}")

#data transformation menjadi bentuk biner
df = df.groupby(['Transaction','Item']).size().reset_index(name='count')
itemset = (df.groupby(['Transaction', 'Item'])['count']
          .sum().unstack().reset_index().fillna(0)
          .set_index('Transaction'))
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1
basket = itemset.applymap(encode_units)
print(f"\nTransformasi menjadi bentuk biner: \n{basket.head()}\n")

#apriori dengan ukuran kinerja support
frequent_items = apriori(basket, min_support = 0.02, use_colnames = True, verbose = 1)
print(frequent_items, "\n")

#association rules yang difilter dengan ukuran kinerja lift
df_ar = association_rules(frequent_items, metric = "lift", min_threshold = 1)
print(f"Aturan Asosiasi: \n{df_ar}")

#filter aturan asosiasi terbaik dengan 3 ukuran kinerja (support, confidence, dan lift)
result = df_ar[ (df_ar['lift'] >= 1) &
                (df_ar['confidence'] >= 0.7)]

best_ar = result.sort_values(by='confidence', ascending=False)
print(f"\nHasil Aturan Asosiasi Terbaik: \n{best_ar}")

#save to excel
with pd.ExcelWriter('ar.xlsx') as writer:
    df_clean.to_excel(writer, sheet_name='data_clean')
    total_items.to_excel(writer, sheet_name='frequent_items')
    trx_data.to_excel(writer, sheet_name='data_transaction')
    basket.to_excel(writer, sheet_name='data_transform')
    frequent_items.to_excel(writer, sheet_name='support_items')
    df_ar.to_excel(writer, sheet_name='association_rules')
    best_ar.to_excel(writer, sheet_name='best_ar')