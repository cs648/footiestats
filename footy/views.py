from django.http import HttpResponse
from django.shortcuts import render_to_response
from footy.models import MatchStat, Team, TeamMatchStat
from footy.config import current_season
from django.views.generic import DetailView, ListView, TemplateView
from random import randint


class MatchDetailView(DetailView):
    model=MatchStat
    context_object_name="match"
    template_name='match_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        return context

class TeamMatchListView(ListView):
    context_object_name = "teams"
    template_name = 'team_match_list.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(TeamMatchListView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.get(team_id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return TeamMatchStat.objects.filter(team_id=self.kwargs['pk']).order_by('match__match_date').reverse()

class TeamDetailView(DetailView):
    model = Team
    context_object_name = "team"
    template_name = 'team_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        team = context['team']
        games = TeamMatchStat.objects.filter(team_id=self.kwargs['pk'])
        context['recent'] = games.order_by('match__match_date').reverse()[:5]
        games_this_season = games.filter(match__season=current_season)
        context['position'] = team.divisioninfo_set.order_by('season').reverse()[0]
        context['won'] = won = games_this_season.filter(match__fulltime_winner=team.team_id)
        context['lost'] = lost = games_this_season.exclude(match__fulltime_winner=team.team_id).exclude(match__fulltime_winner=0)
        context['drawn'] = drawn = games_this_season.filter(match__fulltime_winner=0)
        try:
            context['best_win'] = won.order_by('fulltime_goals').reverse()[0]
        except IndexError:
            context['best_win'] = None
        #context['worst_loss'] = lost.order_by().reverse()[0]
        context['worst_loss'] = None
        context['average_yellows'] = None
        context['worst_yellows'] = games_this_season.order_by('yellows').reverse()[0]
        context['average_reds'] = None
        context['worst_reds'] = games_this_season.order_by('reds').reverse()[0]
        return context

class TeamListView(ListView):
    queryset = Team.objects.all()
    template_name = 'team_list.html'
    context_object_name = "teams"

class MatchListView(ListView):
    # XXX: hack!
    queryset = MatchStat.objects.order_by('match_date').reverse()
    template_name = 'match_list.html'
    context_object_name = "matches"
    paginate_by = 25

class IndexView(TemplateView):
    template_name = "index.html"
    model = Team
    queryset = Team.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)

        num_teams = 5
        max_team = Team.objects.all().count()
        team_ids = [randint(0, max_team) for x in xrange(num_teams)]
        context['random_teams'] = Team.objects.in_bulk(team_ids).values()

        num_matches = 5
        max_match = MatchStat.objects.all().count()
        match_ids = [randint(0, max_match) for x in xrange(num_matches)]
        random_matches = MatchStat.objects.in_bulk(match_ids).values()
        random_tms = [s.teammatchstat_set.all()[0] for s in random_matches]
        context['random_matches'] = random_tms
        return context

