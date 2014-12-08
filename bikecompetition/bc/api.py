from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from bikecompetition.bc.models import (Competition,
                                       Competitor,
                                       CompetitorStats,
)


class CompetitionResource(ModelResource):
    class Meta:
        queryset = Competition.objects.all()
        authentication = Authentication()
        authorization = Authorization()


class CompetitorResource(ModelResource):
    class Meta:
        queryset = Competitor.objects.all()
        authentication = Authentication()
        authorization = Authorization()


class CompetitorStatsResource(ModelResource):
    class Meta:
        queryset = CompetitorStats.objects.all()
        authentication = Authentication()
        authorization = Authorization()
