# drop table bc_competitorstats cascade; drop table bc_competitor cascade; drop table bc_competition cascade; drop table bc_competition_competitors cascade; drop table tastypie_apiaccess; drop table tastypie_apikey; delete from django_migrations where app in ('bc', 'tastypie');
# insert into bc_competitor (id, name) values (1,'First')(2, 'Second'); insert into bc_competition (id, type, status) values (1, 1, 0);
#

from django.db import models
from django.utils.translation import ugettext_lazy as _i

# Create your models here.

COMPETITION_STATUS_PENDING = 0
COMPETITION_STATUS_STARTED = 1
COMPETITION_STATUS_FINISHED = 2
COMPETITION_STATUSES = (
    (COMPETITION_STATUS_PENDING, _i(u'Pending')),
    (COMPETITION_STATUS_STARTED, _i(u'Started')),
    (COMPETITION_STATUS_FINISHED, _i(u'Finished')),
)

COMPETITION_TYPE_TIME = 0
COMPETITION_TYPE_DISTANCE = 1
COMPETITION_TYPES = (
    (COMPETITION_TYPE_TIME, _i(u'Time Cpmpetition')),
    (COMPETITION_TYPE_DISTANCE, _i(u'Distance Cpmpetition')),
)

class Competitor(models.Model):
    name = models.CharField(max_length=30)


class CompetitionManager(models.Manager):
    def get_stats(self, competition_id):
        results = {}
        for competitor in self.get(id=competition_id).competitors.all():
            statistic = CompetitorStats.objects.filter(competitor_id=competitor.id, competition_id=competition_id).last()
            if statistic:
                results[competitor.id] = statistic.distance
        return results


class Competition(models.Model):
    competitors = models.ManyToManyField(Competitor)
    status = models.PositiveSmallIntegerField(choices=COMPETITION_STATUSES, default=COMPETITION_STATUS_PENDING)
    type = models.PositiveSmallIntegerField(choices=COMPETITION_TYPES, default=COMPETITION_TYPE_TIME)

    objects = CompetitionManager()


class CompetitorStats(models.Model):
    competitor = models.ForeignKey(Competitor)
    competition = models.ForeignKey(Competition)
    distance = models.PositiveIntegerField()


