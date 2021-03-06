import sys
import random
import re
import requests
import argparse
from pprint import pprint
import json
import statistics
import copy

ANIMALS = [
        "elk",
        "constrictor-snake",
        "wolf"
    ]

class Roll:

    def __init__(self, name, dice_string, mod):
        self.name = name
        self.dice = []
        self.parse_dice_string(dice_string)
        self.mod = mod
        self.max = sum([die_roll[1] for die_roll in self.dice]) + self.mod

    def parse_dice_string(self, dice_string):
        roll_strings = dice_string.split('+')
        for roll_string in roll_strings:
            self.dice.append([int(num) for num in roll_string.split('d')])

    def roll(self, crit=False):
        total = self.mod
        if crit:
            dice = [[die_roll[0]*2, die_roll[1]] for die_roll in self.dice]
        else:
            dice = self.dice

        for die_roll in dice:
            for die in range(die_roll[0]):
                total += random.randint(1, die_roll[1])

        return total

    def __str__(self):
        result = self.roll()
        dice_string = '+'.join(['{}d{}'.format(die_roll[0], die_roll[1]) for die_roll in self.dice])
        dice_string += '+{}'.format(self.mod)
        return '{}: {} result = {}'.format(self.name, dice_string, result)


class Attack:

    def __init__(self, name, desc, to_hit_mod, damages, has_advantage=False, has_disadvantage=False):
        self.name = name
        self.desc = desc

        self.to_hit_mod = to_hit_mod
        self.to_hit = Roll(
                '{} to hit'.format(self.name),
                '1d20',
                to_hit_mod
            )

        self.for_damage = []
        for damage in damages:
            self.for_damage.append(
                {
                    "roll": Roll(
                        '{} for damage'.format(self.name),
                        damage["damage_dice"],
                        damage["damage_bonus"]
                    ),
                    "type": damage["damage_type"]["name"]
                }
            )

        self.has_advantage    = has_advantage
        self.has_disadvantage = has_disadvantage

    def give_advantage(self):
        self.has_advantage = True

    def give_disadvantage(self):
        self.has_disadvantage = True

    def roll_to_hit(self):
        crit = False
        to_hit_result = self.to_hit.roll()

        second_roll = self.to_hit.roll()
        if self.has_advantage and self.has_disadvantage:
            pass
        elif self.has_advantage:
            to_hit_result = max([to_hit_result, second_roll])
        elif self.has_disadvantage:
            to_hit_result = min([to_hit_result, second_roll])

        if to_hit_result == self.to_hit.max:
            crit = True

        return to_hit_result, crit

    def roll_for_damage(self, crit=False):
        dmg_list = []
        for dmg_roll in self.for_damage:
            dmg_list.append([dmg_roll["roll"].roll(crit), dmg_roll["type"]])
        return dmg_list

    def __str__(self):
        damage_str = [str(dmg["roll"]) for dmg in self.for_damage]
        return '{}: To hit=1d20+{}, Damage={}'.format(self.name, self.to_hit_mod, damage_str)

    def attack(self):
        to_hit_result, crit = self.roll_to_hit()
        dmg = self.roll_for_damage(crit)
        return to_hit_result, crit, dmg


class Monster:
    def __init__(self, name):
        self.attacks={}
        self.info = {}
        self.load_from_api(name)
    # Function with in a class is a method
    def __str__(self):
        return 'Monster: {}, AC={}, Type={}'.format(self.name, self.ac, self.type)

    def add_attack(self, name, attack):
        self.attacks[name] = attack

    def attack(self, name):
        if name in self.attacks:
            print(self)
            print(self.attacks[name])
            print(self.attacks[name].attack())
        else:
            print('ERROR: Attack {} not found for {}'.format(name, self.Name))
            print('    Available attacks:')
            for key in self.attacks.keys():
                print('    --> {}'.format(self.attacks[key]))
            sys.exit()

    def search_all_monsters(self, api_index):
        url = 'http://www.dnd5eapi.co/api/monsters'
        results = requests.get(url).json()['results']
        available_monsters = [result['index'] for result in results]
        for monster in available_monsters:
            if api_index.lower() in monster.lower():
                print('    Partial match --> {}'.format(monster))

    def load_from_api(self, api_index):
        url = 'http://www.dnd5eapi.co/api/monsters/'+api_index
        response = requests.get(url).json()
        if response == {'error': 'Not found'}:
            print('ERROR: Monster {} not found in database'.format(api_index))
            self.search_all_monsters(api_index)
            sys.exit()

        self.info = response
        self.ac = response['armor_class']
        self.type = response['type']
        self.name = response['name']
        self.hp = response['hit_points']
        self.max_hp = response['hit_points']
        pprint(response)

        for i in response['actions']:
            try:
                self.add_attack(
                        i['name'], 
                        Attack(
                            i['name'],
                            i['desc'],
                            i['attack_bonus'],
                            i['damage']
                        )
                    )
            except KeyError:
                continue


class Character:
    def __init__(self,Name):
        self.load_from_char_sheet(Name)
    def load_from_char_sheet(self,char_name):
        with open('Alden.json') as f:
            data = json.load(f)

        self.Name = data['Name']
        self.AC = data['Armor Class']
        self.HP = data['Hit Points']
        self.Init = data['Initiative']
        self.Str = data['Strength']
        self.Dex = data['Dexterity']
        self.Con = data['Constitution']
        self.Int = data['Intelligence']
        self.Wis = data['Wisdom']
        self.Cha = data['Charisma']


