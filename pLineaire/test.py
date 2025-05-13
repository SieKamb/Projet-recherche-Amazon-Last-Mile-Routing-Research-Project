from PL_functions import *
import json

with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_data_by_zone.json", "r") as file:
    PL_data_by_zone = json.load(file)

def chemin_final(V_,p_,x_,t_,v0_, current_zone):
    path = [v0_]
    stop_name = PL_data_by_zone["V_by_zone"][current_zone][str(v0_)]
    path_name = [stop_name + "( " + str(t_[v0_].value()) + " )"]
    p_path_ = {}
    while len(path) < len(V_):
        c = path[-1]
        for j_ in sauf2(V_, path):
            if x_[c, j_].value() == 1:
                path.append(j_)
                stop_name = PL_data_by_zone["V_by_zone"][current_zone][str(j_)]
                path_name.append(stop_name + "( " + str(round(t_[j_].value(), 2)) + " )")
                p_path_[str((c, j_))] = p_[c,j_]
                break
    return path_name, p_path_

a= {0: 10459.541, 1: 10459.541, 2: 10459.541, 3: 10459.541, 4: 10459.541, 5: 10459.541, 6: 10459.541, 7: 10459.541}
b= {0: 28670.0, 1: 28669.0, 2: 28669.0, 3: 28669.0, 4: 28669.0, 5: 28669.0, 6: 28669.0, 7: 28669.0}
v0= 6
vf= 0
p= {(0, 0): 0.0, (0, 1): 37.6, (0, 2): 33.1, (0, 3): 46.2, (0, 4): 96.2, (0, 5): 125.9, (0, 6): 62.5, (0, 7): 40.0, (1, 0): 39.2, (1, 1): 0.0, (1, 2): 70.7, (1, 3): 81.7, (1, 4): 70.7, (1, 5): 112.7, (1, 6): 24.8, (1, 7): 26.8, (2, 0): 29.2, (2, 1): 66.9, (2, 2): 0.0, (2, 3): 55.8, (2, 4): 108.3, (2, 5): 72.5, (2, 6): 91.8, (2, 7): 69.3, (3, 0): 78.9, (3, 1): 68.0, (3, 2): 112.1, (3, 3): 0.0, (3, 4): 106.4, (3, 5): 138.3, (3, 6): 92.9, (3, 7): 50.2, (4, 0): 139.0, (4, 1): 65.7, (4, 2): 109.7, (4, 3): 113.9, (4, 4): 0.0, (4, 5): 104.7, (4, 6): 90.6, (4, 7): 47.6, (5, 0): 105.0, (5, 1): 103.2, (5, 2): 77.4, (5, 3): 133.3, (5, 4): 80.2, (5, 5): 0.0, (5, 6): 128.1, (5, 7): 85.1, (6, 0): 63.0, (6, 1): 23.7, (6, 2): 94.5, (6, 3): 105.5, (6, 4): 98.9, (6, 5): 136.5, (6, 6): 0.0, (6, 7): 50.6, (7, 0): 51.1, (7, 1): 18.0, (7, 2): 108.8, (7, 3): 104.6, (7, 4): 56.1, (7, 5): 85.8, (7, 6): 42.9, (7, 7): 0.0}
M = 37660.6
V = [0, 1, 2, 3, 4, 5, 6, 7]
E = []
for key, value in p.items():
    E.append(key)

x,t = resolution(V, E, p, a, b, M, v0, vf, seuil= 1)

#path_name, p_path = chemin_final(V, p, x, t, v0, "ZoneID8")
for i1 in V:
    for i2 in V:
        if x[i1,i2].value() == 1:
            print(str(i1) + " -> " + str(i2))

t_values = {}
for i in V:
    t_values[i] = t[i].value()

print(t_values)