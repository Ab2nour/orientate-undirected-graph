# couleurs utilisées pour les parcours
BLANC = 0
GRIS = 1
NOIR = 2

options_couleurs = { # pour l'AFFICHAGE du graphe
    'arbre': '#333', # couleur des arcs de l'arbre de parcours 
    'arriere': '#a0a0a0' # couleur des arcs arrières
}

plot_couleur = lambda arbre : arbre.plot(edge_colors=arbre._color_by_label(options_couleurs))


def parcours_graphe(g, ordre=None):
    """
    Cette fonction permet de parcourir un graphe.
    
    
    -----
    g: graphe à parcourir 
    
    ordre (optionnel) : ordre de parcours des noeuds.        
    """
    global arriere, arbre_parcours_uniquement, deux_arete_connexe, deux_sommet_connexe
    
    g = DiGraph(g) # on convertit les graphes non-orientés en orientés
    noeuds = g.vertices()
            
    couleur = {n: BLANC for n in noeuds} # tous les noeuds sont blancs au début
    deja_vu = {n: False for n in noeuds} # pour la décomposition en chaînes
    
    ordre_dfi = [] # DFI-order
    
    chaines = [] # liste des chaines (cf Schmidt)
        
    arbre_parcours = DiGraph() # DFS-tree T (contient *aussi* les arc arrières !)
    arbre_parcours.add_vertices(noeuds) # on met tous les noeuds de G dans T
    
    graphe_ponts = Graph(g.edges()) # liste des ponts
    
    deux_arete_connexe = False # 2-arête-connexité du graphe
    deux_sommet_connexe = False # 2(-sommet)-connexité du graphe
        
    
    def parcours(noeud):
        """ Parcours individuel de chaque noeud.
        
        
        -----
        noeud: noeud à parcourir"""  
          
        couleur[noeud] = GRIS
        ordre_dfi.append(noeud)
        
        for voisin in g.neighbors_out(noeud):
            
            if couleur[voisin] == BLANC: # arc avant
                arbre_parcours.add_edge([voisin, noeud], label='arbre')                
                parcours(voisin)
                
            elif couleur[voisin] == GRIS: # arc arrière
                if voisin not in arbre_parcours.neighbors_out(noeud):
                    arbre_parcours.add_edge([voisin, noeud], label='arriere')  
                      
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
    
    
    def parcours_decomposition_chaine(noeud, t=arbre_parcours):
        """ 
        Parcours individuel de chaque noeud,
        pour la décomposition en chaînes.
        Ici, on s'arrête dès qu'on rencontre un noeud déjà visité.
        
        
        -----
        noeud: noeud à parcourir
        """ 
        
        deja_vu[noeud] = True
        
        chaines[-1].append(noeud)
                
        for voisin in t.neighbors_out(noeud):
            
            graphe_ponts.delete_edge((noeud, voisin))
            if deja_vu[voisin]: # on s'arrête
                chaines[-1].append(voisin)                
                break            
            else:
                parcours_decomposition_chaine(voisin)
                
    
    def decomposition_en_chaines(graphe_arriere, t, ordre=ordre_dfi):
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
        
        SAUF : 
        Si le sommet est de degré 2 (c'est-à-dire que ses autres
        arêtes ont été supprimées entre temps).
        Dans ce cas, on ne fait rien.
        
                
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
                    
                    # Si le sommet est de degré 2, on n'a aucun intérêt
                    # à le cloner. On passe la procédure.
                    if composantes_2_sommet_connexe.degree(noeud) == 2:
                        continue # itération suivante de la boucle for
                    
                    voisin1 = chaine[1] # deuxième
                    voisin2 = chaine[-2] # avant-dernier
                    
                    composantes_2_sommet_connexe.delete_edge((noeud, voisin1))
                    composantes_2_sommet_connexe.delete_edge((noeud, voisin2))
                    
                    # on rajoute un indice qui correspond
                    # au numéro de la chaîne préfixé par la lettre 'c'
                    # ceci est arbitraire et sert juste à différencier
                    # les noeuds.
                    nouveau_noeud = f'{str(noeud)}_c{i}'
                    
                    composantes_2_sommet_connexe.add_vertex(nouveau_noeud)
                    
                    arete1 = (nouveau_noeud, voisin1)
                    arete2 = (nouveau_noeud, voisin2)
                    
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
            
       
    # --------------- code ---------------
    lance_parcours()
        
    # on sépare le graphe en 2 parties pour plus de commodité
    arcs_arrieres = list(filter(lambda e: e[2] == 'arriere', arbre_parcours.edges()))
    arcs_parcours = list(filter(lambda e: e[2] == 'arbre', arbre_parcours.edges()))

    arbre_parcours_uniquement = DiGraph([g.vertices(), arcs_parcours])
    arriere = DiGraph([g.vertices(), arcs_arrieres])
    
       
    # décomposition en chaînes
    decomposition_en_chaines(graphe_arriere=arriere, t=arbre_parcours_uniquement) 
    
    # test de la 2-connexité et 2-arête-connexité via le critère de Schmidt
    deux_connexite()
    
    
    # calcul des composantes 2-arêtes-connexes
    ponts = graphe_ponts.edges()
    composantes_2_arete_connexe = calcule_comp_2_arete_connexe(ponts)
                
    # calcul des composantes 2-sommets-connexes
    sommets_articulation = trouve_sommets_articulation(ponts)    
    comp_2_sommet_connexe = calcule_comp_2_sommet_connexe(ponts)
    
    
    # toutes les informations renvoyées par la fonction sur le graphe
    informations = {
        'arbre_parcours': arbre_parcours, # Graphe contenant : arbre de parcours + arcs arrières
        
        'graphe_ponts': graphe_ponts, # Graphe content les ponts   
        'ponts': ponts, # Liste des ponts
        'composantes_2_arete_connexe': composantes_2_arete_connexe,
        
        'sommets_articulation': sommets_articulation, # Liste des sommets d'aritculation
        'comp_2_sommet_connexe': comp_2_sommet_connexe,
        
        'deux_arete_connexe': deux_arete_connexe, # Booléen : le graphe est-il 2-arête-connexe ?
        'deux_sommet_connexe': deux_arete_connexe, # Booléen : le graphe est-il 2-sommet-connexe ?
        
        'connexe': est_connexe(), # Booléen : le graphe est-il connexe ?
        
        'chaines': chaines, # La liste des chaînes
    }
        
    return informations


