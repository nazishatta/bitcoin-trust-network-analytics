import numpy as np
import networkx as nx
import plotly.graph_objects as go


def adjacency_figure(G, community=None, limit=50):
    """
    Create a readable signed adjacency matrix for the currently
    filtered directed network.

    Positive values represent trust, negative values represent
    distrust, and missing edges are displayed as dark background.
    Nodes are ordered by community and degree when community
    assignments are available.
    """

    if G.number_of_nodes() == 0:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="#0b0f14",
            plot_bgcolor="#0b0f14",
            font_color="#e6edf3",
            height=650,
            annotations=[
                dict(
                    text="No nodes remain under the current filters.",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=16, color="#9da7b3"),
                )
            ],
        )
        return fig

    selected = sorted(
        G.nodes(),
        key=lambda n: G.degree(n),
        reverse=True,
    )[: min(limit, G.number_of_nodes())]

    if community:
        nodes = sorted(
            selected,
            key=lambda n: (
                community.get(n, 999),
                -G.degree(n),
                str(n),
            ),
        )
    else:
        nodes = selected

    H = G.subgraph(nodes)

    A = nx.to_numpy_array(
        H,
        nodelist=nodes,
        weight="rating",
        dtype=float,
    )

    # A zero means there is no directed edge. Display those cells
    # transparently/dark rather than as the midpoint of the scale.
    Z = A.copy()
    Z[Z == 0] = np.nan

    labels = [str(n) for n in nodes]

    hover = np.empty(Z.shape, dtype=object)

    for i, source in enumerate(nodes):
        for j, target in enumerate(nodes):
            value = A[i, j]

            if value == 0:
                hover[i, j] = (
                    f"Source: {source}<br>"
                    f"Target: {target}<br>"
                    "No edge"
                )
            else:
                relation = "Trust" if value > 0 else "Distrust"
                hover[i, j] = (
                    f"Source: {source}<br>"
                    f"Target: {target}<br>"
                    f"Rating: {value:g}<br>"
                    f"Relation: {relation}"
                )

    fig = go.Figure(
        data=go.Heatmap(
            z=Z,
            x=labels,
            y=labels,
            zmin=-10,
            zmax=10,
            zmid=0,
            colorscale=[
                [0.00, "#b2182b"],
                [0.35, "#ef8a62"],
                [0.49, "#f7f7f7"],
                [0.50, "#f7f7f7"],
                [0.51, "#f7f7f7"],
                [0.65, "#67a9cf"],
                [1.00, "#2166ac"],
            ],
            colorbar=dict(
                title="Trust rating",
                tickvals=[-10, -5, 0, 5, 10],
                thickness=14,
            ),
            text=hover,
            hovertemplate="%{text}<extra></extra>",
            hoverongaps=False,
            xgap=0.35,
            ygap=0.35,
        )
    )

    fig.update_layout(
        paper_bgcolor="#0b0f14",
        plot_bgcolor="#0b0f14",
        font_color="#e6edf3",
        height=720,
        margin=dict(l=70, r=50, t=35, b=70),
        xaxis_title="Target node",
        yaxis_title="Source node",
    )

    fig.update_xaxes(
        type="category",
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        fixedrange=False,
    )

    fig.update_yaxes(
        type="category",
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        autorange="reversed",
        scaleanchor="x",
        scaleratio=1,
        fixedrange=False,
    )

    return fig
