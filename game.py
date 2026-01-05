import json
import time
from random import randint
from time import sleep


# player class
class character:
    def __init__(self, level, maxhealth, health,maxmana, mana, damage, xp, weapon, weapon_level):
        self.level = level
        self.xp = xp
        self.health = health
        self.maxhealth = maxhealth
        self.maxmana = maxmana
        self.mana = mana
        self.damage = damage
        self.weapon = weapon
        self.weapon_level = weapon_level

    def show_stats_battle(self):
        print(f'Your health - {self.health}/{self.maxhealth}, your damage - {self.damage}.')
        print(f'Your mana - {self.mana}/{self.maxmana}.')

    def show_stats_main(self):
        print()
        print(f'Your health - {self.health}/{self.maxhealth}, your damage - {self.damage}.')
        print(f'Your mana - {self.mana}/{self.maxmana}.')
        print(f"You're level {self.level}. {self.level * 2 - self.xp} xp till next level.")
        print(f'Your weapon - level {self.weapon_level} {self.weapon}.')
        print()

    def set_health_damaged(self, damage):
        self.health -= damage

    def level_up(self):
        print()
        print(f'Level up! {player.level} => {player.level + 1}')
        print(f'Health: {player.maxhealth} => {player.maxhealth + 10}')
        print(f'Damage: {player.damage} => {player.damage + 1}')
        print()
        self.level += 1
        self.damage += 1
        self.maxhealth += 10
        self.xp -= self.level*2

    def heal(self):
        self.health = self.maxhealth
        self.mana = self.maxmana

    def heal_battle(self):
        if self.mana - 10 < 0:
            print("You don't have enough mana!")
        else:
            if self.health >= self.maxhealth/2:
                self.health = self.maxhealth
            else:
                self.health += int(self.health/2)
            self.mana -= 10


# enemy class
class enemy:
    def __init__(self, name, health, level, damage):
        self.level = level
        self.health = health
        self.name = name
        self.damage = damage

    def set_health_damaged(self, damage):
        self.health -= damage

    def show_stats_battlestart(self):
        print(f'You are fighting {self.name} level {self.level} with {self.health} health')

    def show_stats_battle(self):
        print(f"{self.name}'s health is {self.health}, damage - {self.damage}")


# big intro if new player
def full_intro():
    print("Hello, new player!")
    print("Welcome to my game!")
    # сюда еще сюжет запилить
    print("Press enter to start")
    input()


# short variant of intro for expirienced players
def short_intro():
    print("Welcome back to our game!")
    print("Press enter to start")
    input()


# core battle script
def battle(enemy_type):
    if enemy_type == 'npc':
        enemy_npc = enemy(enemies[randint(0, len(enemies) - 1)], randint(40, 40 + player.level),
                          randint(player.level - 1, player.level + 2), randint(player.level, player.level + 5))
    if enemy_type == 'boss':
        enemy_npc = enemy('Boss', 1000, 100, 500)
    print("Battle")
    enemy_npc.show_stats_battlestart()
    while True:
        enemy_npc.show_stats_battle()
        player.show_stats_battle()
        print()
        print(f'[1] attack for {player.damage}')
        print(f'[2] Use healing spell and recover half of your health (uses 10 mana)')
        print(f'[3] run away')
        option = int(input())
        if option == 1:
            enemy_npc.set_health_damaged(player.damage)
            print(f'You damaged {enemy_npc.name} for {player.damage}')
            if enemy_npc.health <= 0:
                battle_won = True
                break
            player.set_health_damaged(enemy_npc.damage)
            if player.health <= 0:
                battle_won = False
                break
        if option == 2:
            player.heal_battle()
        if option == 3:
            battle_won = False
            break
    if battle_won:
        print("Congrats! You won")
        print()
        drop_script()
        if enemy_type=='npc':
            player.xp += 1
        if enemy_type=='boss':
            player.xp+=100
        if player.xp >= player.level * 2:
            player.level_up()
    if not battle_won:
        print('You lost! Better luck next time!')


# drop gamble on battle won
def drop_script():
    dropchance = randint(0, 10)
    if dropchance == 5:
        drop = weapons[randint(0, len(weapons) - 1)]
        drop_level = randint(player.level-20, player.level + 20)
        print(f'you got a level {drop_level} {drop}!')
        print('Equip it (y/n)')
        choice = str(input())
        if choice == 'y':
            player.weapon = drop
            player.damage = drop_level - player.weapon_level
            player.weapon_level = drop_level


#dungeon
def dungeon(enemy_number):
    for _ in range(enemy_number):
        battle('npc')



# healing in main menu
def rest():
    print('You take a five second nap...')
    print()
    time.sleep(5)
    print(f'You rest and recover {player.maxhealth - player.health} hp, {player.maxmana - player.mana}')
    player.heal()
    print(f'Your health: {player.health}/{player.maxhealth}')
    print(f'Your mana: {player.mana}/{player.maxmana}')


# rewriting save file on exit
def save_game():
    save_data = {
        "maxhealth": str(player.maxhealth),
        "level": str(player.level),
        "damage": str(player.damage),
        "health": str(player.health),
        "xp": str(player.xp),
        "weapon": str(player.weapon),
        "weapon_level": str(player.weapon_level),
        "mana": str(player.mana),
        "maxmana": str(player.maxmana)
    }
    with open('save.json', 'w') as fp:
        json.dump(save_data, fp)


# inicial boot and save load
with open("save.json", "r") as outfile: stats = json.load(outfile)
maxhealth = int(stats.get('maxhealth'))
level = int(stats.get('level'))
damage = int(stats.get('damage'))
health = int(stats.get('health'))
xp = int(stats.get('xp'))
weapon = str(stats.get('weapon'))
weapon_level = int(stats.get('weapon_level'))
maxmana = int(stats.get('maxmana'))
mana = int(stats.get('mana'))
player = character(level, maxhealth, health, maxmana, mana, damage, xp, weapon, weapon_level)

# weapon and enemy database, later turn into a .json or .db
weapons = ['sword', 'katana', 'stick', 'mace']
enemies = ['goblin', 'ghost', 'skeleton']

# choosing intro
if player.level <= 1:
    full_intro()
else:
    short_intro()

# main gameloop
while True:
    print('[1] - battle')
    print('[2] - Your stats')
    print('[3] - Sleep and recover to full health')
    print('[4] - Fight in dungeon (5 enemies in a row).')
    if player.level >= 10:
        print('[5] - boss fight (dangerous, level above 50 recommended.')
    print('[0] - save and exit')
    option = int(input())
    if option == 1:
        battle('npc')
    if option == 2:
        player.show_stats_main()
    if option == 3:
        if player.health != player.maxhealth:
            rest()
        else:
            print("You're already at max health!")
    if option == 4:
        dungeon(5)
    if option == 5:
        battle('boss')
    if option == 0:
        save_game()
        break
