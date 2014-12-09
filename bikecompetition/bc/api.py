from bikecompetition.bc.models import (Competition,
                                       Competitor,
                                       CompetitorStats)
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.resources import ModelResource


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
        filtering = {"name": ALL}
        always_return_data = True

