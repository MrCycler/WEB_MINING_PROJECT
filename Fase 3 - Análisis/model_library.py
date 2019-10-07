from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def grafico_silueta(modelo, data_X, n_clusters):
      # ----------------- Definicion de figura -----------------------------------
  # Crea los subplots para mostrar la figura
  # Especifica tamaños para la figura
  fig, (ax1) = plt.subplots(1, 1) 
  fig.set_size_inches(9, 7) 
  
  # ----------------- Definicion de limites -----------------------------------
  # Limites en X del grafico de siluetas
  # Los limites de Y se incrementan (n_clusters+1)*10, para dejar 
  # espacio entre siluetas
  ax1.set_xlim([-0.1, 1]) 
  ax1.set_ylim([0, len(data_X) + (n_clusters + 1) * 10])

  # ----------------- Predicción de Clases ------------------------------------
  # Se predicen los valores, el puntaje de silueta promedio y elpuntaje silueta
  # de cada muestra 
  cluster_labels = modelo.predict(data_X)
  silhouette_avg = silhouette_score(data_X, cluster_labels)
  sample_silhouette_values = silhouette_samples(data_X, cluster_labels)

  # ----------------- Ploteo de Gráfico ---------------------------------------
  y_lower = 10
  for i in range(n_clusters):
    # Se agregan los valores de la silueta 'i' y se ordenan
    ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
    ith_cluster_silhouette_values.sort()

    #Se hallan el numero de muestras y se suma al lower
    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i

    color = cm.nipy_spectral(float(i) / n_clusters)
    ax1.fill_betweenx(np.arange(y_lower, y_upper),0, ith_cluster_silhouette_values,facecolor=color, edgecolor=color, alpha=0.7)

    # Label the silhouette plots with their cluster numbers at the middle
    ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

    # Compute the new y_lower for next plot
    y_lower = y_upper + 10  # 10 for the 0 samples

  ax1.set_title("The silhouette plot for the various clusters.")
  ax1.set_xlabel("The silhouette coefficient values")
  ax1.set_ylabel("Cluster label")

  # The vertical line for average silhouette score of all the values
  ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

  ax1.set_yticks([])  # Clear the yaxis labels / ticks
  ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])