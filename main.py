import os
import json
import random
import time
import ability

def parse_stat(value_str):
    cleaned_val = str(value_str).upper()

    cleaned_val = cleaned_val.replace(",", "")

    if "K" in cleaned_val:

        number_part = cleaned_val.replace("K", "")
        return int(float(number_part)* 1000) 
    elif "M" in cleaned_val:

        number_part = cleaned_val.replace("M", "")
        return int(float(number_part)* 1000000)
    
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
        self.has_revive = False

        
        self.dodge_chance = 0
        self.attack_count = 0

        if self.card_name == "Blade Captain":
            self.dodge_chance = 35
        
        if self.card_name == "Bijuu Beast":
            self.dodge_chance = 60

        elif self.card_name == "Armored Giant":
            self.shield_active = True

    def perform_attack(self, target):
        if self.card_name == "Bald Hero":
            ability.activate_Bald(self, target)
        elif self.card_name == "Awakened Galactic Tyrant":
            ability.activate_galactic_tyrant(self, target)
        elif self.card_name == "Beast Giant":
            ability.activate_Beast_Giant(self, target)
        elif self.card_name == "Awakened Prideful Prince":
            ability.activate_a_prideful_prince(self, target)
        elif self.card_name == "Blade Captain":
            ability.activate_blade_captain(self, target)
        elif self.card_name == "Body Switcher":
            ability.activate_body_switcher(self, target)
        elif self.card_name == "Deranged Assassin":
            ability.activate_Deranged_assassin (self, target)
        elif self.card_name == "Death Log":
            ability.activate_death_log(self, target)
        elif self.card_name == "Blue Slime":
            ability.activate_blue_slime(self, target)
        elif self.card_name == "Awakened Pale Demon Lord":
            ability.activate_a_pale_demon(self, target)
        else:
            print (f"{self.card_name} damaged")
            target.take_damage(self.damage)


    def try_to_defend(self, incoming_damage):

        if self.card_name == "Bijuu Beast":
            roll = random.randint(1,100)
            if roll <= self.dodge_chance:
                print ("Dodge")
                self.dodge_chance -= 16
                return 0
            
        elif self.card_name == "Armored Giant":
            if self.shield_activated:
                print ("Shield Blocked")
                self.shield_active = False
                return 0
            
        elif self.card_name == "Blade Captain":
            roll1 = random.randint(1,100)
            if roll1 <= self.dodge_chance:
                print ("Dodge")
                return 0
            
        return incoming_damage
    
    def take_damage(self, amount):
        final_damage = self.try_to_defend(amount)
        self.current_hp -= final_damage

    def is_alive(self):
        return self.current_hp >  0

    def check_revival(self):
        if self.card_name == "Berserker Shinigami" and not self.has_revive:
            if self.current_hp <= 0:
                self.has_revive = True
                self.current_hp = int(self.max_hp * 0.5)
                self.damage = int(self.damage * 1.5)
                return True

        if self.card_name == "Combat Giant" and not self.has_revive:
            if self.current_hp <= 0:
                self.has_revive = True
                self.current_hp = int(self.max_hp * 2.5)
                self.damage = int(self.damage * 1.35)
                return True
        if self.card_name == "Awakened Pale Demon Lord" and not self.has_revive:
            if self.current_hp <= 0:
                self.has_revive = True
                self.max_hp = int(self.max_hp * 1.25)
                self.current_hp = self.max_hp
                return True
        if self.card_name == "Crimson Vampire" and not self.has_revive:
            if self.current_hp <= 0:
                roll = random.randint(1, 2)
                if roll == 1:
                    self.has_revive = True
                    self.current_hp = self.max_hp
                    return True

        return False

class BattleSimulation:
    def __init__(self):
        self.turn_count = 0

    def run_1x1 (self, card_a, card_b):
        print ("="*50)
        print (f"Battle started between {card_a} and {card_b}")
        print ("="*50)


        self.turn_count = 0

        while card_a.is_alive() and card_b.is_alive():

            self.turn_count += 1
            print (f"turn {self.turn_count}")

            card_a.perform_attack(card_b)

            if not card_b.is_alive():
                if card_b.check_revival():
                    pass
                else:
                    print (f"{card_a.card_name} wins")
                    break
            card_b.perform_attack(card_a)

            if not card_a.is_alive():
                if card_a.check_revival():
                    pass
                else:
                    print (f"{card_b.card_name} wins")
                    break

        
        print (f"Battle has eneded in {self.turn_count}")


if __name__ == "__main__":

    with open(r"card_database.json") as f:
        raw_data = json.load(f)

    #data_a = random.choice(raw_data)
    #data_b = random.choice(raw_data)

    data_a = get_card_data("Zen Master", raw_data)
    data_b = get_card_data("Blue Slime", raw_data)
    player_1 = Card(data_a)
    player_2 = Card(data_b)

    sim = BattleSimulation()
    sim.run_1x1(player_1,player_2)
