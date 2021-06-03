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
