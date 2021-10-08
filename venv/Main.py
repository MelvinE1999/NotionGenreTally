# find out if an application is okay
# if for the pie chart want to select by check boxes
# any features they want it to have for now

#if notionpy doesnt work could have her export to csv and read from there
import info
import matplotlib.pyplot as plt
from notion.client import NotionClient
import requests
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from tkinter import ttk
import tkinter as tk


collection = {}
labels = []
sizes = []

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


def get_comma_number_of_genre(listOfHeader):
    commaCounter = 0
    if(len(listOfHeader) == 0): return  # gaurdian clause
    listOfHeader = listOfHeader[1:] # gets rid of the formatting at the beginning of the file
    headers = listOfHeader.split(',')
    for header in headers:
        if header == "Column" or header == "column":
            return commaCounter
        else:
            commaCounter = commaCounter + 1



def get_genres(line, commaNumber):
    for char in line:
        if(commaNumber == commaCount):
            if(char == '\"'):
                continue
        # add a checker for open and closed quotes
        # store data in the setup dictionaries
        if(char == ','):
            commaCount = commaCount + 1


def get_data_from_file():
    Tk().withdraw()
    file = askopenfile(mode='r', filetypes=[('comma-seperated values', '*.csv')])
    # need to add parsing below
    header = next(file)
    commaNumber = get_comma_number_of_genre(header)
    for line in file.readlines(): # loop for the rest of the file minus header
        get_genres(line, commaNumber)


def close():
    dataWindow.wm_withdraw() # closes window might be helpful


def run():
    displayChart = True
    choice = ''

    # test_internet()    not needed until notionpy fixed
    # collect_data_from_notion()  notionpy is not working at the moment

    for col in cols:
        dataTable.heading(col, text=col)
    dataTable.grid(row=1, column=0, columnspan=3)

    showScoresInABC = tk.Button(dataWindow, text="Alphabetical Order", width=15,
                                command=abcOrder).grid(row=4, column=0)
    showScoresInQuantityDescending = tk.Button(dataWindow, text="Descending order",
                                               width=15, command=quantity_Order).grid(row=4, column=1)
    closeButton = tk.Button(dataWindow, text="close",width=15, command=close).grid(row=4, column=2)

    dataWindow.mainloop()

    while choice.lower() != 'yes' or choice.lower() != 'no':
        choice = input("Would you like to display the pie chart? (yes or no)\n")
        if choice.lower == 'no':
            displayChart = False

    if displayChart:
        display_chart()


if __name__ == '__main__':
    #run()
    get_data_from_file()
