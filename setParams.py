import tkinter as tk
import os
import test as t

def get_cpu_cores():
    return os.cpu_count()

class SetParams:
    def __init__(self, path, X, y):
        self.path = path
        self.X = X
        self.y = y

        # Create a tkinter window
        self.window = tk.Tk()

        # Create a Label for number of clusters
        lbl_clusters = tk.Label(self.window, text="Ingrese la cantidad de clusters a usar\nNúmero de clusters:")
        lbl_clusters.pack()

        # Create a Textbox (Entry) for number of clusters
        self.txt_clusters = tk.Entry(self.window)
        self.txt_clusters.pack()

        # Create a Label for number of cores
        lbl_cores = tk.Label(self.window,
                             text=f"Cuantos uso nucleos para el entrenamiento?\nDefault: {get_cpu_cores()}\nCantidad de núcleos:")
        lbl_cores.pack()

        # Create a Textbox (Entry) for number of cores
        self.txt_cores = tk.Entry(self.window)
        self.txt_cores.pack()
        self.txt_cores.insert(0, get_cpu_cores())

        # Create a Button to submit the inputs
        submit_button = tk.Button(self.window, text="Start training", command=self.setValues)
        submit_button.pack()

        cancel_button = tk.Button(self.window, text="Cancel training", command=lambda: self.window.destroy())
        cancel_button.pack()

        # Start the tkinter main loop
        self.window.mainloop()

    def setValues(self):
        clusters = int(self.txt_clusters.get())
        cores = int(self.txt_cores.get())
        tmp = t.trainer(clusters, cores, self.path, self.X, self.y)

