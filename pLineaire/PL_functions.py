from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus
from pulp import CPLEX_CMD
import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform

# --- définition de fonctions utiles pour la suite ---
def sauf(l, valeur_a_supprimer):
    result = [elt for elt in l if elt != valeur_a_supprimer]
    return result

def sauf2(l, valeurs_a_supprimer):
    result = [elt for elt in l if elt not in valeurs_a_supprimer]
    return result

def resolution(V, E, p, a, b, M, v0, vf, seuil=None):
    # --- Déclaration du modèle ---
    model = LpProblem("Optimisation_Tournée", LpMinimize)

    # --- Variables de décision ---
    x = {(i, j): LpVariable(f"x_{i}_{j}", cat="Binary") for i in V for j in V}
    t = {i: LpVariable(f"t_{i}", lowBound=a[i], upBound=b[i]) for i in V}

    # --- Fonction objectif ---
    model += lpSum(x[i, j] * p[i, j] for i in V for j in V)

    # --- Contraintes ---

    for i in sauf(V, vf):
        model += lpSum(x[i, j] for j in sauf(V, i) if (i, j) in E) == 1  # (B.2a)

    for j in sauf(V, v0):
        model += lpSum(x[i, j] for i in sauf(V, j) if (i, j) in E) == 1  # (B.2b)

    for i in sauf2(V, [v0, vf]):
        model += lpSum(x[i, j] for j in sauf(V,i) if (i, j) in E) == lpSum(x[j, i] for j in sauf(V,i) if (j, i) in E)  # (B.2c)

    model += lpSum(x[j, v0] for j in sauf(V, v0) if (j, v0) in E) == 0  # (B.2d)
    model += lpSum(x[vf, j] for j in sauf(V, vf) if (vf, j) in E) == 0  # (B.2e)

    for i in V:
        model += x[i, i] == 0  # (B.2f)

    for i in V:
        for j in V:
            model += t[i] + p[i, j] - t[j] <= M * (1 - x[i, j])  # (B.2g)
            if seuil is not None:
                model += t[j] - (b[j] - t[i])/seuil <= M * (1-x[i, j])  # condition spéciale 1
            if i < j :
                model += x[i,j] + x[j,i] <= 1 #condition spéciale 2

    for i in V: # (B.2h)
        model += a[i] <= t[i]
        model += t[i] <= b[i]



    # --- Écriture dans un fichier .lp ---
    model.writeLP("C:\\Users\\HP\\Documents\\S4\\partie2\\projetRecherche\\model.lp")

    # --- Résolution ---
    model.solve(CPLEX_CMD(path="C:\\Program Files\\IBM\\ILOG\\CPLEX_Studio2212\\cplex\\bin\\x64_win64\\cplex.exe"))

    # --- Vérification de la résolution ---
    if LpStatus[model.status] != "Optimal":
        print("❌ Résolution impossible: ", model.status)
        return None, None

    #on retourne les variables
    #print("Le status est", model.status)
    return x, t


def hierarchical_clustering_with_size_constraint(dist_matrix, max_members=10, max_groups=None):
    N = dist_matrix.shape[0]

    # Convertir en format condensé (matrice non symétrique)
    condensed_dist = squareform(dist_matrix, checks=False)

    # Construire l'arbre hiérarchique
    Z = linkage(condensed_dist, method='average')
    root_node, nodes = to_tree(Z, rd=True)

    def get_leaves(node):
        """Retourne tous les indices des feuilles sous ce nœud"""
        if node.is_leaf():
            return [node.id]
        return get_leaves(node.left) + get_leaves(node.right)

    def split_node(node):
        """Découpe récursivement un nœud en groupes valides avec la contrainte max_members"""
        leaves = get_leaves(node)
        if len(leaves) <= max_members:
            return [leaves]
        else:
            left_clusters = split_node(node.left)
            right_clusters = split_node(node.right)
            return left_clusters + right_clusters

    all_clusters = split_node(root_node)

    # Optionnel : limiter à max_groups
    if max_groups and len(all_clusters) > max_groups:
        print(
            f"⚠️ {len(all_clusters)} groupes générés, mais max_groups={max_groups} => regroupement secondaire nécessaire")
        # Optionnel : on pourrait merger les plus proches ici si besoin,
        # mais pour l'instant, on garde tout

    return all_clusters
