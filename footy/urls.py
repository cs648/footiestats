from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, TemplateView
from footy.models import MatchStat, Team
from footy.views import MatchDetailView, TeamDetailView, TeamMatchDetailView, TeamListView, MatchListView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'footy.views.home', name='home'),
    # url(r'^footy/', include('footy.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    #url(r'^match/(?P<match_id>\d+)/$', 'footy.views.match_detail'),
    url(r'^match/(?P<pk>\d+)/$', MatchDetailView.as_view(), name='match_detail'),
    url(r'^team/(?P<pk>\d+)/$', TeamDetailView.as_view(), name='team_detail'),
    url(r'^team/(?P<pk>\d+)/matches$', TeamMatchDetailView.as_view(), name='team_match_detail'),
    url(r'^matches$', MatchListView.as_view(), name='match_list'),
    url(r'^teams$', TeamListView.as_view(), name='team_list'),
    #url(r'^footy/(?P<poll_id>\d+)/vote/$', 'footy.views.vote'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
