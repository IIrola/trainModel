import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import test

class selection:
    def __init__(self, entry: list, result: list, data):
        self.entry = entry
        self.result = result
        self.data = data


# Create the main application window
class CSVViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.title("CSV Viewer")

        # Button to select a CSV file
        self.select_button = tk.Button(self, text="Select CSV File", command=self.select_csv)
        self.select_button.pack(pady=10)

        # the number of rows showed in the table, is a strictly number
        self.mount_showed = tk.Spinbox(self, from_=1, to=1000000, increment=1)
        self.mount_showed.pack(pady=10)

        # label to warnings

        self.label = tk.Label(self, text="")
        self.label.pack(pady=10)

        # Button to save selected column names
        self.save_button = tk.Button(self, text="Save Entry Columns", command=self.save_entry_columns)
        self.save_button.pack(pady=10)
        self.save_button.pack_forget()

        self.result_button = tk.Button(self, text="Save Result Columns", command=self.save_result_columns)
        self.result_button.pack(pady=10)
        self.result_button.pack_forget()

        # Button to close the csv file
        self.close_button = tk.Button(self, text="Close CSV", command=self.close_csv)
        self.close_button.pack(pady=10)
        self.close_button.pack_forget()

        # Create a frame for the checkboxes of model

        self.checkbox_frameM = tk.Frame(self)
        self.checkbox_frameM.pack()

        # Create a frame for checkboxes for entry and result
        self.checkbox_frameS = tk.Frame(self)
        self.checkbox_frameS.pack()

        # Create a frame for checkboxes
        self.checkbox_frame = tk.Frame(self)
        self.checkbox_frame.pack()

        # Create a treeview to display the data
        self.treeview = ttk.Treeview(self)
        self.treeview.pack(expand=True, fill="both")
        self.treeview.pack_forget()


        self.trainBtn = ttk.Button(self, text="Train", command=self.train)
        self.trainBtn.pack(pady=10)
        self.trainBtn.pack_forget()

        # Dictionary to store checkboxes for columns
        self.column_checkboxes = {}

        self.column_checkboxes_config = {}

        # List to store the names of selected columns to entry
        self.entry_columns = []

        # List to store the names of selected columns to results
        self.result_columns = []

    def close_csv(self):
        self.save_button.pack_forget()
        self.close_button.pack_forget()
        self.result_button.pack_forget()
        self.label.config(text="")
        self.checkbox_frame.pack_forget()
        self.treeview.pack_forget()
        self.column_checkboxes.clear()
        self.column_checkboxes_config.clear()
        self.entry_columns.clear()
        self.result_columns.clear()
        self.trainBtn.pack_forget()

    def select_csv(self):
        # Use file dialog to select a CSV file
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if self.file_path and self.mount_showed.get() != '0':
            self.save_button.pack()
            self.result_button.pack()
            self.close_button.pack()
            self.checkbox_frame.pack()
            self.treeview.pack()
            self.load_csv(self.file_path)
            self.trainBtn.pack()
        elif self.mount_showed.get() == '0':
            self.label.config(text="The number of rows showed in the table must be greater than 0")
        else:
            self.label.config(text="No file selected")

    def load_csv(self, file_path):
        # Read CSV file with pandas and limit to the first 100 rows
        self.complete = pd.read_csv(file_path)

        df = self.complete.head(int(self.mount_showed.get()))

        # Clear the current content of the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Clear the existing checkboxes from the frame
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()

        # Clear the dictionary of checkboxes
        self.column_checkboxes.clear()
        self.column_checkboxes_config.clear()

        # Set up the columns in the treeview
        self.treeview["columns"] = list(df.columns)
        self.treeview["show"] = "headings"

        for col in df.columns:
            # Set column heading and width
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor='center')

            # Create a checkbox for the column
            checkbox_var = tk.BooleanVar(value=False)
            checkbox = tk.Checkbutton(self.checkbox_frame, text=col, variable=checkbox_var)
            checkbox.pack(side="left")

            # Store the checkbox in the dictionary with the column name as the key
            self.column_checkboxes[col] = checkbox_var

            self.column_checkboxes_config[col] = checkbox

        # Insert rows into the treeview
        for index, row in df.iterrows():
            # Insert the row data
            self.treeview.insert("", "end", values=list(row))

    def save_entry_columns(self):

        # Iterate over the dictionary of column checkboxes
        for column, checkbox_var in self.column_checkboxes.items():
            # If the checkbox is checked, add the column to the selected columns list
            if checkbox_var.get():
                self.entry_columns.append(column)
                self.column_checkboxes[column] = tk.BooleanVar(value=False)
                self.column_checkboxes_config[column].config(state="disabled")
                # Disable the checkbox since it has been selected

        # Print the list of selected column names
        print("Selected Columns to Entry:", self.entry_columns)

    def save_result_columns(self):

        # Iterate over the dictionary of column checkboxes
        for column, checkbox_var in self.column_checkboxes.items():
            # If the checkbox is checked, add the column to the selected columns list
            if checkbox_var.get():
                self.result_columns.append(column)
                self.column_checkboxes[column] = tk.BooleanVar(value=False)
                self.column_checkboxes_config[column].config(state="disabled")
                # Disable the checkbox since it has been selected

        # Print the list of selected column names
        print("Selected Columns to Result:", self.result_columns)


    def train(self):
        if(self.result_columns != [] and self.entry_columns != []):
            print("Training")
            print("Selected Columns to Entry:", self.entry_columns)
            print("Selected Columns to Result:", self.result_columns)
            test.start_train(self.file_path, self.entry_columns, self.result_columns)
        else:
            print("No columns selected")





# Create an instance of the application
app = CSVViewerApp()

# Run the application
app.mainloop()

