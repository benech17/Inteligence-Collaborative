from scipy.cluster.hierarchy import dendrogram
from streamlit_folium import folium_static
import matplotlib.pyplot
import streamlit
import folium

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
