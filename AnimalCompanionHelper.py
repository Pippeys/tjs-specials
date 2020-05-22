import sys
import DnDBattles as dnd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import pprint

ANIMALS = [
        "elk",
        "constrictor-snake",
        "draft-horse",
        "flying-snake",
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
        self.outputAttack.setReadOnly(True)
        self.inputTargetAC.setValue(12)

        # Connect widgets to methods
        #
        self.buttonLoadPack.clicked.connect(self.loadPack)
        self.buttonAttack.clicked.connect(self.attack)

    def loadPack(self):
        animalName = self.inputAnimalName.currentText()
        animalNum  = self.inputAnimalNum.value()
        self.pack = dnd.Pack(animalName, animalNum)
        animalInfo = pprint.pformat(self.pack.info)

        #TODO format outputAnimalInfo better
        self.outputAnimalInfo.setText(animalInfo)

        self.inputAttackName.clear()
        self.inputAttackName.addItems(list(self.pack.animals[0].attacks.keys()))
        self.outputAttack.clear()

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
        for result in dmg_results:
            self.outputAttack.append("{} attacks with {}...".format(self.pack.animals[0].name, attack))
            if result["hit"] == False:
                self.outputAttack.append("    {} misses!".format(result["to_hit"]))
            else:
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
        for dmg_type, dmg in dmg_totals.items():
            self.outputAttack.append("    {}: {} damage".format(dmg_type, sum(dmg)))

        self.outputAttack.append("\n{}".format(self.pack.chosen_attack.desc))

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
        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

