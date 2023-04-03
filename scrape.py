import pandas as pd
from functions import get_active_players
from functions import get_game_log_url
from functions import get_game_log

activePlayers = get_active_players()

gls = []

for e in activePlayers.values():
    gls.append(get_game_log_url(e))


print(gls)


cald = '/players/c/cabocbr01/gamelog/2015'

from functions import get_game_log

cdf = get_game_log(cald)

