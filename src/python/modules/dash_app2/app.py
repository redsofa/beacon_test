from dash_extensions import WebSocket
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy

# Client-side function (for performance) that updates the graph.
update_graph = """function(msg) {
    if(!msg){return {};}  // no data, just return
    const data = JSON.parse(msg.data);  // read the data
    return {data: [{y: data, type: "scatter"}]}};  // plot the data
"""
# Create small example app.
app = DashProxy(__name__)
app.layout = html.Div([
        WebSocket(id="ws", url="ws://mqtt5:9001/mqtt"),
    dcc.Graph(id="graph")
])
app.clientside_callback(update_graph, Output("graph", "figure"), Input("ws", "message"))

application = app.server

if __name__ == '__main__':
    print('Starting server ...')
    from waitress import serve
    serve(application, host="0.0.0.0", port=8080, threads=20)
