import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from scipy import stats

N = 20
MEAN_Y = 50
STD_Y = 15
MEAN_X = 80
STD_X = 20

COLORS = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]
def generate_random(n=N, mean_x=MEAN_X, std_x=STD_X, mean_y=MEAN_Y, std_y=STD_Y):
    fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.1,  shared_xaxes=True,  shared_yaxes=True)

    for i in [1, 2, 3]: 
        x=np.random.normal(mean_x, std_x, n)
        y=np.random.normal(mean_y, std_y, n)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*x+intercept
        
        fig.add_trace(
            go.Scatter(
                x=x, y=y, mode='markers', marker={'color': COLORS[i-1]}
            )
            ,row=1, col=i
        )
        fig.add_trace(
            go.Scatter(
                x=x, y=line, mode='lines', marker={'color': COLORS[i-1]}
            )
            
            ,row=1, col=i
        )

    fig.update_layout(showlegend=False,  margin={'t': 30, 'b': 0}, title_text='random points')
    
    return fig



def plot_permuted(df, xcol, ycol, color):
    fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.1,  shared_xaxes=True,  shared_yaxes=True)
    x = df[xcol].values
    y = df[ycol].values
    c = df[color].values
    
    fig.update_xaxes(title_text=xcol, row=1, col=1)
    fig.update_xaxes(title_text=xcol, row=1, col=2)
    fig.update_xaxes(title_text=xcol, row=1, col=3)
    
    fig.update_yaxes(title_text=ycol, row=1, col=1)
    fig.update_yaxes(title_text=ycol + ' (permuted)', row=1, col=2)
    fig.update_yaxes(title_text=xcol + ' (permuted)', row=1, col=3)
    
    
    fig.add_trace(
        go.Scatter(
            x=x, y=y,  mode='markers', marker={'color': c}
        )
        ,row=1, col=1
    )
    
    np.random.shuffle(y)
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='markers',  marker={'color': c}
        ), 
        row=1, col=2
    )
    
    np.random.shuffle(y)
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='markers',  marker={'color': c}
        ),
        row=1, col=3
    )

    fig.update_layout(showlegend=False,  margin={'t': 30, 'b': 0})
    
    return fig
