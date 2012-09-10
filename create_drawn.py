from footy.models import Team
t=Team(team_id=0,team_name="Drawn")
t.save()
Team.objects.get(team_name="Drawn")
t.team_id=0
t.save()
