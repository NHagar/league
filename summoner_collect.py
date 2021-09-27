# %%
import os
import pathlib
import random

from dotenv import load_dotenv
import cassiopeia as cass

load_dotenv()
# %%
# Set API client params
cass.set_riot_api_key(os.environ["API_KEY"])
cass.set_default_region("NA")

player_samples = pathlib.Path("./data/players")
# %%
# Pulled random seed users from across rank distribution
# We'll use these to expand out, grabbing 100 users per dfivision
bronze = cass.get_summoner(name="Bruhbarian")
silver = cass.get_summoner(name="x Dr Buzz x")
gold = cass.get_summoner(name="subjext123")
diamond = cass.get_summoner(name="Ayaka")
# %%
# We don't want to get a big clump of associated users,
# So the flow will be get user's most recent game ->
# Select random player not already in our list ->
# Append to list ->
# Repeat until we get 100 users ->
# Repeat for other divisions
def get_sample(seed, rank):
    rank_path = player_samples / f"{rank}.txt"
    sample, current_player = load_or_start(rank_path, seed)
    while len(sample)<=120:
        new_participant = sample_random_participant(current_player, sample)
        sample.append(new_participant.name)
        with open(rank_path, "a", encoding="utf-8") as f:
            f.write(f"{sample[-1]}\n")
        current_player = new_participant

def sample_random_participant(summoner, sample):
    last_matches = summoner.match_history(end_index=5)
    players = [i.participants for i in last_matches]
    players = [i for l in players for i in l]
    valid_players = [i.summoner for i in players if i.summoner.name not in sample]
    new_player = random.choice(valid_players)
    return new_player

def load_or_start(path, seed):
    if path.is_file():
        with open(path, "r", encoding="utf-8") as f:
            players = f.read().splitlines()
        current_player = cass.get_summoner(name=players[-1])
    else:
        players = []
        current_player = seed
    return players, current_player

# %%
get_sample(bronze, "bronze")
# %%
get_sample(silver, "silver")

# %%
get_sample(gold, "gold")

# %%
get_sample(diamond, "diamond")
# %%
test_path = pathlib.Path("./data/players/bronze.txt")
# %%
with open(test_path, "r", encoding="utf-8") as f:
    players = f.read().splitlines()
# %%
test_player = players[40]
# %%
test_s = cass.get_summoner(name=test_player)
# %%
test_m = test_s.match_history
# %%
test_match = test_m[0]
# %%
test_match.teams
# %%
