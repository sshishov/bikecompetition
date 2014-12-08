from tastypie.api import Api
from django.conf.urls import patterns, include, url
from bikecompetition.bc import api, actions

bc_api = Api(api_name='bc')
bc_api.register(api.CompetitionResource())
bc_api.register(api.CompetitorResource())
bc_api.register(api.CompetitorStatsResource())

urlpatterns = patterns('',
    url(r'^api/', include(bc_api.urls)),
    url(r'^api/action/get_competition/', actions.get_competition),
    url(r'^api/action/update_competition/', actions.update_competition),
    url(r'^api/action/stop_competition/', actions.stop_competition),
    url(r'^api/bc/doc/',
        include('tastypie_swagger.urls', namespace='tastypie_swagger')),
)
