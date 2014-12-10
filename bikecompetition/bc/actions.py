import json
import threading

from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from bikecompetition.bc import models as bcModels
from bikecompetition.fakeclient import FakeClient


@csrf_exempt
def get_competitor(request):
    request_json = json.loads(request.body)
    name = request_json['name']
    competitor, created = bcModels.Competitor.objects.get_or_create(name=name)
    response = {'id': competitor.id, 'name': competitor.name}
    return HttpResponse(content=json.dumps(response), content_type="application/json", status=201 if created else 200)


@csrf_exempt
def get_competition(request):
    request_json = json.loads(request.body)
    competition_type = request_json['competition_type']
    competitor = request_json['competitor']
    fake = request_json['fake']
    if int(fake):
        t = threading.Thread(target=FakeClient(id=competitor).start).start()
        return HttpResponse(content=json.dumps({}), content_type="application/json", status=200)

    competition = bcModels.Competition.objects.filter(type=competition_type).last()
    if competition and any((competitor_status.status != bcModels.COMPETITION_STATUS_PENDING for competitor_status in \
                            bcModels.CompetitorStatus.objects.filter(
                                    competition_id=competition.id
                            )
    )):
        competition = None
    if not competition:
        competition = bcModels.Competition.objects.create(type=competition_type)
    competitor_status = bcModels.CompetitorStatus.objects.filter(
        competitor_id=competitor,
        competition_id=competition
    )
    if not competitor_status:
        competitor_status = bcModels.CompetitorStatus.objects.create(
            competitor_id=competitor,
            competition_id=competition.id,
            status=bcModels.COMPETITION_STATUS_PENDING
        )
    else:
        competitor_status = competitor_status.last()
    resp_dict = {
        'competition_id': competition.id,
        'competition_type': competition.type,
        'competition_status': competitor_status.status,
        'competitor_count': competition.competitors.all().count(),
    }
    return HttpResponse(content=json.dumps(resp_dict), content_type="application/json", status=201)


@csrf_exempt
def update_competition(request):
    request_json = json.loads(request.body)
    competition = request_json['competition']
    competitor = request_json['competitor']
    distance = request_json['distance']
    timestamp = request_json['timestamp']
    competitor = bcModels.Competitor.objects.get(id=competitor)
    competition = bcModels.Competition.objects.get(id=competition)
    competition.competitors.add(competitor)
    competitor_stats = {}
    competitor_times = {}
    competitor_status = bcModels.CompetitorStatus.objects.get(
        competitor_id=competitor,
        competition_id=competition
    )
    if competitor_status.status == bcModels.COMPETITION_STATUS_PENDING and \
                    competition.competitors.all().count() > 1:
        competitor_status.status = bcModels.COMPETITION_STATUS_STARTED
        competitor_status.save()
    elif competitor_status.status == bcModels.COMPETITION_STATUS_STARTED:
        bcModels.CompetitorStats.objects.create(competition_id=competition.id,
                                                competitor_id=competitor.id,
                                                distance=distance,
                                                timestamp=datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S.%f'))
        competitor_stats, competitor_times = bcModels.Competition.objects.get_stats(competition.id)
        if (competition.type == bcModels.COMPETITION_TYPE_DISTANCE and \
                    any(((distance > 50) for distance in competitor_stats.itervalues()))) or \
                (competition.type == bcModels.COMPETITION_TYPE_TIME and \
                         any(((timedelta > 30) for timedelta in competitor_times.itervalues()))):
            bcModels.CompetitorStatus.objects.filter(
                competition_id=competition
            ).update(status=bcModels.COMPETITION_STATUS_FINISHED)

    elif competitor_status.status == bcModels.COMPETITION_STATUS_FINISHED:
        competitor_stats, competitor_times = bcModels.Competition.objects.get_stats(competition.id)
    resp_dict = {
        'competition_id': competition.id,
        'competition_status': competitor_status.status,
        'competition_stats': competitor_stats,
        'competition_times': competitor_times
    }
    return HttpResponse(content=json.dumps(resp_dict), content_type="application/json", status=201)


@csrf_exempt
def finish_competition(request):
    competition_id = request.POST.get('competition_id')
    competition = bcModels.Competition.objects.get(competition_id)
    competitor_status = bcModels.CompetitorStatus.objects.get(
        competitor_id=competitor,
        competition_id=competition
    )
    resp_dict = {
        'competition_id': competition.id,
        'competition_status': competition.status
    }
    competitor_status = bcModels.COMPETITION_STATUS_FINISHED
    competitor_status.save()
    return HttpResponse(content=json.dumps(resp_dict), content_type="application/json", status=201)