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

# plt.plot(v.algorithm[i].mins)
# plt.title("Courbe de résultats de l'algorithme " + type(v.algorithm[i]).__name__)
# plt.xlabel("Nombre d'itérations")
# plt.ylabel('Coût trouvé')
# plt.show()

# def plot_dendrogram(model, **kwargs):
#     # Create linkage matrix and then plot the dendrogram

#     # create the counts of samples under each node
#     counts = np.zeros(model.children_.shape[0])
#     n_samples = len(model.labels_)
#     for i, merge in enumerate(model.children_):
#         current_count = 0
#         for child_idx in merge:
#             if child_idx < n_samples:
#                 current_count += 1  # leaf node
#             else:
#                 current_count += counts[child_idx - n_samples]
#         counts[i] = current_count

#     linkage_matrix = np.column_stack(

      
#         [model.children_, model.distances_, counts]
#     ).astype(float)

#     # Plot the corresponding dendrogram
#     dendrogram(linkage_matrix, **kwargs)
# plot_dendrogram(model, truncate_mode="level", p=3)

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
