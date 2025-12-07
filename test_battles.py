import json
import random
import time
import pandas as pd
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import matplotlib.pyplot as plt
from main import Card, BattleSimulation, get_card_data, ability_map, all_playable_cards, parse_stat

BATCH_SIZE = 50000
TOTAL_BATTLES = 1000000
BATTLE_MODE = "1v1"

def load_and_parse_db():
    with open('card_database.json') as f:
        raw_data = json.load(f)
    
    cards_map = {}
    for card in raw_data:
        card['hp'] = parse_stat(card['hp'])
        card['damage'] = parse_stat(card['damage'])
        cards_map[card['name']] = card
        
    return cards_map

def run_batch(num_battles, mode, seed, card_keys_list, parsed_card_data):
    random.seed(seed) 
    

    card_pool = {}
    
    instances_needed = 8 if mode == "4x4" else 2
    
    for name in card_keys_list:
        data = parsed_card_data.get(name)
        if data:
            card_pool[name] = [Card(data) for _ in range(instances_needed)]

    results = []
    
    sim = BattleSimulation(verbose=False)
    
    for _ in range(num_battles):
        if mode == "1v1":
            name1 = random.choice(card_keys_list)
            name2 = random.choice(card_keys_list)
            while name1 == name2:
                name2 = random.choice(card_keys_list)
            
            card1 = card_pool[name1][0]
            card2 = card_pool[name2][0] 
            
            card1.reset()
            card2.reset()
            
            winner = sim.run_1x1(card1, card2)
            results.append(winner)
            
        elif mode == "4x4":

            
            team1_cards = []
            team2_cards = []
            
            usage_counts = {name: 0 for name in card_keys_list}
            
            for _ in range(4):
                name = random.choice(card_keys_list)
                idx = usage_counts[name]
                usage_counts[name] += 1
                
                card_obj = card_pool[name][idx]
                card_obj.reset()
                team1_cards.append(card_obj)

            for _ in range(4):
                name = random.choice(card_keys_list)
                idx = usage_counts[name]
                usage_counts[name] += 1
                
                card_obj = card_pool[name][idx]
                card_obj.reset()
                team2_cards.append(card_obj)
                
            winning_team = sim.run_4x4(team1_cards, team2_cards)
            
            comp_key = tuple(sorted([c.card_name for c in winning_team]))
            results.append(comp_key)

    return results

if __name__ == "__main__":
    t_start = time.time()
    
    full_card_map = load_and_parse_db()
    
    valid_card_keys = [k for k in all_playable_cards if k in full_card_map]
    
    num_workers = multiprocessing.cpu_count()
    chunk_size = TOTAL_BATTLES // num_workers
    futures = []
    
    reduced_results = {}
    all_match_results = []
    
    with ProcessPoolExecutor() as executor:
        for i in range(num_workers):
            seed = random.randint(0, 999999999) + i
            

            futures.append(executor.submit(run_batch, chunk_size, BATTLE_MODE, seed, valid_card_keys, full_card_map))

        print("started")
        
        for f in futures:
            batch_data = f.result()
            
            for item in batch_data:
                if item not in reduced_results:
                    reduced_results[item] = 0
                reduced_results[item] += 1
            
            if BATTLE_MODE == "1v1":
                all_match_results.extend(batch_data)
                
    t_end = time.time()
    print(f"finished in {t_end - t_start:.2f} seconds")
    print("-" * 40)
    
    # 4. Display Stats
    if BATTLE_MODE == "1v1":
        sorted_res = sorted(reduced_results.items(), key=lambda x: x[1], reverse=True)
        print("top")
        for name, wins in sorted_res[:30]:
            print(f"{name}: {wins}")
            
        df = pd.DataFrame(all_match_results, columns=['winner'])
        top_10 = [x[0] for x in sorted_res[:10]]
        df_top = df[df['winner'].isin(top_10)]
        binary_wins = pd.get_dummies(df_top['winner'])
        cumulative_wins = binary_wins.cumsum()
        
        plt.figure(figsize=(12, 8))
        for column in cumulative_wins.columns:
            plt.plot(cumulative_wins.index, cumulative_wins[column], label=column)
            
        plt.title(f"Cumulative Wins (Top 10) - {TOTAL_BATTLES} Battles")
        plt.xlabel("Battle Number")
        plt.ylabel("Wins")
        plt.legend()
        plt.grid(True)
        plt.show()
            
    elif BATTLE_MODE == "4x4":
        sorted_res = sorted(reduced_results.items(), key=lambda x: x[1], reverse=True)
        print("top 30 team comps:")
        for i, (comp, wins) in enumerate(sorted_res[:30], 1):
            print(f"{i}. {wins} wins - {comp}")
