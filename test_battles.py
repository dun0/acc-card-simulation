import json
import random
from main import Card, BattleSimulation, get_card_data, ability_map, all_playable_cards
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

with open('card_database.json') as f:
    raw_data = json.load(f)
the_list = list(ability_map.keys())

available_cards = all_playable_cards
win_counts = {}
for card_name in available_cards:
    win_counts[card_name] = 0

num_battles = 100000
battle_mode = "1v1"

team_comp_wins = {}

if battle_mode == "4x4":
    for _ in range(num_battles):
        team_1 = []
        team_2 = []

        for i in range(4):
            card_name_1 = random.choice(available_cards)
            card_name_2 = random.choice(available_cards)

            data1 = get_card_data(card_name_1, raw_data)
            data2 = get_card_data(card_name_2, raw_data)

            player1 = Card(data1)
            player2 = Card(data2)

            team_1.append(player1)
            team_2.append(player2)

        sim = BattleSimulation(verbose=False)
        winning_team = sim.run_4x4(team_1, team_2)
        team_comp = tuple(sorted([card.card_name for card in winning_team]))

        if team_comp not in team_comp_wins:

            team_comp_wins[team_comp] =0

        team_comp_wins[team_comp] += 1

    sorted_comps = sorted(team_comp_wins.items(), key=lambda x: x[1], reverse=True)
    print ("Top 30")
    for i, (comp, wins) in enumerate(sorted_comps[:30], 1):
        print(f"{i} {wins} - {comp}") 

elif battle_mode == "1v1":
    match_history = []
    for i in range(num_battles):
        card_1 = random.choice(available_cards)
        card_2 = random.choice(available_cards)
        while card_1 == card_2:
            card_2 = random.choice(available_cards)
        data1 = get_card_data(card_1, raw_data)
        data2 = get_card_data(card_2, raw_data)
        player1 = Card(data1)
        player2 = Card(data2)
        sim = BattleSimulation(verbose=False)
        winner = sim.run_1x1(player1, player2)
        match_history.append({
            "match_id": i,
            "winner": winner
        })

    df = pd.DataFrame(match_history)

    binary_wins = pd.get_dummies(df['winner'])

    cumulative_wins = binary_wins.cumsum()
    
    top_10_name = cumulative_wins.iloc[-1].nlargest(10).index

    top_10_data = cumulative_wins[top_10_name]

    top_10_data.plot()

    #    fig = px.line(cumulative_wins,title=f"wins over {num_battles}", labels={"index": "Match Number", "value": "Total Wins", "variable": "Character"})
    #    fig.show()

    plt.title(f"Win History Over {num_battles} Matches")
    plt.xlabel("Match Number")
    plt.ylabel("Total Wins")
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout() # Fixes layout issues
    
    plt.show()