import pandas as pd
import json
from datetime import datetime

folder_path = "C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\Data_Amazon_Challenge\\model_build_inputs"

# Charger le fichier JSON manuellement
with open(f"{folder_path}/route_data.json", "r") as file:
    raw_data = json.load(file)

# Convertir les données en DataFrame
route_data = pd.DataFrame.from_dict(raw_data, orient='index').reset_index()

# Renommer la colonne contenant les RouteID
route_data.rename(columns={'index': 'RouteID'}, inplace=True)

# %%
colonnesDeData = route_data.columns

# %%
# charger les données du fichier package_data.json
with open(f"{folder_path}/package_data.json", "r") as file:
    package_data = json.load(file)

# %%
with open(f"{folder_path}/travel_times.json", "r") as file:
    travel_times = json.load(file)

# %%
L1_route_data = route_data.iloc[0]
# print(L1_route_data['RouteID'])
routId = L1_route_data['RouteID']
departureTime = L1_route_data['date_YYYY_MM_DD'] + " " + L1_route_data['departure_time_utc']
endOfDay = L1_route_data['date_YYYY_MM_DD'] + " 23:59:59"
beginningOfDay = L1_route_data['date_YYYY_MM_DD'] + " 00:00:00"

stops = L1_route_data["stops"]
zone_id = stops['AF']['zone_id']
lenght = len(stops.keys())
V = {0: 'depart'}  # il y a un conflit à résoudre ici
pos = 0
for i in stops.keys():
    V[pos] = i
    pos += 1

times = travel_times[L1_route_data['RouteID']]

packages = package_data[L1_route_data['RouteID']]

# %%
# Création de l'ensemble e des arrêts
E = {}

for i in range(len(stops.keys())):
    for j in range(len(stops.keys())):
        E[(i, j)] = times[V[i]][V[j]]

    # %%



def comparer_dates(date1_str, date2_str):  # verifier si date1_str est avant date2_str
    date_format = "%Y-%m-%d %H:%M:%S"
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    return date1 < date2


# soustraire deux dates
def soustraire_dates(date1_str, date2_str):
    date_format = "%Y-%m-%d %H:%M:%S"
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    difference = date1 - date2
    return difference.total_seconds() / 60  # convertir en minutes


# %%
# Création des ensembles A et B.
A = {}
B = {}
for i in range(lenght):
    packageOfTheStop = packages[V[i]]
    a = 'NaN'
    b = 'NaN'
    for package_details in packageOfTheStop.values():
        start_tmp = package_details['time_window']['start_time_utc']
        end_tmp = package_details['time_window']['end_time_utc']

        # Mise à jour de a (heure minimale de livraison)
        if isinstance(start_tmp, str) and start_tmp != 'NaN':
            if a != 'NaN':
                if comparer_dates(start_tmp, a):
                    a = start_tmp
            else:
                a = start_tmp

        # Mise à jour de b (heure maximale de livraison)
        if isinstance(end_tmp, str) and end_tmp != 'NaN':
            if b != 'NaN':
                if comparer_dates(b, end_tmp):
                    b = end_tmp
            else:
                b = end_tmp

    # Gestion des valeurs par défaut si aucune heure n'est trouvée
    if a == 'NaN':
        a = departureTime
    if b == 'NaN':
        b = endOfDay

    A[i] = a
    B[i] = b

# Transformer les dates de livraison au plus taux en minutes
for i in range(lenght):
    temp = soustraire_dates(A[i], departureTime)
    if temp > 0:
        A[i] = round(temp, 3)
    else:
        A[i] = 0
    temp = soustraire_dates(B[i], departureTime)
    if temp > 0:
        B[i] = round(temp, 3)
    else:
        B[i] = 0

# %%
M = max(E.values())+ max(B.values())

# %%
print(E[(0,0)])


# %%
# définition des variables nécessaires pour l'application du programme linéaire
V_prime = []
for i in V.keys():
    if stops[V[i]]['zone_id'] == zone_id:
        V_prime.append(i)
print(V_prime)
p = E.copy()
E = list(E.keys())
print(A)
print(B)