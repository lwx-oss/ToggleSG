import xbmcgui

class ListItemBuilder():
    def __init__(self):
        self.item = None

    def buildListItemFromItem(self, item):
        listItem = xbmcgui.ListItem()
        listItem.setLabel(item.name)
        listItem.setInfo('video', {
            'title': item.name,
            'plot': item.description
        })

        listItem.setProperty('IsPlayable', 'true')
        
        return listItem