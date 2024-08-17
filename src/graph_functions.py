from typing import Any

from networkx import Graph, DiGraph

# couleurs utilisées pour les parcours
BLANC = 0
GRIS = 1
NOIR = 2

options_couleurs = {  # pour l'AFFICHAGE du graphe
    "arbre": "#333",  # couleur des arcs de l'arbre de parcours
    "arriere": "#a0a0a0",  # couleur des arcs arrières
}

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
            graph_info["arbre_parcours"].add_edge(voisin, noeud, label="arbre")
            parcours(graph, graph_info, voisin)

        elif graph_info["couleur"][voisin] == GRIS:  # arc arrière
            if voisin not in graph_info["arbre_parcours"].neighbors(noeud):
                graph_info["arbre_parcours"].add_edge(voisin, noeud, label="arriere")

    if DEBUG:
        print("fin", noeud)
    graph_info["couleur"][noeud] = NOIR


def lance_parcours(graph: DiGraph, ordre: list[int] | None = None):
    """
    Fonction qui lance le parcours en profondeur.
    """
    arbre_parcours = DiGraph()  # DFS-tree T (contient *aussi* les arc arrières !)
    arbre_parcours.add_nodes_from(graph.nodes)  # on met tous les noeuds de G dans T

    graph_info = {
        "couleur": {n: BLANC for n in graph.nodes},
        "ordre_dfi": [],
        "arbre_parcours": arbre_parcours,
    }

    if ordre:  # si on a un ordre de parcours des noeuds
        for n in ordre:
            if graph_info["couleur"][n] == BLANC:
                parcours(graph, graph_info, n)
    else:
        for n in graph.nodes:
            if graph_info["couleur"][n] == BLANC:
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

        graph_info["graphe_ponts"].remove_edge(noeud, voisin)
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
        "couleur": {i: BLANC for i in graph.nodes},
        "deja_vu": {i: False for i in graph.nodes},
        "chaines": [],
        "graphe_ponts": Graph(graph.edges),
        "nb_aretes_visitees": 0, # todo: useless il semblerait ?
    }

    # ordre de parcours des noeuds
    for noeud in ordre_dfi:  # pour chaque noeud
        graph_info["deja_vu"][noeud] = True

        for voisin in graphe_arriere.neighbors(
                noeud
        ):  # pour chaque arc arrière
            if DEBUG:
                print("\t", voisin)
            graph_info["chaines"].append([noeud])
            graph_info["graphe_ponts"].remove_edge(noeud, voisin)
            parcours_decomposition_chaine(voisin, t, graph_info)

    return graph_info


def calcule_comp_2_arete_connexe(graph: Graph, ponts):
    """
    Renvoie les composantes 2-arêtes-connexes du graphe.

    On supprime les ponts du graphe original.
    Puis on supprime tous les sommets de degré 0 restant après ceci.

    -----
    ponts: liste des ponts du graphe
    """

    # On copie le graphe
    composantes_2_arete_connexe = Graph(graph)

    # On en supprime tous les ponts
    for e in ponts:
        composantes_2_arete_connexe.remove_edge(*e)

    # Maintenant que les ponts sont supprimés,
    # on enlève tout sommet de degré 0
    for v in composantes_2_arete_connexe.nodes:
        if composantes_2_arete_connexe.degree(v) == 0:
            composantes_2_arete_connexe.remove_node(v)

    return composantes_2_arete_connexe


def trouve_sommets_articulation(ponts, chaines):
    """
    Cette fonction renvoie tous les sommets d'articulation
    du graphe.


    On utilise pour ceci le Lemme 5, qui dit
    qu'un sommet d'articulation est soit :

    - une des deux extremités d'un pont
    - le premier sommet d'un cycle différent de C_1


    On récupère donc tous les noeuds appartenant à un pont,
    puis tous les premiers sommets de chaque cycle,
    à partir du 2ème cycle de la décomposition en chaînes.


    -----
    ponts: liste des ponts du graphe
    """

    # on utilise un ensemble pour éviter les doublons
    sommets_articulation = set()

    # les ponts
    for u, v, _ in ponts:  # arête (u, v) et _ représente le label
        sommets_articulation.update([u, v])

    # premier sommet des cycles C_2, ..., C_k
    different_premier_cycle = False
    for chaine in chaines:
        if chaine[0] == chaine[-1]:  # si on a un cycle
            if different_premier_cycle:
                sommets_articulation.add(chaine[0])
            else:
                different_premier_cycle = True

    return sommets_articulation


