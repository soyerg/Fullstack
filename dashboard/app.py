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

def get_school_count_by_ips_range(min_ips, max_ips):
    try:
        params = {"min_ips": min_ips, "max_ips": max_ips}
        response = requests.get(f"{API_URL}/schools/ips", params=params)
        if response.status_code == 200:
            return len(response.json())
        return 0
    except Exception as e:
        print("Erreur API tranche IPS:", e)
        return 0

def compute_avg_ips_by_departement(data):
    df = pd.DataFrame(data)
    df = df[df["ips"].notna()]
    df_grouped = df.groupby("departement")["ips"].mean().reset_index()
    return df_grouped.sort_values("ips", ascending=False)

app.layout = html.Div([
    html.H1("📊 Analyse des écoles par IPS"),
    html.Button("📥 Charger les données", id="load-btn", n_clicks=0),
    html.H2("📌 IPS moyen par région"),
    dcc.Graph(id="ips-graph"),
    html.H2("📈 Répartition des écoles par tranche d’IPS"),
    dcc.Graph(id="ips-range-graph")
])

@app.callback(
    Output("ips-graph", "figure"),
    Output("ips-range-graph", "figure"),
    Input("load-btn", "n_clicks")
)
def update_graphs(n_clicks):
    if n_clicks == 0:
        msg = {"layout": {"title": "Cliquez sur le bouton pour charger les données."}}
        return msg, msg

    schools = get_schools()
    if not schools:
        msg = {"layout": {"title": "❌ Données non disponibles"}}
        return msg, msg

    df = compute_avg_ips_by_departement(schools)

    fig1 = {
        "data": [{
            "x": df["departement"],
            "y": df["ips"],
            "type": "bar",
            "name": "IPS moyen"
        }],
        "layout": {
            "title": "📌 IPS moyen par région",
            "xaxis": {"title": "Département", "tickangle": -45},
            "yaxis": {"title": "IPS moyen"},
        }
    }

    ranges = list(range(80, 115, 5))
    x = [f"{r}–{r+5}" for r in ranges]
    y = [get_school_count_by_ips_range(r, r+5) for r in ranges]

    fig2 = {
        "data": [{
            "x": x,
            "y": y,
            "type": "bar",
            "name": "Nombre d'écoles"
        }],
        "layout": {
            "title": "Répartition des écoles par tranche d’IPS",
            "xaxis": {"title": "Tranches d’IPS"},
            "yaxis": {"title": "Nombre d’écoles"},
        }
    }

    return fig1, fig2

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
