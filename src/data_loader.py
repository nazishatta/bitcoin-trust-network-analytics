from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / 'data' / 'soc-sign-bitcoinalpha.csv'

def load_bitcoin_alpha(path=DATA):
    if not Path(path).exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path, header=None, names=['source','target','rating','time'])
    return df.dropna().astype({'source':int,'target':int,'rating':int,'time':int})
