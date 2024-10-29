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