def affiche_infos(g):
    """
    Affiche des informations relatives aux propriétés de g.
    
    
    -----
    g: un graphe SageMath
    """
    
    informations = parcours_graphe(g)
    
    print(f"sommets d\'articulation : {informations['sommets_articulation']}", end='\n\n') 
    print(f"ponts : {informations['ponts']}", end='\n\n') 
    print(f"chaines : {informations['chaines']}")        
    
    if informations['connexe']:
        print('Le graphe est connexe')
        
    if informations['deux_arete_connexe']:
        print('Le graphe est 2-arête-connexe')
    if informations['deux_sommet_connexe']:
        print('Le graphe est 2-sommet-connexe')
    
    return informations

def affiche_comp_2_sommet_connexe(g):
    """
    Etant donné les infos d'un graphe,
    affiche proprement les composantes 2 sommets connexes
    
    
    -----
    g: un graphe SageMath
    """
    # pour colorier de la même couleur les sommets d'articulation
    # qui ont été séparés
    # on les repère par leur préfixe
    import random # pour les couleurs aléatoires
    import re # pour les regex
    
    comp_2sc = parcours_graphe(g)['comp_2_sommet_connexe']

    def couleur_aleatoire():
        """ 
        Renvoie une couleur aléatoire. 
        Pour ne pas avoir une couleur trop foncée, on fixe une limite.
        """
        LIMITE = 0.5
        r, g, b = random.uniform(LIMITE, 1), random.uniform(LIMITE, 1), random.uniform(LIMITE, 1)
        return (r, g, b)


    # le nom du noeud suivi d'un '_' (début de la chaîne, pas besoin du reste)
    pattern = re.compile('(?P<nom_noeud>(.)+)_')

    # sommets d'articulation séparés
    # exemple : {'5': ['couleur_aleatoire', '5', '5_c1', '5_p3']}
    # on a la couleur du noeud au début
    # et ensuite les noeuds du groupe

    sommets_equivalents = dict()

    # la couleur de chaque sommet d'articulation divisé
    couleurs_sommet = dict() 

    for v in comp_2sc:
        p = pattern.match(str(v))

        if p: # si on a trouvé un préfixe correspondant à la regex
            nom_noeud = p.group('nom_noeud')

            try: # on tente de convertir en entier si possible
                nom_noeud = int(nom_noeud) # '5' -> 5
            except:
                pass

            if nom_noeud in sommets_equivalents.keys():            
                sommets_equivalents[nom_noeud].append(v)
            else: # nouveau groupe de noeuds séparés      
                sommets_equivalents[nom_noeud] = [couleur_aleatoire(), nom_noeud, v]

    for _, tab in sommets_equivalents.items():
        couleur = tab[0]
        s = tab[1:]
        couleurs_sommet[couleur] = s



    options = {
        'edge_colors': comp_2sc._color_by_label(options_couleurs),
        'vertex_colors': couleurs_sommet,
        'vertex_color': '#fff', # couleur par défaut
    }
    
    
    comp_2sc.plot(**options)    
    comp_2sc.show(**options)
