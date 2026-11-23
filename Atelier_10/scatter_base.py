import random
from maya import cmds
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt

"""
J'ai fait un outil pour scatter en temps réel les items dans le monde.
j'était entrein de retirer le bouton scatter completement puisque l'update se fait en temps réel.
mais maya a crash et je ne suis pas capable de le réouvrir pour tester si le code fonctionne toujours. 
normalement, lorsque l'on modifi les spinbox, l'objet se multiplie et se supprime en ordre de création.
le radius affecte tous les objets duppliqués et le seed permet de changer la position des objets.
le tout reste au dessus des autres fenêtres de maya.
"""




class Scatter(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scatter")
        self.setMinimumWidth(250)
        self.build_ui()


        self.source = None
        self.count_spin.valueChanged.connect(self.updated)
        self.radius_spin.valueChanged.connect(self.updated)
        self.seed_spin.valueChanged.connect(self.updated)

        selection = cmds.ls(selection=True, transforms=True)
        self.source = selection[0] if selection else None

    def on_top(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()

    def build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 100)
        self.count_spin.setValue(10)
        form.addRow("Copies", self.count_spin)

        self.radius_spin = QDoubleSpinBox()
        self.radius_spin.setRange(1.0, 50.0)
        self.radius_spin.setValue(10.0)
        form.addRow("Radius", self.radius_spin)

        self.seed_spin = QSpinBox()
        self.seed_spin.setRange(0, 9999)
        form.addRow("Seed", self.seed_spin)


    def updated(self, value=None):
        if self.source and cmds.objExists(self.source):
            self.generate_scatter()

    def generate_scatter(self):
        if not self.source or not cmds.objExists(self.source):
            return
        cmds.undoInfo(openChunk=True)
        try:
            if cmds.objExists("scatter_grp"):
                cmds.delete("scatter_grp")

            random.seed(self.seed_spin.value())
            radius = self.radius_spin.value()
            group = cmds.group(empty=True, name="scatter_grp")
            for i in range(self.count_spin.value()):
                copy = cmds.duplicate(self.source)[0]
                copy = cmds.parent(copy, group)[0]
                x = random.uniform(-radius, radius)
                z = random.uniform(-radius, radius)
                cmds.move(x, 0, z, copy, relative=True)
        finally:
            cmds.undoInfo(closeChunk=True)



def show_tool():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = Scatter()
    tool_window.show()
    tool_window.on_top()


show_tool()
