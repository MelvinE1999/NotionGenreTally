# find out if an application is okay
# if for the pie chart want to select by check boxes
# any features they want it to have for now
import info
import matplotlib.pyplot as plt
from notion.client import NotionClient
import requests
from tkinter import *
from tkinter import ttk
import tkinter as tk

collection = {}
labels = []
sizes = []

scores = tk.Tk()
cols = ('Rank', 'Genre', 'Quantity')
dataTable = ttk.Treeview(scores, columns=cols, show='headings')

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

    dataInOrder = dict(sorted(data.items(), key=lambda item: item[1]))  # sorts by value  in increasing order
    for key in reversed(dataInOrder.keys()):
        labels.append(key)
        sizes.append(dataInOrder[key])
        tempGenre = str(key)
        tempQuantity = str(dataInOrder[key])
        dataTable.insert("", "end", values=(counter, tempGenre, tempQuantity))
        counter = counter + 1


def abcOrder():
    counter = 1

    dataTable.delete(*dataTable.get_children())

    for key in sorted(data.keys()):
        labels.append(key)
        sizes.append(data[key])
        tempGenre = str(key)
        tempQuantity = str(data[key])
        dataTable.insert("", "end", values=(counter, tempGenre, tempQuantity))
        counter = counter + 1


def display_chart():
    # code below copied for testing
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, shadow=True, startangle=90)
    ax1.axis("equal")

    plt.show()


def run():
    displayChart = True
    choice = ''

    test_internet()
    collect_data_from_notion()

    for col in cols:
        dataTable.heading(col, text=col)
    dataTable.grid(row=1, column=0, columnspan=3)

    showScoresInABC = tk.Button(scores, text="Alphabetical Order", width=15,
                                command=abcOrder).grid(row=4, column=0)
    showScoresInQuantityDescending = tk.Button(scores, text="Descending order",
                                               width=15, command=quantity_Order).grid(row=4, column=1)

    scores.mainloop()

    while choice.lower() != 'yes' or choice.lower() != 'no':
        choice = input("Would you like to display the pie chart? (yes or no)\n")
        if choice.lower == 'no':
            displayChart = False

    if displayChart:
        display_chart()


if __name__ == '__main__':
    run()
