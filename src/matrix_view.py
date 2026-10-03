import networkx as nx
import plotly.express as px

def adjacency_figure(G, limit=150):
    nodes=sorted(G.nodes(), key=lambda n:G.degree(n), reverse=True)[:limit]
    H=G.subgraph(nodes)
    A=nx.to_numpy_array(H, nodelist=nodes, weight='rating')
    fig=px.imshow(A, x=[str(n) for n in nodes], y=[str(n) for n in nodes],
                  color_continuous_scale='RdBu', color_continuous_midpoint=0,
                  labels={'x':'Target node','y':'Source node','color':'Trust rating'})
    fig.update_layout(paper_bgcolor='#0b0f14', plot_bgcolor='#0b0f14', font_color='#e6edf3', height=700)
    return fig
