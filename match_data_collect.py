# %%
import os
import pathlib

from dotenv import load_dotenv
import cassiopeia as cass

load_dotenv()

# %%
# Set API client params
cass.set_riot_api_key(os.environ["API_KEY"])
cass.set_default_region("NA")

player_samples = pathlib.Path("./data/players")
# %%
bronze = player_samples / "bronze.txt"
with open(bronze, "r", encoding="utf-8") as f:
    data = f.read().splitlines()
# %%
test = data[0]
# %%
s = cass.get_summoner(name=test)
# %%
# Champion masteries
masteries = [{"champion": i.champion.name,
              "level": i.level} for i in  s.champion_masteries]
# %%
# Rank
r = s.ranks
[v.tier._name_ for k,v in r.items() if "solo" in k._name_][0]
# %%
matches = s.match_history
# %%
# Match metadata
test_match = matches[0]
print(test_match.duration)
print(test_match.is_remake)
print(test_match.mode)
# %%
# Team metadata
team = test_match.blue_team

# %%
print([c.key for c in team.bans])
print(team.baron_kills)
print(team.dragon_kills)
print(team.first_baron)
print(team.first_dragon)
print(team.first_blood)
print(team.first_inhibitor)
print(team.first_tower)
print(team.first_rift_herald)
print(team.inhibitor_kills)
print(team.participants)
print(team.rift_herald_kills)
print(team.side)
print(team.tower_kills)
print(team.win)

# %%
# Participant metadata
participant = team.participants[0]
# %%
print(participant.champion.key)
print(participant.lane)
print(participant.role)
print(participant.stats.kda)
# %%
