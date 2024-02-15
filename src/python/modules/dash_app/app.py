from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from aip.utils import ret_test


app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children=ret_test()),

    html.Div(children='''
        This is a test.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

application = app.server

if __name__ == '__main__':
    print('Starting server ...')
    from waitress import serve
    serve(application, host="0.0.0.0", port=8080, threads=20)
