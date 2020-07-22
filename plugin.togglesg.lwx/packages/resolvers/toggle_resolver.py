import requests
import xbmcgui
import re


class Item():
    ''' Item class used as DTO '''
    '''
        Current Properties:
            - name
            - single video url direct link
            - short title // varies from episode to episode
            - single picture url direct link
            - episode number
            - subtitle(s) // array

    '''

    def __init__(self):
        pass


class ToggleResolver():

    def __init__(self, link):
        self.referer = link
        self.mediaId = link.split('/')[-1]
        self.episodeResponse = None
        self.subtitlesResponse = None
        self.video = None
        self.getEpisodeResponse()
        # call self.buildItemDTO() to build item

    def getEpisodeResponse(self):
        headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Origin': 'https://www.mewatch.sg',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Referer': '{}'.format(self.referer),
            'Accept-Language': 'en-US,en;q=0.9',
        }

        params = (
            ('m', 'GetMediaInfo'),
        )

        data = '{"initObj":{"Platform":"Web","SiteGuid":"","DomainID":"0","UDID":"","ApiUser":"tvpapi_147","ApiPass":"11111","Locale":{"LocaleLanguage":"","LocaleCountry":"","LocaleDevice":"","LocaleUserState":"Unknown"}},"MediaID":"' + self.mediaId + '"}'

        response = requests.post(
            'https://tvpapi-as.ott.kaltura.com/v3_9/gateways/jsonpostgw.aspx', headers=headers, params=params, data=data)

        jsonResult = response.json()

        self.episodeResponse = jsonResult

        return jsonResult

    def getSubtitlesResponse(self):
        headers = {
            'authority': 'sub.toggle.sg',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'origin': 'https://www.mewatch.sg',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'referer': '{}'.format(self.referer),
            'accept-language': 'en-US,en;q=0.9',
        }

        params = (
            ('mediaId', self.mediaId),
        )

        jsonResult = []

        try:
            response = requests.get(
                'https://sub.toggle.sg/toggle_api/v1.0/apiService/getSubtitleFilesForMedia', headers=headers, params=params)

            jsonResult = response.json()

        except Exception:
            print('Error fetching subtitles, might be due to requesting too frequently.')


        self.subtitlesResponse = jsonResult

        return jsonResult

    def _getAllSubtitles(self):
        subtitlesResponse = self.getSubtitlesResponse()

        subtitles = []

        for subtitle in subtitlesResponse['subtitleFiles']:
            subtitles.append(subtitle['subtitleFileUrl'])
        return subtitles

    def buildItemDTO(self):
        '''
            Item class used as DTO

            Current Properties:
                - show name
                - single video url direct link
                - short title // varies from episode to episode
                - single picture url direct link
                - episode number
                - episode name
                - subtitle(s) // array

        '''

        showName = self._getNameOfShow()
        videoURL = self._getHighestQualityVideoFile()
        shortTitle = self._getShortTitle()
        imageURL = self._getHighestQualityPicture()
        epNo = self._getEpisodeNumber()
        epName = self._getEpisodeName()
        subtitles = self._getAllSubtitles()

        item = Item()
        item.video = videoURL
        item.videos = self._getAllVideoURLs()
        # item.shortTitle = shortTitle
        item.image = imageURL
        # item.epNo = epNo
        item.epName = epName
        item.subtitles = subtitles
        return item

    def buildListItem(self):
        ''' decided to use only 4 attributes
                1. name == listitem.setLabel(value) and listitem.setInfo({'title': value})
                2. image == listitem.setArt({'thumb':, 'icon', 'fanart'})
                3. description == listitem.setInfo({'plot': value})
                4. video == used in returning as tuple (url, listItem, isFolder)

            defaults:
                mediatype: video
                isplayable: true
        '''
        item = Item()
        item.name = u'EP{} - {}'.format(self._getEpisodeNumber(),
                                        self._getNameOfShow())
        item.image = self._getHighestQualityPicture()
        item.description = self._getDescription()
        item.video = self._getHighestQualityVideoFile()

        self.video = self._getHighestQualityVideoFile()

        listItem = xbmcgui.ListItem()
        listItem.setLabel(item.name)
        listItem.setInfo('video', {
            'title': item.name,
            'plot': item.description,
            'mediatype': 'video'
        })

        listItem.setArt({
            'thumb': item.image,
            'icon': item.image
        })

        listItem.setProperty('IsPlayable', 'true')
        listItem.setSubtitles(self._getAllSubtitles())

        return listItem

    def _getAllVideoURLs(self):
        files = []
        for file in self.episodeResponse['Files']:
            fileId = file['FileID']
            url = file['URL']
            duration = file['Duration']
            format = file['Format']
            language = file['Language']
            # most likely we only want url and format
            d = {
                'fileId': fileId,
                'url': url,
                'duration': duration,
                'format': format,
                'language': language
            }
            files.append(d)
        return files

        

    def getVideoURL(self):
        self.video = self._getHighestQualityVideoFile()
        return self.video

    def _getDescription(self):
        return self.episodeResponse['Description']

    def _getNameOfShow(self):
        return self.episodeResponse['MediaName']

    def _getAllVideoFiles(self):
        return self.episodeResponse['Files']

    def _getHighestQualityVideoFile(self):
        # have todo: fix formats, should display an array?

        FORMAT_TO_USE = 'HLS_Web_Clear'

        for file in self.episodeResponse['Files']:
            if file['Format'] == FORMAT_TO_USE:
                return file['URL']
        return self.episodeResponse['Files'][-1]['URL']

    def _getShortTitle(self):
        for meta in self.episodeResponse['Metas']:
            if meta['Key'] == "Short title":
                return meta['Value']

    def _getEpisodeName(self):
        for meta in self.episodeResponse['Metas']:
            if meta['Key'] == "Episode name":
                return meta['Value']

    def _getEpisodeNumber(self):
        for meta in self.episodeResponse['Metas']:
            if meta['Key'] == "Episode number":
                return meta['Value']

    def _getPictures(self):
        return self.episodeResponse['Pictures']

    def _getHighestQualityPicture(self):
        return self.episodeResponse['Pictures'][-1]['URL']

    def _mapFileToURL(self, file):
        return file['URL']


