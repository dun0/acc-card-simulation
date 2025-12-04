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
    
    
