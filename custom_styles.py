"""
Extended on Tue Nov 17 10:02:41 2026

Własna paleta barw oraz styl dla mojego projektu.
"""

import seaborn as sns
import matplotlib.pyplot as plt

# własna paleta barw
colors = ['#D291BC',                            #wrzosowy
          '#957DAD',                            #ciemna lawenda
          '#FEC8D8',                            #pudrowy róż
          '#E5B0EA',                            #liliowy
          '#FAACBF',                            #łosoś
          '#FE81D4']                            #słodki róż
sns.set_palette(sns.color_palette(colors))

# definiowanie nowego stylu
style_text = {
    'axes.facecolor' : 'lavender',
    'axes.edgecolor' : 'pink',
    'axes.grid' : True,
    'grid.color' : 'maroon',
    'font.size' : 12,
    'lines.linewidth' : 2,
    'lines.markersize' : 8
}

# mapa typów skóry:
map_skora = {
    'Oily': 'Tłusta',
    'Dry': 'Sucha',
    'Combination': 'Mieszana',
    'Sensitive': 'Wrażliwa',
    'Normal': 'Normalna'
}


# formatowanie tabel - wspólne dla całego projektu
def pokaz_tabele(dane, ile=5):
    
    """Zwraca pierwsze 5 wierszy tabeli w stylu projektu."""
    
    naglowek = dane.columns[0]

    return dane.head(ile).style.set_table_styles([
        {
            'selector': 'th',
            'props': [
                ('font-weight', 'bold'),            #pogrubienie
                ('background-color', '#D291BC'),    #kolor tla - lawendowy
                ('color', 'white'),                 #kolor czcionki
                ('text-align', 'center'),           #wysrodkowanie
                ('padding', '8px')
            ]
        }
    ]).set_properties(
        **{'font-weight': 'bold'},          #pogrubienie pierwszej kolumny
        subset=[naglowek]
    ).hide(axis='index')
