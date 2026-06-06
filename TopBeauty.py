# %%
"""
Created on 06.03.2026
Extended on: 06.06.2026

@author: Kamila Dudzinska
Dataset: https://www.kaggle.com/datasets/waqi786/most-used-beauty-cosmetics-products-in-the-world
"""

# %%
# import modułów
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from custom_styles import colors

# wczytanie pliku
df = pd.read_csv("top_beauty.csv")
df.head()

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

top_cat = df.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(5)
df_ct = top_cat.to_frame()
print(top_cat)

# 2. Wykres dla top5 kategorii:

# własna paleta barw:
sns.set_palette(sns.color_palette(colors))

#wykres
plt.figure(figsize=(8,5))
sns.barplot(data=df_ct,
            x='Category',
            y='Rating',
            #palette='viridis',
            errorbar=None,
            alpha=0.7)
plt.xticks(rotation=45)
plt.title('Najlepiej oceniane kategorie')
plt.xlabel('Kategoria', fontsize=12)
plt.ylabel('Rating', fontsize=12)
plt.tight_layout()

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
print(f'Zależnosc oceny produktu od ceny {price_review:.3f}.')

#tworzymy wykres
#dane wejsciowe dla korelacji
pos = df[df['Rating']>=4.8]
df_corr = pos[['Price_USD', 'Rating']].corr()

#tworzymy wykres
plt.figure(figsize=(8, 6))

#moduł seaborn
sns.heatmap(
    df_corr,                    # korelacja - dane wejciowe
    annot=True,                 # wartoci liczbowe wewnątrz kwadracików
    vmin=-1,                    # min wartoć skali kolorów
    vmax=1                      #maksymalna wartoć skali kolorów
)

plt.title("Korelacje: ")
plt.show()

# %%
# 5. Ile produktów było dedykowanych dla kobiet  i ile dla mężczyzn plus wykres kołowy. 

gender_target = df.groupby('Gender_Target')['Gender_Target'].count().plot(kind='pie',
                                                subplots=True,
                                                autopct='%1.1f%%'
                                                )

# %%
# 6. Które produkty są najlepiej oceniane?

#sprawdzamy średnią ocenę oraz liczbę recenzji
top_products = df.groupby(['Product_Name', 'Brand'])['Rating'].agg(['mean', 'count'])

#filtrowanie, zostawiamy produkty mające wiecej niż 5 recenzji
stars = top_products[top_products['count']>5]

#sortowanie wyników po najwyżeszj średniej ocen
print(stars.sort_values(by='mean', ascending=False).head(5))




# %%
# 7. Srednia cena poroduktów:

# średnia cena i mediana
avg_price = df['Price_USD'].mean()  
median_price = df['Price_USD'].median()
print(f"Średnia cena produktu to {avg_price.round(2)}.")
print(f"Cena, którą zobaczymy na sklepowej półce najczęściej to {median_price.round(2)}.")

#histogramm - podział produktów ze względu na cenę
#definiowanie zmiennych
cena = df['Price_USD']
price_interval = [0, 30, 60, 90, 120, 160]
price_int_names = ['Bardzo tanie\n(0-30 USD)', 
                   'Tanie\n(30-60 USD)',
                   'Średnie\n(60-90 USD)',
                   'Drogie\n (90-120 USD)',
                   'Ekskluzywne\n (pow. 120 USD)']

plt.figure(figsize=(16, 12))
fig, ax = plt.subplots()

# histogram - przediały cenowe
ax.hist(cena, 
        alpha=0.7, 
        label="Cena produktu", 
        color='pink', 
        edgecolor= 'black',
        bins=price_interval)

#środki przedziałów:
middle_int = [(price_interval[i] + price_interval[i+1])/2 for i in range(len(price_interval)-1)]

# nazwy osi x
x_names = ['Bardzo tanie\n(0-30 USD)', 
                   'Tanie\n(30-60 USD)',
                   'Średnie\n(60-90 USD)',
                   'Drogie\n (90-120 USD)',
                   'Ekskluzywne\n (pow. 120 USD)']

