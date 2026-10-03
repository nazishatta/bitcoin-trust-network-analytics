import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from src.data_loader import load_bitcoin_alpha
from src.graph_metrics import build_graph, compute_metrics, filter_graph
from src.network_renderer import build_pyvis
from src.matrix_view import adjacency_figure

st.set_page_config(page_title='Bitcoin Trust Network Analytics', page_icon='🕸️', layout='wide')

st.markdown('''
<style>
.stApp {background:#0b0f14; color:#e6edf3;}
[data-testid="stSidebar"] {background:#10161d;}
[data-testid="stMetric"] {background:#111820;border:1px solid #263241;border-radius:12px;padding:12px;}
h1,h2,h3 {letter-spacing:-0.02em;}
.block-container {padding-top:1.4rem;}
</style>
''', unsafe_allow_html=True)

st.title('Bitcoin Trust Network Intelligence')
st.caption('Interactive signed-network analytics · Stanford Bitcoin Alpha')

try:
    df = load_bitcoin_alpha()
except FileNotFoundError:
    st.error('Dataset not found. Put soc-sign-bitcoinalpha.csv in the data/ folder. See README.md.')
    st.stop()

G = build_graph(df)

with st.sidebar:
    st.header('Control Center')
    layout = st.selectbox('Layout', ['force-directed', 'circular'])
    size_metric = st.selectbox('Node size', ['PageRank', 'Degree', 'Betweenness'])
    edge_mode = st.selectbox('Edge sentiment', ['All', 'Trust only', 'Distrust only'])
    min_degree = st.slider('Minimum degree', 1, 50, 8)
    min_strength = st.slider('Minimum edge strength |rating|', 1, 10, 3)
    max_nodes = st.slider('Maximum displayed nodes', 50, 400, 125, step=25)
    show_labels = st.checkbox('Show node labels', False)
    search_node = st.text_input('Highlight node ID', '')

H = filter_graph(
    G,
    min_degree=min_degree,
    edge_mode=edge_mode,
    min_strength=min_strength,
    max_nodes=max_nodes,
)
metrics, community = compute_metrics(H)

c1,c2,c3,c4 = st.columns(4)
c1.metric('Active nodes', H.number_of_nodes())
c2.metric('Visible edges', H.number_of_edges())
c3.metric('Communities', len(set(community.values())) if community else 0)
dataset_negative_edges = sum(
    1
    for _, _, data in G.edges(data=True)
    if data.get('rating', 0) < 0
)

dataset_distrust_pct = (
    100 * dataset_negative_edges / max(1, G.number_of_edges())
)

c4.metric(
    'Dataset distrust',
    f'{dataset_distrust_pct:.1f}%'
)

tab1, tab2, tab3, tab4 = st.tabs(['Network Explorer','Trust Matrix','Node Intelligence','Methodology'])

with tab1:
    st.subheader('Interactive Network Explorer')
    st.caption(f'Size = {size_metric} · Color = detected community · Edge = signed trust rating')
    if H.number_of_nodes() > 600:
        st.warning('Hairball warning: dense node-link views can obscure structure. Increase filtering or use the matrix view.')
    html = build_pyvis(H, metrics, community, layout, size_metric, show_labels, search_node)
    components.html(html, height=720, scrolling=False)

with tab2:
    st.subheader('Signed Adjacency Matrix')
    st.caption('An alternative view for dense graphs. Cells encode directed trust ratings.')
    st.plotly_chart(adjacency_figure(H, community=community, limit=100), width="stretch")

with tab3:
    st.subheader('Node Intelligence')
    if H.number_of_nodes():
        rows=[]
        for n in H.nodes():
            rows.append({'Node':str(n),'Degree':metrics['Degree'][n], 'PageRank':metrics['PageRank'][n],
                         'Betweenness':metrics['Betweenness'][n], 'Community':community[n]})
        mdf=pd.DataFrame(rows).sort_values(size_metric, ascending=False)
        st.dataframe(mdf.head(30), width="stretch", hide_index=True)
        top15 = (
            mdf.nlargest(15, size_metric)
            .sort_values(size_metric, ascending=True)
            .copy()
        )

        # Treat numeric-looking Bitcoin user IDs as categorical labels.
        top15['Node'] = top15['Node'].astype(str)

        fig = px.bar(
            top15,
            x=size_metric,
            y='Node',
            orientation='h',
            title=f'Top 15 nodes by {size_metric}',
            text_auto='.4g',
        )

        fig.update_traces(
            marker_line_width=0,
            textposition='outside',
            cliponaxis=False,
        )

        fig.update_layout(
            paper_bgcolor='#0b0f14',
            plot_bgcolor='#0b0f14',
            font_color='#e6edf3',
            height=520,
            margin=dict(l=60, r=80, t=60, b=55),
            xaxis_title=size_metric,
            yaxis_title='Node ID',
            showlegend=False,
        )

        fig.update_xaxes(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.12)',
            zeroline=False,
        )

        fig.update_yaxes(
            type='category',
            showgrid=False,
        )

        st.plotly_chart(fig, width="stretch")

with tab4:
    st.subheader('Methodology & Interpretation')
    st.markdown('''
**What the network represents.** Nodes are anonymous Bitcoin Alpha users. Directed edges are trust ratings issued from one user to another; the rating sign distinguishes trust from distrust and its magnitude records rating strength.

**Why these encodings.** Node size represents a selectable structural importance measure (degree, betweenness, or PageRank). Node color represents detected community membership. Edge appearance preserves relationship direction and sign. This makes it possible to compare different definitions of network importance rather than treating one measure as universally correct.

**Limitation.** Force-directed position is algorithmic rather than a measured variable, so visual proximity should not be interpreted as a physical or directly observed distance. Dense node-link diagrams can also become hairballs. Filtering changes what is visible, so the active controls must be considered when interpreting the graph; the adjacency matrix provides an alternative view for dense structure.
''')