def battle(aggressor, defender):
    print("\n{} assalts {}!".format(aggressor.Name, defender.Name))
    num_sims = 10000
    ac = defender.AC
    attacks = aggressor.attacks
    print("    {}'s attacks = [{}]".format(aggressor.Name, ", ".join(list(attacks.keys()))))
    print("    {}'s AC = {}".format(defender.Name, ac))

    for attack in attacks:
        totals = []
        for i in range(num_sims):
            to_hit, for_damage = attacks[attack].attack()
            if to_hit >= ac:
                totals.append(for_damage)
            else:
                totals.append(0)

        print(attack)
        print("    min: {}".format(min(totals)))
        print("   mean: {}".format(int(sum(totals)/len(totals))))
        print(" median: {}".format(statistics.median(totals)))
        print("    max: {}".format(max(totals)))
    print("")


class Animal(Monster):
    def __init__(self, name):
        self.attacks={}
        self.load_from_api(name)


class Pack:
    def __init__(self, animal, size):
        og_animal = Animal(animal)
        self.animals = [copy.deepcopy(og_animal) for i in range(size)]
        enemy_attr = {}
        self.chosen_attack = None
        self.info = self.animals[0].info

    def __str__(self):
        return "\n".join([str(animal) for animal in self.animals])

    def attack(self, attack_name, ac, advantage, disadvantage):
        total_dmg = 0
        self.chosen_attack = self.animals[0].attacks[attack_name]

        if advantage:
            self.chosen_attack.give_advantage()
        if disadvantage:
            self.chosen_attack.give_disadvantage()

        damage_results = []
        for animal in self.animals:
            if animal.hp <= 0:
                continue
            dmg_dict = {}
            dmg_dict["dmg"] = []
            to_hit, is_crit, dmgs = self.chosen_attack.attack()
            dmg_dict["to_hit"] = to_hit
            if to_hit >= ac:
                dmg_dict["hit"] = True
                if is_crit:
                    dmg_dict["crit"] = True
                else:
                    dmg_dict["crit"] = False
                for dmg in dmgs:
                    dmg_dict["dmg"].append({"dmg": dmg[0], "type": dmg[1]})
                total_dmg += dmg[0]
            else:
                dmg_dict["hit"] = False

            damage_results.append(dmg_dict)

        return damage_results

    def apply_damage(self, dmg):
        dmg_left = dmg
        self.animals.sort(key=lambda x: x.hp)
        for i, animal in enumerate(self.animals):
            hp_left = animal.hp - dmg_left
            if hp_left <= 0:
                animal.hp = 0
            else:
                animal.hp = hp_left
                return
            dmg_left = -1*hp_left

    def apply_heal(self, healing):
        healing_left = healing
        self.animals.sort(key=lambda x: x.hp)
        for i, animal in enumerate(self.animals):
            if animal.hp <= 0:
                continue
            healing_needed = animal.max_hp - animal.hp
            if healing_left <= healing_needed:
                animal.hp = animal.hp + healing_left
                return
            else:
                animal.hp = animal.hp + healing_needed
                healing_left = healing_left - healing_needed

    def apply_damage_aoe(self, dmg):
        self.animals.sort(key=lambda x: x.hp)
        for i, animal in enumerate(self.animals):
            animal.hp = max(0, animal.hp - dmg)

    def apply_heal_aoe(self, healing):
        self.animals.sort(key=lambda x: x.hp)
        for i, animal in enumerate(self.animals):
            if animal.hp <= 0:
                continue
            animal.hp = min(animal.max_hp, animal.hp + healing)


def prompt_user(choice, options):
    print("Choose a {}:".format(choice))
    if type(options) == list:
        for i, option in enumerate(options):
            print("{} - {}".format(i, option))
        index = input(": ")
        return options[index]
    elif type(options) == dict:
        key_list = list(options.keys())
        for i, key in enumerate(key_list):
            print("{} - {}".format(i, key))
        index = input(": ")
        return options[key_list[i]]


def main(monster,attack):
    test_monster = Monster(monster)
    test_monster.attack(attack)
    #Alden = Character('Alden The Altruist')
    #print(vars(Alden))

    # test_monster_1 = Monster("adult-copper-dragon")
    # test_monster_2 = Monster("adult-white-dragon")
    # battle(test_monster_1, test_monster_2)
    # battle(test_monster_2, test_monster_1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate DnD Monsters, Characters, and More!')
    parser.add_argument('-m', '--monster',      type=str, default='wolf', help='the name of an animal to simulate')
    parser.add_argument('-s', '--size',         type=int, default=1,      help='how many animals in the pack?')
    parser.add_argument('-ac', '--ac',          type=int, default=10,     help='how many animals in the pack?')
    parser.add_argument('-a', '--advantage',    action="store_true",      help='how many animals in the pack?')
    parser.add_argument('-d', '--disadvantage', action="store_true",      help='how many animals in the pack?')
    args = parser.parse_args()

    #for animal_name in ANIMALS:
    #    animal = Animal(animal_name)
    #    print(animal)
    #    for name, attack in animal.attacks.items():
    #        print("    {}: {}".format(name, attack))
    #        print("        {}".format(attack.desc))

    #    print("")

    pack = Pack(args.monster, args.size)
    dmg = pack.attack(args.ac, args.advantage, args.disadvantage)
    print("Total damage = {}".format(dmg))

