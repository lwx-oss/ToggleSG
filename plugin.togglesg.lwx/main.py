import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from urlparse import parse_qsl

from packages.utils import utils
from packages.router import router as internalRouter
from packages.models import DirectoryItem as ItemModel
from packages.builders import ButtonBuilder
from packages.builders import InputBuilder
from packages.builders import ListItemBuilder
from packages.resolvers import toggle_resolver, resolver
from packages.constants import actions_constants

_url = sys.argv[0]

_handle = int(sys.argv[1])

_router = internalRouter.Router()

_screen = xbmcplugin

_settings = xbmcaddon.Addon()


def _getSetting(id):
    return _settings.getSetting(id)

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

    if action == actions_constants.GET_DIRECT_LINK:
        url = d['url']
        tr = toggle_resolver.ToggleResolver(url)
        item = tr.buildItemDTO()
        listItem = xbmcgui.ListItem(path=item.video)
        listItem.setSubtitles(item.subtitles)
        xbmcplugin.setResolvedUrl(_handle, True, listItem)

    elif action == actions_constants.GET_ALL_EPISODES_OF_SERIES:
        url = d['url']
        if isLazyLoading():
            lazilyResolveAllEpisodesLocally(url)
        else:
            eagerlyResolveAllEpisodesLocally(url)
        # resolveAllEpisodesAndShow(url)
    elif action == actions_constants.GET_ALL_VIDEO_LINKS:
        url = d['url']
        displayAllVideoLinksForSelection(url)
        


def displayAllVideoLinksForSelection(url):
    _screen.setPluginCategory(_handle, 'Select Video Format')
    _screen.setContent(_handle, 'videos')

    tr = toggle_resolver.ToggleResolver(url)
    item = tr.buildItemDTO()

    listItems = []

    for video in item.videos:
            # needs to be a tuple (url, listItem, isFolder)
        listItem = xbmcgui.ListItem()
        listItem.setLabel(video['format'])
        listItem.setInfo('video', {'title': video['format'], 'mediatype': 'video'})
        isFolder = False # we want to play the actual video link
        listItem.setProperty('IsPlayable', 'true')
        listItem.setSubtitles(item.subtitles)
        listItems.append((video['url'], listItem, isFolder))
    
    _screen.addDirectoryItems(_handle, listItems)
    _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    _screen.endOfDirectory(_handle)


def lazilyResolveAllEpisodesLocally(seriesURL):
    tr = toggle_resolver.SeriesResolver()
    episodes = tr.resolveSeriesToEpisodes(seriesURL)
    _screen.setPluginCategory(_handle, 'Episodes')
    _screen.setContent(_handle, 'videos')
    for episode in episodes:
        episodeName = utils.parseEpisodeURLIntoReadableFormat(episode)
        listItem = xbmcgui.ListItem()
        listItem.setLabel(episodeName)
        listItem.setInfo('video', {
            'title': episodeName,
            'plot': episodeName,
            'mediatype': 'video'
        })

        if isAutoSelectVideoFormat():
            listItem.setProperty('IsPlayable', 'true')
            _screen.addDirectoryItem(
                _handle, '{}?&action={}&url={}'.format(_url, actions_constants.GET_DIRECT_LINK, episode), listItem, False)
        else:
            listItem.setProperty('IsPlayable', 'false')
            _screen.addDirectoryItem(
                _handle, '{}?&action={}&url={}'.format(_url, actions_constants.GET_ALL_VIDEO_LINKS, episode), listItem, True)
    _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    _screen.endOfDirectory(_handle)


def eagerlyResolveAllEpisodesLocally(seriesURL):
    tr = toggle_resolver.SeriesResolver()
    episodes = tr.resolveSeriesToEpisodes(seriesURL)
    _screen.setPluginCategory(_handle, 'Episodes')
    _screen.setContent(_handle, 'videos')
    for episode in episodes:
        tr = toggle_resolver.ToggleResolver(episode)
        if isAutoSelectVideoFormat():
            _screen.addDirectoryItem(
                _handle, tr.getVideoURL(), tr.buildListItem(), False)
        else:
            _screen.addDirectoryItem(
                _handle, '{}?&action={}&url={}'.format(_url, actions_constants.GET_ALL_VIDEO_LINKS, episode), tr.buildListItem(), True)
    _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    _screen.endOfDirectory(_handle)


def resolveAllEpisodesAndShow(url):
    # episodesInfo = resolver.getAllEpisodesOfSeries(url)
    # _screen.setPluginCategory(_handle, 'Episodes')
    # _screen.setContent(_handle, 'videos')
    # for episode in episodesInfo['episodes']:
    #     tr = toggle_resolver.ToggleResolver(episode['url'])
    #     _screen.addDirectoryItem(
    #         _handle, tr.getVideoURL(), tr.buildListItem(), False)
    # _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # _screen.endOfDirectory(_handle)
    pass


def _print(content):
    xbmcgui.Dialog().ok('heading', content)


def retrieve(searchTerm):
    xbmcgui.Dialog().ok('heading', searchTerm)


def landingEager():
    allSeries = resolver.getAllSeries()
    _screen.setPluginCategory(_handle, 'All Series')
    _screen.setContent(_handle, 'videos')

    listItems = []

    for series in allSeries:
        tr = toggle_resolver.SeriesInfoResolver()
        metadata = tr.resolveMetadata(series['url'])
        imageURL = metadata['image']
        listItem = xbmcgui.ListItem()
        listItem.setLabel(metadata['title'])
        # listItem.setArt({})
        listItem.setInfo(
            'video', {'title': metadata['title'], 'mediatype': 'video'})

        listItem.setArt({
            'thumb': imageURL,
            'icon': imageURL,
            'fanart': imageURL
        })
        isFolder = True
        # needs to become a tuple (url, listItem, isFolder)
        url = '{}?&action={}&url={}'.format(
            _url, actions_constants.GET_ALL_EPISODES_OF_SERIES, series['url'])
        listItems.append((url, listItem, isFolder))

    _screen.addDirectoryItems(_handle, listItems)
    _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    _screen.endOfDirectory(_handle)


def landingLazy():
    allSeries = resolver.getAllSeries()
    allSeries = [i['url'] for i in allSeries]
    _screen.setPluginCategory(_handle, 'All Series')
    _screen.setContent(_handle, 'videos')

    listItems = []

    for series in allSeries:
        seriesName = utils.parseSeriesURLIntoReadableFormat(series)
        listItem = xbmcgui.ListItem()
        listItem.setLabel(seriesName)
        listItem.setInfo(
            'video', {'title': seriesName, 'mediatype': 'video'})

        isFolder = True
        # needs to become a tuple (url, listItem, isFolder)
        url = '{}?&action=getAllEpisodesOfSeries&url={}'.format(
            _url, series)
        listItems.append((url, listItem, isFolder))

    _screen.addDirectoryItems(_handle, listItems)
    _screen.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    _screen.endOfDirectory(_handle)


def isLazyLoading():
    return _getSetting('lazy-loading') == 'true'

def isAutoSelectVideoFormat():
    return _getSetting('auto-select-video-format') == 'true'


def main():
    print("Main is hit")
    print("sys.argv", sys.argv)
    if sys.argv[2] != '':
        router()
    else:
        if isLazyLoading():
            landingLazy()
        else:
            landingEager()


main()
