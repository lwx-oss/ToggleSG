import xbmcgui
import sys


class DirectoryItem():
    ''' 
        ListItem Properties:
        setLabel(str)
        setInfo(type:str, infoLabels:dict)
            - e.g.:
                setInfo('video', {
                    'title': 'Title',
                    'plot': 'A bunch of words that will appear on the left side of the screen'
                })
    '''

    def __init__(self):
        ''' 
            label:string
            type:string (video|music|pictures|game)
            title:string
            plot: string
        '''
        self.label = None
        self.type = 'video' #set video as default
        self.title = None
        self.plot = None
        self.action = None
        self.image = None

    def setPropertiesFromItem(self, item):
        ''' use Item() to populate properties' values '''
        self.label = item.label
        self.title = item.title
        self.plot = item.plot
        if item.type:
            self.type = item.type

        if item.image:
            self.image = item.image
        
        self.setAction("resolveToSeries&URL=" + item.action)

    
    def setURLAction(self, action):
        self.action = action


    def setAction(self, action):
        self.action = "{}?&action={}".format(sys.argv[0], action)


    def _isValidProperties(self):
        return not (self.label is None or self.type is None or self.title is None or self.plot is None or self.action is None)

    def toListItem(self):
        if not self._isValidProperties():
            print('Directory Item Properties invalid, refusing to build list item')
            return

        listItem = xbmcgui.ListItem()
        listItem.setLabel(self.label)
        listItem.setInfo(self.type, {
            'title': self.title,
            'plot': self.plot
        })

        if self.image:
            listItem.setArt({
                'thumb': self.image
            })
        
        return listItem
