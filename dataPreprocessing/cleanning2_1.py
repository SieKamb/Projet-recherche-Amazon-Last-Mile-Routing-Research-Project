import pandas as pd
import json
from datetime import datetime
import numpy as np
import sys

sys.path.append("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire")

from PL_functions import hierarchical_clustering_with_size_constraint

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
L1_route_data = route_data.iloc[3]

times = travel_times[L1_route_data['RouteID']]

packages = package_data[L1_route_data['RouteID']]

#print(L1_route_data['RouteID'])
routId = L1_route_data['RouteID']
departureTime = L1_route_data['date_YYYY_MM_DD'] + " " + L1_route_data['departure_time_utc']
endOfDay = L1_route_data['date_YYYY_MM_DD'] + " 23:59:59"
beginningOfDay = L1_route_data['date_YYYY_MM_DD'] + " 00:00:00"

#"""
# --- Algorithme  de regroupement ---
stopsFromTimes = list(times.keys())
for i in stopsFromTimes:
    if L1_route_data['stops'][i]["type"] == 'Station':
        stopsFromTimes.remove(i)
        print(f"Removed {i} from stopsFromTimes because it is a station")
        break

#nous allons définir la matrice de distance entre les arrêts
dist_matrix = np.zeros((len(stopsFromTimes), len(stopsFromTimes)))
for i in range(len(stopsFromTimes)):
    for j in range(len(stopsFromTimes)):
        dist_matrix[i][j] = times[stopsFromTimes[i]][stopsFromTimes[j]]


clusters = hierarchical_clustering_with_size_constraint(dist_matrix, max_members=16)

print(f"Nombre de groupes : {len(clusters)}")
for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1}: {cluster}")

for i, cluster in enumerate(clusters):
    for j in cluster:
        stop = stopsFromTimes[j]
        L1_route_data['stops'][stop]["zone_id"] = "ZoneID" + str(i+1)

# --- fin de l'algorithme  de regroupement ---
#"""




stops = L1_route_data["stops"]
# récupérons les différentes zones_id de la route et enregistrons-les dans l'ensemble ZONES_ID
ZONES_ID = set()
V_by_zone = {}
V_by_zone_str = {} # les ensembles V pour chaque zone ID auront pour clés des chaines de caractères
E_by_zone = {} #ensemble des arêtes par zone ID
for stop in stops.keys():
    c = stops[stop]['zone_id']
    if isinstance(c, str):
        ZONES_ID.add(c)
        V_by_zone[c] = {}
        V_by_zone_str[c] = {}
        E_by_zone[c] = {}
    else:
        ZONES_ID.add("station")
        V_by_zone["station"] = {}
        V_by_zone_str["station"] = {}
        E_by_zone["station"] = {}


V = {}
stops_by_zone = {}
pos = 1
for i in ZONES_ID:
    if i == 'station':
        V[0] = i
    else:
        V[pos] = i
        pos += 1
    stops_by_zone[i] = []
lenght = len(V)

#Nous allons maintenant regrouper les stops par zone_id
for stop in stops.keys():
    c = stops[stop]['zone_id']
    if isinstance(c, str):
        stops_by_zone[c].append(stop)
        V_by_zone[c][len(V_by_zone[c])] = stop #on crée les ensemble V pour chaque zone ID
        V_by_zone_str[c][stop] = len(V_by_zone_str[c])
    else:
        stops_by_zone['station'].append(stop)
        V_by_zone['station'][0] = stop
        V_by_zone_str['station'][stop] = 0



# %%
#Création d'une fonction qui permet de calculer la distance entre deux zones
#la distance entre deux zones sera la distance moyenne entre les deux stops quelconques de ces zones
def calculer_distance(zone1, zone2):
    if zone1 == zone2:
        return 0
    else:
        # On récupère les stops de chaque zone
        stops_zone1 = stops_by_zone[zone1]
        stops_zone2 = stops_by_zone[zone2]

        # On calcule la distance entre chaque stop de la première zone et chaque stop de la deuxième zone
        distances = []
        nb = 0
        for stop1 in stops_zone1:
            for stop2 in stops_zone2:
                if stop1 != stop2:
                    distances.append(times[stop1][stop2])
                    nb += 1
        # On calcule la distance moyenne entre les deux zones
        if nb == 0:
            return 0
        else:
            return sum(distances) / nb

# Création de l'ensemble des arêtes
E = {}


for i in range(lenght):
    zone_i = V[i]
    for j in range(lenght):
        if i > j:
            E[(i, j)] = E[(j, i)]
        else:
            E[(i, j)] = round(calculer_distance(V[i], V[j]), 3)
    #on remplit entre les sommets de zone ID i
    for i_prime in stops_by_zone[zone_i]:
        for j in stops_by_zone[zone_i]:
            E_by_zone[zone_i][V_by_zone_str[zone_i][i_prime], V_by_zone_str[zone_i][j]] = times[i_prime][j]


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
    return difference.total_seconds() #en secondes


# %%
# Création de l'ensemble, A, des heures minimums de livraisons
# Jointure des boucles pour créer les ensembles A et B.
A = {}
B = {}
A_by_zone = {}
B_by_zone = {}
for i in range(lenght):
    # On récupère les arrêts de la zone i
    stops_of_zone = stops_by_zone[V[i]]
    A_by_zone[V[i]] = {}
    B_by_zone[V[i]] = {}
    A_prime = []
    B_prime = []
    for stop in stops_of_zone:
        packageOfTheStop = packages[stop]
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
        A_prime.append(a)
        B_prime.append(b)

        a_time = soustraire_dates(a, departureTime)
        if a_time > 0:
            a = round(a_time, 3)
        else:
            a = 0
        b_time = soustraire_dates(b, departureTime)
        if b_time > 0:
            b = round(b_time, 3)
        else:
            b = 0

        A_by_zone[V[i]][V_by_zone_str[V[i]][stop]] = a_time
        B_by_zone[V[i]][V_by_zone_str[V[i]][stop]] = b_time


    A[i] = A_prime
    B[i] = B_prime


# Transformer les dates de livraison au plus tôt et au plus tard en secondes
for i in range(lenght):
    temp = min([soustraire_dates(date, departureTime) for date in A[i]])
    if temp > 0:
        A[i] = round(temp, 3)
    else:
        A[i] = 0
    temp = max([soustraire_dates(date, departureTime) for date in B[i]])
    if temp > 0:
        B[i] = round(temp, 3)
    else:
        B[i] = 0

# %%
M = max(E.values())+ max(B.values())

# %%
E_serialized = {str(key): value for key, value in E.items()}

E_by_zone_serialized = {}
for zone in E_by_zone.keys():
    E_by_zone_serialized[zone] = {str(key): value for key, value in E_by_zone[zone].items()}

with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_data.json", "w") as file:
    json.dump({"V": list(V.keys()), "p": E_serialized, "M": M, "A": A, "B": B}, file, indent=4)

with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_data_by_zone.json", "w") as file:
    json.dump({"V_by_zone": V_by_zone, "V_by_zone_str": V_by_zone_str, "p_by_zone": E_by_zone_serialized, "M": M,
               "A_by_zone": A_by_zone, "B_by_zone": B_by_zone, "V": V, "times": times, "stops_by_zone":stops_by_zone}
              , file, indent=4)

print(V)

