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
        print json.dumps(kwargs)


class FakeClient(object):
    def __init__(self):
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

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

    def start(self, args):
        name = args[0] if args else 'FakeClient'
        competitor = self.get_competitor(name=name)['id']
        log_debug(competitor=competitor)
        competition = self.get_competition(competitor=competitor,
                                           competition_type=1)['competition_id']
        log_debug(competition=competition)
        status = self.update_competition(competitor=competitor,
                                         competition=competition,
                                         distance=random.randint(0, 9),
                                         timestamp=datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S.%f'))
        log_debug(status=status)
        distance = 0
        while True:
            log_debug(substatus="updating")
            time.sleep(0.5)
            distance += random.randint(0, 9)
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


if __name__ == '__main__':
    fakeclient = FakeClient()
    fakeclient.start(sys.argv[1:])
