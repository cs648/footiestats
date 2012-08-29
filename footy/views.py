from django.http import HttpResponse
from django.shortcuts import render_to_response
from footy.models import FootyStats

def index(request):
    stat_list = FootyStats.objects.all().order_by('-idate')[:5]
    output = ', '.join("%s vs %s" % (s.awayteam, s.hometeam) for s in stat_list)
    return HttpResponse(output)

def index(request):
    stat_list = FootyStats.objects.all().order_by('-idate')[:5]
    return render_to_response('index.html', {'stat_list': stat_list})

def match_detail(request, match_id):
    return HttpResponse("You're looking at match %s." % match_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)
