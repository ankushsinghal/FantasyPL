class Team:
  def __init__(self, team_code, team_name, short_name):
    self.team_code = team_code
    self.team_name = team_name
    self.short_name = short_name
    self.players = []

  def setMatchStats(self, matches_played, points_scored, league_position):
    self.matches_played = matches_played
    self.points_scored = points_scored
    self.league_position = league_position

  def setTeamStrength(self, strength):
    self.strength = strength