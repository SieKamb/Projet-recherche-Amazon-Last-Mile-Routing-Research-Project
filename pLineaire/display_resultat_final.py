from pyvis.network import Network
import json
import ast

with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_resultat_final.json", "r") as file:
    PL_res_final = json.load(file)

V = []
E = []
p = {}

print(len(PL_res_final["V"]))
print(len(PL_res_final["T"]))

for key, value in PL_res_final["p"].items():
    k = ast.literal_eval(key)
    s1,s2 = k
    t1 = PL_res_final["T"][s1]
    t2 = PL_res_final["T"][s2]
    s11 = s1 + "(" + str(round(t1, 2)) + ")"
    s22 = s2 + "(" + str(round(t2, 2)) + ")"
    if s11 not in V:
        V.append(s11)
    if s22 not in V:
        V.append(s22)
    E.append((s11, s22))
    p[(s11, s22)] = value


"""p_ = { ast.literal_eval(key) : val for key, val in PL_res_final["p"].items() }

for i in range(len(PL_res_final["V"])-1):
    s1 = PL_res_final["V"][i]
    s2 = PL_res_final["V"][i+1]
    t1 = PL_res_final["T"][s1]
    t2 = PL_res_final["T"][s2]
    s11 = s1 + "(" + str(round(t1, 2)) + ")"
    s22 = s2 + "(" + str(round(t2, 2)) + ")"
    E.append((s11, s22))
    p[(s11, s22)] = p_[s1,s2]
    V.append(s11)
    if i == len(PL_res_final["V"])-2:
        V.append(s22)"""


# Création du graphe PyVis
net = Network(directed=True)

# Ajout des nœuds
for v in V:
    net.add_node(v, label=str(v))

# Ajout des arêtes avec poids
for u, v in E:
    net.add_edge(u, v, label=str(p[(u, v)]), title=f"Coût: {p[(u, v)]}")

# (Facultatif) Désactiver la physique pour plus de stabilité
net.set_options("""
var options = {
  "physics": {
    "enabled": true,
    "stabilization": {
      "iterations": 200
    }
  },
  "interaction": {
    "dragNodes": true
  }
}
""")



net.write_html("resultat_final.html")
net.show("resultat_final.html", notebook=False)
print("end of program.")
