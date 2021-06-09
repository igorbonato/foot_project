import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
# from foot2 import conv_xml
from pandas import json_normalize
import json

app = dash.Dash(__name__)
# ---------------------------------------------------------
#loading data

with open("dataplayers2.0.json", 'r') as infile:
    d = json.load(infile)
    df = json_normalize(d, record_path=["Players"])
    
# -----------------------------------------------------------
app.layout = html.Div([
    html.H1("Stats Player do igor"),
    html.Div([
        html.Div([
            html.H1("Jogador 1"),
            dcc.Dropdown(
                id="players-names",
                options=[{"label": i, "value": i} for i in df.Name],
                value=df.iloc[0].Name
            ),
            dcc.Graph(id="graph-stats-1")
        ]
        ),
        html.Div([
            html.H1("Jogador 2"),
            dcc.Dropdown(
            id="players-names-2",
            options=[{"label": i, "value": i} for i in df.Name],
            value=df.iloc[1].Name
            ),
            dcc.Graph(id="graph-stats-2")
        ]  
        ),
    ]),
])
#------------------------------------------------------
@app.callback(
    Output("graph-stats-1","figure"),
    Output("graph-stats-2","figure"),
    Input("players-names","value"),
    Input("players-names-2","value")
)

def update_graphs(player1,player2):
    dff= df[df.Name == player1]
    dff2= df[df.Name == player2]
    
    def create_figure(df):
        fig = go.Figure(
        data=[go.Bar(text=df.Assists, name="Assists", y=df.Name, x=df.Assists, orientation='h'),
            go.Bar(text=df.Goals, name="Goals", y=df.Name,
                    x=df.Goals, orientation='h'),
            go.Bar(text=df.Games, name="Games", y=df.Name, x=df.Games, orientation='h')],
        layout_xaxis_visible=False, layout_yaxis_visible=False
        )
        fig.update_layout(title_text=str(df.iloc[0].Name), legend_traceorder="grouped", bargroupgap=0.2,
                        legend_tracegroupgap=15, plot_bgcolor="#fff")
        fig.update_traces(textposition="outside")
        
        return fig
    
    figure1=create_figure(dff)
    figure2=create_figure(dff2)
    
    return figure1, figure2

if __name__ == '__main__':
    app.run_server(debug=True)
    


#modelo que segui p n esquecer: https://dash.plotly.com/basic-callbacks
#Dash App With Multiple Inputs

# Import and clean data (json into pandas)
with open("dataplayers2.0.json", 'r') as infile:
    d = json.load(infile)
    df = json_normalize(d, record_path=["Players"])
# df = pd.read_json(normed)
# df = df.set_index(["Name"])
# print(df.head(5))

df = df[df.Name == "Lionel Messi"]
# print(y)
# print(df)
fig = go.Figure(
    data=[go.Bar(text=df.Assists, name="Assists", y=df.Name, x=df.Assists, orientation='h'),
          go.Bar(text=df.Goals, name="Goals", y=df.Name,
                 x=df.Goals, orientation='h'),
          go.Bar(text=df.Games, name="Games", y=df.Name, x=df.Games, orientation='h')],
    layout_xaxis_visible=False, layout_yaxis_visible=False
)
fig.update_layout(title_text=str(df.iloc[0].Name), legend_traceorder="grouped", bargroupgap=0.2,
                  legend_tracegroupgap=15, plot_bgcolor="#fff")
fig.update_traces(textposition="outside")
# fig = go.Figure(data=[go.Bar(x=df.Name, y=["800", "950", "1000"])])
fig.show()
# fig = px.bar(df,  orientation="h", title="STATS PLAYER",)
# fig.show()
