import streamlit
from streamlit_folium import folium_static
import folium
import matplotlib.pyplot

def introduction():
    streamlit.title('Welcolme to ICOnprend Rien')
    streamlit.write("Created by Andreis, Colin, Mehdi, Yaniv, Paul and James")
    

def map(model):
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred','lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    deposits = model.agents['deposits']
    center = list(deposits.values())[0]
    clients = model.agents['clients']
    m = folium.Map(location=[center.lat,center.lon], zoom_start=12)
    for deposit in deposits.values():
        folium.Marker([deposit.lat, deposit.lon], icon=folium.Icon(color=colors[-2], icon="cloud")).add_to(m)
    for client in clients.values():
        folium.Marker([client.lat, client.lon], icon=folium.Icon(color=colors[client.cluster])).add_to(m)
    folium_static(m)
    pass
