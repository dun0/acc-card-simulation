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

def activated_a_prideful_prince(attacker, target):

    damage_amount = int(target.max_hp * .20)

    target.take_damage(damage_amount)

    target.take_damage(attacker.damage)


def blade_captain(attacker, target):
    roll = random.randint(1,100)
    if roll <= 35:
        dodge_damage = int(attacker.damage * 1.5)
        target.take_damage(dodge_damage)
    else:
        target.take_damage(attacker.damage)

def body_switcher(attacker, target):
    stolen_damage = (target.damage * .15)
    stolen_hp = (target.max_hp * .15)
    attacker.max_hp = (attacker.max_hp + stolen_hp)
    attacker.damage = (attacker.damage + stolen_damage)
    target.take_damage (attacker.damage)
