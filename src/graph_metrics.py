import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


def build_graph(df):
    G = nx.DiGraph()

    for row in df.itertuples(index=False):
        rating = int(row.rating)

        G.add_edge(
            int(row.source),
            int(row.target),
            rating=rating,
            timestamp=int(row.time),
            weight=abs(rating),
        )

    return G


def filter_graph(
    G,
    min_degree=1,
    edge_mode="All",
    min_strength=1,
    max_nodes=300,
):
    keep = [
        node
        for node, degree in G.degree()
        if degree >= min_degree
    ]

    keep = sorted(
        keep,
        key=lambda node: G.degree(node),
        reverse=True,
    )[:max_nodes]

    H = G.subgraph(keep).copy()

    remove_edges = []

    for u, v, data in H.edges(data=True):
        rating = data.get("rating", 0)

        if abs(rating) < min_strength:
            remove_edges.append((u, v))
            continue

        if edge_mode == "Trust only" and rating <= 0:
            remove_edges.append((u, v))

        elif edge_mode == "Distrust only" and rating >= 0:
            remove_edges.append((u, v))

    H.remove_edges_from(remove_edges)
    H.remove_nodes_from(list(nx.isolates(H)))

    return H


def compute_metrics(G):
    if G.number_of_nodes() == 0:
        return {
            "Degree": {},
            "PageRank": {},
            "Betweenness": {},
        }, {}

    degree = dict(G.degree())

    pagerank = nx.pagerank(
        G,
        weight=None,
    )

    k = min(100, G.number_of_nodes())

    betweenness = nx.betweenness_centrality(
        G,
        k=k if k < G.number_of_nodes() else None,
        seed=42,
    )

    UG = G.to_undirected()

    if UG.number_of_edges():
        communities = list(
            greedy_modularity_communities(UG)
        )
    else:
        communities = [
            {node}
            for node in UG.nodes()
        ]

    community = {
        node: community_id
        for community_id, members in enumerate(communities)
        for node in members
    }

    return {
        "Degree": degree,
        "PageRank": pagerank,
        "Betweenness": betweenness,
    }, community
