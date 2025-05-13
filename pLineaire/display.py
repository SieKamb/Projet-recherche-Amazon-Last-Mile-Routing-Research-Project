from pyvis.network import Network
import networkx as nx
import random

# Création du graphe NetworkX
G = nx.DiGraph()
nodes = [chr(i) for i in range(65, 80)]  # A à O

# Ajout des arêtes avec poids
for i in range(len(nodes) - 1):
    G.add_edge(nodes[i], nodes[i + 1], weight=random.randint(1, 10))

# Ajout d'arêtes supplémentaires
while G.number_of_edges() < 25:
    src, tgt = random.sample(nodes, 2)
    if not G.has_edge(src, tgt):
        G.add_edge(src, tgt, weight=random.randint(1, 10))

# Création du graphe PyVis
net = Network(directed=True)

# Ajout des nœuds et des arêtes
for node in G.nodes():
    net.add_node(node, label=node)

for u, v, data in G.edges(data=True):
    net.add_edge(u, v, label=str(data['weight']))

# Forcer l'utilisation de Jinja2 avec un template interne
net.set_options("""
var options = {
  "physics": {
    "enabled": false
  }
}
""")

# Essaye d'afficher directement sans passer par la fonction "show"
#net.write_html("graphe_interactif.html")
net.show("graphe_interactif.html", notebook=False)
