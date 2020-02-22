import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objs as go

N = 20
MEAN_Y = 50
STD_Y = 15
MEAN_X = 80
STD_X = 20


def generate_random(n=N, mean_x=MEAN_X, std_x=STD_X, mean_y=MEAN_Y, std_y=STD_Y):
    fig = make_subplots(rows=1, cols=3)

    fig.add_trace(
        go.Scatter(
            x=np.random.normal(mean_x, std_x, n), y=np.random.normal(mean_y, std_y, n), mode='markers'
        )
        ,row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=np.random.normal(mean_x, std_x, n), y=np.random.normal(mean_y, std_y, n), mode='markers'
        ), 
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=np.random.normal(mean_x, std_x, n), y=np.random.normal(mean_y, std_y, n), mode='markers'
        ),
        row=1, col=3
    )

    fig.update_layout(showlegend=False,  margin={'t': 30, 'b': 0}, title_text='random points')
    
    return fig



def plot_permuted(df, xcol, ycol, color):
    fig = make_subplots(rows=1, cols=3)
    x = df[xcol].values
    y = df[ycol].values
    
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='markers'
        )
        ,row=1, col=1
    )
    
    np.random.shuffle(y)
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='markers'
        ), 
        row=1, col=2
    )
    
    np.random.shuffle(y)
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='markers'
        ),
        row=1, col=3
    )

    fig.update_layout(showlegend=False,  margin={'t': 30, 'b': 0}, title_text='random points')
    
    return fig
