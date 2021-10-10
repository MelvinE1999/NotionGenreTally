# find out if an application is okay
# if for the pie chart want to select by check boxes
# any features they want it to have for now

# if notionpy doesnt work could have her export to csv and read from there
# import info     # unneded for now until notionpy is fixed
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from notion.client import NotionClient
import requests
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import Tk
from tkinter import ttk
import tkinter as tk

collection = {}
labels = []
sizes = []
hasDataBeenEntered = False

dataWindow = tk.Tk()
cols = ('Rank', 'Genre', 'Quantity')
dataTable = ttk.Treeview(dataWindow, columns=cols, show='headings')


def test_internet():
    url = "http://www.google.com"
    timeout = 2
    try:
        r = requests.get(url, timeout=timeout)
    except (requests.ConnectionError, requests.Timeout) as exception:

        quit()


def collect_data_from_notion():
    client = NotionClient(token_v2=info.info['token_v2'])

    page = client.get_collection_view(info.info['site'])

    for row in page.collection.get_rows():
        for tag in row.genre:
            if tag in collection.keys():
                collection[tag] = collection[tag] + 1
            else:
                collection[tag] = 1


def quantity_Order():
    counter = 1

    dataTable.delete(*dataTable.get_children())

    dataInOrder = dict(sorted(collection.items(), key=lambda item: item[1]))  # sorts by value  in increasing order
    for key in reversed(dataInOrder.keys()):
        tempGenre = str(key)
        tempQuantity = str(dataInOrder[key])
        dataTable.insert("", "end", values=(counter, tempGenre, tempQuantity))
        counter = counter + 1


def abcOrder():
    counter = 1

    dataTable.delete(*dataTable.get_children())

    for key in sorted(collection.keys()):
        tempGenre = str(key)
        tempQuantity = str(collection[key])
        dataTable.insert("", "end", values=(counter, tempGenre, tempQuantity))
        counter = counter + 1


def display_chart():
    global hasDataBeenEntered

    pieChartWindow = Toplevel()
    pieChartWindow.title("Pie Chart")

    figure = plt.figure(figsize=(6, 6), dpi=100)
    figure.set_size_inches(10, 8)

    if not hasDataBeenEntered:
        for key in sorted(collection.keys()):
            labels.append(key)
            sizes.append(collection[key])
        hasDataBeenEntered = True

    plt.pie(sizes, labels=labels, shadow=True, startangle=90)
    plt.axis("equal")

    graph = FigureCanvasTkAgg(figure, pieChartWindow)
    graph.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



def get_comma_number_of_genre(listOfHeader):
    commaCounter = 0
    if (len(listOfHeader) == 0): return  # gaurdian clause
    listOfHeader = listOfHeader[1:]  # gets rid of the formatting at the beginning of the file
    headers = listOfHeader.split(',')
    for header in headers:
        if header == "Tags" or header == "tags":
            return commaCounter
        else:
            commaCounter = commaCounter + 1


def get_genres(line, targetedIndex):
    parenChecker = False
    entries = line.split(',')
    while True:
        if entries[targetedIndex] == '':
            return
        elif entries[targetedIndex].startswith('\"'):
            parenChecker = True
            entries[targetedIndex] = entries[targetedIndex][1:]
        elif entries[targetedIndex].endswith('\"'):
            parenChecker = False
            entries[targetedIndex] = entries[targetedIndex][0:
                                                len(entries[targetedIndex]) - 1]
        tempValue = entries[targetedIndex]
        if tempValue in collection.keys():
            collection[tempValue] = collection[tempValue] + 1
        else:
            collection[tempValue] = 1

        if parenChecker == False:
            return

        targetedIndex = targetedIndex + 1


def get_data_from_file():
    Tk().withdraw()
    file = askopenfile(mode='r', filetypes=[('comma-seperated values', '*.csv')])
    # need to add parsing below
    header = next(file)
    commaNumber = get_comma_number_of_genre(header)
    for line in file.readlines():  # loop for the rest of the file minus header
        get_genres(line, commaNumber)


def run():
    # test_internet()    not needed until notionpy fixed
    # collect_data_from_notion()  notionpy is not working at the moment
    get_data_from_file()

    for col in cols:
        dataTable.heading(col, text=col)
    dataTable.grid(row=1, column=0, columnspan=3)

    showScoresInABC = tk.Button(dataWindow, text="Alphabetical Order", width=15,
                                command=abcOrder).grid(row=4, column=0)
    showScoresInQuantityDescending = tk.Button(dataWindow, text="Descending order",
                                               width=15, command=quantity_Order).grid(row=4, column=1)
    displayChart = tk.Button(dataWindow, text="Display Chart", width=15,
                             command=display_chart).grid(row=4, column=2)

    dataWindow.mainloop()


if __name__ == '__main__':
    run()
