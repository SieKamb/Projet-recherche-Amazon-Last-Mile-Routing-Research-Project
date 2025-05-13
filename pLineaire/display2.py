from pyvis.network import Network
import json
import ast

with open("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\PrPycharm\\pLineaire\\Pl_results.json", "r") as file:
    PL_res = json.load(file)

V = PL_res["V"]
E = []
p = {}

for key, value in PL_res["p"].items():
    t = ast.literal_eval(key)
    p[t] = value
    E.append(t)

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
  "edges": {
    "smooth": false
  },
  "physics": {
    "enabled": false
  }
}
""")


net.write_html("result.html")
net.show("result.html", notebook=False)
print("end of program.")
