import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances_argmin_min
from mpl_toolkits.mplot3d import Axes3D
import os  # or however many cores you want to use
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog

label = []
canvas = []

plt.cla()
plt.clf()



class window:
    def __init__(self, trainer):

        self.train = trainer
        # Create a tkinter window
        self.window = tk.Tk()

        self.btnFrame = tk.Frame(self.window)
        self.btnFrame.pack(side=tk.TOP, fill=tk.X)

        btnCluster = tk.Button(self.btnFrame, text="Get Clusters", command=lambda: self.train.getClusters(), pady=10)
        btnCluster.pack(side=tk.LEFT)

        btnResults = tk.Button(self.btnFrame, text="Predict results", command=lambda: self.train.predict_results(), pady=10)
        btnResults.pack(side=tk.LEFT)

        btnPrediction = tk.Button(self.btnFrame, text="Predict", command=lambda: self.train.start_predict(), pady=10)
        btnPrediction.pack(side=tk.LEFT)

        btnClose = tk.Button(self.btnFrame, text="Close", command=lambda: self.window.destroy(), pady=10)
        btnClose.pack(side=tk.LEFT)

        # Create a Canvas
        self.canvass = tk.Canvas(self.window)
        self.canvass.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Create a Scrollbar and add it to the Canvas
        scrollbar = tk.Scrollbar(self.window, command=self.canvass.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Configure the Canvas to use the Scrollbar
        self.canvass.configure(yscrollcommand=scrollbar.set, width=16*60, height=9*60)

        # Create a Frame and add it to the Canvas
        self.frameTxt = tk.Frame(self.canvass)
        self.frameTxt.pack(fill=tk.BOTH, expand=True)
        self.canvass.create_window((0, 0), window=self.frameTxt, anchor='e')
        self.frameFig = tk.Frame(self.canvass)
        self.frameFig.pack(fill=tk.BOTH, expand=True)
        self.canvass.create_window((0, 0), window=self.frameFig, anchor='w')

    def genText(self, txt):
        label.append(tk.Label(self.frameTxt, text=txt, justify='center'))
        label[label.__len__() - 1].pack()

        self.window.update()
        self.canvass.configure(scrollregion=self.canvass.bbox('all'))

    # Create a matplotlib figure
    def genFig(self, fig):
        # Add the figure to a tkinter canvas
        canvas.append(FigureCanvasTkAgg(fig, master=self.frameFig))
        canvas[canvas.__len__() - 1].draw()
        canvas[canvas.__len__() - 1].get_tk_widget().pack()

        self.window.update()
        self.canvass.configure(scrollregion=self.canvass.bbox('all'))

    def quickE(self, title, question):
        return simpledialog.askstring(title=title, prompt=question)

class trainer:
    def __init__(self, clusters, cores, path, entry, result):
        self.clusters = clusters
        self.cores = cores
        self.path = path
        self.entry = entry
        self.result = result

        self.DataFrame = pd.read_csv(path)

        self.X = np.array(self.DataFrame[entry])
        self.y = np.array(self.DataFrame[result])

        self.dX = pd.DataFrame(self.X)
        self.dy = pd.DataFrame(self.y)

        os.environ["LOKY_MAX_CPU_COUNT"] = f'{cores}'

        color_list = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'black', 'white', 'gray',
                      'cyan', 'magenta', 'lime', 'teal', 'lavender', 'maroon', 'navy', 'olive', 'coral']

        self.colores = color_list[:self.clusters]

        self.P = window(self)


    def getClusters(self):
        self.kmeans = KMeans(n_clusters=self.clusters).fit(self.X)
        self.centroids = self.kmeans.cluster_centers_
        self.P.genText(f'Centroides: {self.centroids}')

    def predict_results(self):
        # Predicting the clusters
        self.labels = self.kmeans.predict(self.X)

        self.asignar = []
        for row in self.labels:
            self.asignar.append(self.colores[int(row)])

        self.C = self.kmeans.cluster_centers_

        # Getting the values and plotting it
        completes = []
        for i in self.dX.columns:
            for j in self.dX.columns:
                if (i+j) and i != j not in completes:
                    plt.cla()
                    plt.clf()
                    # Getting the values and plotting it
                    f1 = self.dX[i].values
                    f2 = self.dX[j].values
                    plt.scatter(f1, f2, c=self.asignar, s=70)
                    plt.scatter(self.C[:, i], self.C[:, j], marker='*', c=self.colores, s=1000)
                    self.P.genFig(plt.gcf())
                    completes.append(i+j)

        copy = pd.DataFrame()
        copy[self.result] = self.DataFrame[self.result].values
        copy['label'] = self.labels
        cantidadGrupo = pd.DataFrame()
        cantidadGrupo['color'] = self.colores
        cantidadGrupo['cantidad'] = copy.groupby('label').size()
        self.P.genText(cantidadGrupo)
        print(cantidadGrupo)


        # vemos el representante del grupo, el usuario cercano a su centroid
        closest, _ = pairwise_distances_argmin_min(self.kmeans.cluster_centers_, self.X)
        self.P.genText(closest)

        users = self.DataFrame['usuario'].values
        for row in closest:
            self.P.genText(users[row])


    def start_predict(self):
        values = []

        print(self.entry[0])
        for i in self.entry:
            val = self.P.quickE('Predict values', str(i))
            values.append(float(val))

        X_new = np.array([values])  # davidguetta personality traits
        new_labels = self.kmeans.predict(X_new)
        print(new_labels)
        self.P.genText(new_labels)