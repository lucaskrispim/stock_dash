# plotly_app/views.py
from django.shortcuts import render
import plotly.graph_objs as go
from plotly.offline import plot
import yfinance as yf
from .graph import *
from .indicators import *
from .utils import *

def plotly_view(request):

    origin = yf.download(["VALE3.sa","^BVSP"],period='1y', progress=False)

    df = getDataFrameByIndex(origin,"VALE3.SA")

    BVSP = getDataFrameByIndex(origin,"^BVSP")

    plot_div = getCandleStickGraph(df.copy(),"VALE")

    data = []
    data = RSI(data=df.copy(),column='Close', window=14)

    plot_div2 = getLinekGraph(data,"RSI 14","rsi")

    plot_div3 = getHistogramGraph(data,"","Returns","")

    plot_div4 = getBetaGraph(origin,"^BVSP","VALE3.SA","Beta de mercado")

    return render(request, 'index.html', context={'plot_div': plot_div,'plot_div2': plot_div2,'plot_div3': plot_div3,'plot_div4': plot_div4})
