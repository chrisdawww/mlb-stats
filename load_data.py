# load_data.py is designed to load data from Retrosheet event files for use
# later in statistical queries. Loading everything into to memory is inefficient
# but that's what I'm doing now so...
# Reference: https://www.retrosheet.org/eventfile.htm
import re
import pickle
from glob import glob
from collections import defaultdict

FILETYPE_MAP = { "EVA": "American", "EVN": "National" }
YEARS_OF_INTEREST_GLOB = "20*"
BEGINNING_OF_GAME = "^id,(.*)"
BEGINNING_OF_PLAY = "^play,"
DATA_LOCATION = '/Users/chrisdaw/Development/Data/mlbdata/events'

event_files = glob(f'{DATA_LOCATION}/{YEARS_OF_INTEREST_GLOB}')
#print(event_files)

# events is a dictionary with play.player.game.home_team
events = defaultdict(dict)
for f in event_files:
    with open(f) as events:
        lines = [l.strip() for l in events.readlines()]
        team = ""
        date = ""
        game = ""
        for line in lines:
            play = ""
            if line[0:3] == "id,":
                game_code = re.search(BEGINNING_OF_GAME, line).groups()[0]
                home_team = game_code[0:3]
                date_and_game = game_code[3:]
                date = game_code[3:-1]
                game = game_code[-1]
            if line[0:5] == "play,":
                parts = line.split(',')
                inning = parts[1]
                home_away = parts[2]
                player = parts[3]
                count = parts[4]
                play = parts[6]

                if team != "":
                    if not events[play][player]:
                        events[play][player] = defaultdict(int)

                    events[play][player][game_code] += 1

with open("mlb_events.pickle", 'w') as pickle_file:
    pickle.dump(events, pickle_file)
