from django.db import models


DIVISION_CHOICES = (
    ('E0', 'Premier League'),
    ('E1', 'Championship'),
    ('E2', 'League One'),
    ('E3', 'League Two'),
    ('EC', 'Conference'),
)

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=75, unique=True)
    class Meta:
        db_table = u'footy_teams'
    def __unicode__(self):
        return self.team_name

    @models.permalink
    def get_absolute_url(self):
        return ('team_detail', [self.team_id])

class DivisionInfo(models.Model):
    team = models.ForeignKey(Team)
    season = models.DateField()
    division = models.CharField(max_length=2, choices=DIVISION_CHOICES)
    def __unicode__(self):
        return "%s in %s for season %s" %(self.team, self.division, self.season)

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

    @property
    def opponent(self):
        tms = TeamMatchStat.objects.exclude(team_id=self.team_id).get(match_id=self.match_id)
        return tms
        #return tms.team


class MatchStat(models.Model):
    class Meta:
        db_table = u'footy_stats'
    match_id = models.AutoField(primary_key=True)
    season = models.DateField()
    division = models.CharField(max_length=2, choices=DIVISION_CHOICES)
    match_date = models.DateField()
    fulltime_winner = models.ForeignKey(Team, null=True, related_name="matchstat_ftw")
    halftime_winner = models.ForeignKey(Team, null=True, related_name="matchstat_htw")
    attendance = models.IntegerField(null=True, blank=True)
    referee = models.CharField(max_length=45, null=True)
    def __unicode__(self):
        return "%s (%s)" % (self.versus(), self.match_info())

    def versus(self):
        return "%s vs %s" % (self.home().team, self.away().team)

    def match_info(self):
        return "Match %s on %s" % (self.match_id, self.match_date)

    @property
    def teams(self):
        if getattr(self, "_teams", None) is None:
            self._teams = TeamMatchStat.objects.filter(match_id=self.match_id)
            self._teams[0] # force evaluation #is this necessary?
        return self._teams

    def home(self):
        return self.teams.filter(status='H')[0]

    def away(self):
        return self.teams.filter(status='A')[0]

    def result(self):
        #winner = self.teams.filter(team_id=self.fulltime_winner)
        #loser = self.teams.exclude(team_id=self.fulltime_winner)
        if self.home().team == self.fulltime_winner:
            return "beat"
        elif self.away().team == self.fulltime_winner:
            return "lost to"
        else:
            assert self.fulltime_winner.team_id == 0
            return "drew with"

    @models.permalink
    def get_absolute_url(self):
        return ('match_detail', [self.match_id])

