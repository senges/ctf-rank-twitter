from urllib import parse
from lxml import html

from libs.ChallengePlatform import ChallengePlatform, UserInfo

import requests
import time

# Delay between API requests
# to avoid HTTP error 429 (Too Many Requests)
# 500ms looks to be a good compromize

DELAY = 0.5

RM_URL_ROOT  = 'https://www.root-me.org'

# Shortened URL encoding function
encode = parse.urlencode

class RootMe(ChallengePlatform):

    def __init__(self, login):
        self._login = login
        self._userInfo = None

    # -- Unified api compliant get method
    def get(self, url) -> requests.Response:
        time.sleep(DELAY)

        response = requests.get( url )

        if not response.ok:
            self.panic(f'HTTP Error on ({ url })[{ response.status_code }]')
        
        return response

    # -- Update client state
    def update(self) -> bool:
        infos = self.fetchInfos()

        # If fetched data is different from current
        if infos != self._userInfo:
            self._userInfo = infos

            return True

        return False

    # -- Fetch last user data
    def fetchInfos(self) -> UserInfo:

        url = f'{ RM_URL_ROOT }/{ self._login }?inc=score&lang=fr'

        tree = html.fromstring( self.get( url ).text )
        score = tree.xpath('//span[contains(@class, "txxl") ]/span[@class = "gris"]').pop()

        rank = score.getparent().text.strip()
        nrank = score.text[1:]

        challenges = tree.xpath('//span[contains(@class, "txxl") ]/span[@class = "gris tl"]').pop()
        score = challenges.getparent().text.strip().split('Points')[0]

        return UserInfo( rank, nrank, score, None )

    # -- Return local user data
    def yieldInfos(self) -> UserInfo:
        return self._userInfo

    # -- Pretty print
    def pprint(self):
        return 'RootMe rank : {}/{} ({}pts)'.format(
            self._userInfo.rank,
            self._userInfo.nrank,
            self._userInfo.score
        )
