import json
import requests
import time
import random

from datetime import datetime
from optparse import OptionParser

HOST = 'localhost'
PORT = 8001
DEBUG = True


def log_debug(**kwargs):
    if DEBUG:
        print json.dumps(kwargs)

def get_max_key(d):
     v=list(d.values())
     return list(d.keys())[v.index(max(v))]

class FakeClient(object):
    def __init__(self, id=None, name=None, competition_type=None, competition_limit=None):
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.id = id
        self.name = name
        self.competition_type = competition_type
        self.competition_limit = competition_limit

    def _get(self, url, **params):
        return requests.get(url, params=params, headers=self.headers)

    def _post(self, url, **data):
        return requests.post(url, data=json.dumps(data), headers=self.headers)

    def get_competitor(self, **kwargs):
        log_debug(progress='Creating/getting competitor')
        competitor = self._post('http://{}:{}/api/action/get_competitor/'.format(HOST, PORT), **kwargs)
        return competitor.json()

    def get_competition(self, **kwargs):
        log_debug(progress='Fetching competition')
        competition = self._post('http://{}:{}/api/action/get_competition/'.format(HOST, PORT), **kwargs)
        return competition.json()

    def update_competition(self, **kwargs):
        log_debug(progress='Updating competition')
        status = self._post('http://{}:{}/api/action/update_competition/'.format(HOST, PORT), **kwargs)
        return status.json()

    def finish_competition(self):
        log_debug(progress='Finishing competition')
        status = self._post(
            'http://{}:{}/api/action/finish_competition/'.format(HOST, PORT),
            competition=competition, competitor=competitor, distance=0)
        return status.json()

    def start(self):
        if self.id:
            competitor = self.id
        else:
            competitor = self.get_competitor(name=self.name)['id']
        log_debug(competitor=competitor)
        competition = self.get_competition(competitor=competitor,
                                           competition_type=self.competition_type,
                                           competition_limit=self.competition_limit,
                                           fake=0)['competition_id']
        log_debug(competition=competition)
        status = self.update_competition(competitor=competitor,
                                         competition=competition,
                                         distance=random.randint(1, 10),
                                         timestamp=datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S.%f'))
        log_debug(status=status)
        distance = 0
        while True:
            log_debug(substatus="updating")
            time.sleep(1)
            distance += random.randint(1, 10)
            status_before = status['competition_status']
            status = self.update_competition(competitor=competitor,
                                             competition=competition,
                                             distance=distance,
                                             timestamp=datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S.%f'))

            if status_before == 0 and status['competition_status'] == 1:
                distance = 0
            log_debug(status=status)
            if status['competition_status'] == 2:
                break

        if status['competition_stats']:
            winner = get_max_key(status['competition_stats'])
            if int(competitor) == int(winner):
                print "YOU ARE THE WINNER!"
            else:
                print "YOU ARE THE LOOSER!"
        else:
            print "COMPETITION FINISHED WITHOUT RESULTS!"
