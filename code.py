#!/usr/bin/env python
# coding: utf-8


# couleurs utilisées pour les parcours
BLANC = 0
GRIS = 1
NOIR = 2


# pour décomposition en chaînes :
STOP = 'STOP'


def parcours_graphe(g, ordre=None):
    """
    Cette fonction permet de parcourir un graphe.
    
    ordre (optionnel) : ordre de parcours des noeuds.        
    """
    global nb_aretes_visitees
    
    g = DiGraph(g) # on convertit les graphes non-orientés en orientés
    noeuds = g.vertices()
            
    couleur = {n: BLANC for n in noeuds} # tous les noeuds sont blancs au début
    deja_vu = {n: False for n in noeuds} # pour la décomposition en chaînes
    
    ordre_dfi = [] # DFI-order
    nb_aretes_visitees = 0 # pour la décomposition en chaînes
    
    chaines = []
        
    arbre_parcours = DiGraph() # DFS-tree T (contient *aussi* les arc arrières !)
    arbre_parcours.add_vertices(noeuds) # on met tous les noeuds de G dans T
    
    
    def parcours(noeud):
        """ Parcours individuel de chaque noeud. """  
        
        print('debut', noeud)        
        couleur[noeud] = GRIS
        
        ordre_dfi.append(noeud)
        
        for voisin in g.neighbors_out(noeud):
            print('\t', voisin)
            
            if couleur[voisin] == BLANC: # arc avant
                arbre_parcours.add_edge([voisin, noeud], label='arbre')                
                parcours(voisin)
                
            elif couleur[voisin] == GRIS: # arc arrière
                if voisin not in arbre_parcours.neighbors_out(noeud):
                    arbre_parcours.add_edge([voisin, noeud], label='arriere')  
        
              
        print('fin', noeud)
        couleur[noeud] = NOIR
        
    
    def est_connexe():
        """ 
        Renvoie True si le graphe est connexe, False sinon.
        On vérifie qu'il ne reste aucun sommet blanc.
        """                
        return not(BLANC in couleur.values())
    
    
    def lance_parcours():
        """
        Fonction qui lance le parcours en profondeur.
        """    
        if ordre: # si on a un ordre de parcours des noeuds        
            for n in ordre:
                if couleur[n] == BLANC:
                    parcours(n)
        else:
            for n in noeuds:
                if couleur[n] == BLANC:                
                    parcours(n)
    
    
    def parcours_decomposition_chaine(noeud, ic, t=arbre_parcours):
        """ 
        Parcours individuel de chaque noeud,
        pour la décomposition en chaînes.
        Ici, on s'arrête dès qu'on rencontre un noeud déjà visité.
        
        ic: indice de la chaîne dans laquelle on rajoute les noeuds
        """  
        global nb_aretes_visitees
        
        print('debut', noeud)        
        deja_vu[noeud] = True
        chaines[ic].append(noeud)
        
        for voisin in t.neighbors_out(noeud):
            print('\t', voisin)
            
            if deja_vu[voisin]: # on s'arrête
                chaines[ic].append(voisin)
                return STOP
            
            else:
                nb_aretes_visitees += 1
                resultat = parcours_decomposition_chaine(voisin, ic)
                
                if resultat == STOP:
                    return STOP
              
        print('fin', noeud)
        
        
    
    def decomposition_en_chaines(t=arbre_parcours, ordre=ordre_dfi):
        """
        Fonction qui effectue la décomposition en chaîne,
        à partir de l'arbre de parcours.
        """
        
        indice_chaine = 0 # sert à indicer la liste 'chaines'
        
        #ordre de parcours des noeuds        
        for n in ordre:
            if not deja_vu[n]:
                chaines.append([])
                parcours_decomposition_chaine(n, indice_chaine, t)
                indice_chaine += 1
                
        return chaines
    
    
    # code
    lance_parcours()
    print("---------- DECOMPO EN CHAINES ----------")
    decomposition_en_chaines()
    
    print(chaines)
    
    print(est_connexe())
    print(f'ordre DFI {ordre_dfi}')
    
    return arbre_parcours


g = Graph()
g.add_edges([[0, 1], [1, 2]])

g.add_edges([[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [4, 5], [5, 6], [5, 7], 
    [6, 7], [4, 9], [4, 8], [8, 9], [1, 2], [2, 3]])


parcours_graphe(g)

g.add_vertex(25)
parcours_graphe(g)

a = parcours_graphe(g)

options_couleurs = { # pour l'AFFICHAGE du graphe
    'arbre': '#333', # couleur des arcs de l'arbre de parcours 
    'arriere': '#a0a0a0' # couleur des arcs arrières
}

a.plot(edge_colors=a._color_by_label(options_couleurs))

plot_couleur = lambda arbre : arbre.plot(edge_colors=arbre._color_by_label(options_couleurs))


ordre = [4, 3, 2, 1, 9, 8, 7, 6, 5, 0]


