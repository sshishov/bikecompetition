from django.test import TestCase, Client

from bikecompetition.models import User

# Create your tests here.

class FakeClientTestCase(TestCase):

    def setUp(self):
        self.api_user = User.objects.get(name="FakeClient")

    def _client_post(self, url, **kwargs):
        client = Client()
        data = json.dumps(kwargs)
        return client.post(url, content_type='application/json', data=data)

    def test_start_client(self):
        print self.user
