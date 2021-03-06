from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from footy.models import MatchStat, Team
from footy.views import MatchDetailView, TeamDetailView, TeamMatchListView, TeamListView, \
    MatchListView, IndexView, LeagueIndexView, LeagueListView
from django.views.generic.dates import DayArchiveView, MonthArchiveView, YearArchiveView
from footy.sitemap import sitemaps

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Landing page
    url(r'^$', IndexView.as_view()),

    # Static
    url(r'^about$', TemplateView.as_view(template_name="about.html")),

    # Teams
    url(r'^teams$', TeamListView.as_view(), name='team_list'),
    url(r'^team/(?P<pk>\d+)/$', TeamDetailView.as_view(), name='team_detail'),
    url(r'^team/(?P<pk>\d+)/matches$', TeamMatchListView.as_view(), name='team_match_detail'),

    # Matches
    url(r'^matches$', MatchListView.as_view(), name='match_list'),
    url(r'^matches/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$', DayArchiveView.as_view(
        model=MatchStat,
        month_format="%m",
        date_field='match_date',
        template_name='match_day_list.html',
    ), name='match_day_list'),
    url(r'^matches/(?P<year>\d{4})-(?P<month>\d{2})$', MonthArchiveView.as_view(
        model=MatchStat,
        month_format="%m",
        date_field='match_date',
        template_name='match_day_list.html',
    ), name='match_month_list'),
    url(r'^matches/(?P<year>\d{4})$', YearArchiveView.as_view(
        model=MatchStat,
        date_field='season',
        template_name='match_day_list.html',
        make_object_list=True,
    ), name='match_year_list'),
    url(r'^match/(?P<pk>\d+)/$', MatchDetailView.as_view(), name='match_detail'),

    # Search
    url(r'^search/', include('haystack.urls')),

    # League
    url(r'^leagues$', LeagueIndexView.as_view(), name='league_index'),
    url(r'^league/(?P<league>E[0123C])$', LeagueListView.as_view(), name='league_list'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Cache stats
    url(r'^cache/', include('django_memcached.urls')),

    # Sitemap
    url(r'^sitemap.xml$',
        cache_page(86400)(sitemaps_views.index),
        (sitemaps_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(86400)(sitemaps_views.sitemap),
        (sitemaps_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),
)
