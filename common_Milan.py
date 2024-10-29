# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# Milan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
# %pip install xlrd==2.0.1

# %%
Data= pd.read_excel('DataForTable2023.xls')


# %%
Data.head(12)

# %%
Data['Freedom to make life choices'].plot(x='year');

# %%
NOMS=list(Data.columns)   #les noms des colonnes
PAYS=Data['Country name'].unique() 

# %%
Data.groupby('Country name').count().year.max()


# %%
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



# %%
np.vectorize(select)
DYNAMIQUE=select(PAYS,NOMS)

# %%
L1=[DYNAMIQUE[pays]['Generosity']+DYNAMIQUE[pays]['Social support']+DYNAMIQUE[pays]['Freedom to make life choices'] for pays in PAYS]
#L2=[DYNAMIQUE[pays]['Log GDP per capita']+DYNAMIQUE[pays]['Social support']+DYNAMIQUE[pays]['Freedom to make life choices'] for pays in PAYS]
L2=[DYNAMIQUE[pays]['Log GDP per capita'] for pays in PAYS]
#L3=[DYNAMIQUE[pays]['Freedom to make life choices'] for pays in PAYS]



#plt.scatter(PAYS, L1, marker='+');
#plt.scatter(PAYS, L2, marker='+');
#plt.scatter(PAYS, L3, marker='+');
DYNAMIQUE['Afghanistan']['Generosity']

# %%

# %%
Data2=pd.DataFrame({'Pays':PAYS, 'Dynamique humaine':L1 , 'Dynamique éco':L2})
Data_hum=Data2.sort_values('Dynamique humaine').reset_index()
Data_eco=Data2.sort_values('Dynamique éco').reset_index()

# %%
Data_hum['Dynamique humaine'].plot(marker='+');
Data_eco['Dynamique éco'].plot(marker='+');
plt.legend()
