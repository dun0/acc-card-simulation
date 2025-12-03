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

        
        self.dodge_chance = 0
        
        self.shield_activated = False

        if self.card_name == "Bijuu Beast":
            self.dodge_chance = 60

        elif self.card_name == "Armored Giant":
            self.shield_active = True

    def perform_attack(self, target):
        if self.card_name == "Bald Hero":
            self._ability_Bald(target)
        elif self.card_name == "Awakened Galactic Tyrant":
            self._ability_galactic_tyrant(target)
        elif self.card_name == "Beast Giant":
            self._ability_Beast_Giant(target)
        else:
            print (f"{self.card_name} damaged")
            target.take_damage(self.damage)

    def _ability_Bald(self, target):
        roll = random.randint(1,20)
        if roll == 20:
            target.take_damage(99999999)
        else:
            target.take_damage(self.damage)

    def _ability_Beast_Giant(self, target):
        rock = random.randint(4,10)
        rock_damage = int(self.damage * 20)
        
        total_damage = rock_damage * rock

        target.takedamage(total_damage)    

    def _ability_galactic_tyrant(self, target):
        damage_amount = int(target.max_hp * .20)
        target.take_damage(damage_amount)
        target.current_hp - self.damage

        heal_amount = int(self.max_hp * 0.10)
        self.current_hp += heal_amount

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
            
        return incoming_damage
    
    def take_damage(self, amount):
        final_damage = self.try_to_defend(amount)
        self.current_hp -= final_damage

    def is_alive(self):
        return self.current_hp >  0

    def take_damage(self, amount):
        self.current_hp -= amount

    def activate_ability(self, target):

        if self.card_name == "Bijuu Beast":
            self.dodge_chance = 60
            dodgechance = random.randint(1,100)
            if dodgechance <= self.dodge_chance:
                self.dodge_chance -= 16
                print("Dodge successful")
            else:
                pass

        elif self.card_name == "Bald Hero":
            self._ability_Bald(target)
        elif self.card_name == "Armored Giant":
            self._ability_Armored_giant(self)


        elif self.card_name == "Awakened Galactic Tyrant":
            self._ability_galactic_tyrant(target)
            
        elif self.card_name == "Beast Giant":

            self._ability_Beast_Giant(target)
    

class BattleSimulation:
    def __init__(self, card_data_list):
        self.card_pool = card_data_list

    def run_1x1 (self, card_a, card_b):
        pass

    

if __name__ == "__main__":

    with open(r"card_database.json") as f:
        raw_data = json.load(f)


