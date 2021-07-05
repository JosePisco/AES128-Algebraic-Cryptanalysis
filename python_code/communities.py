from sage.all import mq
import networkx as nx
import osmnx as ox
import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# $pip install community
# $pip install python-louvain
# --------------------------------------------
# augmenter le nombre de tours ne change pas le comportement des communautés entre elles
# le graphe grossit énormément entre n=1 et n=10 mais le graphe garde un bon équilibre
# --------------------------------------------
# réduire les colonnes / lignes de mq.SR simplifie énormément le graphe
# pour aes-64, le graphe donné par les paramètres (n, 2, 4, 8) est beaucoup plus petit
# que celui donné par (n, 4, 4, 4)

def init_polynomials(n, r, c, e):
    sr = mq.SR(n, r, c, e, gf2=True, polybori=True, allow_zero_inversions=True)
    f, s = sr.polynomial_system()
    G = f.connection_graph()
    return G

def plot_graph(G):
    N = G.networkx_graph() # N is undirected by default
    partition = community_louvain.best_partition(N)

    # draw the graph
    pos = nx.spring_layout(N)
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis_r', max(partition.values()) + 1)

    nx.draw_networkx_nodes(N, pos, partition.keys(), node_size=40, cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(N, pos, alpha=0.5)
    
    print("Number of communities within the graph:", max(partition.values()) + 1) # nombre de communautés
    print("Number of nodes:", len(pos)) # nombre de sommets dans le graphe

    plt.show()

def plot_gephi(G):
    partition = community_louvain.best_partition(G)

    # draw the graph
    pos = nx.spring_layout(G)
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis_r', max(partition.values()) + 1)

    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40, cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    
    print("Number of communities within the graph:", max(partition.values()) + 1) # nombre de communautés
    print("Number of nodes:", len(pos)) # nombre de sommets dans le graphe
    print("Number of connected components:", nx.number_connected_components(G))

    plt.show()

# remove tous les noeuds du graphe dont le degré est compris dans entre deg_min et deg_max inclus
# spécifier un chemin pour savegarder en fichier gexf
# avec un graphe de sagemath
def cut_nodes_degree(G, deg_min, deg_max, path=""):
    N = G.networkx_graph()
    print("density:", nx.density(N))
    
    nodes = list(N.degree)
    count = 0
    for i in range(N.number_of_nodes()):
        if nodes[i][1] >= deg_min and nodes[i][1] <= deg_max:
            count += 1
            N.remove_node(nodes[i][0])
            
    print("removed", count, "cut points")
    print("new density:", nx.density(N))
    print("connected components:", nx.number_connected_components(N))
    
    if path != "":
        nx.write_gexf(N, path)
        print("graph file saved")


# exemple avec AES-4
# graph4 = init_polynomials(10, 1, 1, 4)
# plot_graph(graph4)

# GEPHI work...

# path = "../graph_files/aes4_separated.gml"
# separated = nx.read_gml(path)
# plot_gephi(separated)


# Exemple avec AES128 10 tours

graph128 = init_polynomials(10, 4, 4, 8)
cut_nodes_degree(graph128, 100, 315, "aes128_10tours_200cp_removed.gexf")