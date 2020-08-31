import requests
from ElementType import ElementType
from Team import Team
from Player import Player

class FantasyPL:
  def __init__(self):
    print("Initializing FantasyPL Object")

  def getFPLJson(self):
    print("Calling getFPLJson method to call FPL API")
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    resp = requests.get(url=url)
    data = resp.json()
    self.full_data = data

  def createElementTypes(self):
    self.element_types = []
    element_types = self.full_data["element_types"]
    for element_type in element_types:
      id = element_type["id"]
      name = element_type["singular_name"]
      short_name = element_type["singular_name_short"]
      squad_select = element_type["squad_select"]
      squad_min_play = element_type["squad_min_play"]
      squad_max_play = element_type["squad_max_play"]

      new_element_type = ElementType(id, name, short_name, squad_select, squad_min_play, squad_max_play)

      self.element_types.append(new_element_type)

      attrs = vars(new_element_type)
      print(', '.join("%s: %s" % item for item in attrs.items()))

  def createTeams(self):
    self.teams = []
    teams = self.full_data["teams"]
    for team in teams:
      team_code = team["code"]
      team_name = team["name"]
      short_name = team["short_name"]
      matches_played = team["played"]
      points_scored = team["points"]
      league_position = team["position"]
      strength = team["strength"]
      
      new_team = Team(team_code, team_name, short_name)
      new_team.setMatchStats(matches_played, points_scored, league_position)
      new_team.setTeamStrength(strength)

      self.teams.append(new_team)

      # attrs = vars(new_team)
      # print(', '.join("%s: %s" % item for item in attrs.items()))

  def createPlayers(self):
    self.players = []
    players = self.full_data["elements"]
    for player in players:
      player_id = player["id"]
      player_code = player["code"]
      first_name = player["first_name"]
      second_name = player["second_name"]
      element_type = player["element_type"]
      team_code = player["team_code"]
      minutes_played = player["minutes"]
      cost = player["now_cost"]
      total_points = player["total_points"]
      bonus = player["bonus"]
      status = player["status"]
      form = player["form"]

      new_player = Player(player_id, player_code, first_name, second_name, element_type, team_code)
      new_player.setMatchStats(minutes_played)
      new_player.setFPLStats(cost, total_points, bonus)
      new_player.setIndividualStats(status, form)

      self.players.append(new_player)
      
      # attrs = vars(new_player)
      # print(', '.join("%s: %s" % item for item in attrs.items()))

  def predictSquad(self):
    print("Calling predictSquad function")
