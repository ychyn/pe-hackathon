import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calc_indice(tab,poids):
    #rescale data + calc indice
    #poids doit être de la forme {"Life Ladder":0.123,"Log GDP":0.2767, ... }
    #table doit contenir toutes les colonnes qui entrent dans le calcul de l'indice
    table=tab.copy()
    
    #Rescale
    cles = list(poids.keys())
    for cle in cles:
        col=table[cle]
        mini=col.min()
        maxi=col.max()
        scale=maxi-mini
        table[cle]+= (col-mini)/scale

    #Calc
    table["indice"]=0
    for cle in cles:
        col=table.pop(cle,axis=1)
        table["indice"]+=poids[cle]*col

    return table


# +
# Milan
Data= pd.read_excel('DataForTable2023.xls')
NOMS=list(Data.columns)   #les noms des colonnes
PAYS=Data['Country name'].unique() 

def select(Pays,nom):
    DYNAMIQUE={}
    for pays in Pays:
        mask= Data['Country name']==pays
        D2= Data[mask]
        DYNAMIQUE[pays]={}
        for col in NOMS:
            if col=='year' or col=='Country name':
                pass
            else:
                a,b=np.polyfit(D2['year'],D2[col], 1)
                nb=len(D2['year'])
                DYNAMIQUE[pays][col]=a*nb/17   #17 max du nb d'années pour les données, lisser les données
    
    return DYNAMIQUE

np.vectorize(select)
DYNAMIQUE=select(PAYS,NOMS)

L1=[DYNAMIQUE[pays]['Generosity']+DYNAMIQUE[pays]['Social support']+DYNAMIQUE[pays]['Freedom to make life choices'] for pays in PAYS]
L2=[DYNAMIQUE[pays]['Log GDP per capita'] for pays in PAYS]

Data2=pd.DataFrame({'Pays':PAYS, 'Dynamique humaine':L1 , 'Dynamique éco':L2})
Data_hum=Data2.sort_values('Dynamique humaine').reset_index()
Data_eco=Data2.sort_values('Dynamique éco').reset_index()

Data_hum['Dynamique humaine'].plot(marker='+');
Data_eco['Dynamique éco'].plot(marker='+');
plt.legend()

# -

df = pd.read_excel('DataForTable2023.xls')
country = 'Country name'
year = 'year'
happiness = 'Life Ladder'
GDP = 'Log GDP per capita'
freedom = 'Freedom to make life choices'
life_exp = 'Freedom to make life choices'
df.head(5)

# # Correlation entre liberté et bonheur ?

# +
countries = df[country].unique()[:16]
num_countries = len(countries)
num_cols = 3  # Number of columns
num_rows = (num_countries + num_cols - 1) // num_cols  # Calculate number of rows needed

fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
axs = axs.flatten()  # Flatten the 2D array of axes for easy iteration

for i, countr in enumerate(countries):
    country_data = df[df[country] == countr]

    ax1 = axs[i]
    ax1.plot(country_data[year], country_data[happiness], 'b-', label='y1')
    ax1.set_ylabel(happiness, color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    ax2.plot(country_data[year], country_data[freedom], 'r-', label='y2')
    ax2.set_ylabel(freedom, color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    ax1.set_title(f'Data for {countr}')
    ax1.set_xlabel('X-axis')

plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()
# -

# # Comparaison avec d'autres sources: bonheur perçu

df_perceived_happiness = pd.read_csv('happiness-cantril-ladder.csv')
df_perceived_happiness.head()
perception = 'Cantril ladder score'

df_perceived_happiness.describe()

mixed_df = pd.merge(left=df,right=df_perceived_happiness,left_on=[country,year],right_on=['Entity','Year'])
mixed_df.drop(columns = ['Entity','Code','Year'],axis = 1,inplace=True)
mixed_df

moyenne_pays = mixed_df.groupby(country).mean()
difference = moyenne_pays[happiness]-moyenne_pays[perception]
difference.describe()

# Ici on vient de comparer la donnée de happiness donnée par le report de World Hapiness avec une donée qui se base sur la perception des habitants des différents pays de leur vie. La moyenne étant tres faible, ces valeurs sont de maniere generale similaires. Cependant, puisque la std est importante, ...

mean = 0.011828
std = 0.123801
list(moyenne_pays[ (difference - mean).abs() > std ].index)

moyenne_pays['ecart'] = difference - mean
sorted_df = moyenne_pays.sort_values(by= GDP)

sorted_df.reset_index(drop=False, inplace=True)

plt.scatter(sorted_df.index,sorted_df[GDP],c=sorted_df['ecart'])
plt.colorbar()

# En abcisses les pays, en ordonnées le GDP. Les couleurs representent l'ecart a la moyenne de la difference entre le happines et le happiness perçu.
