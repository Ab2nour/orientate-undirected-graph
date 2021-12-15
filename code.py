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
    
    deja_vu = [False for i in range(len(noeuds))] #todo remplacer par un dico ?
        # car les noeuds ne sont pas forcément à la suite
        
    couleur = [BLANC for i in range(len(noeuds))] # chaque noeud est blanc au début
    
    arbre_parcours = DiGraph() # DFS-tree T
    arbre_parcours.add_vertices(noeuds) # on met tous les noeuds de G dans T
    
    def parcours(noeud):
        """ Parcours individuel de chaque noeud. """  
        
        print('debut', noeud)        
        couleur[noeud] = GRIS
        
        for voisin in g.neighbors_out(noeud):
            print('\t', voisin)
            
            if deja_vu[voisin] == False: # arc avant
                deja_vu[voisin] = True
                arbre_parcours.add_edge([voisin, noeud])                
                parcours(voisin)
                
            elif couleur[voisin] == GRIS: # arc arrière
                arbre_parcours.add_edge([noeud, voisin])
        
              
        print('fin', noeud)
        couleur[noeud] = NOIR
        
    
    
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
    
    
    if ordre: # si on a un ordre de parcours des noeuds        
        for i in range(len(ordre)):
            if not deja_vu[i]:
                deja_vu[ordre[i]] = True
                parcours(ordre[i])          
    else:
        for i in range(len(noeuds)):
            if not deja_vu[i]:
                deja_vu[i] = True
                
                couleur[noeuds[i]] = GRIS
                parcours(noeuds[i])      
                couleur[noeuds[i]] = NOIR
    
    
    print(est_connexe())
    
    return arbre_parcours


g = Graph()
g.add_edges([[0, 1], [1, 2]])

g.add_edges([[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [4, 5], [5, 6], [5, 7], 
    [6, 7], [4, 9], [4, 8], [8, 9], [1, 2], [2, 3]])


parcours_graphe(g)

g.add_vertex(25)
parcours_graphe(g)




