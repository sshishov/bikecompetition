import json

from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from bikecompetition.bc import models as bcModels

@csrf_exempt
def get_competition(request):
    competition_type = request.POST.get('competition_type')
    competition = bcModels.Competition.objects.filter(type=competition_type, status=bcModels.COMPETITION_STATUS_PENDING).last()
    if not competition:
        competition = bcModels.Competition.objects.create(type=competition_type, status=bcModels.COMPETITION_STATUS_PENDING)
    resp_dict = {
        'competition_id':  competition.id,
        'competition_type': competition.type,
        'competition_status': competition.status,
        'competitor_count': competition.competitors.all().count(),
    }
    return HttpResponse(content=json.dumps(resp_dict), content_type="application/json", status=201)

@csrf_exempt
def update_competition(request):
    competition_id = request.POST.get('competition_id')
    competitor_id = request.POST.get('competitor_id')
    distance = request.POST.get('distance')
    competitor = bcModels.Competitor.objects.get(id=competitor_id)
    competition = bcModels.Competition.objects.get(id=competition_id)
    competition.competitors.add(competitor)
    competitor_stats = {}
    if competition.competitors.all().count() > 1:
        competition.status = bcModels.COMPETITION_STATUS_STARTED
        bcModels.CompetitorStats.objects.create(competition_id=competition.id,
                                                competitor_id=competitor.id,
                                                distance=distance)
        competitor_stats = bcModels.Competition.objects.get_stats(competition.id)

    competition.save()
    resp_dict = {
        'competition_id': competition.id,
        'competition_status': competition.status,
        'competition_stats': competitor_stats
    }
    return HttpResponse(content=json.dumps(resp_dict), content_type="application/json", status=201)

@csrf_exempt
def stop_competition(request):
    competition_id = request.POST.get('competition_id')
    competition = bcModels.Competition.objects.get(competition_id)
    resp_dict = {
        'competition_id': competition.id,
        'competition_status': bcModels.COMPETITION_STATUS_FINISHED,
    }
    return HttpResponse(content=json.dumps(resp_dict), content_type="application/json", status=201)