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
    
    
    -----
    ordre (optionnel) : ordre de parcours des noeuds.        
    """
    global nb_aretes_visitees, arriere, arbre_parcours_uniquement, deux_arete_connexe, deux_sommet_connexe
    
    g = DiGraph(g) # on convertit les graphes non-orientés en orientés
    noeuds = g.vertices()
            
    couleur = {n: BLANC for n in noeuds} # tous les noeuds sont blancs au début
    deja_vu = {n: False for n in noeuds} # pour la décomposition en chaînes
    
    ordre_dfi = [] # DFI-order
    nb_aretes_visitees = 0 # pour la décomposition en chaînes
    
    chaines = []
        
    arbre_parcours = DiGraph() # DFS-tree T (contient *aussi* les arc arrières !)
    arbre_parcours.add_vertices(noeuds) # on met tous les noeuds de G dans T
    
    graphe_ponts = Graph(g.edges()) # liste des ponts
    
    deux_arete_connexe = False # 2-arête-connexité du graphe
    deux_sommet_connexe = False # 2(-sommet)-connexité du graphe
        
    
    def parcours(noeud, DEBUG=False):
        """ Parcours individuel de chaque noeud. """  
        
        if DEBUG: print('debut', noeud)        
        couleur[noeud] = GRIS
        ordre_dfi.append(noeud)
        
        for voisin in g.neighbors_out(noeud):
            if DEBUG: print('\t', voisin)
            
            if couleur[voisin] == BLANC: # arc avant
                arbre_parcours.add_edge([voisin, noeud], label='arbre')                
                parcours(voisin)
                
            elif couleur[voisin] == GRIS: # arc arrière
                if voisin not in arbre_parcours.neighbors_out(noeud):
                    arbre_parcours.add_edge([voisin, noeud], label='arriere')  
        
              
        if DEBUG: print('fin', noeud)
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
    
    
    def parcours_decomposition_chaine(noeud, t=arbre_parcours, DEBUG=True):
        """ 
        Parcours individuel de chaque noeud,
        pour la décomposition en chaînes.
        Ici, on s'arrête dès qu'on rencontre un noeud déjà visité.
        """  
        global nb_aretes_visitees
        
        if DEBUG: print('debut', noeud)        
        deja_vu[noeud] = True
        
        if DEBUG: print(f'\nAJOUT debut fonction : {chaines}')
        chaines[-1].append(noeud)
                
        for voisin in t.neighbors_out(noeud):
            if DEBUG: print('\t', voisin)
            
            graphe_ponts.delete_edge((noeud, voisin))
            if deja_vu[voisin]: # on s'arrête
                if DEBUG: print(f'\nAJOUT voisin : {chaines}')
                chaines[-1].append(voisin)                
                break            
            else:
                nb_aretes_visitees += 1
                parcours_decomposition_chaine(voisin)
        
        if DEBUG: print('fin', noeud)
        
        
    
    def decomposition_en_chaines(graphe_arriere, t, ordre=ordre_dfi, DEBUG=True):
        """
        Fonction qui effectue la décomposition en chaîne,
        à partir de l'arbre de parcours.
        
        
        -----
        graphe_arriere: graphe des arc arrières
        
        t: arbre de parcours
        
        ordre: ordre des noeuds à parcourir (DFI index) 
        """
                
        #ordre de parcours des noeuds
        for noeud in ordre: # pour chaque noeud
            deja_vu[noeud] = True
            
            for voisin in graphe_arriere.neighbors_out(noeud): # pour chaque arc arrière
                if DEBUG: print('\t', voisin)
                chaines.append([noeud])
                graphe_ponts.delete_edge((noeud, voisin))
                parcours_decomposition_chaine(voisin, t)                
    
    
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
    
    
    def calcule_comp_2_arete_connexe(ponts):
        """
        Renvoie les composantes 2-arêtes-connexes du graphe.
        
        On supprime les ponts du graphe original.
        Puis on supprime tous les sommets de degré 0 restant après ceci.
        
        -----
        ponts: liste des ponts du graphe
        """
        
        # On copie le graphe
        composantes_2_arete_connexe = Graph(g)
        
        # On en supprime tous les ponts
        for e in ponts:
            composantes_2_arete_connexe.delete_edge(e)
        
        # Maintenant que les ponts sont supprimés,
        # on enlève tout sommet de degré 0
        for v in composantes_2_arete_connexe.vertices():
            if composantes_2_arete_connexe.degree(v) == 0:
                composantes_2_arete_connexe.delete_vertex(v)

        return composantes_2_arete_connexe
    
    
    
    def trouve_sommets_articulation(ponts):
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
        for (u, v, _) in ponts: # arête (u, v) et _ représente le label
            sommets_articulation.update([u, v])
            
        # premier sommet des cycles C_2, ..., C_k
        different_premier_cycle = False
        for chaine in chaines:
            if chaine[0] == chaine[-1]: # si on a un cycle
                if different_premier_cycle:
                    sommets_articulation.add(chaine[0])
                else:
                    different_premier_cycle = True
        
        return sommets_articulation
        
        
    def calcule_comp_2_sommet_connexe(ponts):
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
        
                
        -----
        ponts: liste des ponts du graphe
        """        
        
        # On copie le graphe
        composantes_2_sommet_connexe = Graph(g)
        
        # les ponts
        for i in range(len(ponts)):
            u, v, _ = ponts[i] # arête (u, v) et _ représente le label
            
            composantes_2_sommet_connexe.delete_edge((u, v))

            # on rajoute un indice qui correspond
            # au numéro du pont préfixé par la lettre 'p'
            # ceci est arbitraire et sert juste à différencier
            # les noeuds.
            nouveau_u = f'{str(u)}_p{i}'
            nouveau_v = f'{str(v)}_p{i}'

            composantes_2_sommet_connexe.add_vertex(nouveau_u)
            composantes_2_sommet_connexe.add_vertex(nouveau_v)

            nouvelle_arete = (nouveau_u, nouveau_v)

            composantes_2_sommet_connexe.add_edge(nouvelle_arete)  
        
        # premier sommet des cycles C_2, ..., C_k
        different_premier_cycle = False
        for i in range(len(chaines)):
            chaine = chaines[i]
            
            if chaine[0] == chaine[-1]: # si on a un cycle  
                
                if different_premier_cycle:
                    noeud = chaine[0]
                    voisin1 = chaine[1] # deuxième
                    voisin2 = chaine[-2] # avant-dernier
                    
                    composantes_2_sommet_connexe.delete_edge((noeud, voisin1))
                    composantes_2_sommet_connexe.delete_edge((noeud, voisin2))
                    
                    # on rajoute un indice qui correspond
                    # au numéro de la chaîne
                    # ceci est arbitraire et sert juste à différencier
                    # les noeuds.
                    nouveau_noeud = f'{str(noeud)}_{i}'
                    
                    composantes_2_sommet_connexe.add_vertex(nouveau_noeud)
                    
                    arete1 = (nouveau_noeud, voisin1)
                    arete2 = (nouveau_noeud, voisin1)
                    
                    composantes_2_sommet_connexe.add_edges([arete1, arete2])                    
                else:
                    different_premier_cycle = True
        
        return composantes_2_sommet_connexe
    
    
    def deux_connexite():
        """
        Met à jour la 2-arête-connexité et 2-sommet-connexité du graphe.
        """
        global deux_arete_connexe, deux_sommet_connexe
        
        nb_cycles = nombre_cycles(chaines)
        nb_ponts = len(graphe_ponts.edges())
        
        if nb_ponts > 0: # il y a des ponts
            pass # aucun des deux
        elif nb_cycles > 1: # il y a un cycle différent de C_1
            deux_arete_connexe = True
        else:
            deux_arete_connexe = True
            deux_sommet_connexe = True
            
    
    
    # code
    lance_parcours()
    print("---------- DECOMPO EN CHAINES ----------")
    # on sépare le graphe en 2 parties pour plus de commodité
    arcs_arrieres = list(filter(lambda e: e[2] == 'arriere', arbre_parcours.edges()))
    arcs_parcours = list(filter(lambda e: e[2] == 'arbre', arbre_parcours.edges()))

    arbre_parcours_uniquement = DiGraph([g.vertices(), arcs_parcours])
    arriere = DiGraph([g.vertices(), arcs_arrieres])
    
       
    decomposition_en_chaines(graphe_arriere=arriere, t=arbre_parcours_uniquement)
    
    ponts = graphe_ponts.edges()
    
    print(f'chaines : {chaines}')
    
    print(f'nb de cycles : {nombre_cycles(chaines)}')
    
    print(est_connexe())
    print(f'ordre DFI {ordre_dfi}')
    
    deux_connexite()
    if deux_arete_connexe: print('Le graphe est 2-arête-connexe')
    if deux_sommet_connexe: print('Le graphe est 2-sommet-connexe')
        
    composantes_2_arete_connexe = calcule_comp_2_arete_connexe(ponts)
    
    sommets_art = trouve_sommets_articulation(ponts)
    
    comp_2_sommet_connexe = calcule_comp_2_sommet_connexe(ponts)
    
    return arbre_parcours, graphe_ponts, composantes_2_arete_connexe, comp_2_sommet_connexe
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

# graphes séparés
arcs_arrieres = list(filter(lambda e: e[2] == 'arriere', a.edges()))
arcs_parcours = list(filter(lambda e: e[2] == 'arbre', a.edges()))

arbre_parcours_uniquement = DiGraph([exemple.vertices(), arcs_parcours])
arriere = DiGraph([exemple.vertices(), arcs_arrieres])

plot_couleur(arbre_parcours_uniquement)
plot_couleur(arriere)


