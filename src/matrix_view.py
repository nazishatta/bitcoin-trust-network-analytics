import networkx as nx
import plotly.express as px


def adjacency_figure(
    G,
    community=None,
    limit=100,
):
    if G.number_of_nodes() == 0:
        return px.imshow([[0]])

    community = community or {}

    nodes = sorted(
        G.nodes(),
        key=lambda node: (
            community.get(node, 9999),
            -G.degree(node),
        ),
    )[:limit]

    H = G.subgraph(nodes)

    matrix = nx.to_numpy_array(
        H,
        nodelist=nodes,
        weight="rating",
    )

    labels = [
        str(node)
        for node in nodes
    ]

    fig = px.imshow(
        matrix,
        x=labels,
        y=labels,
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        zmin=-10,
        zmax=10,
        labels={
            "x": "Target node",
            "y": "Source node",
            "color": "Trust rating",
        },
        aspect="auto",
    )

    fig.update_layout(
        paper_bgcolor="#0b0f14",
        plot_bgcolor="#0b0f14",
        font_color="#e6edf3",
        height=700,
        margin=dict(
            l=60,
            r=30,
            t=30,
            b=60,
        ),
    )

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    return fig
