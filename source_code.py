#####
# Contains source code to recreate the analysis
# Author: Kishore Vasan
#####


import networkx as nx
import pandas as pd
import numpy as np

# load network
df = pd.read_csv("cofunding_net_edgelist.csv")
g3 = nx.from_pandas_edgelist(df)
print(nx.info(g))

####
# find communities
####
part = community.community_louvain.best_partition(newg)
val = part.values()
print("Modularity:", community.community_louvain.modularity(part,newg))
print("Number of communities:", len(set(val)))

#### NOTE: do the same above method to find sub-communities
# the resulting communities are released in - funder_community.csv
###
# g-index score
###
# given the citations list for each funder
# the function returns the g index measure for those citations
def get_g_index(x):
    x = list(x)
    x.sort(reverse = True)
    g_index = 0
    highest = True

    for i in range(len(x)):
        if np.mean(x[:i+1])<g_index+1:
            break
        else:
            g_index+=1
    return g_index

### NOTE: the calculated scores for each funder, along with # papers and #citations is released in funder_g_index_scores.csv

# filter the network for further analysis

# filter edge weight to 10 to get better insights into ego level measures
# The intuition is, this thresholding removes "author brought" co-funding efforts
# As we can see, if still retain most of the nodes by this threshold.
edges = []
for e in g.edges(data=True):
    if e[2]['weight']>10:
        edges.append(e[:2])

newg = g.edge_subgraph(edges)
#newg = max(nx.connected_component_subgraphs(newg),key = len)
print(nx.info(newg))

####
# get the network measures
####

# create the ego graph
density_vals = {}
ego_bet_vals = {}
frag_idx = {}
for node in newg.nodes():
    tmp_g = nx.ego_graph(newg, node)
    # density = (= number of edges[not counting ego]/ number of possible edges)
    # get the density (= number of edges/ number of possible edges) = (m/n(n-1))
    density_vals[node] = nx.density(tmp_g)
    # get the betweenness centrality
    ego_bet_vals[node] = nx.betweenness_centrality(tmp_g)[node]
    tmp_g.remove_node(node)
    tmp_val = 0
    num_nodes = len(tmp_g.nodes())
    for n1 in tmp_g.nodes():
        for n2 in tmp_g.nodes():
            if n1 != n2:
                if nx.has_path(tmp_g,n1,n2):
                    tmp_val+=1
    if tmp_val == 0:
        frag_idx[node] = 1
    else:
        frag_idx[node] = 1 - float(tmp_val)/float(num_nodes*(num_nodes -1))

# effective size (number of alters - avg deg of each alter)
esize = nx.effective_size(newg,weight='weight')

efficiency = {n: v / newg.degree(n) for n, v in esize.items()}
# efficiency ( effective size / number of alters)

# constraint
#constraint_vals = nx.constraint(newg)

# degree centrality
deg = nx.degree_centrality(newg)

density_val = []
deg_cen = []
ego_bet_cen = []
effective_size = []
efficiency_val = []
constraint_val = []
agencies = []
fragment_idx = []

for i in deg.keys():
    agencies.append(i)
    deg_cen.append(deg[i])
    ego_bet_cen.append(ego_bet_vals[i])
    effective_size.append(esize[i])
    efficiency_val.append(efficiency[i])
    constraint_val.append(constraint_vals_2[i])
    density_val.append(density_vals[i])
    fragment_idx.append(frag_idx[i])

network_vals = pd.DataFrame({'agency_name':agencies,'deg_cen':deg_cen,'ego_bet_cen':ego_bet_cen,'effective_size':effective_size,'efficiency':efficiency_val,'constraint':constraint_val,'density':density_val,'frag_idx':fragment_idx})
print(network_vals.head())

#### NOTE: for ease, this data is provided in - egonet_stats.csv

