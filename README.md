# Projet de Recherche : Amazon Last Mile Routing

Ce dépôt contient l'ensemble des fichiers relatifs à notre projet de recherche sur l'optimisation du "dernier kilomètre" dans la livraison Amazon.

Pour une compréhension théorique approfondie, veuillez consulter les deux rapports disponibles dans ce dépôt.

---

## 📂 DataPreprocessing

Ce dossier contient les scripts de traitement et de préparation des données nécessaires aux algorithmes.

### 🔹 `cleanning2_1.py`

Il s'agit du fichier principal de ce dossier. Il effectue l’ensemble des opérations de nettoyage et de préparation des données utilisées dans les étapes ultérieures.  
Le script est commenté pour en faciliter la compréhension.

---

## 📂 pLinéaire

Ce dossier regroupe tous les fichiers liés à la modélisation linéaire, permettant notamment :

- de déterminer l’ordre de passage optimal entre les zones (`zone_id`)
- de calculer une solution globale d’optimisation sur une route complète

Il contient également des fichiers d’affichage pour la visualisation des résultats.

---

### 🔹 `PL_function.py`

Ce fichier contient :

- les fonctions de résolution du programme linéaire
- la fonction de regroupement des `stops` en `zone_id`
- une fonction de clustering hiérarchique avec contrainte de taille : `hierarchical_clustering_with_size_constraint`

D’autres fonctions de regroupement peuvent y être ajoutées au besoin.

---

### 🔹 `programmeL.py` & `display2.py`

- `programmeL.py` : utilise les données nettoyées par `cleanning2_1.py` pour déterminer l’ordre de passage optimal entre les zones (`zone_id`) via un programme linéaire. Le résultat est sauvegardé dans le fichier `Pl_results.json`.
- `display2.py` : génère une page HTML pour visualiser graphiquement le résultat du programme linéaire.

---

### 🔹 `PL_by_zone.py` & `display_resultat_final.py`

`PL_by_zone.py` est le cœur du projet. Il applique une résolution locale dans chaque `zone_id`, puis assemble les solutions locales en une solution globale, en suivant l’ordre optimal des zones.

🔧 Les paramètres clés se trouvent aux lignes 154 et 155 :

- `seuil` : seuil utilisé dans la résolution linéaire
- `pas` : intervalle d’itération (voir les rapports pour plus de détails)

Le code est structuré de manière lisible et comprend des commentaires utiles.

`display_resultat_final.py` permet de visualiser la solution globale de façon similaire à `display2.py`.

---

### 📄 `resultat_final_1_6_0.6.html` & `resultat_final_route_2_7_0.5.html`

Ces fichiers contiennent respectivement les solutions pour la première et la deuxième route. Les tuples $(1,6,0.6)$ et $(2,6,0.5)$ représentent 
$(\text{le numéro de la route}, \text{le seuil pour le PL}, \text{le pas pour le PL})$.


---

📝 N’hésitez pas à vous référer aux rapports pour les détails théoriques et méthodologiques du projet.