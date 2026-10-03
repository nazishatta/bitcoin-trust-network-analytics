import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

def build_graph(df):
    G=nx.DiGraph()
    for r in df.itertuples(index=False):
        G.add_edge(int(r.source), int(r.target), rating=int(r.rating), timestamp=int(r.time), weight=abs(int(r.rating)))
    return G

def filter_graph(G, min_degree=1, edge_mode='All', max_nodes=300):
    keep=[n for n,d in G.degree() if d >= min_degree]
    keep=sorted(keep, key=lambda n:G.degree(n), reverse=True)[:max_nodes]
    H=G.subgraph(keep).copy()
    if edge_mode != 'All':
        remove=[]
        for u,v,d in H.edges(data=True):
            rating=d.get('rating',0)
            if edge_mode=='Trust only' and rating <= 0: remove.append((u,v))
            if edge_mode=='Distrust only' and rating >= 0: remove.append((u,v))
        H.remove_edges_from(remove)
        H.remove_nodes_from(list(nx.isolates(H)))
    return H

def compute_metrics(G):
    if not G.number_of_nodes(): return {'Degree':{},'PageRank':{},'Betweenness':{}}, {}
    degree=dict(G.degree())
    pagerank=nx.pagerank(G, weight=None)
    # Approximation keeps the interactive app responsive on larger filtered graphs.
    k=min(100, G.number_of_nodes())
    btw=nx.betweenness_centrality(G, k=k if k < G.number_of_nodes() else None, seed=42)
    UG=G.to_undirected()
    comms=list(greedy_modularity_communities(UG)) if UG.number_of_edges() else [{n} for n in UG.nodes()]
    community={n:i for i,c in enumerate(comms) for n in c}
    return {'Degree':degree,'PageRank':pagerank,'Betweenness':btw}, community
