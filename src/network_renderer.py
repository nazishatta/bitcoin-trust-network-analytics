import networkx as nx
from pyvis.network import Network

PALETTE=['#35b6ff','#ff6b6b','#56d364','#d2a8ff','#f2cc60','#39d0c3','#ff9b50','#8b949e']

def _sizes(values):
    if not values: return {}
    lo,hi=min(values.values()),max(values.values())
    if hi==lo: return {k:18 for k in values}
    return {k:10+30*(v-lo)/(hi-lo) for k,v in values.items()}

def build_pyvis(G, metrics, community, layout, size_metric, show_labels, search_node):
    net=Network(height='700px', width='100%', bgcolor='#0b0f14', font_color='#e6edf3', directed=True,
                cdn_resources='in_line', notebook=False)
    sizes=_sizes(metrics[size_metric])
    highlight=str(search_node).strip()
    for n in G.nodes():
        selected=highlight and str(n)==highlight
        color='#ffffff' if selected else PALETTE[community.get(n,0)%len(PALETTE)]
        title=(f'Node {n}<br>Degree: {metrics["Degree"].get(n,0)}<br>'
               f'PageRank: {metrics["PageRank"].get(n,0):.5f}<br>'
               f'Betweenness: {metrics["Betweenness"].get(n,0):.5f}<br>'
               f'Community: {community.get(n,0)}')
        net.add_node(n, label=str(n) if show_labels else ' ', size=sizes.get(n,12)*(1.6 if selected else 1),
                     color=color, title=title, borderWidth=3 if selected else 0)
    for u,v,d in G.edges(data=True):
        rating=d.get('rating',0)
        color='#56d364' if rating>0 else '#ff6b6b'
        net.add_edge(u,v,color=color,width=0.5+abs(rating)*0.18,title=f'Rating: {rating}',arrows='to')
    if layout=='circular':
        pos=nx.circular_layout(G, scale=500)
        for node in net.nodes:
            x,y=pos[node['id']]
            node['x'],node['y']=float(x),float(y)
            node['physics']=False
        net.toggle_physics(False)
    else:
        net.set_options('''{"physics":{"barnesHut":{"gravitationalConstant":-9000,"springLength":110,"springConstant":0.025,"damping":0.4},"stabilization":{"iterations":150}},"interaction":{"hover":true,"navigationButtons":true,"keyboard":true},"edges":{"smooth":false}}''')
    return net.generate_html(notebook=False)
