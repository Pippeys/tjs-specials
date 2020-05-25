import sys
import DnDBattles as dnd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import pprint
import re

ANIMALS = [
        "brown-bear",
        "constrictor-snake",
        "dire-wolf",
        "draft-horse",
        "elk",
        "flying-snake",
        "giant-elk",
        "giant-frog",
        "giant-constrictor-snake",
        "wolf"
    ]

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("AnimalCompanionHelper.ui", self)

        # Available widgets
        #
        #     self.inputAnimalName
        #     self.inputAnimalNum
        #     self.buttonLoadPack
        #     self.outputAnimalInfo
        #     self.inputAdvantage
        #     self.inputDisadvantage
        #     self.inputTargetAC
        #     self.inputAttackName
        #     self.buttonAttack
        #     self.outputAttack

        # Initialize properties
        #
        self.pack = None

        # Configure widget properties
        #
        self.inputAnimalName.addItems(ANIMALS)
        self.inputAnimalName.setCurrentIndex(self.inputAnimalName.findText("wolf"))
        self.inputAnimalNum.setMinimum(1)
        self.inputAnimalNum.setValue(4)
        self.outputAnimalInfo.setReadOnly(True)
        self.outputAnimalInfo.setCurrentFont(QtGui.QFont("Courier New", 8))
        self.outputAttack.setReadOnly(True)
        self.inputTargetAC.setValue(12)

        # Connect widgets to methods
        #
        self.buttonLoadPack.clicked.connect(self.loadPack)
        self.buttonAttack.clicked.connect(self.attack)
        self.buttonDamage.clicked.connect(self.damage)
        self.buttonHeal.clicked.connect(self.heal)

    def loadPack(self):
        animalName = self.inputAnimalName.currentText()
        animalNum  = self.inputAnimalNum.value()
        self.pack = dnd.Pack(animalName, animalNum)
        self.formatAnimalInfo()

        self.inputAttackName.clear()
        self.inputAttackName.addItems(list(self.pack.animals[0].attacks.keys()))
        self.outputAttack.clear()

        self.outputHitPoints.clear()
        self.outputHitPoints.setColumnCount(1)
        self.outputHitPoints.setRowCount(len(self.pack.animals))
        if self.inputMightySummoner.checkState():
            self.applyMightySummoner()
        self.updateHitPoints()

    def updateHitPoints(self):
        for i, animal in enumerate(self.pack.animals):
            self.outputHitPoints.setItem(i, 0, QtWidgets.QTableWidgetItem(str(animal.hp)))

    def applyMightySummoner(self):
        extra_hp = 2 * int(self.pack.info["hit_dice"].split("d")[0])
        for i, animal in enumerate(self.pack.animals):
            animal.max_hp = animal.max_hp + extra_hp
            animal.hp = animal.hp + extra_hp

    def formatAnimalInfo(self):
        info = self.pack.info
        speed_str  = ", ".join(["{} {}".format(k, v) for k, v in info["speed"].items()])
        senses_str = ", ".join(["{} {}".format(k, v) for k, v in info["senses"].items()])
        try:
            specials_str = "\n\n".join(["<b>{}</b>: {}<br><br>".format(d["name"], d["desc"]) for d in info["special_abilities"]])
        except KeyError:
            specials_str = "None<br>"
        actions_str  = "\n\n".join(["<b>{}</b>: {}<br><br>".format(d["name"], d["desc"]) for d in info["actions"]])

        animalCleanInfo = """Name: {}
Armor Class: {}
 Hit Points: {}
      Speed: {}

        STR   DEX   CON   INT   WIS   CHA
         {:2d}    {:2d}    {:2d}    {:2d}    {:2d}    {:2d}
        ({})  ({})  ({})  ({})  ({})  ({})

Senses: {}
    CR: {}/{}""".format(
                info["name"],
                info["armor_class"],
                info["hit_points"],
                speed_str,
                info["strength"],
                info["dexterity"],
                info["constitution"],
                info["intelligence"],
                info["wisdom"],
                info["charisma"],
                mod(info["strength"]),
                mod(info["dexterity"]),
                mod(info["constitution"]),
                mod(info["intelligence"]),
                mod(info["wisdom"]),
                mod(info["charisma"]),
                senses_str,
                str(float(info["challenge_rating"]).as_integer_ratio()[0]),
                str(float(info["challenge_rating"]).as_integer_ratio()[1])
            )

        animalComplexInfo = """<html><p style="font-family:'Courier New';font-size:12px">
_________________________________________________<br><br>
{}
_________________________________________________<br><br>
{}
<br>
</p></html>""".format(
                specials_str,
                actions_str
        )

        self.outputAnimalInfo.setText(animalCleanInfo)
        self.outputAnimalInfo.append(animalComplexInfo)

    def attack(self):
        if not self.isLoaded():
            return

        self.outputAttack.clear()

        # Load current options for attack
        #
        adv    = self.inputAdvantage.checkState()
        dis    = self.inputDisadvantage.checkState()
        ac     = self.inputTargetAC.value()
        attack = self.inputAttackName.currentText()

        dmg_results = self.pack.attack(attack, ac, adv, dis)
        dmg_totals = {}
        total_hits = 0
        for result in dmg_results:
            self.outputAttack.append("{} attacks with {}...".format(self.pack.animals[0].name, attack))
            if result["hit"] == False:
                self.outputAttack.append("    {} misses!".format(result["to_hit"]))
            else:
                total_hits += 1
                if result["crit"]:
                    self.outputAttack.append("    {} is a critical hit!".format(result["to_hit"]))
                else:
                    self.outputAttack.append("    {} hits!".format(result["to_hit"]))

                for dmg in result["dmg"]:
                    self.outputAttack.append("    {} {} damage!".format(dmg["dmg"], dmg["type"].lower()))
                    if dmg["type"] not in dmg_totals.keys():
                        dmg_totals[dmg["type"]] = [dmg["dmg"]]
                    else:
                        dmg_totals[dmg["type"]].append(dmg["dmg"])

        self.outputAttack.append("TOTALS:")
        self.outputAttack.append("    Successful hits: {}".format(total_hits))
        for dmg_type, dmg in dmg_totals.items():
            self.outputAttack.append("    {}: {} damage".format(dmg_type, sum(dmg)))

        attack_desc = re.search(r".*(Hit: .*)", self.pack.chosen_attack.desc)
        if attack_desc: 
            self.outputAttack.append("\n{}".format(attack_desc.group(1)))

    def damage(self):
        if not self.isLoaded():
            return
        if self.inputDamageAOE.checkState():
            self.pack.apply_damage_aoe(self.inputDamage.value())
        else:
            self.pack.apply_damage(self.inputDamage.value())
        self.updateHitPoints()

    def heal(self):
        if not self.isLoaded():
            return
        if self.inputHealAOE.checkState():
            self.pack.apply_heal_aoe(self.inputHeal.value())
        else:
            self.pack.apply_heal(self.inputHeal.value())
        self.updateHitPoints()

    def isLoaded(self):
        if self.pack is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setInformativeText("Load an animal dummy.")
            msg.setWindowTitle("No Pack")
            msg.exec_()
            return False
        else:
            return True

def mod(stat):
    return "{:+}".format(int((stat-10)/2))

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
