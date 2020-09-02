class Player:
  def __init__(self, player_id, player_code, first_name, second_name, element_type, team_code):
    self.player_id = player_id
    self.player_code = player_code
    self.first_name = first_name
    self.second_name = second_name
    self.element_type = element_type
    self.team_code = team_code

  def setMatchStats(self, minutes_played):
    self.minutes_played = minutes_played

  def setFPLStats(self, cost, total_points, bonus):
    self.cost = cost
    self.total_points = total_points
    self.bonus = bonus

  def setIndividualStats(self, status, form):
    self.status = status
    self.form = form

  def isUnavailable(self):
    if self.status == "i" or self.status == "n" or self.status == "u":
      return True
    return False