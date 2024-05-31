import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['figure.figsize'] = (7, 7)
plt.rcParams['figure.dpi'] = 100
plt.style.use('ggplot')
fig = plt.Figure()



label = []
canvas = []


# Create a tkinter window
class window:
    def __init__(self, entry, result, path):
        self.gEntry = entry
        self.gResult = result
        self.gPath = path
        self.fig = plt.Figure()

        self.gDataFrame = pd.read_csv(path)

        self.gX = np.array(self.gDataFrame[entry])
        self.gY = np.array(self.gDataFrame[result])
        self.window = tk.Tk()

        #btn frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        #buttons
        headbtn = tk.Button(button_frame, text="Show Head", command=lambda: self.genHead(), pady=10)
        headbtn.pack(side=tk.LEFT)

        descbtn = tk.Button(button_frame, text="Show Describe", command=lambda: self.genDescribe(), pady=10)
        descbtn.pack(side=tk.LEFT)

        histbtn = tk.Button(button_frame, text="Show Histogram", command=lambda: self.genHistogram(), pady=10)
        histbtn.pack(side=tk.LEFT)

        pairbtn = tk.Button(button_frame, text="Show Pairplot", command=lambda: self.genPairplot(), pady=10)
        pairbtn.pack(side=tk.LEFT)

        elbowbtn = tk.Button(button_frame, text="Show Elbow Curve", command=lambda: self.genElbowCurve(), pady=10)
        elbowbtn.pack(side=tk.LEFT)

        continueBtn = tk.Button(button_frame, text="Start train", command=lambda: self.start(self.gPath, self.gX, self.gY), pady=10)
        continueBtn.pack(side=tk.LEFT)

        closeBtn = tk.Button(button_frame, text="Close", command=lambda: self.window.destroy(), pady=10)
        closeBtn.pack(side=tk.LEFT)

        # Create a Canvas
        self.canvass = tk.Canvas(self.window)
        self.canvass.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Create a Scrollbar and add it to the Canvas
        self.scrollbar = tk.Scrollbar(self.window, command=self.canvass.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Configure the Canvas to use the Scrollbar
        self.canvass.configure(yscrollcommand=self.scrollbar.set, width=700, height=500)

        # Create a Frame and add it to the Canvas
        self.frame = tk.Frame(self.canvass)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.canvass.create_window((0, 0), window=self.frame, anchor='nw')

        # Start the tkinter main loop
        self.window.mainloop()

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

    def genHead(self):
        self.genText(fulldf(self.gDataFrame.head()))

    def genDescribe(self):
        self.genText(fulldf(self.gDataFrame.describe()))

    def genHistogram(self):
        show = fig.add_subplot(111)
        self.gDataFrame.drop(self.gResult, axis=1).hist(ax=show)

        self.genFig(fig)

    def genPairplot(self):
        show = sb.pairplot(self.gDataFrame.dropna(), hue='categoria', height=(len(self.gEntry) + len(self.gResult)),
                           vars=self.gEntry, kind='scatter').figure
        self.genFig(show)

    def genElbowCurve(self):
        fig = plt.figure()
        Nc = range(1, 20)
        kmeans = [KMeans(n_clusters=i) for i in Nc]
        score = [kmeans[i].fit(self.gX).score(self.gX) for i in range(len(kmeans))]
        plt.plot(Nc, score)
        plt.xlabel('Number of Clusters')
        plt.ylabel('Score')
        plt.title('Elbow Curve')
        self.genFig(fig)


    def start(self, path, X, y):
        import setParams as sP
        sP.SetParams(path, X, y)

def fulldf(df):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    return df

