# %%
"""
Created on 06.03.2026
Extended on: 06.06.2026
Extended on Tue Nov 17 10:49:15 2026

@author: Kamila Dudzinska
Dataset: https://www.kaggle.com/datasets/waqi786/most-used-beauty-cosmetics-products-in-the-world
Project created in order to train data analysis in python-pandas, 
matplotlib and seaborn.
"""

# %%
# import modułów
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from custom_styles import colors, map_skora

# wczytanie pliku
df = pd.read_csv("top_beauty.csv")
print(df.head())

# spr podstawowe staystyki o Data Frame: jakiego typu są to dane?
# czy są nulle? Ile mamy kolumn i jakie mają nazwy?

df.info()
print(df.isnull().sum())
print(df.describe())

# własna paleta barw - ustawiona raz dla całego skryptu**
sns.set_palette(sns.color_palette(colors))

# %%
# 1.Które firmy mają najwyższą średnią ocen. - Top 5:
top5 = df.groupby('Brand')['Rating'].mean().sort_values(ascending=False)
print(top5.head(5))


# 2.W jakiej kategorii produkty oceniane są najlepiej?
top_cat = df.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(5)
df_ct = top_cat.to_frame()

# 2. Wykres dla top5 kategorii:
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

# 3. średnia cena i mediana
avg_price = df['Price_USD'].mean()
median_price = df['Price_USD'].median()
print(f"Średnia cena produktu to {avg_price:.2f} USD, a mediana {median_price:.2f} USD.")

# definiowanie zmiennych
cena = df['Price_USD']
price_interval = [0, 30, 60, 90, 120, 160]
price_int_names = ['Bardzo tanie\n(0-30 USD)',
                   'Tanie\n(30-60 USD)',
                   'Średnie\n(60-90 USD)',
                   'Drogie\n (90-120 USD)',
                   'Ekskluzywne\n (pow. 120 USD)']

fig, ax = plt.subplots(figsize=(9, 5))

# histogram - przediały cenowe
ax.hist(cena,
        alpha=0.7,
        label="Cena produktu",
        color='pink',
        edgecolor= 'black',
        bins=price_interval)

# środki przedziałów:
middle_int = [(price_interval[i] + price_interval[i+1])/2 for i in range(len(price_interval)-1)]

# oś Y pokazuje ile produktów jest w danym przedziale cenowym
ax.set_ylabel("Liczba produktów")
ax.set_title("Rozkład cenowy produktów")
plt.xticks(middle_int, price_int_names)
plt.grid(axis = 'x',
        linestyle = '--',
        alpha=0.5 )
plt.tight_layout()
plt.show()

#4. Top 5 produktów - Identyfikacja segmentu premium!
# rozmiar jako liczba, np. '30ml' -> 30
df['Product_Size'] = df['Product_Size'].str.replace('ml', '').astype(int)

# cena za 1 ml liczona dla każdego wiersza, zanim zaczniemy grupować
df['Cena_za_ml'] = (df['Price_USD'] / df['Product_Size']).round(2)

# dla każdego produktu bierzemy wiersz z jego najwyższą ceną (idxmax zwraca indeks tego wiersza),
# dzięki temu cena i cena za ml pochodzą z tego samego produktu
idx_max = df.groupby('Product_Name')['Price_USD'].idxmax()

expensive_product = (
    df.loc[idx_max, ['Product_Name', 'Price_USD', 'Product_Size', 'Cena_za_ml']]
      .rename(columns={'Product_Name': 'Nazwa produktu',
                       'Price_USD': 'Cena',
                       'Product_Size': 'Pojemność (ml)',
                       'Cena_za_ml': 'Cena za ml'})
      .sort_values(by='Cena', ascending=False)
      .head(5)
)

print(expensive_product)

#5. Czy jest zależność między ceną, a oceną produktu?
price_review = df['Price_USD'].corr(df['Rating'])
print(f'Zależność oceny produktu od ceny {price_review:.3f}. co oznacza, '
      'ocena klientów nie jest zależna od ceny produktu.')

