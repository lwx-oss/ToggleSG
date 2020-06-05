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


_handle = int(sys.argv[1])

_router = internalRouter.Router()

def _transformQueryStringIntoDict(queryString):
    d = {}

    for i in queryString:
        d[i[0]] = i[1]

    return d


def router():
    queryString = parse_qsl(sys.argv[2])
    d = _transformQueryStringIntoDict(queryString)

    action = d['action']

    if action == 'search':
        getSearchInputValue()
    elif action == 'retrieve':
        retrieve(d['searchTerm'])


def retrieve(searchTerm):
    xbmcgui.Dialog().ok('heading', searchTerm)


def getSearchInputValue():
    searchInputValue = InputBuilder.searchInput()
    print(searchInputValue)


def landing():
    xbmcplugin.setContent(_handle, 'videos')
    ButtonBuilder.searchButton()
    ButtonBuilder.lastSearchItemButton('Crimewatch')
    xbmcplugin.endOfDirectory(_handle)



def main():
    if sys.argv[2] != '':
        router()
    else:
        landing()

main()