def calcule_comp_2_sommet_connexe(graph: Graph, ponts, chaines):
    """
    Renvoie les composantes 2-sommet-connexes du graphe.


    * Pour chaque pont (u, v) :

    On supprime l'arête (u, v) du graphe.
    On rajoute un noeud u' (si déjà pris, u_2, sinon u_3, etc)
        et de même un noeud v'.
    On rajoute une arête (u', v') dans le graphe.


    * Pour chaque sommet u en début de cycle, à partir de C_2 :

    Le cycle est de la forme : u, v_1, ..., v_k, u

    Dans ce cas :

    On supprime les arêtes (u, v_1) et (u, v_k) du graphe.
    On rajoute un noeud u' (si déjà pris, u_2, sinon u_3, etc).
    On rajoute deux arêts (u', v_1) et (u', v_k) dans le graphe.

    SAUF :
    Si le sommet est de degré 2 (c'est-à-dire que ses autres
    arêtes ont été supprimées entre temps).
    Dans ce cas, on ne fait rien.


    -----
    ponts: liste des ponts du graphe
    """

    # Pour éviter de traiter plusieurs fois les sommets d'articulation:
    # deja_vu = {i: False for i in a}

    # On copie le graphe
    composantes_2_sommet_connexe = Graph(graph)

    # les ponts
    for i in range(len(ponts)):
        u, v, _ = ponts[i]  # arête (u, v) et _ représente le label

        composantes_2_sommet_connexe.remove_edge(u, v)

        # on rajoute un indice qui correspond
        # au numéro du pont préfixé par la lettre 'p'
        # ceci est arbitraire et sert juste à différencier
        # les noeuds.
        nouveau_u = f"{str(u)}_p{i}"
        nouveau_v = f"{str(v)}_p{i}"

        composantes_2_sommet_connexe.add_node(nouveau_u)
        composantes_2_sommet_connexe.add_node(nouveau_v)

        nouvelle_arete = (nouveau_u, nouveau_v)

        composantes_2_sommet_connexe.add_edge(*nouvelle_arete)

    # premier sommet des cycles C_2, ..., C_k
    different_premier_cycle = False
    for i in range(len(chaines)):
        chaine = chaines[i]

        if chaine[0] == chaine[-1]:  # si on a un cycle
            if different_premier_cycle:
                noeud = chaine[0]

                # Si le sommet est de degré 2, on n'a aucun intérêt
                # à le cloner. On passe la procédure.
                if composantes_2_sommet_connexe.degree(noeud) == 2:
                    continue  # itération suivante de la boucle for

                voisin1 = chaine[1]  # deuxième
                voisin2 = chaine[-2]  # avant-dernier

                composantes_2_sommet_connexe.remove_edge(noeud, voisin1)
                composantes_2_sommet_connexe.remove_edge(noeud, voisin2)

                # on rajoute un indice qui correspond
                # au numéro de la chaîne préfixé par la lettre 'c'
                # ceci est arbitraire et sert juste à différencier
                # les noeuds.
                nouveau_noeud = f"{str(noeud)}_c{i}"

                composantes_2_sommet_connexe.add_node(nouveau_noeud)

                arete1 = (nouveau_noeud, voisin1)
                arete2 = (nouveau_noeud, voisin2)

                composantes_2_sommet_connexe.add_edges_from([arete1, arete2])
            else:
                different_premier_cycle = True

    return composantes_2_sommet_connexe
