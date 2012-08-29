from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from footy.models import MatchStat, Team

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'footy.views.home', name='home'),
    # url(r'^footy/', include('footy.foo.urls')),
    url(r'^footy/$', 'footy.views.index'),
    #url(r'^match/(?P<match_id>\d+)/$', 'footy.views.match_detail'),
    url(r'^match/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=MatchStat,
            context_object_name="match",
            template_name='match_detail.html'),
        name='match_detail'),
    url(r'^team/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Team,
            context_object_name="team",
            template_name='team_detail.html'),
        name='team_detail'),
    url(r'^footy/(?P<poll_id>\d+)/vote/$', 'footy.views.vote'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