class SeriesResolver(object):
    def __init__(self):
        self.contentId = None
        self.navigationId = None
        self.seriesURL = None
        pass

    def resolveSeriesToEpisodes(self, seriesUrl):
        ''' main driver '''
        self.seriesURL = seriesUrl
        self.getIds()
        return self.getBlueprint()

    def getIds(self):
        r = requests.get(self.seriesURL)
        content = r.content
        r = r'\s(\d+), (\d+), isCatchup'
        match = re.search(r, content)
        contentId = match.group(1)
        navigationId = match.group(2)
        self.contentId = contentId
        self.navigationId = navigationId

    def getBlueprint(self):
        ''' returns all episodes urls in an array '''
        headers = {
            'Accept': '*/*',
            'Referer': self.seriesURL,
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        }

        params = (
            ('pageSize', '1000'),
            ('pageIndex', '0'),
            ('contentId', self.contentId),
            ('navigationId', self.navigationId),
            ('isCatchup', '1'),
        )

        response = requests.get(
            'https://tv.mewatch.sg/en/blueprint/servlet/toggle/paginate', headers=headers, params=params)
        content = response.content

        r = r'<a href=\"(https?.*ep\d+\/\d+)\"'
        matches = re.findall(r, content)
        # matches are all the episodes urls in an array, but contains duplicates
        normalized = list(set(matches))
        return normalized


class SeriesInfoResolver(object):
    def __init__(self):
        pass

    def resolveMetadata(self, seriesURL):
        arr = seriesURL.split('/')
        arr[-1] = 'info'
        seriesURL = '/'.join(arr)
        r = requests.get(seriesURL)
        content = r.content
        r = r'<img class=\"programinfo-item__banner\" src=\"(.*?)\" alt=\"(.*?)\">'
        match = re.search(r, content)
        imageURL = ''
        seriesTitle = arr[7] # default if fail to parse from regex
        try:
            imageURL = match.group(1)
            seriesTitle = match.group(2)
            imageURL = 'https://tv.mewatch.sg/' + imageURL
        except Exception as e:
            print('[ERROR] resolveMetadata() for {} failed.'.format(seriesURL))
        return {'image': imageURL, 'title': seriesTitle}