ax.set_ylabel("Cena produktu")
ax.set_title("Rozkład cenowy produktów")
plt.xticks(middle_int, price_int_names)
plt.grid(axis = 'x',
        linestyle = '--',
        alpha=0.5 )
plt.tight_layout()
plt.show()



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


#wykres pokazujący ofertę rynkową deydkowaną dla koniet, meżczyzn oraz 'unisex'
plt.figure(figsize=(8,6))

sns.set_palette(sns.color_palette(colors))

gender_target = df.groupby('Gender_Target')['Gender_Target'].count().plot(kind='pie',
                                                figsize=(10,6),
                                                subplots=True,
                                                autopct='%1.1f%%',
                                                #cmap='PuRd'
                                                )

plt.title('Grupy odbiorców produktów')
plt.tight_layout()
plt.show()


# %%
# 9. kraj pochodzenia, a cruelty free

ountry_c_free = df.groupby(['Cruelty_Free' , 'Country_of_Origin']).count()

# pivotka
pivot_ccf = df.pivot_table(index='Cruelty_Free', 
                     columns='Country_of_Origin',
                     aggfunc='size',
                     fill_value=0)

print(df.columns.tolist())

#    1 - ile wierszy  # 2 - ile kolumn   #sharey - o y jest dzielona

country_counts = df.groupby('Country_of_Origin').size()

sns.set_palette(sns.color_palette(colors))

fig, ax = plt.subplots(1, 2, 
                       figsize=(10, 4),
                       sharey=True)  
fig.tight_layout(rect=[0, 0, 0.7, 0.9])

# wykres 1
pivot_ccf.groupby('Cruelty_Free').size().plot(ax=ax[0], 
                                              kind='pie',
                                              autopct='%1.1f%%',
                                              color='pink')
                                              #cmap='viridis')  
# wykres 2
country_counts.plot(ax=ax[1], 
                    kind='pie',
                    autopct='%1.1f%%',
                    color='pink'
                    )
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
best_sen_chosen = best_sen[['Product_Name', 'Brand', 'Category', 'Rating', 'Price_USD']]
print(best_sen_chosen)

# %%
# skumulowany wykres słupkowy - najczęsciej stosowane składniki aktywne ze względu na typ skóry
# Stacked Bar Chart - skumulowany wykres słupkowy

# przygotowanie danych

df_top3_skin = (
df.groupby("Skin_Type")["Main_Ingredient"]
    .value_counts()
    .groupby(level=0)
    .head(3)
    .reset_index(name="liczba produktów")
)

#sortowanie po typie skóry
df_top3_skin = df_top3_skin.sort_values(
                                        by=["Skin_Type", "liczba produktów"], 
                                        ascending=[True, False]
                                        ).reset_index(drop=True)

# moja paleta kolorystyczna - słownik
kolory={'Combination':'#B7BDF7', 
        'Dry':'#FE81D4',
        'Normal': '#C7EABB',
        'Oily' :'#FFEABB',
        'Sensitive': '#FAACBF'}

# rysowanie wykresu
plt.style.use("default")
plt.figure(figsize=(11, 7))

#lista kolorów i przypisanie do typu skóry
colors_list = [kolory[skin] for skin in df_top3_skin["Skin_Type"]]

# histogram
bars = plt.barh(
    df_top3_skin.index,
    df_top3_skin["liczba produktów"],
    color=colors_list,
    height=0.7,
)

# napisy na pasku

labels = [f"{row['Main_Ingredient']} ({int(row['liczba produktów'])})"
         for _, row in df_top3_skin.iterrows()]

# funkcja bar_label - do napisów na pasku
plt.gca().bar_label(
    bars,
    labels=labels,
    label_type="center",
    fontsize=10,
    weight="bold",
    color="white",
)


# oś Y typy skóry
plt.yticks(df_top3_skin.index, df_top3_skin["Skin_Type"])

# tytuł wykresu, labelki
plt.title("Najczęściej używane składniki aktywne ze względu na typ cery",
          fontsize=13,
          weight="bold",
          pad=15)
plt.xlabel("Liczba wystąpień danego składnika")
plt.ylabel("Typ skóry")

# odwrócenie osi Y
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()




































