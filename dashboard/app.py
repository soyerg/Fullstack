import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import requests
import pandas as pd

app = dash.Dash(__name__)
server = app.server

API_URL = "http://api:8000"

def get_schools():
    try:
        response = requests.get(f"{API_URL}/schools")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Erreur API:", e)
        return []

def compute_avg_ips_by_departement(data):
    df = pd.DataFrame(data)
    df = df[df["ips"].notna()]
    df_grouped = df.groupby("departement")["ips"].mean().reset_index()
    return df_grouped.sort_values("ips", ascending=False)

app.layout = html.Div([
    html.H1("📊 IPS moyen par département"),
    html.Button("📥 Charger les données", id="load-btn", n_clicks=0),
    dcc.Graph(id="ips-graph")
])

@app.callback(
    Output("ips-graph", "figure"),
    Input("load-btn", "n_clicks")
)
def update_graph(n_clicks):
    if n_clicks == 0:
        return {"layout": {"title": "Cliquez sur le bouton pour charger les données."}}

    data = get_schools()
    if not data:
        return {"layout": {"title": "❌ Données non disponibles"}}

    df = compute_avg_ips_by_departement(data)

    return {
        "data": [{
            "x": df["departement"],
            "y": df["ips"],
            "type": "bar",
            "name": "IPS moyen"
        }],
        "layout": {
            "title": "Indice de Position Sociale (IPS) moyen par département",
            "xaxis": {"title": "Département", "tickangle": -45},
            "yaxis": {"title": "IPS moyen"},
        }
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
