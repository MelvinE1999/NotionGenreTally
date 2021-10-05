import info
import matplotlib.pyplot as plt
from notion.client import NotionClient
import requests

collection = {}
labels = []
sizes = []


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


def display_genre_count():
    sortingOption = int(input("Would you like to sort the genres alphabetically"
                              " or in descending order of frequency? "))
    if sortingOption == 1:
        for key in sorted(collection.keys()):
            print(key + ": " + str(collection[key]))
            labels.append(key)
            sizes.append(collection[key])
    else:
        collection = dict(sorted(collection.items(), key=lambda item: item[1]))  # sorts by value  in increasing order
        for key in reversed(collection.keys()):
            print(key + ": " + str(collection[key]))
            labels.append(key)
            sizes.append(collection[key])


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
    display_genre_count()

    while choice.lower() != 'yes' or choice.lower() != 'no':
        choice = input("Would you like to display the pie chart? (yes or no)\n")
        if choice.lower == 'no':
            displayChart = False

    if displayChart:
        display_chart()


if __name__ == '__main__':
    run()
