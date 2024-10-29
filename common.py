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
