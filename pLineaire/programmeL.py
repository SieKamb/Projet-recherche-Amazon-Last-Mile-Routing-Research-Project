import json
import ast
from PL_functions import *

# --- importation des données ---
with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_data.json", "r") as file:
    PL_data = json.load(file)

# --- Définition des données ---
V = PL_data["V"]
#V = V[:7]
if 0 not in V:
    V.append(0)
M = PL_data["M"]  # Grande constante
E = []  # Ensemble des arcs (i, j)
p = {}  # Coûts associés aux arcs
a = {} # borne inf de départ
b = {} #Borne sup d'arrivée

#remplissage des variables
for key, value in PL_data["p"].items():
    t = ast.literal_eval(key)
    p[t] = value
    E.append(t)

for i in PL_data["A"].keys():
    v = int(i)
    a[v] =PL_data["A"][i]
    b[v]=PL_data["B"][i]

# --- définition de fonctions qui permettent de trouver les v0 et vf optimaux ---
def choix_vf():
    current = -1
    current_value = V[-1]
    for key in b.keys():
        if key in V:
            if b[key] > current_value:
                current = key
                current_value = b[key]
    if current == -1:
        raise Exception("Choix de vf impossible")
    return current
v0=0 #choisir le sommet qui a le plus petit t[i]
vf=choix_vf()#choisir le sommet qui a le plus grand t[i]


x,t = resolution(V, E, p, a, b, M, v0, vf, seuil=4)

# --- Affichage des résultats ---
"""print("=== Valeurs des variables x[i,j] ===")
for i in V:
    for j in V:
        val = x[i, j].value()
        print(f"x[{i},{j}] = {val}")

print("-----------------------------------")
for i in V:
    val = t[i].value()
    print(f"t[{i}] = {val}")"""


# --- enregistrer  ---
p_res= {}
for i in V:
    for j in V:
        if x[i, j].value() == 1:
            p_res[str((i,j))]=p[i,j]

# --- enregistrement de l'ordre de passage des arêtes puis les résultats dans un fichier json pour ensuite l'afficher---
ordre_passage = [v0]
deliveryTime = [t[v0].value()]
p_res= {}
while len(ordre_passage) < len(V):
    current = ordre_passage[-1]
    for i in sauf2(V, ordre_passage):
        if x[current, i].value() == 1:
            ordre_passage.append(i)
            deliveryTime.append(t[i].value())
            p_res[str((current,i))] = p[current,i]
            break





print(ordre_passage)

with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_results.json", "w") as file:
    json.dump({"V": V, "p": p_res, "Ordre": ordre_passage, "deliveryTime": deliveryTime}, file, indent=4)


