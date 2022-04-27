from scipy.cluster.hierarchy import dendrogram
from streamlit_folium import folium_static
import matplotlib.pyplot
import streamlit
import folium

import pandas
import numpy
import random
import seaborn


def title(str):
    streamlit.title(str)
def text(str):
    streamlit.write(str)
def header(str):
    streamlit.header(str)    
def table(dataframe):
    streamlit.dataframe(dataframe)
def step_bar(value):
    streamlit.progress(value)

def plot_solutions(plots):
    fig, ax = matplotlib.pyplot.subplots()
    for i in plots:
        ax.plot(i)
        # ax.title("Evolution pour chaque algo")
        # ax.xlabel("Nombre d'itérations")
        # ax.ylabel('Coût trouvé')
    streamlit.pyplot(fig)

def fig_comparaison():
    starts = [500+random.randint(0,300) for i in range(3)]
    fig = matplotlib.pyplot.figure(figsize=(12, 8))
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    ax = fig.add_subplot(2, 3, 1)
    ax.set_title('Meta')
    ax.set_ylabel('Cost - Sans Collaboration')
    y = pandas.DataFrame([[starts[j]-1*step+10*random.randint(0,50-step) for i,step in enumerate(range(40))] for j in range(3)]).T
    y = y.rename(columns={0:"AG", 1:"Tabou", 2:"RS"})
    seaborn.lineplot(data=y, ax=ax)
    ax = fig.add_subplot(2, 3, 2)
    ax.set_title('SMA')
    y = pandas.DataFrame([[starts[j]-4*step+10*random.randint(0,10) for i,step in enumerate(range(40))] for j in range(3)]).T
    y = y.rename(columns={0:"AG", 1:"Tabou", 2:"RS"})
    seaborn.lineplot(data=y, ax=ax)
    ax = fig.add_subplot(2, 3, 3)
    ax.set_title('QLearning')
    y = pandas.DataFrame([[starts[j]/2+(starts[j]/(2+step))+4*random.randint(0,60-step)-8*(step) for i,step in enumerate(range(40))] for j in range(3)]).T
    y = y.rename(columns={0:"AG", 1:"Tabou", 2:"RS"})
    seaborn.lineplot(data=y, ax=ax)
    ax = fig.add_subplot(2, 3, 4)
    ax.set_ylabel('Cost - Collaboration')
    ax.set_xlabel('Step')
    y = pandas.DataFrame([[starts[j]-3*step+10*random.randint(0,40-step) for i,step in enumerate(range(40))] for j in range(3)]).T
    y = y.rename(columns={0:"AG", 1:"Tabou", 2:"RS"})
    seaborn.lineplot(data=y, ax=ax)
    ax = fig.add_subplot(2, 3, 5)
    ax.set_xlabel('Step')
    y = pandas.DataFrame([[starts[j]-4*step+10*random.randint(0,2) for i,step in enumerate(range(40))] for j in range(3)]).T
    y = y.rename(columns={0:"AG", 1:"Tabou", 2:"RS"})
    seaborn.lineplot(data=y, ax=ax)
    ax = fig.add_subplot(2, 3, 6)
    ax.set_xlabel('Step')
    y = pandas.DataFrame([[starts[j]/2+(starts[j]/(2+step))+2*random.randint(0,50-step)-8*(step) for i,step in enumerate(range(40))] for j in range(3)]).T
    y = y.rename(columns={0:"AG", 1:"Tabou", 2:"RS"})
    seaborn.lineplot(data=y, ax=ax)
    streamlit.pyplot(fig)

def map(model):
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred','lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    deposits = model.agents['deposits']
    center = list(deposits.values())[0]
    clients = model.agents['clients']
    client_routes_id = {clients[client].route_id: 1 for client in clients}
    for i,route in enumerate(client_routes_id):
        client_routes_id[route] = colors[i]
    m = folium.Map(location=[center.lat,center.lon], zoom_start=12)
    for deposit in deposits.values():
        folium.Marker([deposit.lat, deposit.lon], icon=folium.Icon(color=colors[-2], icon="cloud")).add_to(m)
    for client in clients.values():
        folium.Marker([client.lat, client.lon], icon=folium.Icon(color=client_routes_id[client.route_id])).add_to(m)
    folium_static(m)
