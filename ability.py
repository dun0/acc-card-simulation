import random

def activate_Bald(attacker, target):
    roll = random.randint(1,20)
    if roll == 20:
        target.take_damage(99999999)
    else:
        target.take_damage(attacker.damage)

def activate_Beast_Giant(attacker, target):
    rock = random.randint(4,10)
    rock_damage = int(attacker.damage * .20)
    
    total_damage = rock_damage * rock

    target.take_damage(total_damage)    

def activate_galactic_tyrant(attacker, target):
    damage_amount = int(target.max_hp * .20)
    target.take_damage(damage_amount)

    target.take_damage(attacker.damage)

    heal_amount = int(attacker.max_hp * 0.10)
    attacker.current_hp += heal_amount

    if attacker.current_hp > attacker.max_hp:
        attacker.current_hp = attacker.max_hp

def activate_a_prideful_prince(attacker, target):

    damage_amount = int(target.max_hp * .20)
    target.take_damage(damage_amount)
    target.take_damage(attacker.damage)


def activate_blade_captain(attacker, target):
    roll = random.randint(1,100)
    if roll <= 35:
        dodge_damage = int(attacker.damage * 1.5)
        target.take_damage(dodge_damage)
    else:
        target.take_damage(attacker.damage)

def activate_body_switcher(attacker, target):
    stolen_damage = (target.damage * .15)
    stolen_hp = (target.max_hp * .15)
    attacker.max_hp = (attacker.max_hp + stolen_hp)
    attacker.damage = (attacker.damage + stolen_damage)
    target.take_damage (attacker.damage)

def activate_Deranged_assassin (attacker, target):
    target.take_damage(attacker.damage)
    target.take_damage(attacker.damage)
    selfdamage = int(attacker.current_hp * 0.2)
    attacker.current_hp = (attacker.current_hp - selfdamage)

def activate_death_log(attacker, target):
    attacker.attack_count += 1
    target.take_damage(attacker.damage)
    
    if attacker.attack_count >= 5:
        target.take_damage(9999999999)

def activate_blue_slime(attacker, target):
    heal_amount = int(attacker.damage * 0.40)
    target.take_damage(attacker.damage)
    attacker.current_hp += heal_amount

    if attacker.current_hp > attacker.max_hp:
        attacker.current_hp = attacker.max_hp

def activate_a_pale_demon(attacker, target):
    if not attacker.has_revive:
        target.take_damage(attacker.damage)
    else:
        strikes = random.randint(2, 5)
        damage_per_hit = int(attacker.damage * 0.5)
        total_damage = damage_per_hit * strikes
        target.take_damage(total_damage)


def activate_soul_king (attacker, target):
    statsteal = random.randint(15, 40)
    target.take_damage(attacker.damage)
    if target.current_hp <= 0:
        hp_gain = float((target.max_hp * statsteal) / 100)
        damage_gain = float((target.damage * statsteal) / 100)
        attacker.current_hp += hp_gain
        attacker.damage += damage_gain

def activate_esper_prodigy(attacker, target):
    missing_hp = attacker.max_hp - attacker.current_hp
    bonus_damage = int(missing_hp * 1.0) 
    total_damage = attacker.damage + bonus_damage
    target.take_damage(total_damage)

def activate_flame_head_captain(attacker, target):
    if attacker.flame_stacks < 3:
        attacker.flame_stacks += 1
        attacker.max_hp = int(attacker.max_hp * 1.3)
        attacker.current_hp = int(attacker.current_hp * 1.3)
        attacker.damage = int(attacker.damage * 1.3)
    
    target.take_damage(attacker.damage)
    
    if attacker.flame_stacks >= 3:
        if attacker.burn_target != target:
            attacker.burn_target = target
            attacker.burn_turns_remaining = 2
        
        if attacker.burn_turns_remaining > 0:
            burn_damage = int(attacker.damage * 0.4)
            target.take_damage(burn_damage)
            attacker.burn_turns_remaining -= 1

def activate_zen_masta(attacker, target):
    if attacker.zen_target != target:
        attacker.zen_target = target
        attacker.zenstack = 0
    
    roll = random.randint(1, 100)
    
    target.take_damage(attacker.damage)
    
    if roll <= 45:
        follow_up_damage = int(attacker.damage * 0.75)
        target.take_damage(follow_up_damage)
        attacker.zenstack += 1

        if attacker.zenstack >= 2:
            bonus_damage = int(attacker.damage * 2.25)
            target.take_damage(bonus_damage)
            attacker.zenstack = 0 
            # TODO: Apply 225% damage to next enemy

def activate_bijuu_beast (attacker, target):
    target.take_damage(attacker.damage)

def activate_black_swordsman(attacker, target):
    target.take_damage(attacker.damage)
    remaining_hp = int(target.current_hp * 0.2)
    target.take_damage(remaining_hp)

