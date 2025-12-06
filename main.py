import os
import json
import random
import time
import ability

ability_map = {
    "Bald Hero": ability.activate_Bald,
    "Awakened Galactic Tyrant": ability.activate_galactic_tyrant,
    "Beast Giant": ability.activate_Beast_Giant,
    "Awakened Prideful Prince": ability.activate_a_prideful_prince,
    "Blade Captain": ability.activate_blade_captain,
    "Body Switcher": ability.activate_body_switcher,
    "Deranged Assassin": ability.activate_Deranged_assassin,
    "Death Log": ability.activate_death_log,
    "Blue Slime": ability.activate_blue_slime,
    "Awakened Pale Demon Lord": ability.activate_a_pale_demon,
    "Soul King": ability.activate_soul_king,
    "Esper Prodigy": ability.activate_esper_prodigy,
    "Flame Head Captain": ability.activate_flame_head_captain,
    "Zen Master": ability.activate_zen_masta,
    "Bijuu Beast": ability.activate_bijuu_beast,
    "Black Swordsman": ability.activate_black_swordsman,
    "Awakened Wild Hunter": ability.activate_awakened_wildhunter,
    "Destroyer Deity": ability.activate_destroyer_deity,
    "Bamboo Demon": ability.activate_bamboo_demon,
    "Blade Rebel": ability.activate_blade_rebel,
    "Awakened Shadow Summoner": ability.activate_awakened_shadow_sum,
    "Fire Dragon": ability.activate_fire_dragon,
    "Crimson Eyes": ability.activate_crimson_eyes,
    "Blood Fiend": ability.activate_blood_fiend,
    "Chainsaw Fiend": ability.activate_Chainsaw_fiend,
}

playable_cards_without_attack_abilities = [
    "Armored Giant",
    "Blade Warrior",
    "Undead Commander",
    "Berserker Shinigami",
    "Combat Giant",
    "Crimson Vampire",

]

all_playable_cards = list(ability_map.keys()) + playable_cards_without_attack_abilities


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
        
        if self.card_name == "Science King":
            roll = random.randint(1, 2)
            if roll == 1:
                self.max_hp = int(self.max_hp * 1.15)
                self.current_hp = self.max_hp
            else:
                self.damage = int(self.damage * 1.15)
        
        if self.card_name == "Flame Head Captain":
            self.flame_stacks = 0
            self.burn_target = None
            self.burn_turns_remaining = 0

        if self.card_name == "Zen Master":
            self.zenstack = 0
            self.zen_target = None
        
        if self.card_name == "Bamboo Demon":
            self.bamboo_stack = 0

        if self.card_name == "Awakened Wild Hunter":
            self.wild_attacks = 1
        
        if self.card_name == "Dark Avenger":
            self.dark_stacks = 0
            self.burn_turns_remaining = 0
            self.burn_target = None
        
        if self.card_name == "Fire Dragon":
            self.burn_turns_remaining = 0
        
        if self.card_name == "Chainsaw Fiend":
            self.bleed_turns_remaining = 0
            self.bleed_target = None

        self.pending_counter_damage = 0
        
        if not hasattr(self, 'stun_turns'):
            self.stun_turns = 0
        if not hasattr(self, 'burn_turns_remaining'):
            self.burn_turns_remaining = 0
        if not hasattr(self, 'burn_target'):
            self.burn_target = None
        if not hasattr(self, 'bleed_turns_remaining'):
            self.bleed_turns_remaining = 0
        if not hasattr(self, 'bleed_target'):
            self.bleed_target = None

    def perform_attack(self, target):
        ability_func = ability_map.get(self.card_name)
        if ability_func:
            ability_func(self, target)
        else:
            target.take_damage(self.damage)


    def try_to_defend(self, incoming_damage): #defense logic section

        if self.card_name == "Bijuu Beast":
            roll = random.randint(1,100)
            if roll <= self.dodge_chance:
                self.dodge_chance -= 16
                return 0
            
        elif self.card_name == "Armored Giant":
            if self.shield_active:
                self.shield_active = False
                return 0
            
        elif self.card_name == "Blade Captain":
            roll1 = random.randint(1,100)
            if roll1 <= self.dodge_chance:
                return 0
        
        if self.card_name == "Shadow Monarch":
            incoming_damage = int(incoming_damage * 1.1)
            
        if self.card_name == "Flame Head Captain":
            if self.flame_stacks >= 3:
                incoming_damage = int(incoming_damage * 0.65)

        if self.card_name == "Undead Commander" and self.has_revive:
            incoming_damage = int(incoming_damage * 0.8)

        return incoming_damage
    
    def take_damage(self, amount):
        final_damage = self.try_to_defend(amount)
        self.current_hp -= final_damage
        
        if self.card_name == "Undead Commander" and final_damage > 0:
            self.pending_counter_damage = int(self.damage * 1.15)
        elif self.card_name == "Blade Warrior" and final_damage > 0:
            self.pending_counter_damage = int(self.damage * 1.25)

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
        if self.card_name == "Undead Commander" and not self.has_revive:
            if self.current_hp <= 0:
                self.has_revive = True
                self.current_hp = int(self.max_hp)
                return True

        return False

