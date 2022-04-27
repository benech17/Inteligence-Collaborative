import numpy
import pandas
import matplotlib.pyplot
import math
import random

def kmeans(vehicles, k = 9):
  diff = 1
  cluster = numpy.zeros(len(vehicles))
  sample_vehicles = [vehicles[i] for i in random.sample(range(0,len(vehicles)),k)]
  centroids = [[v.lat,v.lon] for v in sample_vehicles]
  while diff:
    for i, row in enumerate(vehicles):
      mn_dist = math.inf
      for idx, centroid in enumerate(centroids):
        d = numpy.sqrt((centroid[0]-row.lat)**2 + (centroid[1]-row.lon)**2)
        if mn_dist > d:
          mn_dist = d
          cluster[i] = idx
    new_centroids = [[0,0] for i in range(k)]
    size_centroids = [0 for i in range(k)]
    for i,vehicle in enumerate(vehicles):
      new_centroids[int(cluster[i])][0] += vehicle.lat
      new_centroids[int(cluster[i])][1] += vehicle.lon
      size_centroids[int(cluster[i])] += 1
    for i in range(k):
      new_centroids[i][0] = new_centroids[i][0]/size_centroids[int(cluster[i])]
      new_centroids[i][1] = new_centroids[i][1]/size_centroids[int(cluster[i])]
    if numpy.count_nonzero(numpy.array(centroids)-numpy.array(new_centroids)) == 0:
      diff = 0
    else:
      centroids = new_centroids
  return centroids, cluster