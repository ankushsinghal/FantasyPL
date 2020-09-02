import requests
import operator
import matplotlib.pyplot as plt
import pandas as pd
from ElementType import ElementType
from Team import Team
from Player import Player

PLAYER_TYPE_DEFAULT = "ANY"
MIN_PRICE_DEFAULT = 0.0
MAX_PRICE_DEFAULT = 20.0

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

      # attrs = vars(new_element_type)
      # print(', '.join("%s: %s" % item for item in attrs.items()))

  def getElementTypeIdFromShortName(self, short_name):
    for element_type in self.element_types:
      if element_type.short_name == short_name:
        return element_type.id
    print("Wrong short_name provided for Element Type")
    return -1

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

  def addToTeam(self, player):
    code = player.team_code
    for team in self.teams:
      if team.team_code == code:
        team.players.append(player)
        break

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
      cost = player["now_cost"]/10.0
      total_points = player["total_points"]
      bonus = player["bonus"]
      status = player["status"]
      form = player["form"]

      new_player = Player(player_id, player_code, first_name, second_name, element_type, team_code)
      new_player.setMatchStats(minutes_played)
      new_player.setFPLStats(cost, total_points, bonus)
      new_player.setIndividualStats(status, form)

      self.players.append(new_player)
      self.addToTeam(new_player)
      
      # attrs = vars(new_player)
      # print(', '.join("%s: %s" % item for item in attrs.items()))

  def sortByROI(self, is_descending, num_players, player_type=PLAYER_TYPE_DEFAULT, min_cost=MIN_PRICE_DEFAULT, max_cost=MAX_PRICE_DEFAULT):
    players_dict = {}
    for player in self.players:
      
      # check if player type matches the input provided
      if player_type != "ANY" and player.element_type != self.getElementTypeIdFromShortName(player_type):
        continue
      # check if player is unavailable
      if player.isUnavailable():
        continue
      # check if player satisfies cost constraints
      if player.cost < min_cost or player.cost > max_cost:
        continue
      
      # calculate ROI
      y_item = (player.total_points)*1.0/(player.cost)

      player_name = player.first_name.replace(' ', '\n') + '\n' + player.second_name.replace(' ', '\n')
      players_dict[player_name] = y_item
    
    sorted_players_dict = sorted(players_dict.items(), key=operator.itemgetter(1), reverse=is_descending)

    name_list = []
    y_items_list = []
    counter = 0

    for key, value in sorted_players_dict:
      if counter < num_players:
        counter = counter + 1
      else:
        break
      name_list.append(key)
      y_items_list.append(value)

    if len(name_list) > 0 and len(y_items_list) > 0:
      sorted_players_list = {"Name": name_list, "ROI": y_items_list}
      sorted_players_data_frame = pd.DataFrame(sorted_players_list)
      # print(sorted_players_data_frame)
      ax = sorted_players_data_frame.plot.bar(x='Name', y="ROI", rot=0)
      plt.show()
    else:
      print("No Data to plot")

  def sortByTotalPoints(self, is_descending, num_players, player_type=PLAYER_TYPE_DEFAULT, min_cost=MIN_PRICE_DEFAULT, max_cost=MAX_PRICE_DEFAULT):
    players_dict = {}
    for player in self.players:
      
      # check if player type matches the input provided
      if player_type != "ANY" and player.element_type != self.getElementTypeIdFromShortName(player_type):
        continue
      # check if player is unavailable
      if player.isUnavailable():
        continue
      # check if player satisfies cost constraints
      if player.cost < min_cost or player.cost > max_cost:
        continue
      
      # calculate ROI
      y_item = (player.total_points)

      player_name = player.first_name.replace(' ', '\n') + '\n' + player.second_name.replace(' ', '\n')
      players_dict[player_name] = y_item
    
    sorted_players_dict = sorted(players_dict.items(), key=operator.itemgetter(1), reverse=is_descending)

    name_list = []
    y_items_list = []
    counter = 0

    for key, value in sorted_players_dict:
      if counter < num_players:
        counter = counter + 1
      else:
        break
      name_list.append(key)
      y_items_list.append(value)

    if len(name_list) > 0 and len(y_items_list) > 0:
      sorted_players_list = {"Name": name_list, "Total Points": y_items_list}
      sorted_players_data_frame = pd.DataFrame(sorted_players_list)
      # print(sorted_players_data_frame)
      ax = sorted_players_data_frame.plot.bar(x='Name', y="Total Points", rot=0)
      plt.show()
    else:
      print("No Data to plot")

  def predictSquad(self):
    print("Calling predictSquad function")
