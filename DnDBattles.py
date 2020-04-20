import sys
import random
import re
import requests
from pprint import pprint


class Roll:

    def __init__(self, name, dice_string, mod):
        self.name = name
        self.dice = []
        self.parse_dice_string(dice_string)
        self.mod = mod
        self.max = sum([die_roll[1] for die_roll in self.dice]) + self.mod
        self.critical = False

    def parse_dice_string(self, dice_string):
        roll_strings = dice_string.split("+")
        for roll_string in roll_strings:
            self.dice.append([int(num) for num in roll_string.split("d")])

    def make_critical(self):
        self.critical = True

    def roll(self):
        total = self.mod
        if self.critical:
            dice = [[die_roll[0]*2, die_roll[1]] for die_roll in self.dice]
        else:
            dice = self.dice

        for die_roll in dice:
            for die in range(die_roll[0]):
                total += random.randint(1, die_roll[1])

        self.critical = False
        return total

    def __str__(self):
        result = self.roll()
        dice_string = "+".join(["{}d{}".format(die_roll[0], die_roll[1]) for die_roll in self.dice])
        dice_string += "+{}".format(self.mod)
        return "{}: {} result = {}".format(self.name, dice_string, result)


class Attack:

    def __init__(self, name, to_hit_mod, damage_string, damage_mod, damage_type, has_advantage=False):
        self.name = name
        self.to_hit_mod = to_hit_mod
        self.damage_string = damage_string
        self.damage_mod = damage_mod
        self.to_hit = Roll(
                "{} to hit".format(self.name),
                "1d20",
                to_hit_mod
            )
        self.for_damage = Roll(
                "{} for damage".format(self.name),
                damage_string,
                damage_mod
            )
        self.has_advantage = has_advantage

    def give_advantage(self):
        self.has_advantage = True

    def roll_to_hit(self):
        to_hit_result = self.to_hit.roll()

        if self.has_advantage:
            second_roll = self.to_hit.roll()
            to_hit_result = max([to_hit_result, second_roll])

        if to_hit_result == self.to_hit.max:
            self.for_damage.make_critical()
        return to_hit_result

    def roll_for_damage(self):
        return self.for_damage.roll()

    def __str__(self):
        return "{}: To hit=1d20+{}, Damage={}+{}".format(self.name, self.to_hit_mod, self.damage_string, self.damage_mod)

    def attack(self):
        return self.roll_to_hit(), self.roll_for_damage()


class Monster:
    def __init__(self,Name):
        self.attacks={}
        self.load_from_api(Name)
    # Function with in a class is a method
    def __str__(self):
        return 'Monster: {}, AC={}, Type={}'.format(self.Name,self.AC,self.Type)

    def add_attack(self, name, attack):
        self.attacks[name] = attack

    def attack(self, name):
        if name in self.attacks:
            print(self)
            print(self.attacks[name])
            print(self.attacks[name].attack())
        else:
            print("ERROR: Attack {} not found for {}".format(name, self.Name))
            print("    Available attacks:")
            for key in self.attacks.keys():
                print("    --> {}".format(self.attacks[key]))
            sys.exit()

    def load_from_api(self,api_index):
        url = 'http://www.dnd5eapi.co/api/monsters/'+api_index
        response = requests.get(url).json()
        self.AC = response['armor_class']
        self.Type = response['type']
        self.Name = response['name']
        self.Health = response['hit_points']

        for i in response['actions']:
            try:
                self.add_attack(i['name'], Attack(i['name'],i['attack_bonus'],i['damage'][0]['damage_dice'],
                       i['damage'][0]['damage_bonus'],i['damage'][0]['damage_type']['name']))
            except KeyError:
                continue


class Character:
    def __init__(self,):
        self.load_from_char_sheet(Name,AC,Ini,)


def Battle (Player,Monster,Player_Attack,Monster_Attack):
    pass


def main():
    test_monster = Monster('lion')
    test_monster.attack('Bit')


if __name__ == '__main__':
    main()