class BattleSimulation:
    def __init__(self, verbose=False):
        self.turn_count = 0
        self.verbose = verbose


    def process_card_turn(self, attacker, defender):

        if attacker.burn_turns_remaining > 0 and attacker.burn_target and attacker.burn_target.is_alive():
            if attacker.card_name == "Dark Avenger":
                burn_dmg = int(attacker.burn_target.max_hp * 0.10)
            elif attacker.card_name == "Fire Dragon":
                burn_dmg = int(attacker.burn_target.max_hp * 0.05)
            else:
                burn_dmg = int(attacker.burn_target.max_hp * 0.05)

            attacker.burn_target.current_hp -= burn_dmg
            attacker.burn_turns_remaining -= 1

        if attacker.bleed_turns_remaining > 0 and attacker.bleed_target and attacker.bleed_target.is_alive():
            if attacker.card_name == "Chainsaw Fiend":
                bleed_dmg = int(attacker.bleed_target.max_hp * 0.10)
                attacker.bleed_target.current_hp -= bleed_dmg
                attacker.bleed_turns_remaining -= 1
        
        if attacker.stun_turns > 0:
            attacker.stun_turns -= 1
        else:
            attacker.perform_attack(defender)
        
        if defender.pending_counter_damage > 0 and defender.is_alive():
            attacker.take_damage(defender.pending_counter_damage)
            defender.pending_counter_damage = 0
        
        if not defender.is_alive():
            if defender.check_revival():
                pass  
            else:
                return (True, attacker.card_name) 
        

        if not attacker.is_alive():
            return (True, defender.card_name)
        
        return (False, None)



    def run_1x1(self, card_a, card_b):
        if self.verbose:
            print ("="*50)
            print (f"Battle started between {card_a.card_name} and {card_b.card_name}")
            print ("="*50)
        self.turn_count = 0
        while card_a.is_alive() and card_b.is_alive():
            self.turn_count += 1
            if self.verbose:
                print(f"turn {self.turn_count}")
            battle_over, winner = self.process_card_turn(card_a, card_b)
            if battle_over:
                if self.verbose:
                    print(f"{winner} wins")
                return (winner)
            
            battle_over, winner = self.process_card_turn(card_b, card_a)
            if battle_over:
                if self.verbose:
                    print(f"{winner} wins")
                return (winner)
        if self.verbose:
            print(f"Battle has ended in {self.turn_count} turns")
    
    def run_4x4(self,team_1,team_2):

        active_index1 = 0
        active_index2 = 0
        self.turn_count = 0

        while (active_index1 < 4 and active_index2 < 4):
            active_card_1 = team_1[active_index1]
            active_card_2 = team_2[active_index2]

            self.turn_count += 1

            battle_over, winner = self.process_card_turn(active_card_1, active_card_2)

            if not active_card_2.is_alive():
                active_index2 +=1
                if active_index2 >= 4:
                    return team_1
                    
            battle_over, winner = self.process_card_turn(active_card_2, active_card_1)

            if not active_card_1.is_alive():
                active_index1 += 1
                if active_index1 >= 4:
                    return team_2

            

if __name__ == "__main__":

    with open(r"card_database.json") as f:
        raw_data = json.load(f)

    #data_a = random.choice(raw_data)
    #data_b = random.choice(raw_data)

    data_a = get_card_data("Bijuu Beast", raw_data)
    data_b = get_card_data("Blue Slime", raw_data)
    player_1 = Card(data_a)
    player_2 = Card(data_b)
    
    sim = BattleSimulation()
    sim.run_1x1(player_1,player_2)
