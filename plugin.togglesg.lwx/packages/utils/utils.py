import re

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


def parseSeriesURLIntoReadableFormat(seriesURL = 'https://tv.mewatch.sg/en/shows/t/titoudao-inspired-by-the-true-story-of-a-wayang-star/episodes'):
    r = r'/.+/.+/(.*?)/episodes'
    match = re.search(r, seriesURL)
    name = match.group(1)
    name = ' '.join(name.split('-')).title()
    return name


def parseEpisodeURLIntoReadableFormat(episodeURL = 'https://www.mewatch.sg/en/series/titoudao-inspired-by-the-true-story-of-a-wayang-star/ep12/922732'):
    r = r'/series/(.*?)/(.*?)/'
    match = re.search(r, episodeURL)
    name = match.group(1)
    episode = match.group(2).upper()
    name = ' '.join(name.split('-')).title()
    return '{} - {}'.format(name, episode)