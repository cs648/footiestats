import sys
from footy.models import Team, MatchStat, TeamMatchStat
from datetime import datetime
from csv import DictReader


def load(file, season, match_id):
    season = datetime.strptime(season, "%Y")
    for row in DictReader(open(file)):
        match_date = datetime.strptime(row['Date'], "%d/%m/%y")
        hometeam = row['HomeTeam']
        awayteam = row['AwayTeam']
        if Team.objects.filter(team_name=hometeam).count() == 0:
            Team(team_name=hometeam).save()
        if Team.objects.filter(team_name=awayteam).count() == 0:
            Team(team_name=awayteam).save()

        if row['FTAG'] < row['FTHG']:
            fulltime_winner = hometeam
        elif row['FTAG'] > row['FTHG']:
            fulltime_winner = awayteam
        else:
            fulltime_winner = "Drawn"

        if row['HTAG'] < row['HTHG']:
            halftime_winner = hometeam
        elif row['HTAG'] > row['HTHG']:
            halftime_winner = awayteam
        else:
            halftime_winner = "Drawn"

        m=MatchStat(match_id=match_id,
                division=row['Div'],
                match_date=match_date,
                referee=row.get('Referee', None),
                fulltime_winner=Team.objects.get(team_name=fulltime_winner),
                halftime_winner=Team.objects.get(team_name=halftime_winner),
                season=season,
                )
        m.save()

        home = TeamMatchStat(match_id=m.match_id,
            team=Team.objects.get(team_name=hometeam),
            status="H",
            fulltime_goals=row['FTHG'],
            halftime_goals=row['HTHG'],
            shots=row.get('HS', None),
            shots_on_target=row.get('HST', None),
            hit_woodwork=row.get('HHW', None),
            corners=row.get('HC', None),
            fouls=row.get('HF', None),
            offsides=row.get('HO', None),
            yellows=row.get('HY', None),
            reds=row.get('HR', None),
            bookings_points=row.get('HBP', None),
                )

        away = TeamMatchStat(match_id=m.match_id,
            team=Team.objects.get(team_name=awayteam),
            status="A",
            fulltime_goals=row['FTAG'],
            halftime_goals=row['HTAG'],
            shots=row.get('AS', None),
            shots_on_target=row.get('AST', None),
            hit_woodwork=row.get('AHW', None),
            corners=row.get('AC', None),
            fouls=row.get('AF', None),
            offsides=row.get('AO', None),
            yellows=row.get('AY', None),
            reds=row.get('AR', None),
            bookings_points=row.get('ABP', None),
                )
        home.save()
        away.save()
        match_id += 1
    return match_id
