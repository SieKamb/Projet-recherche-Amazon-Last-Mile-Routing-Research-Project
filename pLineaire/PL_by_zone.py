import json
import ast
from PL_functions import *

with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_data_by_zone.json", "r") as file:
    PL_data_by_zone = json.load(file)

with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_results.json", "r") as file:
    PL_res = json.load(file)

ordre_passage = PL_res["Ordre"]
V_zone_id = PL_data_by_zone["V"]
zone = ""
zone_name = ""
for i in V_zone_id.keys():
    if 2 < len(PL_data_by_zone["V_by_zone"][V_zone_id[i]]):
        zone = i
        zone_name = V_zone_id[i]
        break

V = PL_data_by_zone["V_by_zone"][zone_name]
V = [int(i) for i in V.keys()]
p1 = PL_data_by_zone["p_by_zone"][zone_name]
M = PL_data_by_zone["M"]
p = {}
E = []
a = {}
b = {}
for key, value in PL_data_by_zone["A_by_zone"][zone_name].items():
    t = ast.literal_eval(key)
    a[t] = value
    b[t] = PL_data_by_zone["B_by_zone"][zone_name][key]

for key, value in p1.items():
    t = ast.literal_eval(key)
    p[t] = value
    E.append(t)

v0 = 0
vf= V[-1]

# --- Implémentation des fonctions qui vont permettre de choisir les stops de départs et les stops d'arrivée de chaque zone ID ---
#on suppose que len(ordr_passage) > 2

#definition de la fonction qui permet de déterminer le stop de départ de la première zone ID
def v0_premiere_zone(indice):
    if ordre_passage.index(indice) != 1:
        raise Exception("Ce n'est pas la première zone ID à visiter")
    name_of_the_zone = PL_data_by_zone["V"][str(indice)]
    stops_of_current_zone = PL_data_by_zone["stops_by_zone"][name_of_the_zone]
    stops_of_previous_zone = PL_data_by_zone["stops_by_zone"]["station"]
    dist = float("inf")
    v0_of_the_zone = 0
    for stop in stops_of_previous_zone:
        for stop_of_current_zone in stops_of_current_zone:
            x_ = PL_data_by_zone["times"][stop][stop_of_current_zone]
            if x_ < dist:
                dist = x_
                v0_of_the_zone = int(PL_data_by_zone["V_by_zone_str"][name_of_the_zone][stop_of_current_zone])
    return v0_of_the_zone, dist


# Implémentation de la fonction qui permet de trouver le dernier stop à livrer dans la zone ID courante et le premier
#a liver dans la prochaine zone ID

def current_vf_and_next_v0(current_indice, next_indice, current_v0: int):
    name_of_the_zone = PL_data_by_zone["V"][str(current_indice)]
    name_of_the_next_zone = PL_data_by_zone["V"][str(next_indice)]
    stops_of_current_zone = PL_data_by_zone["stops_by_zone"][name_of_the_zone]
    stops_of_next_zone = PL_data_by_zone["stops_by_zone"][name_of_the_next_zone]
    dist = float("inf")
    vf_of_the_zone = 0
    v0_of_the_next_zone = 0
    name_of_current_v0 = PL_data_by_zone["V_by_zone"][name_of_the_zone][str(current_v0)]
    for stop in stops_of_current_zone:
        if stop == name_of_current_v0 and len(stops_of_current_zone) != 1:
            continue
        for stop_of_next_zone in stops_of_next_zone:
            x_ = PL_data_by_zone["times"][stop][stop_of_next_zone]
            if x_ < dist:
                dist = x_
                vf_of_the_zone = int(PL_data_by_zone["V_by_zone_str"][name_of_the_zone][stop])
                v0_of_the_next_zone = int(PL_data_by_zone["V_by_zone_str"][name_of_the_next_zone][stop_of_next_zone])
    return vf_of_the_zone, v0_of_the_next_zone, dist

def chemin_final(V_, p_, x_, dt, v0_, current_zone):
    path = [v0_]
    stop_name = PL_data_by_zone["V_by_zone"][current_zone][str(v0_)]
    path_names = [stop_name]
    valeurs_t_ = {path_names[-1]: dt[v0_].value()}
    p_path_ = {}
    while len(path) < len(V_):
        c = path[-1]
        for j_ in sauf2(V_, path):
            if x_[c, j_].value() == 1:
                path.append(j_)
                stop_name = PL_data_by_zone["V_by_zone"][current_zone][str(j_)]
                path_names.append(stop_name)
                p_path_[(path_names[-2], path_names[-1])] = p_[c,j_]
                valeurs_t_[path_names[-1]] = dt[j_].value()
                break
    return path_names, p_path_, valeurs_t_

