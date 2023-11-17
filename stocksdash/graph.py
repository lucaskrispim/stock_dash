import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
from .utils import *

def getCandleStickGraph(df,stock_name):
    # Crie um gráfico de dispersão simples
    trace = go.Candlestick(x=df.index,open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'] )

    data = [trace]
    layout = go.Layout(title=stock_name, xaxis=dict(title='Date'), yaxis=dict(title='Price'),xaxis_rangeslider_visible=False,plot_bgcolor='rgb(240, 240, 240)',)

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div


def getLinekGraph(df,title,column):
    # Crie um gráfico de dispersão simples
    trace = go.Scatter(x=df.index,y=df[column], mode='lines')

    # Adicione linhas horizontais fixas em Y=30 e Y=70
    shapes = [
        dict(
            type='line',
            xref='paper',
            yref='y',
            x0=0,
            y0=30,
            x1=1,
            y1=30,
            line=dict(color='red', width=3),
        ),
        dict(
            type='line',
            xref='paper',
            yref='y',
            x0=0,
            y0=70,
            x1=1,
            y1=70,   
            line=dict(color='blue', width=3),
        ),
    ]

    data = [trace]
    layout = go.Layout(title=title, xaxis=dict(title='Date'), yaxis=dict(title="index"),xaxis_rangeslider_visible=False,yaxis_range=[0,100],shapes=shapes,plot_bgcolor='rgb(240, 240, 240)',)

    fig = go.Figure(data=data, layout=layout)

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div


def getHistogramGraph(df,title,x_title,y_title):
    data = df['Variation'].tolist()  # Dados para o histograma

    # Crie um histograma com os dados
    trace = go.Histogram(x=data, nbinsx=20, marker=dict(color='green'),opacity=0.4)

    counts, bins = np.histogram(data, bins=15)

    avg_return = round(df['Variation'].mean(),2)

    var = round(np.quantile(df['Variation'][:], 0.05),2)

    # Encontra a altura máxima entre os bins
    max_bin_height = max(counts)

    vline = dict(
        type='line',
        x0=avg_return,
        y0=0,
        x1=avg_return,
        y1=max_bin_height,  # Altura máxima do histograma para a linha vertical
        line=dict(color='blue', width=3),

    )

    annotation = dict(
        x=avg_return+1,
        y=max_bin_height+2,
        xref='x',
        yref='y',
        text=f"Average value {avg_return}",
        showarrow=False,
        arrowhead=7,
        ax=0,
        ay=-40
    )

    vline2 = dict(
        type='line',
        x0=var,
        y0=0,
        x1=var,
        y1=max_bin_height,  # Altura máxima do histograma para a linha vertical
        line=dict(color='red', width=3),

    )

    annotation2 = dict(
        x=var+1,
        y=max_bin_height+2,
        xref='x',
        yref='y',
        text=f"VaR {var}",
        showarrow=False,
        arrowhead=7,
        ax=0,
        ay=-40
    )

    layout = go.Layout(
        title=title,
        xaxis=dict(title=x_title, tickformat='.2f'),
        yaxis=dict(title=y_title, tickformat='.2f'),
        shapes=[vline,vline2],
        annotations=[annotation,annotation2],
        plot_bgcolor='rgb(240, 240, 240)',
    )

    fig = go.Figure(data=[trace], layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div

def getBetaGraph(df,benchmark,asset,title):
    df_pctchange = getPctChange(df,benchmark,asset)

    # Crie um gráfico de dispersão simples
    trace = go.Scatter(x=df_pctchange[benchmark],y=df_pctchange[asset],mode='markers',name="")

    a,b = getLinearCoef(df_pctchange,benchmark,asset)

    x0 = min(df_pctchange[benchmark].values)
    y0 = a * min(df_pctchange[benchmark].values) + b
    
    x1 = max(df_pctchange[benchmark].values)
    y1 = a * max(df_pctchange[benchmark].values) + b

    vline = dict(
        type='line',
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,  
        line=dict(color='red', width=3),
    )

    line_trace = go.Scatter(
        x=[x0,x1],
        y=[y0[0],y1[0]],
        mode='lines',  # Define o modo como linha para representar uma reta
        line=dict(color='red', width=3),  # Define a cor e a largura da linha,
        name=f"Beta {a}"
    )

    data = [trace,line_trace]
    layout = go.Layout(title=title, xaxis=dict(title=benchmark), yaxis=dict(title=asset),xaxis_rangeslider_visible=False,plot_bgcolor='rgb(240, 240, 240)',)

    fig = go.Figure(data=data, layout=layout)

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_div