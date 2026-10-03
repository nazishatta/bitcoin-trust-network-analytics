₿ Bitcoin Trust Network Intelligence
Interactive signed-network analytics for exploring trust, distrust, communities, centrality, and structural patterns in the Stanford Bitcoin Alpha network.
 
 
Python · Streamlit · NetworkX · PyVis · Plotly · Pandas · SciPy
🚀 Explore the Project
Live dashboard: https://bitcoin-trust-network-analytics.streamlit.app/
Source repository: https://github.com/nazishatta/bitcoin-trust-network-analytics
The dashboard turns a signed, directed trust network into an interactive analytical experience. Rather than presenting one static graph, it lets users change the visible network, structural importance measure, edge sentiment, layout, and filtering thresholds and immediately inspect how the structure changes.
🔎 The Analytical Question
How does the structure of a peer-to-peer trust network change when we examine different definitions of importance, relationship sentiment, communities, and connectivity thresholds?
Bitcoin Alpha users rated other users in a directed trust network. The sign of an edge distinguishes trust from distrust, while its magnitude records the strength of the rating.
The project focuses on influential users, trust/distrust relationships, community structure, directed connectivity, dense-network visualization, and alternative representations of the same graph.
📊 Dashboard at a Glance
Component	Purpose
Network Explorer	Interactive node-link representation of the filtered trust network
Trust Matrix	Signed adjacency-matrix alternative for examining dense structure
Node Intelligence	Ranked centrality table and Top-15 structural-importance chart
Methodology	Explains the network, visual encodings, and interpretation limitations
Control Center	Coordinates filtering and visualization choices


🎛️ Interactive Control Center
Control	What it changes	Why it matters
Layout	Network layout strategy	Compare alternative spatial organizations
Node size	Degree, betweenness, or PageRank	Compare definitions of structural importance
Edge sentiment	All, trust, or distrust	Isolate positive or negative relationships
Minimum degree	Connectivity threshold	Reduce weakly connected nodes and visual clutter
Minimum edge strength |rating|	Required rating magnitude	Focus on stronger relationships
Maximum displayed nodes	Number of visible nodes	Manage density and the hairball problem
Show node labels	Node-ID visibility	Trade annotation detail for clarity


Because the controls modify the graph being analyzed, the active filter state is part of the interpretation—not merely a presentation setting.
🕸️ 01 · Interactive Network Explorer
The primary view is an interactive node-link visualization of the filtered Bitcoin Alpha network.
Visual encodings
Visual channel	Network attribute
Node	Bitcoin Alpha user
Directed edge	Rating issued from one user to another
Node size	Selected structural-importance metric
Node color	Detected community membership
Edge sign / appearance	Trust versus distrust relationship
Edge magnitude	Strength of the signed rating
Position	Algorithmic network layout


Structural importance
Degree captures how connected a node is within the displayed graph.
Betweenness centrality highlights nodes that frequently lie along shortest paths and may act as structural bridges.
PageRank measures importance recursively, giving greater weight to connections involving other important nodes.
Switching node-size encoding makes these different definitions directly comparable.
🧩 Community Structure
Node color represents detected community membership. Community detection adds a structural layer beyond individual-node centrality by making groups with stronger internal connectivity easier to inspect.
Community colors represent categorical membership, not an ordered quantity.
🔴 Trust and Distrust
Bitcoin Alpha is a signed network. Positive ratings represent trust relationships and negative ratings represent distrust relationships.
The Edge sentiment control lets users examine all visible relationships, trust-only relationships, or distrust-only relationships.
The minimum edge-strength control uses absolute rating magnitude, allowing weaker relationships to be removed while preserving positive and negative signs.
🧱 02 · Signed Adjacency Matrix
Dense node-link diagrams can become difficult to interpret as relationships increase. The Trust Matrix provides an alternative representation.
Each matrix cell corresponds to a directed relationship:
row = source node
column = target node
cell value = signed trust rating
The diverging color scale is centered at zero so positive and negative relationships remain visually distinct. Nodes are selected from the currently filtered graph and ordered to make structural patterns easier to inspect.
Why include a matrix?
A node-link diagram emphasizes paths, hubs, communities, and topology.
An adjacency matrix emphasizes relationship density, block structure, signed patterns, clusters of interactions, and the presence or absence of edges.
Providing both views demonstrates that visualization choice depends on the analytical task.
🧠 03 · Node Intelligence
The Node Intelligence view converts network structure into a ranked analytical summary.
For visible nodes, the dashboard reports:
- Node ID
- Degree
- PageRank
- Betweenness
- Community
A ranked Top 15 horizontal bar chart responds to the selected structural metric, providing a quantitative companion to the network visualization.
📈 Dynamic KPI Layer
The dashboard summarizes the active analytical state with headline metrics:
Active nodes — nodes represented after filtering.
Visible edges — directed relationships remaining in the active graph.
Communities — detected community groups represented in the current view.
Dataset distrust — share of negative relationships in the underlying dataset.
Keeping dataset distrust independent from the visible sentiment filter avoids implying that a trust-only filtered view means the original network contains no distrust.
🧹 Managing the Network “Hairball”
Large node-link diagrams can become visually saturated. This project addresses that problem through coordinated filtering:
- minimum-degree threshold;
- minimum absolute edge strength;
- maximum displayed-node control;
- sentiment filtering;
- alternative adjacency-matrix representation.
The dashboard deliberately exposes the tradeoff between completeness and readability rather than hiding network complexity.
⚠️ Visualization Integrity & Interpretation
This dashboard is intended for exploratory structural analysis.
Layout is not measured distance. Force-directed position is algorithmic. Visual proximity should not automatically be interpreted as physical, social, or temporal distance.
Filtering changes the visible network. Apparent structure must be interpreted in the context of active controls.
Centrality is metric-dependent. Degree, betweenness, and PageRank represent different concepts of importance.
Community color is categorical. A community number or color does not imply higher or lower trustworthiness or importance.
Dense graphs can obscure structure. The adjacency matrix provides an alternative representation when the node-link diagram becomes difficult to read.
Network structure does not establish causality. The visualization describes relationships represented in the data; it does not establish why a rating was issued.
🗂️ Data
The application uses the Stanford Bitcoin Alpha signed trust network.
Project data file:
data/soc-sign-bitcoinalpha.csv
The network is modeled as a directed weighted graph:
source user ── signed rating ──▶ target user
The rating sign distinguishes trust from distrust, while rating magnitude represents relationship strength.
🧮 Analytical Pipeline
Bitcoin Alpha data
        │
        ▼
