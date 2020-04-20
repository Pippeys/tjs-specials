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

    def parse_dice_string(self, dice_string):
        roll_strings = dice_string.split("+")
        for roll_string in roll_strings:
            self.dice.append([int(num) for num in roll_string.split("d")])

    def add_die(self, num, size):
        self.dice.append([num, size])

    def roll(self):
        total = self.mod
        for die_roll in self.dice:
            for die in range(die_roll[0]):
                total += random.randint(1, die_roll[1])
        return total

    def __str__(self):
        result = self.roll()
        dice_string = "+".join(["{}d{}".format(die_roll[0], die_roll[1]) for die_roll in self.dice])
        dice_string += "+{}".format(self.mod)
        return "{}: {} result = {}".format(self.name, dice_string, result)

        class Attack:

            def __init__(self, name, to_hit_mod, damage_string, damage_mod, damage_type):
                self.name = name
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


            def roll_to_hit(self):
                return self.to_hit.roll()

            def roll_for_damage(self):
                return self.for_damage.roll()

            def __str__(self):
                return "Attack Type: {} \nTo hit: {} \nDamage: {}".format(self.name, self.roll_to_hit(), self.roll_for_damage())

class Monster:
    def __init__(self,Name):
        self.attacks={}
        self.load_from_api(Name)
    # Function with in a class is a method
    def __str__(self):
        return 'Monster: {}, AC={}, Type={}'.format(self.Name,self.AC,self.Type)

    def add_attack(self, name, attack):
        self.attacks[name] = attack

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

class Alden:
    def __init__(self,AC,Health)

def Battle (Player,Monster,Player_Attack,Monster_Attack):


def main():
    Zombie = Monster('lion')
    print(Zombie)
    print(Zombie.attacks['Bite'])

if __name__ == '__main__':
    main()
