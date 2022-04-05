import streamlit as st

def introduction():
    st.title('Welcolme to ICOnprend Rien')
    st.write("Created by Andreis, Colin, Mehdi, Yaniv, Paul and James")
    
def get_data():
    default = st.radio("What data will you use:",("None","Default","Custom Data"))
    if default=="Default":
        st.write("Nah!")
    elif default=="Custom Data":
        st.write("Yeah")
    

