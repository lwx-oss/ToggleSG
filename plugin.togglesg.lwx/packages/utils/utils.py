class Item():
    def __init__(self):
        pass

def parseSearchResultsList(searchResults):
    items = []
    for i in searchResults:
        item = Item()
        item.label = i['FullMediaName']
        item.title = item.label
        item.type = 'video'
        item.action = i['FullUrl']
        item.image = 'https://www.mewatch.sg' + i['PicURL']
        plot = 'Language: {}'.format(i['Language'])
        item.plot = plot
        items.append(item)

    return items