# --- implementation des résolutions locales du problème ---

save_dict = {}
solution_global = {"V" : [], "p" : {}, "T": {}}
for i in range(1, len(ordre_passage)):

    zone_name = PL_data_by_zone["V"][str(ordre_passage[i])]
    next_zone_name = None
    if i != len(ordre_passage) - 1:
        next_zone_name = PL_data_by_zone["V"][str(ordre_passage[i + 1])]
    else :
        next_zone_name = PL_data_by_zone["V"][str(ordre_passage[0])]
    V = PL_data_by_zone["V_by_zone"][zone_name]
    V = [int(i) for i in V.keys()]
    m = None
    v0 = None
    if i == 1:
        v0,m = v0_premiere_zone(ordre_passage[i])
    else :
        v0 = save_dict["v0"]
        m = save_dict["m"]
    print("⚠️m pour la résolution ", i,"= ",m, "--------------------------------------")
    p1 = PL_data_by_zone["p_by_zone"][zone_name]
    M = PL_data_by_zone["M"]
    p = {}
    E = []
    a = {}
    b = {}
    for key, value in PL_data_by_zone["A_by_zone"][zone_name].items():
        t = ast.literal_eval(key)
        a[t] = max(value, m) #m représente le temps qu'il faut pour arriver dans la zone ID
        b[t] = PL_data_by_zone["B_by_zone"][zone_name][key]

    for key, value in p1.items():
        t = ast.literal_eval(key)
        p[t] = value
        E.append(t)

    current_vf = None
    next_v0 = None
    next_m = None
    if i != len(ordre_passage) - 1:
        current_vf, next_v0, next_m = current_vf_and_next_v0(ordre_passage[i], ordre_passage[i+1], v0)
    else:
        current_vf, next_v0, next_m = current_vf_and_next_v0(ordre_passage[i], ordre_passage[0], v0)


    #resolution du problème local dans la zone ID courante
    if len(V) != 1:
        x,t = None,None
        s = 4
        pas = 0.7
        while x is None and s > 0:
            x,t = resolution(V, E, p, a, b, M, v0, current_vf, seuil=s)
            s -= pas
        if x is None:
            x,t = resolution(V, E, p, a, b, M, v0, current_vf)
        if x is None:
            print("❌ Impossible de trouver une solution pour la ", i, "eme zone ID du parcours (", ordre_passage, ")")
            print(len(V)," sommets dans la zone ID courante")
            print("a: ",a)
            print("b: ",b)
            print("v0 :", v0)
            print("vf :", current_vf)
            print("p :", p)
            break
        print("✅ résolution",i," faite------------------------------------------------------------------------------------------------")

        print("a:", a)
        print("b:", b)
        print("v0:", v0)
        print("vf:", current_vf)
        #print("zone_name:", zone_name)
        print("p:", p)
        t_value = {}
        if i != len(ordre_passage) - 1:
            sommet1 = PL_data_by_zone["V_by_zone"][zone_name][str(current_vf)]
            sommet2 = PL_data_by_zone["V_by_zone"][next_zone_name][str(next_v0)]
            solution_global["p"][(sommet1, sommet2)] = round(next_m,3)
        pathname, p_path, valeurs_t = chemin_final(V,p,x,t,v0, zone_name)
        solution_global["V"].extend(pathname)
        solution_global["p"].update(p_path)
        solution_global["T"].update(valeurs_t)
        for j in V:
            t_value[j] = t[j].value()
        print("t:", t_value)
        save_dict["v0"] = next_v0
        save_dict["m"] = round(next_m + t[current_vf].value(), 3)
    else:
        t_ = a[0]
        sommet1 = PL_data_by_zone["V_by_zone"][zone_name][str(V[0])]
        sommet2 = PL_data_by_zone["V_by_zone"][next_zone_name][str(next_v0)]
        if i != len(ordre_passage) - 1:
            solution_global["p"][(sommet1, sommet2)] = round(next_m,2)
        solution_global["V"].append(sommet1)
        solution_global["T"][sommet1] = t_
        save_dict["v0"] = next_v0
        save_dict["m"] = round(next_m + t_,3)
        print("✅✅ résolution", i," faite------------------------------------------------------------------------------------------------")
    #print(solution_global)

solution_global['p'] = {str(k): v for k, v in solution_global["p"].items()}
with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_resultat_final.json", "w") as file:
    json.dump({"V": solution_global["V"], "p": solution_global["p"], "T": solution_global["T"]}, file)
        
