from typing import Any

from networkx import Graph, DiGraph

from src.archive.code import GRIS, BLANC, NOIR


def nombre_cycles(decomp_chaines):
    """
    Étant donné une décomposition en chaînes,
    renvoie le nombre de cycles qu'elle contient.

    Chaque chaîne est de la forme [v_1, v_2, ..., v_n].


    Une chaîne est un cycle si elle est de la forme :
    [v1, v2, ..., v_1]

    c'est-à-dire : v_n = v_1.


    -----
    decomp_chaines: une décomposition en chaînes
    """

    nb_cycles = 0

    for chaine in decomp_chaines:
        if chaine[0] == chaine[-1]:
            nb_cycles += 1

    return nb_cycles


def deux_connexite(chaines, graphe_ponts):
    """
    Met à jour la 2-arête-connexité et 2-sommet-connexité du graphe.
    """
    deux_arete_connexe = False
    deux_sommet_connexe = False

    nb_cycles = nombre_cycles(chaines)
    nb_ponts = len(graphe_ponts.edges())

    if nb_ponts > 0:  # il y a des ponts
        pass  # aucun des deux
    elif nb_cycles > 1:  # il y a un cycle différent de C_1
        deux_arete_connexe = True
    else:
        deux_arete_connexe = True
        deux_sommet_connexe = True

    return deux_arete_connexe, deux_sommet_connexe


def est_connexe(couleur: dict):
    """
    Renvoie True si le graphe est connexe, False sinon.
    On vérifie qu'il ne reste aucun sommet blanc.

    couleur est un dict dict[Graph.nodes, int] (todo: type invalide mais donne une
    bonne idée)
    """
    return not (BLANC in couleur.values())


arbre_parcours_example = DiGraph()
arbre_parcours_example.add_nodes_from([0, 1, 2])

graph_info_example = {
    "couleur": {0: BLANC, 1: BLANC, 2: BLANC},
    "ordre_dfi": [],
    "arbre_parcours": arbre_parcours_example,
}


def parcours(graph: DiGraph, graph_info: dict[str, Any], noeud, DEBUG=False):
    """Parcours individuel de chaque noeud."""
    if DEBUG:
        print("debut", noeud)
    graph_info["couleur"][noeud] = GRIS
    graph_info["ordre_dfi"].append(noeud)

    for voisin in graph.neighbors(noeud):
        if DEBUG:
            print("\t", voisin)

        if graph_info["couleur"][voisin] == BLANC:  # arc avant
            graph_info["arbre_parcours"].add_edge([voisin, noeud], label="arbre")
            parcours(graph, graph_info, voisin)

        elif graph_info["couleur"][voisin] == GRIS:  # arc arrière
            if voisin not in graph_info["arbre_parcours"].neighbors(noeud):
                graph_info["arbre_parcours"].add_edge([voisin, noeud], label="arriere")

    if DEBUG:
        print("fin", noeud)
    graph_info["couleur"][noeud] = NOIR


def lance_parcours(graph: DiGraph, noeuds: list[int], couleur: dict,
                   ordre: list[int] | None = None):
    """
    Fonction qui lance le parcours en profondeur.
    """
    arbre_parcours = DiGraph()  # DFS-tree T (contient *aussi* les arc arrières !)
    arbre_parcours.add_nodes_from(noeuds) # on met tous les noeuds de G dans T

    graph_info = {
        "couleur": {n: BLANC for n in noeuds},
        "ordre_dfi": [],
        "arbre_parcours": arbre_parcours,
    }

    if ordre:  # si on a un ordre de parcours des noeuds
        for n in ordre:
            if couleur[n] == BLANC:
                parcours(graph, graph_info, n)
    else:
        for n in noeuds:
            if couleur[n] == BLANC:
                parcours(graph, graph_info, n)

    return graph_info


graph_info_example2 = {
    "couleur": {0: BLANC, 1: BLANC, 2: BLANC},
    "deja_vu": [False, False, False],
    "chaines": [[0], [1], [2]],
    "graphe_ponts": Graph(),
    "nb_aretes_visitees": 0,
}


def parcours_decomposition_chaine(noeud, t, graph_info: dict[str, Any], DEBUG=True):
    """
    Parcours individuel de chaque noeud,
    pour la décomposition en chaînes.
    Ici, on s'arrête dès qu'on rencontre un noeud déjà visité.

    t: arbre de parcours
    """
    if DEBUG:
        print("debut", noeud)
    graph_info["deja_vu"][noeud] = True

    if DEBUG:
        print(f"\nAJOUT debut fonction : {graph_info['chaines']}")
    graph_info["chaines"][-1].append(noeud)

    for voisin in t.neighbors(noeud):
        if DEBUG:
            print("\t", voisin)

        graph_info["graphe_ponts"].remove_edge((noeud, voisin))
        if graph_info["deja_vu"][voisin]:  # on s'arrête
            if DEBUG:
                print(f"\nAJOUT voisin : {graph_info['chaines']}")
            graph_info["chaines"][-1].append(voisin)
            break
        else:
            graph_info["nb_aretes_visitees"] += 1
            parcours_decomposition_chaine(voisin, t, graph_info)

    if DEBUG:
        print("fin", noeud)


def decomposition_en_chaines(graph: Graph, graphe_arriere, t, ordre_dfi: list[int],
                             DEBUG=True):
    """
    Fonction qui effectue la décomposition en chaîne,
    à partir de l'arbre de parcours.


    -----
    graphe_arriere: graphe des arc arrières

    t: arbre de parcours

    ordre_dfi: ordre des noeuds à parcourir (DFI index)
    """
    graph_info = {
        "couleur": {0: BLANC, 1: BLANC, 2: BLANC},
        "deja_vu": [False, False, False],
        "chaines": [],
        "graphe_ponts": Graph(graph.edges()),
        "nb_aretes_visitees": 0,
    }

    # ordre de parcours des noeuds
    for noeud in ordre_dfi:  # pour chaque noeud
        graph_info["deja_vu"][noeud] = True

        for voisin in graphe_arriere.neighbors_out(
            noeud
        ):  # pour chaque arc arrière
            if DEBUG:
                print("\t", voisin)
            graph_info["chaines"].append([noeud])
            graph_info["graphe_ponts"].remove_edge(noeud, voisin)
            parcours_decomposition_chaine(voisin, t, graph_info)
