from django.db import models

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=75, unique=True)
    class Meta:
        db_table = u'footy_teams'
    def __unicode__(self):
        return self.team_name

class TeamMatchStat(models.Model):
    match = models.ForeignKey('MatchStat')
    team = models.ForeignKey(Team)
    STATUS_CHOICES = (
        ('H', 'Home'),
        ('A', 'Away'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    fulltime_goals = models.IntegerField(null=True)
    halftime_goals = models.IntegerField(null=True)
    shots = models.IntegerField(null=True)
    shots_on_target = models.IntegerField(null=True)
    hit_woodwork = models.IntegerField(null=True)
    corners = models.IntegerField(null=True)
    fouls = models.IntegerField(null=True)
    offsides = models.IntegerField(null=True)
    yellows = models.IntegerField(null=True)
    reds = models.IntegerField(null=True)
    bookings_points = models.IntegerField(null=True)
    class Meta:
        db_table = u'footy_matches'

class MatchStat(models.Model):
    class Meta:
        db_table = u'footy_stats'
    match_id = models.IntegerField(primary_key=True)
    season = models.DateField()
    division = models.CharField(max_length=15)
    match_date = models.DateField()
    fulltime_winner = models.ForeignKey(Team, null=True, related_name="matchstat_ftw")
    halftime_winner = models.ForeignKey(Team, null=True, related_name="matchstat_htw")
    attendance = models.IntegerField(null=True, blank=True)
    referee = models.CharField(max_length=45, null=True)
    def __unicode__(self):
        return "Match %s on %s" % (self.match_id, self.match_date)
    def teams(self):
        return TeamMatchStat.objects.filter(match_id=self.match_id)
