import sys
import xbmc
import xbmcgui
import xbmcplugin
from urlparse import parse_qsl

from packages.utils import utils
from packages.router import router as internalRouter
from packages.models import DirectoryItem as ItemModel
from packages.builders import ButtonBuilder
from packages.builders import InputBuilder
from packages.builders import ListItemBuilder
from packages.resolvers import toggle_resolver, resolver

_url = sys.argv[0]

_handle = int(sys.argv[1])

_router = internalRouter.Router()

_screen = xbmcplugin


# import web_pdb; web_pdb.set_trace()


class Item():
    def __init__(self):
        pass


def _transformQueryStringIntoDict(queryString):
    d = {}

    for i in queryString:
        d[i[0].replace('?', '')] = i[1]

    return d


def router():
    queryString = parse_qsl(sys.argv[2])
    d = _transformQueryStringIntoDict(queryString)
    action = d['action']

    if action == 'getDirectLink':
        url = d['url']
        tr = toggle_resolver.ToggleResolver(url)
        item = tr.buildItemDTO()
        listItem = xbmcgui.ListItem(path=item.video)
        listItem.setSubtitles(item.subtitles)
        xbmcplugin.setResolvedUrl(_handle, True, listItem)

    elif action == 'getAllEpisodesOfSeries':
        url = d['url']
        resolveAllEpisodesLocally(url)
        # resolveAllEpisodesAndShow(url)


def resolveAllEpisodesLocally(seriesURL):
    tr = toggle_resolver.SeriesResolver()
    episodes = tr.resolveSeriesToEpisoeds(seriesURL)
    _screen.setPluginCategory(_handle, 'Episodes')
    _screen.setContent(_handle, 'videos')
    for episode in episodes:
        tr = toggle_resolver.ToggleResolver(episode)
        _screen.addDirectoryItem(
            _handle, tr.getVideoURL(), tr.buildListItem(), False)
    _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    _screen.endOfDirectory(_handle)



def resolveAllEpisodesAndShow(url):
    episodesInfo = resolver.getAllEpisodesOfSeries(url)
    _screen.setPluginCategory(_handle, 'Episodes')
    _screen.setContent(_handle, 'videos')
    for episode in episodesInfo['episodes']:
        tr = toggle_resolver.ToggleResolver(episode['url'])
        _screen.addDirectoryItem(
            _handle, tr.getVideoURL(), tr.buildListItem(), False)
    _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    _screen.endOfDirectory(_handle)


def _print(content):
    xbmcgui.Dialog().ok('heading', content)


def retrieve(searchTerm):
    xbmcgui.Dialog().ok('heading', searchTerm)


def landing():
    allSeries = resolver.getAllSeries()
    _screen.setPluginCategory(_handle, 'All Series')
    _screen.setContent(_handle, 'videos')

    listItems = []

    for series in allSeries:
        listItem = xbmcgui.ListItem()
        listItem.setLabel(series['title'])
        # listItem.setArt({})
        listItem.setInfo(
            'video', {'title': series['title'], 'mediatype': 'video'})

        listItem.setArt({
            'thumb': series['imageURL'],
            'icon': series['imageURL'],
            'fanart': series['imageURL']
        })
        isFolder = True
        # needs to become a tuple (url, listItem, isFolder)
        url = '{}?&action=getAllEpisodesOfSeries&url={}'.format(
            _url, series['url'])
        listItems.append((url, listItem, isFolder))

    _screen.addDirectoryItems(_handle, listItems)
    _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    _screen.endOfDirectory(_handle)


def main():
    print("Main is hit")
    print("sys.argv", sys.argv)
    if sys.argv[2] != '':
        router()
    else:
        landing()


main()
