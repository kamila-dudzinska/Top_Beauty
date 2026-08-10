# %%
"""
Created on 06.03.2026
Extended on: 06.06.2026

@author: Kamila Dudzinska
Dataset: https://www.kaggle.com/datasets/waqi786/most-used-beauty-cosmetics-products-in-the-world
Project created in order to train data analysis in python-pandas, matplotlib and seaborn. 
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

# spr podstawowe staystyki o Data Frame: jakiego typu są to dane?
# czy są nulle? Ile mamy kolumn i jakie mają nazwy?

df.info()
df.isnull().sum()
df.descibe()

# %%
# 1.Które firmy miały najwięcej pozytywnych recenzji. - Top 5:

top5 = df.groupby('Brand')['Rating'].mean().sort_values(ascending=False)
print(top5.head(5))


# 2.W jakiej kategorii produkty oceniane są najlepiej?

top_cat = df.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(5)
df_ct = top_cat.to_frame()

# 2. Wykres dla top5 kategorii:

# własna paleta barw:
sns.set_palette(sns.color_palette(colors))

#wykres
plt.figure(figsize=(8,5))
sns.barplot(data=df_ct,
            x='Category',
            y='Rating',
            errorbar=None,
            alpha=0.7)
plt.xticks(rotation=45)
plt.title('Najlepiej oceniane kategorie: ')
plt.xlabel('Kategoria', fontsize=12, labelpad =15)
plt.ylabel('Ocena', fontsize=12, labelpad =15)
plt.tight_layout()

plt.show()


# 3. # średnia cena i mediana
# średnia cena i mediana
avg_price = df['Price_USD'].mean()  
print(f"Cena, którą zobaczymy na sklepowej półce najczęściej to {avg_price.round(2)}.")

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


#4. Top 5 produktów - Identyfikacja segmentu premium!

#przeliczenie ceny na 1ml
df['Product_Size'] = df['Product_Size'].str.replace('ml', '').astype(int)

# grupowanie i pobranie maksymalnej ceny
expensive_product = (
    df.groupby('Product_Name', 
               as_index=False)['Price_USD']
      .max()
      .rename(columns={'Product_Name': 'Nazwa produktu', 
                       'Price_USD': 'Cena'}).sort_values(by='Cena', ascending=False)
      .head(5)
)


expensive_product['cena_za_ml'] = df['Price_USD']/ df["Product_Size"]

print(expensive_product.sort_values(by='cena_za_ml', ascending=False))          
            , 
#5. Czy jest zależność między ceną, a oceną produktu?

price_review = df['Price_USD'].corr(df['Rating'])
print(f'Zależność oceny produktu od ceny {price_review:.3f}. co oznacza, ocena klientów nie jest zależna od ceny produktu.')
print('Im wyższa cena, tym klienci minimalnie gorzej oceniają produkt.')

#dane wejsciowe dla korelacji
df_corr = df[['Price_USD', 'Rating']].corr()

#tworzymy wykres
plt.figure(figsize=(5, 3))

#moduł seaborn
sns.heatmap(
    df_corr,                    # korelacja - dane wejciowe
    annot=True,                 # wartoci liczbowe wewnątrz kwadracików
    vmin=-1,                    # min wartoć skali kolorów
    vmax=1                      # maksymalna wartoć skali kolorów
)

plt.title("Korelacja pomiędzy ceną produktu, a jego oceną: ")
plt.show()


# 6. Produkty dla kobiet vs mężczyzn vs unisex - czy mamy balans?. 
# wykres kołowy (pie chart)
plt.figure(figsize=(6,4))

sns.set_palette(sns.color_palette(colors))

gender_target = df.groupby('Gender_Target')['Gender_Target'].count().plot(kind='pie',
                                                figsize=(10,6),
                                                subplots=True,
                                                autopct='%1.1f%%',
                                                )

plt.title('Grupy odbiorców produktów')
plt.tight_layout()
plt.show()


# 7. Które produkty są najlepiej oceniane? Pod uwagę bierzemy produkty mające minimum 5 recenzji.

# grupowanie danych po nazwie produktu i marce
wynik = (
    df.groupby(['Product_Name', 'Brand'])
      .agg({'Rating':'mean', 'Number_of_Reviews':'sum'})
      .reset_index() 
)

# zmiana nazw kolumn
wynik.columns = ['Nazwa produktu', 'Marka', 'średni wynik', 'liczba recenzji']

# filtrowanie produktów z więcej niż 5 recenzjami
wynik = wynik[wynik['liczba recenzji'] > 5]

# zaokrąglenie średniego wyniku do 2 miejsc po przecinku
wynik['średni wynik'] = wynik['średni wynik'].round(2)

# sortowanie po najwyższym średnim wyniku
wynik = wynik.sort_values(by='średni wynik', ascending=False)

#usuwane indexów
wynik = wynik.reset_index(drop=True)

print(wynik.head())

# Kraj pochodzenia, a Cruelty-Free?

map_kraje = {
    'USA': 'Stany Zjednoczone',
    'France': 'Francja',
    'Germany': 'Niemcy',
    'Poland': 'Polska',
    'Italy': 'Włochy',
    'UK': 'Wielka Brytania',
    'South Korea': 'Korea Południowa',
    'Australia': 'Australia',
    'Japan': 'Japonia'
}

df['Country_of_Origin'] = df['Country_of_Origin'].replace(map_kraje)

country_c_free = (df.groupby('Country_of_Origin')
                             ['Cruelty_Free']
                             .mean()
                             .mul(100)
                             .round(1)
                             .sort_values(ascending= False))

print(df.columns.tolist())

country_counts = df.groupby('Country_of_Origin').size()

sns.set_palette(sns.color_palette(colors))

fig, ax = plt.subplots(
                       figsize=(10, 4),
                       sharey=True)  
fig.tight_layout(rect=[0, 0, 0.7, 0.9])

country_counts.plot(
                    kind='pie',
                    autopct='%1.1f%%',
                    color='pink'
                    )

plt.show()

#9. Główny składnik a typ skóry.

main_ing = (
    df.groupby(['Skin_Type'])['Main_Ingredient']
      .agg(lambda x: x.value_counts().idxmax())
      .reset_index(name='Most_Common_Ingredient')
)

# zmiana nazw kolumn
main_ing = main_ing.rename(columns={
    'Skin_Type': 'Rodzaj skóry',
    'Most_Common_Ingredient': 'Główny składnik'
})

# mapa tłumaczeń typów skóry
map_skora = {
    'Oily': 'Tłusta',
    'Dry': 'Sucha',
    'Combination': 'Mieszana',
    'Sensitive': 'Wrażliwa',
    'Normal': 'Normalna'
}

# podmiana nazw w kolumnie
main_ing['Rodzaj skóry'] = main_ing['Rodzaj skóry'].replace(map_skora)
print(main_ing)

# 10. Znajdźmy najlepszy produkt dla skóry wrażliwej.

main_ing = (
    df.groupby(['Skin_Type'])['Main_Ingredient']
      .agg(lambda x: x.value_counts().idxmax())
      .reset_index(name='Most_Common_Ingredient')
)

# zmiana nazw kolumn
main_ing = main_ing.rename(columns={
    'Skin_Type': 'Rodzaj skóry',
    'Most_Common_Ingredient': 'Główny składnik'
})

# mapa tłumaczeń typów skóry
map_skora = {
    'Oily': 'Tłusta',
    'Dry': 'Sucha',
    'Combination': 'Mieszana',
    'Sensitive': 'Wrażliwa',
    'Normal': 'Normalna'
}

# podmiana nazw w kolumnie
main_ing['Rodzaj skóry'] = main_ing['Rodzaj skóry'].replace(map_skora)
print(main_ing)

# 11. Jakie są główne składniki aktywne dydykowane dla różnych typów cery?
import matplotlib.pyplot as plt
import pandas as pd

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

# mapa tłumaczeń typów skóry
map_skora = {
    'Oily': 'Tłusta',
    'Dry': 'Sucha',
    'Combination': 'Mieszana',
    'Sensitive': 'Wrażliwa',
    'Normal': 'Normalna'
}
# podmiana nazw w kolumnie
df_top3_skin['Skin_Type'] = df_top3_skin['Skin_Type'].replace(map_skora)

# moja paleta kolorystyczna - słownik
kolory={'Mieszana':'#B7BDF7', 
        'Sucha':'#FE81D4',
        'Normalna': '#C7EABB',
        'Tłusta' :'#FFEABB',
        'Wrażliwa': '#FAACBF'}

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
          pad=16)
plt.xlabel("Liczba wystąpień danego składnika", labelpad=15)
plt.ylabel("Typ skóry", labelpad=15)

# odwrócenie osi Y
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()
























