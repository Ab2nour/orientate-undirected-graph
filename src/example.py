from matplotlib import pyplot as plt
from networkx import DiGraph

from src.graphs import example
from src.graph_functions import lance_parcours, decomposition_en_chaines, nombre_cycles, \
    est_connexe, deux_connexite, calcule_comp_2_arete_connexe, \
    trouve_sommets_articulation, calcule_comp_2_sommet_connexe
from src.utils import draw_graph

resultat = lance_parcours(example)

from pprint import pp

pp(resultat)

arbre_parcours = resultat["arbre_parcours"]
ordre_dfi = resultat["ordre_dfi"]
draw_graph(arbre_parcours)
#plt.show()

edges = list(arbre_parcours.edges.data())
arcs_arrieres = list(filter(lambda e: e[2]["label"] == "arriere", edges))
arcs_parcours = list(filter(lambda e: e[2]["label"] == "arbre", edges))

arbre_parcours_uniquement = DiGraph()
arbre_parcours_uniquement.add_nodes_from(example.nodes)
arbre_parcours_uniquement.add_edges_from(arcs_parcours)

graphe_arriere = DiGraph()
graphe_arriere.add_nodes_from(example.nodes)
graphe_arriere.add_edges_from(arcs_arrieres)

resultat2 = decomposition_en_chaines(example, graphe_arriere, arbre_parcours_uniquement, ordre_dfi)

pp(resultat2)

chaines = resultat2["chaines"]
graphe_ponts = resultat2["graphe_ponts"]
couleur = resultat2["couleur"]

## todo

ponts = graphe_ponts.edges

print(f"nb de cycles : {nombre_cycles(chaines)}")
print(f"{est_connexe(couleur) = }") # broken car les couleurs sont toutes blanches (jamais actualisées)
# je pense qu'il faut regarder deja_vu à la place
print(f"ordre DFI {ordre_dfi}")

deux_arete_connexe, deux_sommet_connexe = deux_connexite(chaines, graphe_ponts)

if deux_arete_connexe:
    print("Le graphe est 2-arête-connexe")
if deux_sommet_connexe:
    print("Le graphe est 2-sommet-connexe")

composantes_2_arete_connexe = calcule_comp_2_arete_connexe(example, ponts)
plt.figure()
draw_graph(composantes_2_arete_connexe)
#plt.show()
#
sommets_art = trouve_sommets_articulation(ponts, chaines)
#
comp_2_sommet_connexe = calcule_comp_2_sommet_connexe(example, list(ponts), chaines)
plt.figure()
draw_graph(comp_2_sommet_connexe)
