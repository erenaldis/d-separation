
# coding: utf-8
import numpy as np
import itertools



# In[112]:

def is_collider(x, G):
    parents = []
    collider = False
    if np.sum(G[:, x]) > 1:
        parents.append(np.where(G[:, x] == 1)[0])
        collider = True
    return collider, parents 
def is_active(x, C, G):
    if is_collider(x, G) and x in C:
        return True
    elif not is_collider(x, G) and x not in C:
        return True
    else:
        return False


# In[176]:

#Build ancestral graph
def ancestral_graph(A, B, C, G):
    ancestral_idx = set()
    nodes = set([A] + [B] + C)
    ancestral_idx.update(nodes)
    while len(nodes) > 0:
        temp_idx = set()
        for node in nodes:
            if np.sum(G[:, node]) > 0:
                parents = np.where(G[:, node] == 1)[0]
                for p in parents:
                    if p not in ancestral_idx:
                        ancestral_idx.add(p)
                        temp_idx.add(p)
        nodes = temp_idx
    idx_to_delete = set(range(len(G))).difference(ancestral_idx)
    G_new = G.copy()
    for idx in idx_to_delete:
        G_new[idx, :] = np.zeros(len(G))
        G_new[:, idx] = np.zeros(len(G))
        #cuts off all the connections
    return G_new


# In[182]:

#marry the parents
def marry_parents(G):
    G_new = G.copy()
    for i in range(len(G)):
        collider, parents = is_collider(i, G)
        if collider:
            pairs = list(itertools.combinations(parents[0], 2))
            for pair in pairs:
                G_new[pair] = 1
    return G_new


# In[199]:

#moralize
def moralize(G):
    Gnew = G.copy()
    Gnew = Gnew + Gnew.T
    Gnew[Gnew > 1] = 1
    return Gnew


# In[205]:

def remove_conditioned(C, G):
    Gnew = G.copy()
    for c in C:
        Gnew[:, c] = np.zeros(len(G))
        Gnew[c, :] = np.zeros(len(G))
    return Gnew


# In[214]:

def is_connected(A, B, G):
    #BFS implemented using code from 
    #https://www.geeksforgeeks.org/find-if-there-is-a-path-between-two-vertices-in-a-given-graph/
    visited = [False]*len(G)
    queue = []
    queue.append(A)
    visited[A] = True
    while queue:
        x = queue.pop(0)
        if x == B:
            return True
        for i in np.where(G[x, :] == 1)[0]:
            if visited[i] == False:
                queue.append(i)
                visited[i] = True
    return False


# In[238]:

def d_separated(A, B, C, G, index_start=1):
    if index_start==1:
        A = A-1
        B = B-1
        for i in range(len(C)):
            C[i] = C[i]-1
    G_ancestral = ancestral_graph(A, B, C, G)
    G_married = marry_parents(G_ancestral)
    G_moral = moralize(G_married)
    G_final = remove_conditioned(C, G_moral)
    return not is_connected(A, B, G_final)

if __name__=="__main__":

    dag = np.loadtxt('dag.txt', skiprows=1, usecols=range(1, 101))
    A = 61
    B= 68
    C = [4, 19, 90]
    print(str(d_separated(A, B, C, dag, index_start=1)).upper())

    A = 55
    B= 27
    C = [4, 8, 9, 12, 29, 32, 40, 44, 45, 48, 50, 52]
    print(str(d_separated(A, B, C, dag, index_start=1)).upper())
