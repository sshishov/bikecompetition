import json
import os
import requests
import sys
import time
import random

from datetime import datetime

HOST = 'localhost'
PORT = 8001
DEBUG = True

def log_debug(**kwargs):
    if DEBUG:
        for key, value in kwargs.iteritems():
            print '{}: {}'.format(key, value)

class FakeClient(object):

    def __init__(self):
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def _get(self, url, **params):
        return requests.get(url, params=params, headers=self.headers)

    def _post(self, url, **data):
        return requests.post(url, data=json.dumps(data), headers=self.headers)

    def get_competitor(self):
        log_debug(progress='Fetching competitor')
        competitor = self._get('http://{}:{}/api/bc/competitor'.format(HOST, PORT), name=self.name)
        print competitor
        competitor = competitor.json()
        print competitor
        competitor = competitor['objects']
        print competitor
        if not competitor:
            log_debug(progress='Creating competitor')
            competitor = self._post('http://{}:{}/api/bc/competitor/'.format(HOST, PORT), name=self.name).json()
        else:
            competitor = competitor[0]
        return competitor['id']

    def get_competition(self, **kwargs):
        log_debug(progress='Fetching competition')
        competition = self._post('http://{}:{}/api/action/get_competition/'.format(HOST, PORT), **kwargs)
        return competition

    def update_competition(self, **kwargs):
        log_debug(progress='Updating competition')
        status = self._post('http://{}:{}/api/action/update_competition/'.format(HOST, PORT), **kwargs)
        return status

    def finish_competition(self):
        log_debug(progress='Finishing competition')
        status = self._post(
            'http://{}:{}/api/action/finish_competition/'.format(HOST, PORT),
            competition=competition, competitor=competitor, distance=0)
        return status

    def start(self, args):
        self.name = args[0] if args else 'FakeClient'
        competitor = self.get_competitor()
        log_debug(competitor=competitor)
        competition = self.get_competition(competitor=competitor,
                                           competition_type=1).json()['competition_id']
        log_debug(competition=competition)
        status = self.update_competition(competitor=competitor,
                                         competition=competition,
                                         distance=random.randint(0,9),
                                         timestamp=datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S.%f')).json()
        log_debug(status=status)
        distance = 0
        while status['competition_status'] == 0:
            log_debug(substatus="pending")
            time.sleep(0.5)
            distance += random.randint(0, 9)
            status = self.update_competition(competitor=competitor,
                                             competition=competition,
                                             distance=distance,
                                             timestamp=datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S.%f')).json()
            log_debug(distance=distance, status=status)
        log_debug(progress="Competition started")
        distance = 0
        while status['competition_status'] == 1:
            log_debug(substatus="started")
            time.sleep(0.5)
            distance += random.randint(0, 9)
            status = self.update_competition(competitor=competitor,
                                             competition=competition,
                                             distance=distance,
                                             timestamp=datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S.%f')).json()
            log_debug(distance=distance, status=status)
        log_debug(progress="Competition finished")


if __name__ == '__main__':
    fakeclient = FakeClient()
    fakeclient.start(sys.argv[1:])
