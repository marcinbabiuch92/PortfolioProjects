import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import lines
from matplotlib import patches
from matplotlib.patheffects import withStroke
sns.set(color_codes=True)
sns.set_style("white")

# Loading data frame
path = 'C:\Python_projects\Car_Features_and_MSRP\data\cars.csv'
df = pd.read_csv(path)

# Check data types
print(df.dtypes)

#Check missing data
for column in df.columns:
    missing = np.mean(df[column].isnull())
    print('{} - {}%'.format(column, missing))

# Droping some of the columns
df = df.drop(['Engine Fuel Type', 'Market Category', 'Vehicle Style', 'Popularity', 'Number of Doors', 'Vehicle Size'], axis=1)
print(df.head().to_string())

# Converting MPG to KPL, KPL - Kilometer per litre
df['highway MPG'] = df['highway MPG'] * 1.609344 / 3.78541178
df['highway MPG'] = df['highway MPG'].astype(int)
df['city mpg'] = df['city mpg'] * 1.609344 / 3.78541178
df['city mpg'] = df['city mpg'].astype(int)

# Renaming the columns
df = df.rename(columns={"Engine HP": "HP",
                        "Engine Cylinders": "Cylinders",
                        "Transmission Type": "Transmission",
                        "Driven_Wheels": "Drive Mode",
                        "highway MPG": "KPL-H",
                        "city mpg": "KPL-C",
                        "MSRP": "Price" })

print(df.head())

# Droping the duplicated rows
print(df.shape)
duplicated_rows_df = df[df.duplicated()]
print("number of duplicated rows: ", duplicated_rows_df.shape)
print(df.count())

# Droping duplicates
df = df.drop_duplicates()
# print(df.head().to_string())
# print(df.count())

# Droping missing values
df = df.dropna()
print(df.head().to_string())
print(df.count())
print(df.isnull().sum())

# Detecting outliers

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
print(IQR)

df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
print(df.shape)


# Horizontal histogram
# Initial parameters and values
colors = {'blue': '#076FA2', 'red': '#E3120B', 'black': '#202020', 'grey': '#A2A2A2'}
y = df.Make.value_counts().sort_values(ascending=True)
names = y.index
y_pos = [i * 1 for i in range(len(names))]

# Basic histogram (bar plot)
fig, ax = plt.subplots(figsize=(12, 16))
ax.barh(y.index, y, height=0.75, align='edge', color=colors['blue'])

# Customizing layout
ax.xaxis.set_ticks([i * 100 for i in range(15)])
ax.xaxis.set_ticklabels([i * 100 for i in range(15)], size=12, fontfamily="Econ Sans Cnd", fontweight=400)
ax.xaxis.set_tick_params(labelbottom=False, labeltop=True, length=0)

# Limits values on the axes
ax.set_xlim((0, 1000))
ax.set_ylim((0, len(y.index) * 1.02 - 0.2))

# Sets frame of the chart
ax.set_axisbelow(True)
ax.grid(axis = 'x', color='#A8BAC4', lw=1.2)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_lw(1.5)
ax.spines['left'].set_capstyle('butt')

ax.yaxis.set_visible(False)

# Adding text on the bars and near bars
PAD = 5
for name, value, y_pos in zip(y.index, y, y_pos):
    x = 5
    color = 'white'
    path_effects = None
    if value < 100:
        x = value
        color = colors['blue']
        path_effects=[withStroke(linewidth=6, foreground='white')]
        
    ax.text(
        x + PAD, y_pos + 0.5 / 2, name, color=color, fontfamily='Econ Sans Cnd',
        fontsize=14, va='center', path_effects=path_effects)

# Making a room on top and bottom
fig.subplots_adjust(left=0.005, right=1, top=0.8, bottom=0.1)

# Add title
fig.text(0, 0.850, "Car Brands", fontsize=22, fontweight='bold', fontfamily='Econ Sans Cnd')

# Add subtitle
subtitle = "Number of car types produced, 1994-2017"
fig.text(0, 0.825, subtitle, fontsize=20, fontfamily='Econ Sans Cnd')

# Add caption
caption = "Source: https://www.kaggle.com/datasets/CooperUnion/cardataset"
fig.text(0, 0.085, caption, color=colors['grey'], fontsize=14, fontfamily='Econ Sans Cnd')

# Add authorship
fig.text(0, 0.07, 'Kaggle', color=colors['grey'], fontsize=16, fontfamily='Milo TE W01')

