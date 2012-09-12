from django.contrib.sitemaps import Sitemap, FlatPageSitemap, GenericSitemap
from django.db import models
from footy.models import division_dict, Team, MatchStat
from django.core.urlresolvers import reverse


class LeagueSitemap(Sitemap):
    priority = 0.6
    def items(self):
        return division_dict.keys()
    @models.permalink
    def location(self, item):
        return ('league_list', [item])


class YearArchiveSitemap(Sitemap):
    priority = 0.7
    def items(self):
        return MatchStat.objects.all().dates('season', 'year')
    @models.permalink
    def location(self, item):
        return ('match_year_list', (), {'year': item.year})


class MonthArchiveSitemap(Sitemap):
    priority = 0.5
    def items(self):
        return MatchStat.objects.all().dates('match_date', 'month')
    @models.permalink
    def location(self, item):
        return ('match_month_list', (), {'year': item.year, 'month': item.strftime("%m")})


class DayArchiveSitemap(Sitemap):
    priority = 0.3
    def items(self):
        return MatchStat.objects.all().dates('match_date', 'day')
    @models.permalink
    def location(self, item):
        return ('match_day_list', (), {'year': item.year, 'month': item.strftime("%m"), 'day': item.strftime("%d")})


class StaticSitemap(Sitemap):
    priority = 1.0
    def items(self):
        return ("about", "leagues", "matches")
    def location(self, item):
        return "/" + item


team_dict = {'queryset': Team.objects.all()}
match_dict = {'queryset': MatchStat.objects.all()}

sitemaps = {
    'teams': GenericSitemap(team_dict, priority=0.6),
    #'matches': GenericSitemap(match_dict, priority=0.4),
    'year-match-archive': YearArchiveSitemap,
    'month-match-archive': MonthArchiveSitemap,
    #'day-match-archive': DayArchiveSitemap,
    'league': LeagueSitemap,
    'static': StaticSitemap,
}
