from django.contrib.sitemaps import views as sitemaps_views
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from footy.models import MatchStat, Team
from footy.views import MatchDetailView, TeamDetailView, TeamMatchListView, TeamListView, \
    MatchListView, IndexView, LeagueIndexView, LeagueListView
from django.views.generic.dates import DayArchiveView, MonthArchiveView, YearArchiveView
from footy.sitemap import sitemaps

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'footy.views.home', name='home'),
    # url(r'^footy/', include('footy.foo.urls')),
    url(r'^$', IndexView.as_view()),
    url(r'^about$', TemplateView.as_view(template_name="about.html")),
    url(r'^match/(?P<pk>\d+)/$', MatchDetailView.as_view(), name='match_detail'),
    url(r'^team/(?P<pk>\d+)/$', TeamDetailView.as_view(), name='team_detail'),
    url(r'^team/(?P<pk>\d+)/matches$', TeamMatchListView.as_view(), name='team_match_detail'),
    url(r'^matches$', MatchListView.as_view(), name='match_list'),
    url(r'^teams$', TeamListView.as_view(), name='team_list'),
    url(r'^matches/(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)$', DayArchiveView.as_view(
        model=MatchStat,
        month_format="%m",
        date_field='match_date',
        template_name='match_day_list.html',
    ), name='match_day_list'),
    url(r'^matches/(?P<year>\d\d\d\d)-(?P<month>\d\d)$', MonthArchiveView.as_view(
        model=MatchStat,
        month_format="%m",
        date_field='match_date',
        template_name='match_day_list.html',
    ), name='match_month_list'),
    url(r'^matches/(?P<year>\d\d\d\d)$', YearArchiveView.as_view(
        model=MatchStat,
        date_field='season',
        template_name='match_day_list.html',
        make_object_list=True,
    ), name='match_year_list'),

    url(r'^leagues$', LeagueIndexView.as_view(), name='league_index'),
    url(r'^league/(?P<league>E[0123C])$', LeagueListView.as_view(), name='league_list'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^sitemap.xml$',
        #cache_page(86400)(sitemaps_views.index),
        (sitemaps_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        #cache_page(86400)(sitemaps_views.sitemap),
        (sitemaps_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),
)
