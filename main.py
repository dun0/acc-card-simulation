import os
import json
import random

def parse_stat(value_str):
    cleaned_val = str(value_str).upper()

    cleaned_val = cleaned_val.replace(",", "")

    if "K" in cleaned_val:

        number_part = cleaned_val.replace("K", "")
        return int(float(number_part)* 1000) 
    elif "M" in cleaned_val:

        number_part = cleaned_val.replace("M", "")
        return int(float(number_part)* 10000)
    
    else:

        return int(float(cleaned_val))
    
def get_card_data (card_name, full_database):

    for card in full_database:

        if card["name"] == card_name:

            return card

    return None
    

class Card:
    def __init__(self,data):
        self.max_hp = parse_stat(data['hp'])
        self.current_hp = self.max_hp
        self.damage = parse_stat(data['damage'])
        self.card_name = data['name']
        self.ability_desc = data['ability']

        
        self.dodge_chance = 0

        if self.card_name == "Bijuu Beast":
            self.dodge_chance = 60

    def is_alive(self):
        return self.current_hp >  0

    def take_damage(self, amount):
        self.current_hp -= amount

class BattleSimulation:
    def __init__(self, card_data_list):
        self.card_pool = card_data_list

    def run_1x1 (self, card_a, card_b):
        pass

    

if __name__ == "__main__":

    with open(r"card_database.json") as f:
        raw_data = json.load(f)


    baldhero = get_card_data("Bald Hero",raw_data)
    bijuu = get_card_data("Bijuu Beast", raw_data)

    card_a = Card(baldhero)
    card_b = Card(bijuu)

    print(f"Battle Start: {card_a.card_name} vs {card_b.card_name}")
    print(f"{card_a.card_name} HP: {card_a.current_hp}")
    print(f"{card_b.card_name} HP: {card_b.current_hp}")
    print(f"{card_b.card_name} Dodge: {card_b.dodge_chance}%")

    turn_count = 0

    while card_a.is_alive() and card_b.is_alive():
        turn_count += 1
        print (f"turn count is {turn_count}")

        dodge_roll = random.randint(1,100)

        if dodge_roll <= card_b.dodge_chance:
            print("Bijuu dodged")
            card_b.dodge_chance -= 16
            if card_b.dodge_chance < 0:
                card_b.dodge_chance = 0
            print (f"dodge chance is {card_b.dodge_chance}")

        else:
            instakill = random.randint(1, 20)
            print (f"instakill roll is {instakill}")

            if instakill == 1:
                card_b.take_damage(999999999999)
            else:
                print (f"Bald hero does {card_a.damage} to {card_b.card_name}")
                card_b.take_damage(card_a.damage)

            if not card_b.is_alive():
                print ("Bijuu beast died")
                break

        
        print (f"Bijuu does {card_b.damage}")
        card_a.take_damage(card_b.damage)

        if not card_a.is_alive():
            print ("Bald hero lost")
            break