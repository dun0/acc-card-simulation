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

    def perform_attack(self, target): #ability activat
        ability_func = ability_map.get(self.card_name)
        if ability_func:
            ability_func(self, target)
            print (f"{self.card_name} damaged")
        else:
            print (f"{self.card_name} damaged")
            target.take_damage(self.damage)


    def try_to_defend(self, incoming_damage): #defense logic section

        if self.card_name == "Bijuu Beast":
            roll = random.randint(1,100)
            if roll <= self.dodge_chance:
                print ("Dodge")
                self.dodge_chance -= 16
                return 0
            
        elif self.card_name == "Armored Giant":
            if self.shield_active:
                print ("Shield Blocked")
                self.shield_active = False
                return 0
            
        elif self.card_name == "Blade Captain":
            roll1 = random.randint(1,100)
            if roll1 <= self.dodge_chance:
                print ("Dodge")
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
        else:
            self.pending_counter_damage = 0
                
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
            
            if card_a.burn_turns_remaining > 0 and card_a.burn_target and card_a.burn_target.is_alive():
                if card_a.card_name == "Dark Avenger":
                    burn_dmg = int(card_a.burn_target.max_hp * 0.10)
                elif card_a.card_name == "Fire Dragon":
                    burn_dmg = int(card_a.burn_target.max_hp * 0.05)
                else:
                    burn_dmg = int(card_a.burn_target.max_hp * 0.05)
                card_a.burn_target.current_hp -= burn_dmg
                card_a.burn_turns_remaining -= 1
            
            if card_a.bleed_turns_remaining > 0 and card_a.bleed_target and card_a.bleed_target.is_alive():
                bleed_dmg = int(card_a.bleed_target.max_hp * 0.10)
                card_a.bleed_target.current_hp -= bleed_dmg
                card_a.bleed_turns_remaining -= 1
            
            if card_a.stun_turns > 0:
                card_a.stun_turns -= 1
            else:
                card_a.perform_attack(card_b)
            
            if card_b.pending_counter_damage > 0 and card_b.is_alive():
                card_a.take_damage(card_b.pending_counter_damage)
                card_b.pending_counter_damage = 0

            if not card_b.is_alive():
                if card_b.check_revival():
                    pass
                else:
                    print (f"{card_a.card_name} wins")
                    break
            
            if not card_a.is_alive():
                print (f"{card_b.card_name} wins")
                break
            
            if card_b.burn_turns_remaining > 0 and card_b.burn_target and card_b.burn_target.is_alive():
                if card_b.card_name == "Dark Avenger":
                    burn_dmg = int(card_b.burn_target.max_hp * 0.10)
                elif card_b.card_name == "Fire Dragon":
                    burn_dmg = int(card_b.burn_target.max_hp * 0.05)
                else:
                    burn_dmg = int(card_b.burn_target.max_hp * 0.05)
                card_b.burn_target.current_hp -= burn_dmg
                card_b.burn_turns_remaining -= 1
            
            if card_b.bleed_turns_remaining > 0 and card_b.bleed_target and card_b.bleed_target.is_alive():
                bleed_dmg = int(card_b.bleed_target.max_hp * 0.10)
                card_b.bleed_target.current_hp -= bleed_dmg
                card_b.bleed_turns_remaining -= 1
                
            if card_b.stun_turns > 0:
                card_b.stun_turns -= 1
            else:
                card_b.perform_attack(card_a)
            
            if card_a.pending_counter_damage > 0 and card_a.is_alive():
                card_b.take_damage(card_a.pending_counter_damage)
                card_a.pending_counter_damage = 0  # Reset after applying

            if not card_a.is_alive():
                if card_a.check_revival():
                    pass
                else:
                    print (f"{card_b.card_name} wins")
                    break

        
        print (f"Battle has eneded in {self.turn_count}")
        # later do a 4x4 simulation or a 2x2/3x3 to see what comps will work later


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