Load edge data
        │
        ▼
Construct directed weighted graph
        │
        ▼
Apply interactive filters
        │
        ▼
Compute structural metrics
        │
        ├── Degree
        ├── Betweenness
        ├── PageRank
        └── Community detection
        │
        ▼
Coordinate analytical views
        │
        ├── Network Explorer
        ├── Signed Trust Matrix
        ├── Node Intelligence
        └── KPI summaries
🛠️ Technology Stack
Technology	Role
Python	Application and analytical logic
Streamlit	Interactive dashboard interface
NetworkX	Graph construction and network analysis
PyVis	Interactive node-link visualization
Plotly	Trust matrix and analytical charts
Pandas	Data loading and transformation
SciPy	Numerical support for graph analytics
Git / GitHub	Version control and source hosting
Streamlit Community Cloud	Public application deployment


📁 Repository Structure
bitcoin-trust-network-analytics/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── soc-sign-bitcoinalpha.csv
└── src/
    ├── graph_metrics.py
    ├── network_renderer.py
    └── matrix_view.py
app.py coordinates the Streamlit interface and analytical views.
graph_metrics.py contains graph-analysis and structural-metric logic.
network_renderer.py builds the interactive PyVis network.
matrix_view.py generates the signed adjacency-matrix visualization.
💻 Run Locally
Clone the repository:
git clone https://github.com/nazishatta/bitcoin-trust-network-analytics.git
cd bitcoin-trust-network-analytics
Create and activate a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
Install dependencies:
python -m pip install -r requirements.txt
Run the application:
python -m streamlit run app.py
Then open:
http://localhost:8501
🧭 Suggested Exploration
1. Start with the default filtered network.
2. Switch node size between Degree, Betweenness, and PageRank.
3. Compare All, Trust, and Distrust edge sentiment.
4. Increase minimum degree and observe which nodes remain.
5. Increase minimum edge strength to isolate stronger ratings.
6. Change the maximum displayed nodes and observe the density/readability tradeoff.
7. Compare the node-link graph with the Trust Matrix.
8. Open Node Intelligence and compare centrality rankings with visually prominent nodes.
🔬 Potential Extensions
Future development could add ego-network exploration, temporal trust evolution, centrality-threshold filtering, community-level summaries, trust/distrust ratios by community, additional layouts, signed-network-specific measures, shortest-path analysis, temporal animation, and structural anomaly analysis.
These are potential extensions rather than features claimed by the current application.
👤 Author
Nazish Atta
M.S. Data Science · George Washington University
Data Science · Analytics · Machine Learning · Interactive Visualization
GitHub Profile · Project Repository · Live Dashboard
⭐ Explore the Network
Change the filters. Compare centrality measures. Separate trust from distrust. Inspect communities. See how the network story changes.
👉 Launch Bitcoin Trust Network Intelligence
Python · NetworkX · PyVis · Plotly · Streamlit · Pandas · SciPy
