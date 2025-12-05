import json
import random
from main import Card, BattleSimulation, get_card_data, ability_map, all_playable_cards

with open('card_database.json') as f:
    raw_data = json.load(f)
the_list = list(ability_map.keys())

available_cards = all_playable_cards
win_counts = {}
for card_name in available_cards:
    win_counts[card_name] = 0

num_battles = 10000
for _ in range(num_battles):
    card_1 = random.choice(available_cards)
    card_2 = random.choice(available_cards)
    data1 = get_card_data(card_1, raw_data)
    data2 = get_card_data(card_2, raw_data)
    player1 = Card(data1)
    player2 = Card(data2)
    sim = BattleSimulation(verbose=False)
    winner = sim.run_1x1(player1, player2)
    win_counts[winner] += 1

sorted_results = sorted(win_counts.items(), key=lambda x: x[1], reverse=True)
for card_name, wins in sorted_results:
    print(f"{card_name}: {wins} wins")