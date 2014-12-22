import json
import threading

from datetime import datetime
from django.core.management import call_command
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bikecompetition.bc import models as bcModels


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
    competition_type = request_json.get('competition_type') or bcModels.COMPETITION_TYPE_TIME
    competitor = request_json['competitor']
    competition_limit = request_json.get('competition_limit') or \
                                         bcModels.DEFAULT_LIMIT_TIME \
                                             if competition_type == bcModels.COMPETITION_TYPE_TIME \
                                             else bcModels.DEFAULT_LIMIT_DISTANCE
    fake = request_json['fake']
    if int(fake):
        threading.Thread(target=call_command, args=['fakeclient'], kwargs=dict(competitor_id=competitor, competition_type=competition_type, competition_limit=competition_limit)).start()
        return HttpResponse(content=json.dumps({}), content_type="application/json", status=200)

    competition = bcModels.Competition.objects.filter(type=competition_type).last()
    if competition and any((competitor_status.status != bcModels.COMPETITION_STATUS_PENDING for competitor_status in \
                            bcModels.CompetitorStatus.objects.filter(
                                    competition_id=competition.id
                            )
    )):
        competition = None
    if not competition:
        competition = bcModels.Competition.objects.create(type=competition_type, limit=competition_limit)
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
        'competition_type': competition.type,
        'competitor_limit': competition.limit,
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
                    any(((distance > competition.limit) for distance in competitor_stats.itervalues()))) or \
                (competition.type == bcModels.COMPETITION_TYPE_TIME and \
                         any(((timedelta > competition.limit) for timedelta in competitor_times.itervalues()))):
            bcModels.CompetitorStatus.objects.filter(
                competition_id=competition
            ).update(status=bcModels.COMPETITION_STATUS_FINISHED)

    elif competitor_status.status == bcModels.COMPETITION_STATUS_FINISHED:
        competitor_stats, competitor_times = bcModels.Competition.objects.get_stats(competition.id)
    resp_dict = {
        'competition_id': competition.id,
        'competition_status': competitor_status.status,
        'competition_stats': competitor_stats,
        'competition_times': competitor_times,
        'competitor_count': competition.competitors.all().count(),
        'competition_type': competition.type,
        'competition_limit': competition.limit,
    }
    return HttpResponse(content=json.dumps(resp_dict), content_type="application/json", status=201)


@csrf_exempt
def finish_competition(request):
    request_json = json.loads(request.body)
    competition = request_json['competition']
    competitor = request_json['competitor']
    competitor_status = bcModels.CompetitorStatus.objects.get(
        competitor_id=competitor,
        competition_id=competition
    )
    competitor_status.status = bcModels.COMPETITION_STATUS_FINISHED
    competitor_status.save()
    competitor_stats, competitor_times = bcModels.Competition.objects.get_stats(competition)
    resp_dict = {
        'competition_id': competition,
        'competitor_id': competitor,
        'competition_status': competitor_status.status,
        'competition_stats': competitor_stats,
        'competition_times': competitor_times,
        'competitor_count': competition.competitors.all().count(),
        'competition_type': competition.type,
        'competition_limit': competition.limit,
    }
    return HttpResponse(content=json.dumps(resp_dict), content_type="application/json", status=200)