def activate_awakened_wildhunter (attacker, target):
    if attacker.wild_attacks % 2 == 0:

        rockfist = int(attacker.damage* 1.5)
        target.take_damage(rockfist)

    else:

        target.take_damage(attacker.damage)

    attacker.wild_attacks += 1


def activate_destroyer_deity (attacker, target):
    percenthp = int(target.max_hp * 0.15)
    target.take_damage(attacker.damage)
    if target.current_hp <= percenthp:
        target.take_damage(9999999)

def activate_bamboo_demon (attacker, target):
    target.take_damage (attacker.damage)
    attacker.bamboo_stack += 1

    if attacker.bamboo_stack >= 2:
        explosiondamage = int(target.max_hp * 0.2)
        target.take_damage (explosiondamage)
        attacker.bamboo_stack = 0

def activate_blade_rebel (attacker, target):
    target.take_damage (attacker.damage)
    target.damage = int(target.damage * 0.9)

def activate_dark_avenger(attacker, target):
    target.take_damage(attacker.damage)

    if attacker.burn_turns_remaining == 0:
        attacker.burn_turns_remaining = 2
        attacker.burn_target = target
        burn_damage = int(target.max_hp * 0.1)
        target.take_damage(burn_damage)

    
def activate_awakened_shadow_sum (attacker, target):
    target.take_damage (attacker.damage)
    target.take_damage( int(attacker.damage * 0.35))

def activate_fire_dragon (attacker, target):
    roll = random.randint (1,100)

    target.take_damage(attacker.damage)
    if roll <= 10 and attacker.burn_turns_remaining == 0:
        attacker.burn_turns_remaining = 2
        attacker.burn_target = target

def activate_crimson_eyes (attacker, target):
    target.take_damage(attacker.damage)
    target.take_damage(attacker.damage)

def on_entry_crimson_eyes(attacker, target):
    target.stun_turns = 1

def activate_blood_fiend(attacker, target):
    roll = random.randint(1,100)
    if roll <= 50:
        target.take_damage(int(attacker.damage * 1.3))
        percentlost = int(attacker.max_hp * 0.15)
        attacker.current_hp = int(attacker.current_hp - percentlost)
    else:
        target.take_damage(attacker.damage)

def activate_Chainsaw_fiend (attacker, target):
    roll = random.randint(1,100)
    target.take_damage (attacker.damage)
    if roll <= 25 and attacker.bleed_turns_remaining == 0:
        attacker.bleed_turns_remaining = 2
        attacker.bleed_target = target

def activate_golden_wnd (attacker, target):
    target.take_damage(attacker.damage)
    heal_amount = int(attacker.max_hp * 0.15)
    attacker.current_hp += heal_amount

def activate_green_bomba (attacker, target):
    target.take_damage(attacker.damage)

def on_death_green_bomber(attacker, target):
    target.take_damage(attacker.max_hp)

def activate_homeroom_teach (attacker, target):
    target.take_damage(attacker.damage)

def on_entry_homeroom_teacher(attacker, target):
    attacker.max_hp = int(attacker.max_hp * 1.2)
    attacker.damage = int(attacker.damage * 1.2)
    attacker.current_hp = attacker.max_hp
    
def activate_light_admiral(attacker, target):
    target.take_damage(attacker.damage)

def on_entry_light_admiral(attacker, target):
    target.damage = int(target.damage * 0.9)

def activate_mist_hashira(attacker, target):
    missing_hp_percent = int((1 - attacker.current_hp / attacker.max_hp) * 100)
    additional_dodge = (missing_hp_percent // 10) * 5
    attacker.dodge_chance = 10 + additional_dodge
    target.take_damage(attacker.damage)
    

def activate_muscle_head (attacker, target):
    target.take_damage(attacker.damage)

def on_entry_muscle_head(attacker, target):
    target.take_damage(int(target.max_hp * 0.12))

def activate_namekian_sage (attacker, target):
    roll = random.randint(1,100)
    if roll <= 60:
        target.take_damage(int(attacker.damage*1.75))
    else:
        target.take_damage(attacker.damage)

def activate_peaceful_swordsman(attacker, target):
    roll = random.randint(1,100)
    target.take_damage(attacker.damage)
    if roll <= 60:
        for _ in range(5):
            target.take_damage(int(attacker.damage * 0.1))

def activate_red_emperor (attacker, target):
    target.take_damage(attacker.damage)

def on_entry_red_emperor(attacker, target):
    target.damage = int(target.damage * 0.8)

def activate_ripple_knight (attacker, target):
    target.take_damage(attacker.damage)
    attacker.current_hp += int(attacker.damage *0.1)

def activate_straw_hat(attacker, target):
    target.take_damage(attacker.damage)

def on_entry_straw_hat(attacker, target):
    target.current_hp = int(target.current_hp * 0.85)

def activate_water_hasira(attacker, target):
    target.take_damage(attacker.damage)

def on_entry_water_hashira(attacker, target):
    attacker.max_hp = int(attacker.max_hp * 1.25)
    attacker.current_hp = attacker.max_hp