import requests

def getAllSeries():
    url = 'https://us-central1-togglesg.cloudfunctions.net/toggle'
    r = requests.get(url)
    content = r.json()
    content = content['shows']
    return content


# def getAllEpisodesOfSeries(seriesURL):
#     url = 'https://us-central1-togglesg.cloudfunctions.net/toggle?showURL={}'.format(seriesURL)
#     r = requests.get(url)
#     # will change to array of objects, right now is array of links
#     episodes = r.json()
#     return episodes