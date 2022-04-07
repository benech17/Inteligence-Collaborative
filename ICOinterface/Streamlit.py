import streamlit
import folium

def say_hi():
    streamlit.title('Welcolme to ICOnprend Rien')
    streamlit.write("Created by Andreis, Colin, Mehdi, Yaniv, Paul and James")
    default = streamlit.radio("What data will you use:",("None","Default","Custom Data"))
    
def df_pandas(df):
    streamlit.dataframe(df)

def Streamlit():
    m = folium.Map(location=[center.depot_latitude,center.depot_longitude], zoom_start=12)
    pass
