#!/usr/bin/env python
# coding: utf-8


def parcours_graphe(g):
    """ Cette fonction permet de parcourir un graphe. """
    g = DiGraph(g)
    noeuds = g.vertices()
    deja_vu = [False for i in range(len(noeuds))]
    
    def parcours(noeud):
        """ Parcours individuel de chaque noeud. """      
        print(noeud)
        
        for voisin in g.neighbors_out(noeud):
            print('\t', voisin)
            if deja_vu[voisin] == 0:
                deja_vu[voisin] = 1
                parcours(voisin)
        print('fin', noeud)
    
    def est_connexe():
        """ 
        Renvoie True si le graphe est connexe, False sinon.
        On vérifie que chaque sommet a été visité, sinon le graphe
        n'est pas connexe.
        """        
        # somme de 0 et de 1
        # si chaque sommet a été visité, toutes les cases sont à 1
        nb_sommets_parcourus = sum(deja_vu)
        
        if nb_sommets_parcourus == len(noeuds):
            return True
        else:
            return False
        
        
    deja_vu[0] = True
    parcours(noeuds[0])
    print(est_connexe())


g = Graph()
g.add_edges([[0, 1], [1, 2]])

g.add_edges([[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [4, 5], [5, 6], [5, 7], 
    [6, 7], [4, 9], [4, 8], [8, 9], [1, 2], [2, 3]])


parcours_graphe(g)

g.add_vertex(25)
parcours_graphe(g)




