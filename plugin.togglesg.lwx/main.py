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
from packages.resolvers import resolver


_handle = int(sys.argv[1])

_router = internalRouter.Router()

def _transformQueryStringIntoDict(queryString):
    d = {}

    for i in queryString:
        d[i[0].replace('?', '')] = i[1]

    return d


def router():
    queryString = parse_qsl(sys.argv[2])
    d = _transformQueryStringIntoDict(queryString)
    action = d['action']

    if action == 'search':
        getSearchInputValue()
    elif action == 'resolveVideoURL':
        retrieve(d['searchTerm'])
    elif action == 'resolveToSeries':
        listAllEpisodesOfSeries(d['URL'])

def listAllEpisodesOfSeries(url):
    episodes = resolver.resolveToEpisodesListings(url)
    # directly resolve all episodes URL to direct link like in previous version and populate



def _print(content):
    xbmcgui.Dialog().ok('heading', content)


def retrieve(searchTerm):
    xbmcgui.Dialog().ok('heading', searchTerm)


def getSearchInputValue():
    searchInputValue = InputBuilder.searchInput()
    searchResults = resolver.toggleSearch(searchInputValue)
    items = utils.parseSearchResultsList(searchResults['list'])
    xbmcplugin.setContent(_handle, 'videos')
    for item in items:
        di = ItemModel.DirectoryItem()
        di.setPropertiesFromItem(item)
        xbmcplugin.addDirectoryItem(_handle, di.action, di.toListItem(), False)
    xbmcplugin.endOfDirectory(_handle, updateListing = True)



def landing():
    xbmcplugin.setContent(_handle, 'videos')
    ButtonBuilder.searchButton()
    ButtonBuilder.lastSearchItemButton('Crimewatch')
    xbmcplugin.endOfDirectory(_handle, updateListing = True)



def main():
    print("Main is hit")
    print("sys.argv", sys.argv)
    if sys.argv[2] != '':
        router()
    else:
        landing()

main()