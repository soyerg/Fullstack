# dashboard/app.py
import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Tableau de bord IPS"),
    html.P("Bienvenue sur votre dashboard !"),
])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
