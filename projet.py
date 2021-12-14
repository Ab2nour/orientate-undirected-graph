#!/usr/bin/env python
# coding: utf-8

# In[1]:


g = Graph()


# In[2]:


g . add_edges ([[0 ,1] ,[1 ,2]])


# In[3]:


g


# In[4]:


print(g)


# In[7]:


g . add_edges([[0 ,1] ,[0 ,2] ,[0 ,3] ,[1 ,4] ,[2 ,4] ,[4 ,5] ,[5 ,6] ,[5 ,7] ,[6 ,7] ,
[4 ,9] ,[4 ,8] ,[8 ,9] ,[1 ,2] ,[2 ,3]])


# In[8]:


g


# In[29]:


def parcours_graphe(g):
    g = DiGraph(g)
    noeuds = g.vertices()
    deja_vu = [False for i in range(len(noeuds))]
    
    def parcours(noeud):
        global g
        
        print(noeud)
        
        for voisin in DiGraph(g).neighbors_out(noeud):
            print('\t', voisin)
            if deja_vu[voisin] == 0:
                deja_vu[voisin] = 1
                parcours(voisin)
        print('fin', noeud)
        
    deja_vu[0] = True
    parcours(noeuds[0])
    


# In[30]:


parcours_graphe(g)


# In[17]:


DiGraph(g)


# In[18]:


DiGraph(g).neighbors_out(5)


# In[ ]:




