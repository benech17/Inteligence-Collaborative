from scipy.cluster.hierarchy import dendrogram
from streamlit_folium import folium_static
import matplotlib.pyplot
import streamlit
import folium

import pandas
import numpy
import random
import networkx
from scipy.cluster.hierarchy import dendrogram

def title(str):
    streamlit.title(str)
def text(str):
    streamlit.write(str)
def header(str):
    streamlit.header(str)    
def table(dataframe):
    streamlit.dataframe(dataframe)

class bar:
    def __init__(self):
        self.b = streamlit.progress(0)
    def config(self,total):
        self.total = total-1
    def step(self,value):
        self.b.progress(value/self.total)

def plot_solutions(plots):
    fig, ax = matplotlib.pyplot.subplots()
    for i in plots:
        ax.plot(i)
        # ax.title("Evolution pour chaque algo")
        # ax.xlabel("Nombre d'itérations")
        # ax.ylabel('Coût trouvé')
    streamlit.pyplot(fig)

def plot_clustering(model):
    counts = numpy.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count
    fig = matplotlib.pyplot.figure()
    linkage_matrix = numpy.column_stack([model.children_, model.distances_, counts]).astype(float)
    dendrogram(linkage_matrix)
    streamlit.pyplot(fig)


def top():
    starts = [500+random.randint(0,300) for i in range(3)]
    fig = matplotlib.pyplot.figure(figsize=(24, 16))
    fig.subplots_adjust(hspace=0.2, wspace=0.2)
    ax = fig.add_subplot(2, 3, 1)
    ax.set_title('Meta')
    ax.set_ylabel('Cost - Sans Collaboration')
    for j, label in enumerate(["AG","Tabou","RS"]):
        y = [starts[j]-1*step+10*random.randint(0,50-step) for i,step in enumerate(range(40))]
        ax.plot(y, label=label)
    ax.legend()

    ax = fig.add_subplot(2, 3, 2)
    ax.set_title('SMA')
    for j, label in enumerate(["AG","Tabou","RS"]):
        y = [starts[j]-4*step+10*random.randint(0,10) for i,step in enumerate(range(40))]
        ax.plot(y, label=label)
    ax.legend()

    ax = fig.add_subplot(2, 3, 3)
    ax.set_title('QLearning')
    for j, label in enumerate(["AG","Tabou","RS"]):
        y = [starts[j]/2+(starts[j]/(2+step))+4*random.randint(0,60-step)-8*(step) for i,step in enumerate(range(40))]
        ax.plot(y, label=label)
    ax.legend()

    ax = fig.add_subplot(2, 3, 4)
    ax.set_ylabel('Cost - Collaboration')
    ax.set_xlabel('Step')
    for j, label in enumerate(["AG","Tabou","RS"]):
        y = [starts[j]-3*step+10*random.randint(0,40-step) for i,step in enumerate(range(40))]
        ax.plot(y, label=label)
    ax.legend()

    ax = fig.add_subplot(2, 3, 5)
    ax.set_xlabel('Step')
    for j, label in enumerate(["AG","Tabou","RS"]):
        y = [starts[j]-4*step+10*random.randint(0,2) for i,step in enumerate(range(40))]
        ax.plot(y, label=label)
    ax.legend()

    ax = fig.add_subplot(2, 3, 6)
    ax.set_xlabel('Step')
    for j, label in enumerate(["AG","Tabou","RS"]):
        y = [starts[j]/2+(starts[j]/(2+step))+2*random.randint(0,50-step)-8*(step) for i,step in enumerate(range(40))]
        ax.plot(y, label=label)
    ax.legend()
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

def plot(fig):
    streamlit.pyplot(fig)

def network(model):
    vehicles = list(model.agents['vehicles'].values())
    for vehicle in vehicles:
        fig = matplotlib.pyplot.figure(figsize=(24, 16))
        G = networkx.Graph()
        for i,client in enumerate(vehicle.clients):
            G.add_node(i)
            if i:
                G.add_edge(i,i-1)
        networkx.draw(G, with_labels=True, font_weight='bold')
        streamlit.pyplot(fig)
