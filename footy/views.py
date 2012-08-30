from django.http import HttpResponse
from django.shortcuts import render_to_response
from footy.models import MatchStat, Team, TeamMatchStat
from django.views.generic import DetailView, ListView


class MatchDetailView(DetailView):
    model=MatchStat
    context_object_name="match"
    template_name='match_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        return context

class TeamMatchDetailView(DetailView):
    model = Team
    context_object_name = "team"
    template_name = 'team_match_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TeamMatchDetailView, self).get_context_data(**kwargs)
        #a.teammatchstat_set.exclude(match__fulltime_winner=a.team_id)
        #a.teammatchstat_set.exclude(match__fulltime_winner=a.team_id).exclude(match__fulltime_winner=0)
        #a.teammatchstat_set.filter(match__fulltime_winner=0) 
        return context

class TeamDetailView(DetailView):
    model = Team
    context_object_name = "team"
    template_name = 'team_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        team = context['team']
        context['game'] = games = TeamMatchStat.objects.filter(team_id=self.kwargs['pk'])
        context['recent'] = games.order_by('match__match_date').reverse()[:5]
        context['won'] = won = games.filter(match__fulltime_winner=team.team_id)
        context['lost'] = lost = games.exclude(match__fulltime_winner=team.team_id).exclude(match__fulltime_winner=0)
        context['drawn'] = drawn = games.filter(match__fulltime_winner=0)
        context['best_win'] = won.order_by('fulltime_goals').reverse()[0]
        #context['worst_loss'] = lost.order_by().reverse()[0]
        context['average_yellows'] = 0
        context['worst_yellows'] = games.order_by('yellows').reverse()[0]
        context['average_reds'] = 0
        context['worst_reds'] = games.order_by('reds').reverse()[0]
        return context

class TeamListView(ListView):
    queryset = Team.objects.all()
    template_name = 'team_list.html'
    context_object_name = "teams"

    #def get_context_data(self, **kwargs):
    #    # Call the base implementation first to get a context
    #    context = super(TeamDetailView, self).get_context_data(**kwargs)
    #    team = context['team']
    #    return context

class MatchListView(ListView):
    # XXX: hack!
    queryset = [s.teammatchstat_set.all()[0] for s in MatchStat.objects.all()]
    template_name = 'match_list.html'
    context_object_name = "matches"
    paginate_by = 25
