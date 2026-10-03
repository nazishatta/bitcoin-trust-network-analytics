# Bitcoin Trust Network Analytics

### Interactive Network Intelligence for Trust, Community & Structural Risk

A dark-themed Streamlit dashboard for exploring the Stanford SNAP Bitcoin Alpha signed trust network with NetworkX, PyVis, and Plotly.

## Features
- Interactive directed PyVis network: drag, zoom, hover, navigation
- Force-directed and circular layouts
- Node size switch: Degree, Betweenness, PageRank
- Community-based node color
- Trust vs. distrust edge encoding and filtering
- Degree threshold and maximum-node controls
- Node search/highlighting
- Signed adjacency-matrix view
- Node intelligence table and centrality chart
- Methodology and visualization-limitations panel

## Dataset
Download the Bitcoin Alpha signed network from Stanford SNAP and place the extracted file at:

`data/soc-sign-bitcoinalpha.csv`

The expected columns are: source, target, rating, timestamp.

## Run in VS Code
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
streamlit run app.py
```

## Structural encodings
- Node size: selected centrality measure
- Node color: detected community
- Edge color: positive/negative trust
- Edge width: absolute rating magnitude
- Arrow: rating direction

## Limitation
Force-directed position is algorithmic, not a measured distance. Dense networks can become unreadable hairballs, and filtering changes the visible structure; the matrix view provides an alternative representation.
