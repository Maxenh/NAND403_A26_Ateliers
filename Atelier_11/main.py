import math

from maya import cmds
from maya import OpenMayaUI as omui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QSlider,
    QLabel,
    QPushButton,
)
from shiboken6 import wrapInstance


def maya_main_window():
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(pointer), QWidget)


class RockMaker(QDialog):
    def __init__(self):
        super().__init__(maya_main_window())
        self.setWindowTitle("Rock Maker")
        self.setMinimumWidth(260)
        self.build_ui()
        self.rock = None
        self.start_position =[]

    def build_ui(self):
        main_layout = QVBoxLayout(self)
        form = QFormLayout()
        main_layout.addLayout(form)

        self.subdivisions_slider = self.add_slider(form, "Subdivisions", 4, 64, 20)
        self.amplitude_slider = self.add_slider(form, "Amplitude", 0, 100, 30, divisor=100)
        self.frequency_slider = self.add_slider(form, "Frequency", 5, 80, 30, divisor=10)
        self.seed_slider = self.add_slider(form, "Seed", 0, 100, 0)

        self.amplitude_slider.valueChanged.connect(self.live_rocky)
        self.frequency_slider.valueChanged.connect(self.live_rocky)
        self.seed_slider.valueChanged.connect(self.live_rocky)

        create_button = QPushButton("Create rock")
        create_button.clicked.connect(self.make_rock)
        main_layout.addWidget(create_button)

    def add_slider(self, form, name, minimum, maximum, value, divisor=1):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(minimum, maximum)
        slider.setValue(value)

        value_label = QLabel(f"{value / divisor:g}")
        value_label.setMinimumWidth(30)
        slider.valueChanged.connect(lambda v: value_label.setText(f"{v / divisor:g}"))

        row = QHBoxLayout()
        row.addWidget(slider)
        row.addWidget(value_label)
        form.addRow(name, row)
        return slider

    def make_rock(self):
        self.create_rock(
            self.subdivisions_slider.value(),
            self.amplitude_slider.value() / 100,
            self.frequency_slider.value() / 10,
            self.seed_slider.value(),
        )

    def create_rock(self, subdivisions, amplitude, frequency, seed):
        # étape 1 : créer une sphère
        self.rocky=cmds.polySphere(radius=amplitude,subdivisionsX=subdivisions,subdivisionsY=subdivisions)[0]

        
        vert=cmds.ls(self.rocky+".vtx[*]",flatten=True)
        self.start_position=[]
        # étape 2 : faire une for loop sur chacun des vertices
        for i in vert:
            position=cmds.pointPosition(i,world=True)
            self.start_position.append(position)

        self.update_rocky(amplitude,frequency,seed)

        pass
    def update_rocky(self, amplitude,frequency,seed):
        vert = cmds.ls(self.rocky+".vtx[*]", flatten=True)
        for j, vertex in enumerate(vert):
            position = self.start_position[j]
            x = position[0]
            y = position[1]
            z = position[2]
            bump= self.get_bump(x,y,z, frequency, seed)
            direct_vert=math.sqrt(x*x+y*y+z*z) #trouve la direction vers où déplacer le vertice
            if direct_vert==0:
                print("error on vertice")
                continue
            norm_x= x/direct_vert
            norm_y= y/direct_vert
            norm_z= z/direct_vert

            dist=amplitude*0.5
            
            new_x= x + norm_x * bump * dist
            new_y= y + norm_y * bump * dist
            new_z= z + norm_z * bump * dist
            
            cmds.xform(vertex, worldSpace=True, translation=(new_x,new_y,new_z))


    def live_rocky(self):
        if self.rocky is None:
            return
        self.update_rocky(self.amplitude_slider.value()/100, self.frequency_slider.value(),self.seed_slider.value())

    def get_bump(self, x, y, z, frequency, seed):
        return (math.sin(x * frequency + seed)
                + math.sin(y * frequency + seed * 2)
                + math.sin(z * frequency + seed * 3)) / 3


def show_tool():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = RockMaker()
    tool_window.show()


show_tool()
