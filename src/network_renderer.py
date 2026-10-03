import networkx as nx
from pyvis.network import Network


PALETTE = [
    "#35b6ff",
    "#ff6b6b",
    "#56d364",
    "#d2a8ff",
    "#f2cc60",
    "#39d0c3",
    "#ff9b50",
    "#8b949e",
]


def _sizes(values):
    if not values:
        return {}

    lo = min(values.values())
    hi = max(values.values())

    if hi == lo:
        return {node: 16 for node in values}

    return {
        node: 9 + 22 * (value - lo) / (hi - lo)
        for node, value in values.items()
    }


def build_pyvis(
    G,
    metrics,
    community,
    layout,
    size_metric,
    show_labels,
    search_node,
):
    net = Network(
        height="700px",
        width="100%",
        bgcolor="#0b0f14",
        font_color="#e6edf3",
        directed=True,
        cdn_resources="in_line",
        notebook=False,
    )

    sizes = _sizes(metrics[size_metric])
    highlight = str(search_node).strip()

    for node in G.nodes():
        selected = bool(
            highlight and str(node) == highlight
        )

        if selected:
            color = "#ffffff"
        else:
            color = PALETTE[
                community.get(node, 0) % len(PALETTE)
            ]

        title = (
            f"<b>Node {node}</b><br>"
            f"Degree: {metrics['Degree'].get(node, 0)}<br>"
            f"PageRank: {metrics['PageRank'].get(node, 0):.5f}<br>"
            f"Betweenness: {metrics['Betweenness'].get(node, 0):.5f}<br>"
            f"Community: {community.get(node, 0)}"
        )

        node_size = sizes.get(node, 12)

        if selected:
            node_size *= 1.55

        net.add_node(
            node,
            label=str(node) if show_labels else " ",
            size=node_size,
            color=color,
            title=title,
            borderWidth=4 if selected else 0,
        )

    for u, v, data in G.edges(data=True):
        rating = data.get("rating", 0)

        if rating > 0:
            edge_color = "rgba(86,211,100,0.20)"
        else:
            edge_color = "rgba(255,107,107,0.55)"

        edge_width = 0.20 + abs(rating) * 0.045

        net.add_edge(
            u,
            v,
            color=edge_color,
            width=edge_width,
            title=f"Rating: {rating}",
            arrows={
                "to": {
                    "enabled": True,
                    "scaleFactor": 0.28,
                }
            },
        )

    if layout == "circular":
        positions = nx.circular_layout(
            G,
            scale=650,
        )

        for node in net.nodes:
            x, y = positions[node["id"]]

            node["x"] = float(x)
            node["y"] = float(y)
            node["physics"] = False

        net.toggle_physics(False)

    else:
        net.set_options(
            """
            {
              "physics": {
                "enabled": true,
                "barnesHut": {
                  "gravitationalConstant": -18000,
                  "centralGravity": 0.16,
                  "springLength": 175,
                  "springConstant": 0.018,
                  "damping": 0.34,
                  "avoidOverlap": 0.65
                },
                "minVelocity": 0.75,
                "stabilization": {
                  "enabled": true,
                  "iterations": 300,
                  "updateInterval": 25,
                  "fit": true
                }
              },
              "interaction": {
                "hover": true,
                "navigationButtons": true,
                "keyboard": true,
                "tooltipDelay": 100,
                "hideEdgesOnDrag": true
              },
              "edges": {
                "smooth": false,
                "selectionWidth": 1.3,
                "hoverWidth": 1.1
              },
              "nodes": {
                "shape": "dot"
              }
            }
            """
        )

    return net.generate_html(notebook=False)
