import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from mpl_toolkits.mplot3d import Axes3D
import os  # or however many cores you want to use
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#matplotlib inline
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
label = []
canvas = []



class window:
    def __init__(self):
        # Create a tkinter window
        self.window = tk.Tk()

        # Create a Canvas
        self.canvass = tk.Canvas(self.window)
        self.canvass.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Create a Scrollbar and add it to the Canvas
        scrollbar = tk.Scrollbar(self.window, command=self.canvass.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Configure the Canvas to use the Scrollbar
        self.canvass.configure(yscrollcommand=scrollbar.set, width=700, height=500)

        # Create a Frame and add it to the Canvas
        self.frame = tk.Frame(self.canvass)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.canvass.create_window((0, 0), window=self.frame, anchor='nw')

    def genText(self, txt):
        label.append(tk.Label(self.frame, text=txt, justify='center'))
        label[label.__len__() - 1].pack()

    # Create a matplotlib figure
    def genFig(self, fig):
        # Add the figure to a tkinter canvas
        canvas.append(FigureCanvasTkAgg(fig, master=self.frame))
        canvas[canvas.__len__() - 1].draw()
        canvas[canvas.__len__() - 1].get_tk_widget().pack()

        self.window.update()
        self.canvass.configure(scrollregion=self.canvass.bbox('all'))


def start_train(clusters, cores, path, X, y):
    os.environ["LOKY_MAX_CPU_COUNT"] = f'{cores}'

    dataframe = pd.read_csv(path)

    P = window()

    kmeans = KMeans(n_clusters=clusters).fit(X)
    centroids = kmeans.cluster_centers_
    P.genText(f'Centroides: {centroids}')


    # Predicting the clusters
    labels = kmeans.predict(X)
    # Getting the cluster centers

    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X)

    C = kmeans.cluster_centers_
    colores = ['red', 'green', 'blue', 'cyan', 'yellow']
    asignar = []
    for row in labels:
        asignar.append(colores[int(row)])

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=asignar, s=60)
    ax.scatter(C[:, 0], C[:, 1], C[:, 2], marker='*', c=colores, s=1000)

    plt.show()

    # Getting the values and plotting it
    f1 = dataframe['op'].values
    f2 = dataframe['ex'].values

    plt.scatter(f1, f2, c=asignar, s=70)
    plt.scatter(C[:, 0], C[:, 1], marker='*', c=colores, s=1000)
