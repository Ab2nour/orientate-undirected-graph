#!/usr/bin/env python
# coding: utf-8


# couleurs utilisées pour les parcours
BLANC = 0
GRIS = 1
NOIR = 2

def parcours_graphe(g, ordre=None):
    """
    Cette fonction permet de parcourir un graphe.
    
    ordre (optionnel) : ordre de parcours des noeuds.        
    """
    
    g = DiGraph(g) # on convertit les graphes non-orientés en orientés
    noeuds = g.vertices()
            
    couleur = {n: BLANC for n in noeuds} # tous les noeuds sont blancs au début
        
    arbre_parcours = DiGraph() # DFS-tree T
    arbre_parcours.add_vertices(noeuds) # on met tous les noeuds de G dans T
    
    def parcours(noeud):
        """ Parcours individuel de chaque noeud. """  
        
        print('debut', noeud)        
        couleur[noeud] = GRIS
        
        for voisin in g.neighbors_out(noeud):
            print('\t', voisin)
            
            if couleur[voisin] == BLANC: # arc avant
                arbre_parcours.add_edge([voisin, noeud])                
                parcours(voisin)
                
            elif couleur[voisin] == GRIS: # arc arrière
                if voisin not in arbre_parcours.neighbors_out(noeud):
                    arbre_parcours.add_edge([voisin, noeud])  
        
              
        print('fin', noeud)
        couleur[noeud] = NOIR
        
    
    
    def est_connexe():
        """ 
        Renvoie True si le graphe est connexe, False sinon.
        On vérifie qu'il ne reste aucun sommet blanc.
        """                
        return not(BLANC in couleur.values())
    
    
    if ordre: # si on a un ordre de parcours des noeuds        
        for i in range(len(ordre)):
            if couleur[i] == BLANC:
                parcours(ordre[i])
    else:
        for i in range(len(noeuds)):
            if couleur[i] == BLANC:                
                parcours(noeuds[i])
    
    
    print(est_connexe())
    
    return arbre_parcours


g = Graph()
g.add_edges([[0, 1], [1, 2]])

g.add_edges([[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [4, 5], [5, 6], [5, 7], 
    [6, 7], [4, 9], [4, 8], [8, 9], [1, 2], [2, 3]])


parcours_graphe(g)

g.add_vertex(25)
parcours_graphe(g)