# Add line and rectangle on top
fig.add_artist(lines.Line2D([0, 1], [0.895, 0.895], lw=3, color=colors['red'], solid_capstyle='butt'))
fig.add_artist(patches.Rectangle((0, 0.875), 0.1, 0.020, color=colors['red']))

fig.savefig("Barchart Horizontal.png", bbox_inches='tight')

# Heat Map
# Initial parametres
fig, ax = plt.subplots(figsize=(12, 6))
ticks = ['Horsepower', 'Cylinders', 'Kilometres \nper Liter \n- Highway', 'Kilometres \nper Liter \n- City', 'Price']
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

# Adjusting heatmap so there's no empty values
mask = mask[1:, :-1]
corr = corr.iloc[1:,:-1].copy()

cmap = sns.diverging_palette(240, 10, n=9)
fig.text(0.05, 0.900, "Correlation matrix", size=22, fontfamily="Econ Sans Cnd")

# Creating a heatmap
sns.heatmap(corr, cmap=cmap, vmin=-0.9, vmax=1.00, linewidth=5, mask=mask, annot=False, cbar_kws={'shrink': 0.9})
ax.xaxis.set_ticklabels([i for i in ticks], size=10, fontfamily="Econ Sans Cnd", fontweight=400, fontstyle='italic')
ax.yaxis.set_ticklabels([i for i in ticks], size=10, fontfamily="Econ Sans Cnd", fontweight=400, fontstyle='italic', rotation=0)

# Add line and rectangle on top
fig.add_artist(lines.Line2D([0.05, 0.82], [1.02, 1.02], lw=3, color=colors['red'], solid_capstyle='butt'))
fig.add_artist(patches.Rectangle((0.05, 0.97), 0.10, 0.05, color=colors['red']))

# Saving heat map
fig.savefig('correlation.png', bbox_inches='tight')

# #3 Scatterplot
categories = np.unique(df.Make)
columns = 2
rows = 19
fig, ax_array = plt.subplots(rows, columns, squeeze=False, figsize=(12,80))
chart = 0

# Plotting scatterplot, price per horsepower for every car brand in database
for i, ax_row, in enumerate(ax_array):
    for j, axes in enumerate(ax_row):
        
        axes.set_title(categories[chart], size=12, fontfamily="Econ Sans Cnd")
        
        # Defining ticks
        axes.xaxis.set_ticks([k * 50 for k in range(12)])
        axes.xaxis.set_ticklabels([k * 50 for k in range(12)], size=9, fontfamily="Econ Sans Cnd", fontweight=400, fontstyle='italic', color=colors['blue'])
        axes.yaxis.set_ticks([k * 10000 for k in range(9)])
        axes.yaxis.set_ticklabels([k * 10000 for k in range(9)], size=9, fontfamily="Econ Sans Cnd", fontweight=400, fontstyle='italic', color=colors['blue'])
        axes.set_xlim((0,500))
        axes.set_ylim((0,80000))
        axes.grid(axis = 'y', color='#A8BAC4', lw=0.8, ls='--')
        
        # Erasing spines in every chart
        for spine in ['left', 'right', 'top']:
            axes.spines[spine].set_visible(False)
            axes.spines['bottom'].set_visible(True)
            axes.spines['bottom'].set_lw(1.2)

        # Creating scatter plot
        axes.plot('HP', 'Price', data=df.loc[df['Make']==categories[chart]], linestyle='none', marker='.', c='#076fa2')
        chart += 1

# Add title
fig.text(0.08, 0.890, "Price per horsepower", fontsize=22, fontweight='bold', fontfamily='Econ Sans Cnd')

# Add subtitle
text = "Relationship between price and horsepower with distinction to car brand"
fig.text(0.08, 0.885, text, fontsize=20, fontfamily='Econ Sans Cnd')

# Add caption
caption = "Source: https://www.kaggle.com/datasets/CooperUnion/cardataset" # ERASE THIS LINE!
fig.text(0.08, 0.118, caption, color=colors['grey'], fontsize=14, fontfamily='Econ Sans Cnd')

# Add authorship
fig.text(0.08, 0.115, "The Cooper Union", color=colors['grey'], fontsize=16, fontfamily='Econ Sans Cnd')

# Add line and rectangle on top
fig.add_artist(lines.Line2D([0.08, 0.9], [0.8975, 0.8975], lw=3, color=colors['red'], solid_capstyle='butt'))
fig.add_artist(patches.Rectangle((0.08, 0.895), 0.10, 0.0025, color=colors['red']))

# Saving plot
fig.savefig('Scatterplot.png', bbox_inches='tight')
