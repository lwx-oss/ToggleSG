import requests

def getAllSeries():
    url = 'http://localhost:5000'
    r = requests.get(url)
    content = r.json()
    content = content['shows']
    return content


def getAllEpisodesOfSeries(seriesURL):
    url = 'http://localhost:5000/show?showURL={}'.format(seriesURL)
    r = requests.get(url)
    # will change to array of objects, right now is array of links
    episodes = r.json()
    return episodes