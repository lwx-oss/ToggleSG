import requests
import re


def getSeriesURL(url):
    r = requests.get(url)
    content = r.content

    pattern = r'data-series-canonical=\"(.*?)\"'

    match = re.search(pattern, content)

    seriesURL = match.group(1)

    return seriesURL


def getAllEpisodesInSeries(url):
    r = requests.get(url)
    content = r.content

    pattern = r'href=\"(https?.*ep\d+/\d+)\"'

    match = re.findall(pattern, content)

    allEpisodes = list(set(match))

    return allEpisodes


def getBlueprint(url):
    r = requests.get(url)
    content = r.content

    pattern = r'\s(\d+), (\d+), isCatchup'

    match = re.search(pattern, content)

    contentId = match.group(1)
    navigationId = match.group(2)

    return _buildBlueprintURL(contentId, navigationId)


def _buildBlueprintURL(contentId, navigationId):
    url = 'https://tv.mewatch.sg/en/blueprint/servlet/toggle/paginate?pageSize=1000&pageIndex=0&contentId={}&navigationId={}&isCatchup=1'.format(contentId, navigationId)
    return url


def toggleSearch(searchTerm, pageIndex = 0):
    cookies = {
        'UID': '614f5c0a-b62a-490d-80c1-878ce36f2695',
        'MeID_Seg': 'none',
        'adtechTargetingKeys': 'none',
        'volumeControl_volumeValue': '0',
        'visid_incap_2170514': 'Y9jWDjNKQP2NvukX40SZBxKG2F4AAAAAQUIPAAAAAABER9uhAtKV+eTiXLhY/EXL',
        'incap_ses_168_2170514': 'AmLgBhCS9i8hIjkKTdtUAhOG2F4AAAAABJoJCkf3QnShM1hMJEDCMw==',
        'incap_ses_990_2170514': 'NNocO3rHIG2T0pSMwy+9DRSG2F4AAAAAoD92B8Tml4Yh5WnmEyAwBQ==',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.mewatch.sg/en/search?q={}&section=video'.format(searchTerm),
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = (
        ('text', '{}'.format(searchTerm)),
        ('mediaType', 'Episode'),
        ('sortBy', ''),
        ('sortDirection', ''),
        ('pageIndex', '{}'.format(pageIndex)),
        ('tgPage', '5007044'),
        ('filterList', ''),
    )

    response = requests.get('https://www.mewatch.sg/en/blueprint/servlet/togglev3/search', headers=headers, params=params, cookies=cookies)

    return response.json()

def resolveToEpisodesListings(url):
    seriesUrl = getSeriesURL(url)
    blueprint = getBlueprint(seriesUrl)
    return getAllEpisodesInSeries(blueprint)