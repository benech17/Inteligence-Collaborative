import folium
import matplotlib.pyplot
from mpl_toolkits.basemap import Basemap

def basemap():
    Australia_map = Basemap(llcrnrlat=43.36701275870108,urcrnrlat=17.55707823960915,llcrnrlon=17.620764612008408,urcrnrlon=43.390219758207465)
    matplotlib.pyplot.figure(figsize=(12,10))
    Australia_map.bluemarble(alpha=0.9)
    matplotlib.pyplot.savefig('hey.png')


def map(center, points):
    print(center)
    m = folium.Map(location=[center.depot_latitude,center.depot_longitude], zoom_start=12)