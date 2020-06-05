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
    _router.setRoutes({
        'search': getSearchInputValue
    })
    _router.route(d['action'])



def getSearchInputValue():
    searchInputValue = InputBuilder.searchInput()
    print(searchInputValue)


def main():
    if sys.argv[2] != '':
        router()
    else:
        ButtonBuilder.searchButton()


main()