import pandas as pd
import matplotlib.pyplot as plt
from FantasyPL import FantasyPL

fantasyPL = FantasyPL()
fantasyPL.getFPLJson()
fantasyPL.createElementTypes()
fantasyPL.createTeams()
fantasyPL.createPlayers()
fantasyPL.sortBy("MPP", False, 10)
# fantasyPL.predictSquad()

# fields = ['first_name', 'second_name', 'cost']
# df = pd.DataFrame([{fn: getattr(f, fn) for fn in fields} for f in fantasyPL.players[0:10]])
# ax = df.plot.bar(x='second_name', y='cost', rot=0)
# plt.show()