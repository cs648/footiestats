import datetime
from haystack.indexes import *
from haystack import site
from footy.models import Team, DivisionInfo, TeamMatchStat, MatchStat



class TeamIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='team_name')
    team_id = IntegerField(model_attr='team_id')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Team.objects.all()

#
#class TeamIndex(indexes.SearchIndex, indexes.Indexable):
#    text = indexes.CharField(document=True, use_template=True)
#    author = indexes.CharField(model_attr='user')
#    pub_date = indexes.DateTimeField(model_attr='pub_date')
#
#    def get_model(self):
#        return Note
#
#    def index_queryset(self):
#        """Used when the entire index for model is updated."""
#        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
#
#
#class TeamIndex(indexes.SearchIndex, indexes.Indexable):
#    text = indexes.CharField(document=True, use_template=True)
#    author = indexes.CharField(model_attr='user')
#    pub_date = indexes.DateTimeField(model_attr='pub_date')
#
#    def get_model(self):
#        return Note
#
#    def index_queryset(self):
#        """Used when the entire index for model is updated."""
#        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
#
#
#class TeamIndex(indexes.SearchIndex, indexes.Indexable):
#    text = indexes.CharField(document=True, use_template=True)
#    author = indexes.CharField(model_attr='user')
#    pub_date = indexes.DateTimeField(model_attr='pub_date')
#
#    def get_model(self):
#        return Note
#
#    def index_queryset(self):
#        """Used when the entire index for model is updated."""
#        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
#
#

site.register(Team, TeamIndex)
