# %%
import pandas as pd
import os

print(os.getcwd())

# %% zmiana working directory
new_dir = "C:\\Users\\lila_\\Desktop\\Programowanie_All\\TopBeauty"
os.chdir(new_dir)
print(new_dir)

# %% import modułów
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# %% import danych z pliku csv

top_beauty = pd.read_csv('./top_beauty.csv')
df = top_beauty

# %%
# spr podstawowe staystyki o Data Frame: jakiego typu są to dane?
# czy są nulle? Ile mamy kolumn i jakie mają nazwy?

df.info()
df.isnull().sum()
df.descibe()

# %%
# 1.Które firmy miały najwięcej pozytywnych recenzji. - Top 5:

top5 = df.groupby('Brand')['Rating'].mean().sort_values(ascending=False)
print(top5.head(5))


# %%
# 2.W jakiej kategorii produkty oceniane są najlepiej?

top_cat = df.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(5)
df_ct = top_cat.to_frame()
print(top_cat)

# 2. Wykres dla top5 kategorii:

plt.figure(figsize=(8,5))
sns.barplot(data=df_ct,
            x='Category',
            y='Rating',
            palette='viridis',
            errorbar=None,
            alpha=0.7)
plt.xticks(rotation=45)

plt.show()

# %%
# 3. Top najdroższych produktów:

expensive_cat = df.groupby('Product_Name')['Price_USD'].max().head(5)
print(expensive_cat)

# %%
# 4. zależnosc i korelacja między ceną produktu, 
#    a pozytywna opinią (dla celow badawczych za pozytywną  opinię dalismy rating => 4.8)

pos = df[df['Rating']>=4.8]

price_review = pos['Price_USD'].corr(pos['Rating'])
print(f'Zależnosc oceny produktu od ceny {price_review:.2f}.')

# %%
# 5. Ile produktów było dedykowanych dla kobiet  i ile dla mężczyzn plus wykres kołowy. 

gender_target = df.groupby('Gender_Target')['Gender_Target'].count().plot(kind='pie',
                                                subplots=True,
                                                autopct='%1.1f%%'
                                                )

# %%
# 6. Które produkty są najlepiej oceniane?

product_top_5 = df.groupby('Product_Name')['Rating'].count().sort_values(ascending=False).head(5)
#product_top_5 = df[product_top_5]
product_top_5_df = pd.DataFrame(product_top_5)
print(product_top_5)

# %%
# 7. Srednia cena poroduktów:

avg_price = df['Price_USD'].mean()  
print(f"Średnia cena produktu to {avg_price.round(2)}.")

# %%
# 7. pivot table z dwoma funkjcami agregującymmi 
pd.pivot_table(data=df,
               index='Product_Name',
               columns='Rating',
               aggfunc={'Rating':'sum'})

# %%
# 8. typ opakowania a płeć (róznice)

pack_gen = df.groupby(['Packaging_Type', 'Gender_Target']).size().reset_index(name='Count')

# pivotka
pivot_df = pack_gen.pivot(index='Packaging_Type', columns='Gender_Target', values='Count').fillna(0)

# różnica między płciami - tabelka
pivot_df['Max_Diff'] = (pivot_df.max(axis=1) - pivot_df.min(axis=1)).astype(int)
print(pivot_df)

#max. różnica
md = pivot_df['Max_Diff'].max()
op = pivot_df['Max_Diff'].idxmax()

#z czego wynika największa różnica?
print(f'Największa różnica to {md} na opakowaniu typu: {op} ')


# %%
# 9. kraj pochodzenia, a cruelty free

country_c_free = df.groupby(['Cruelty_Free' , 'Country_of_Origin']).count()

# pivotka
pivot_ccf = df.pivot_table(index='Cruelty_Free', 
                     columns='Country_of_Origin',
                     aggfunc='size',
                     fill_value=0)

print(df.columns.tolist())

# %%
# 9. wykres do subplotow
#    1 - ile wierszy  # 2 - ile kolumn   #sharey - o y jest dzielona

country_counts = df.groupby('Country_of_Origin').size()

fig, ax = plt.subplots(1, 2, 
                       figsize=(10, 4),
                       sharey=True)  
fig.tight_layout(rect=[0, 0, 0.7, 0.9])

# wykres 1
pivot_ccf.groupby('Cruelty_Free').size().plot(ax=ax[0], 
                                              kind='pie',
                                              autopct='%1.1f%%',
                                              color='pink',
                                              cmap='viridis')  
# wykres 2
country_counts.plot(ax=ax[1], 
                    kind='pie',
                    autopct='%1.1f%%',
                    color='pink',
                    cmap='viridis')
# legenda
ax[1].legend('Cruelty Free')

plt.legend(title="Creulty Free",
           frameon=True,
           shadow=True,
           loc="center left",
           bbox_to_anchor=(1.3, 0.5))
plt.show()


# %%
# 10. Główny składnik dla danego typu skóry

main_ing = df.groupby(['Skin_Type'])['Main_Ingredient'].agg(lambda x: x.value_counts().idxmax()).reset_index(name='Most_Common_Ingredient')
print(main_ing)

# %%
# najlepszy produkt dla skóry wrażliwej

best = df[df['Skin_Type'] == 'Sensitive']

best_sen = best.sort_values(by='Rating', ascending=False).head(5).reset_index()
print(best_sen)

# %%




