# dane wejsciowe dla korelacji
df_corr = df[['Price_USD', 'Rating']].corr()

# tworzymy wykres
plt.figure(figsize=(5, 3))

# moduł seaborn
sns.heatmap(
    df_corr,                    # korelacja - dane wejściowe
    annot=True,                 # wartości liczbowe wewnątrz kwadracików
    vmin=-1,                    # min wartość skali kolorów
    vmax=1,                     # maksymalna wartość skali kolorów
    cmap=sns.color_palette(colors, as_cmap=True)
)

plt.title("Korelacja pomiędzy ceną produktu, a jego oceną: ")
plt.show()

# 6. Produkty dla kobiet vs mężczyzn vs unisex - czy mamy balans?.
# podmiana nazw w kolumnie
df['Gender_Target'] = df['Gender_Target'].replace({
    'Female': 'Kobiety',
    'Male': 'Mężczyźni',
    'Unisex': 'Uniwersalne'
})

# wykres kołowy (pie chart) - value_counts liczy produkty w każdej grupie
plt.figure(figsize=(6, 4))
df['Gender_Target'].value_counts().plot(kind='pie',
                                        autopct='%1.1f%%',
                                        startangle=90)
plt.ylabel('')
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

# sortowanie po najwyższym średnim wyniku i usunięcie starych indeksów
wynik = wynik.sort_values(by='średni wynik', ascending=False).reset_index(drop=True)

print(wynik.head())


# 8. Kraj pochodzenia, a Cruelty-Free?
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

# jaki % produktów z danego kraju jest cruelty-free
# cruelty-free - nietestowane na zwierzętach
country_c_free = (df.groupby('Country_of_Origin')
                             ['Cruelty_Free']
                             .mean()
                             .mul(100)
                             .round(1)
                             .sort_values(ascending= False))

print(country_c_free)

# wykres słupkowy - pokazujemy procentowy udział kosmetyków cruelty-free
fig, ax = plt.subplots(figsize=(10, 4))
country_c_free.plot(kind='bar', 
                    color=colors, 
                    ax=ax)
ax.bar_label(ax.containers[0], 
             fmt='%.1f%%')
ax.set_ylim(0, 100)
ax.set_title('Odsetek produktów cruelty-free według kraju pochodzenia')
ax.set_xlabel('')
ax.set_ylabel('% produktów cruelty-free')
plt.xticks(rotation=45)
plt.tight_layout()
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

# podmiana nazw w kolumnie (map_skora jest w custom_styles.py)
main_ing['Rodzaj skóry'] = main_ing['Rodzaj skóry'].replace(map_skora)
print(main_ing)


# 10. Znajdźmy najlepszy produkt dla skóry wrażliwej.
best = df[df['Skin_Type'] == 'Sensitive']

best_sen = best.sort_values(by='Rating', 
                            ascending=False).head(5)

best_sen_chosen = best_sen[['Product_Name', 
                            'Brand', 
                            'Category', 
                            'Rating', 
                            'Price_USD']]

# zmiana nazw kolumn
best_sen_chosen = best_sen_chosen.rename(columns={
    'Product_Name': 'Nazwa produktu',
    'Brand': 'Marka',
    'Category':'Kategoria',
    'Rating':'Ocena',
    'Price_USD':'Cena'
})

print(best_sen_chosen)


# 11. Jakie są główne składniki aktywne dedykowane dla różnych typów cery?

# Stacked Bar Chart - skumulowany wykres słupkowy
# przygotowanie danych
df_top3_skin = (
df.groupby("Skin_Type")["Main_Ingredient"]
    .value_counts()
    .groupby(level=0)
    .head(3)
    .reset_index(name="liczba produktów")
)

# sortowanie po typie skóry
df_top3_skin = df_top3_skin.sort_values(
                                        by=["Skin_Type", "liczba produktów"],
                                        ascending=[True, False]
                                        ).reset_index(drop=True)

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

# lista kolorów i przypisanie do typu skóry
colors_list = [kolory[skin] for skin in df_top3_skin["Skin_Type"]]

# wykres słupkowy poziomy
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
