import streamlit
import folium

def introduction():
    streamlit.title('Welcolme to ICOnprend Rien')
    streamlit.write("Created by Andreis, Colin, Mehdi, Yaniv, Paul and James")
    
def get_data():
    default = streamlit.radio("What data will you use:",("None","Default","Custom Data"))
    if default=="Default":
        streamlit.write("Nah!")
    elif default=="Custom Data":
        streamlit.write("Yeah")

def Streamlit():
    m = folium.Map(location=[center.depot_latitude,center.depot_longitude], zoom_start=12)
    pass
