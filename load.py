import sys
from footy.models import Team, MatchStat, TeamMatchStat
from datetime import datetime
from csv import DictReader

def int2(i):
    if i is None:
        return None
    if i == '':
        return None
    return int(i)


def load(file, season):
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

        if row['HTR'] == 'H':
            halftime_winner = hometeam
        elif row['HTR'] == 'A':
            halftime_winner = awayteam
        elif row['HTR'] == 'D':
            halftime_winner = "Drawn"
        else:
            assert(False)

        m=MatchStat(
                #match_id=match_id,
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
            fulltime_goals=int2(row['FTHG']),
            halftime_goals=int2(row['HTHG']),
            shots=int2(row.get('HS', None)),
            shots_on_target=int2(row.get('HST', None)),
            hit_woodwork=int2(row.get('HHW', None)),
            corners=int2(row.get('HC', None)),
            fouls=int2(row.get('HF', None)),
            offsides=int2(row.get('HO', None)),
            yellows=int2(row.get('HY', None)),
            reds=int2(row.get('HR', None)),
            bookings_points=int2(row.get('HBP', None)),
                )

        away = TeamMatchStat(match_id=m.match_id,
            team=Team.objects.get(team_name=awayteam),
            status="A",
            fulltime_goals=int2(row['FTAG']),
            halftime_goals=int2(row['HTAG']),
            shots=int2(row.get('AS', None)),
            shots_on_target=int2(row.get('AST', None)),
            hit_woodwork=int2(row.get('AHW', None)),
            corners=int2(row.get('AC', None)),
            fouls=int2(row.get('AF', None)),
            offsides=int2(row.get('AO', None)),
            yellows=int2(row.get('AY', None)),
            reds=int2(row.get('AR', None)),
            bookings_points=int2(row.get('ABP', None)),
                )
        home.save()
        away.save()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, "Need file, season arguments"
    load(sys.argv[1], sys.argv[2])
