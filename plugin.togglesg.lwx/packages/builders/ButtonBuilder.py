import sys
import xbmcplugin
from packages.models import DirectoryItem as ItemModel

def searchButton():
    _handle = int(sys.argv[1])
    directoryItem = ItemModel.DirectoryItem()
    directoryItem.label = 'Label'
    directoryItem.type = 'video'
    directoryItem.title = 'Title'
    directoryItem.plot = 'Some plot'
    directoryItem.setAction('search')

    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.addDirectoryItem(_handle, directoryItem.action, directoryItem.toListItem(), False)
    xbmcplugin.endOfDirectory(_handle)