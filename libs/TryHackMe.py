from lxml import html

from libs.ChallengePlatform import ChallengePlatform, UserInfo

import requests
import json

THM_WEBSITE  = 'https://tryhackme.com'

class TryHackMe(ChallengePlatform):

   def __init__(self, login, password, username):
      self._login = login
      self._password = password
      self._username = username
      self._userInfo = None
      
      self.session = requests.Session()
      self.login()

   def login(self):
      response = self.session.get(f'{ THM_WEBSITE }/login')
      tree = html.fromstring(response.text)
      csrf_token = tree.xpath('//input[@name="_csrf"]/@value')
      response = self.session.post(f'{ THM_WEBSITE }/login', data = {'email': self._login, 'password': self._password, '_csrf': csrf_token[0]})

   def update(self) -> bool:
      infos = self.fetchInfos()

      # If fetched data is different from current
      if infos != self._userInfo:
         self._userInfo = infos

         return True

      return False

   def fetchInfos(self):
      return UserInfo(
         self.getUserRank(), 
         self.getTotalUsers(), 
         self.getUserScore(), 
         None
      )

   def yieldInfos(self) -> UserInfo:
      return self._userInfos

   def getTotalUsers(self):
      response = self.session.get(f'{ THM_WEBSITE }/api/getstats')
      globalStats = json.loads(response.text)

      return str( globalStats['totalUsers'] )

   def getUserRank(self):
      response = self.session.get(f'{ THM_WEBSITE }/api/usersRank/{ self._username }')
      userStats =  json.loads(response.text)

      return str(userStats['userRank'])

   def getUserScore(self):
      response = self.session.get(f'{ THM_WEBSITE }/api/user/{ self._username }')
      userScore =  json.loads(response.text)

      return str(userScore['points'])

   def pprint(self):
      return 'TryHackMe rank : {}/{} ({}pts)'.format(
            self._userInfo.rank,
            self._userInfo.nrank,
            self._userInfo.score
        )