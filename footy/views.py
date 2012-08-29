from django.http import HttpResponse
from django.shortcuts import render_to_response
from footy.models import MatchStat, Team
from django.views.generic import DetailView


class MatchDetailView(DetailView):
    model=MatchStat
    context_object_name="match"
    template_name='match_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        return context

class TeamDetailView(DetailView):
    model = Team
    context_object_name = "team"
    template_name = 'team_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        #a.teammatchstat_set.exclude(match__fulltime_winner=a.team_id)
        #a.teammatchstat_set.exclude(match__fulltime_winner=a.team_id).exclude(match__fulltime_winner=0)
        #a.teammatchstat_set.filter(match__fulltime_winner=0) 
        return context

