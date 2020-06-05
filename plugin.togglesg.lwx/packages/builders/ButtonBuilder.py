import sys
import xbmcplugin
from packages.models import DirectoryItem as ItemModel

def searchButton():
    _handle = int(sys.argv[1])
    directoryItem = ItemModel.DirectoryItem()
    directoryItem.label = 'Search'
    directoryItem.type = 'video'
    directoryItem.title = 'Search'
    directoryItem.plot = 'Search for a show'
    directoryItem.setAction('search')
    xbmcplugin.addDirectoryItem(_handle, directoryItem.action, directoryItem.toListItem(), False)


def lastSearchItemButton(searchTerm):
    _handle = int(sys.argv[1])
    directoryItem = ItemModel.DirectoryItem()
    directoryItem.label = 'Previously searched: {}'.format(searchTerm)
    directoryItem.type = 'video'
    directoryItem.title = searchTerm
    directoryItem.plot = searchTerm
    directoryItem.setAction('retrieve&searchTerm=Crimewatch')
    xbmcplugin.addDirectoryItem(_handle, directoryItem.action, directoryItem.toListItem(), False)