import seaborn as sns
import matplotlib.pyplot as plt

#własna paleta barw
colors = ['#D291BC', '#957DAD', '#FEC8D8', '#E5B0EA', '#FAACBF', '#FE81D4']
sns.set_palette(sns.color_palette(colors))

#definiowanie nowego stylu
style_text = {
    'axes.facecolor' : 'lavender',
    'axes.edgecolor' : 'pink',
    'axes.grid' : True,
    'grid.color' : 'maroon',
    'font.size' : 12,
    'lines.linewidth' : 2,
    'lines.markersize' : 8
}

