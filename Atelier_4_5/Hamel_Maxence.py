import bpy
import sys
import random
import math


from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QWidget, QTableWidgetItem, QVBoxLayout, QLineEdit,\
        QMessageBox, QLabel, QSpinBox, QPushButton, QDoubleSpinBox, QHBoxLayout, QGroupBox, QFormLayout
from PySide6.QtCore import Qt

app = QApplication(sys.argv)

def delete_anciens_objets(): #si des anciens objets sont présents, les supprimer.
    collection = bpy.data.collections.get("Nouvelle_Collection")
    if collection:
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

def creer_nouvelle_collection():#quand il ny a pas d'objet, creer une nouvelle collection pour les objets generes
    collection = bpy.data.collections.get("Nouvelle_Collection")
    if collection is None:
        collection = bpy.data.collections.new("Nouvelle_Collection")
        bpy.context.scene.collection.children.link(collection)
    return collection

def box_des_choix(valeur=0.0):#je crois que c'est pour gérer les valeurs des box pour les positions et les tailles
    box = QDoubleSpinBox()
    box.setRange(-1000,1000)
    box.setDecimals(2)
    box.setSingleStep(0.5)
    box.setValue(valeur)
    return box

def nom_des_box(layout,nom,box_min,box_max):
    box_line = QHBoxLayout()
    box_line.addWidget(QLabel(nom))
    box_line.addWidget(box_min)
    box_line.addWidget(box_max)
    layout.addLayout(box_line)

def generation_objets():#genere les objets aleatoires selon les parametres choisis par l'utilisateur tout en gerant la suppression des anciens objets et la creation d'une nouvelle collection
    quantiter = spin_quantiter.value()


    #choix des position dans la box
    min_x, max_x = box_min_x.value(), box_max_x.value()
    min_y, max_y = box_min_y.value(), box_max_y.value()
    min_z, max_z = box_min_z.value(), box_max_z.value()

    min_scale = box_min_scale.value()
    max_scale = box_max_scale.value()

    bornes = [(min_x, max_x, "Position X"), (min_y, max_y, "Position Y"), (min_z, max_z, "Position Z"), (min_scale, max_scale, "Taille")]

    for minimum, maximum, nom in bornes:
        if minimum > maximum:
            QMessageBox.critical(None, "Erreur de bornes", f"La borne minimale pour {nom} est supérieure à la borne maximale.")
            return

    if min_scale <= 0 or max_scale <= 0:
        QMessageBox.critical(None, "Erreur de taille", "La taille minimale et maximale doit être supérieure à 0.")
        return
    
    #supprimer les objets existants avant de générer de nouveaux objets
    delete_anciens_objets()
    collection = creer_nouvelle_collection()

    primitives = ["CUBE", "SPHERE", "CYLINDER"]
    
    objets_presents = []
  


    for i in range(quantiter):
    

        position = (random.uniform(min_x, max_x), random.uniform(min_y, max_y), random.uniform(min_z, max_z))

        primitive = random.choice(primitives)



        if primitive == "CUBE":
            bpy.ops.mesh.primitive_cube_add(location=position)

        elif primitive == "SPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(location=position)

        elif primitive == "CYLINDER":
            bpy.ops.mesh.primitive_cylinder_add(location=position)

       
       
        objets = bpy.context.view_layer.objects.active
        objets.name = f"Objet_Aleatoire_{i+1}"

        for ancienne_collection in list(objets.users_collection):
            ancienne_collection.objects.unlink(objets)
        collection.objects.link(objets)

        #faire un scale aléatoire sur les objets creers
        taille = random.uniform(min_scale, max_scale)
        objets.scale = (taille, taille, taille)


        objets_presents.append(objets)

    QMessageBox.information(None, "Génération terminée", f"{len(objets_presents)} objets ont été générés avec succès.")

class Window(QMainWindow):
    def __init__(self):
        super().__init__() #creation widget
        self.setWindowTitle("Générateur d'objets aléatoires du Farwest")
        self.resize(400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        label_quantiter = QLabel("Quantité d'objets à générer :")
        layout.addWidget(label_quantiter)

        question_label = QLabel("Combien d'objets voulez-vous générer (de 1 à 10) ?")
        layout.addWidget(question_label)

        global spin_quantiter
        spin_quantiter = QSpinBox()
        spin_quantiter.setRange(1, 10)
        spin_quantiter.setValue(10)
        layout.addWidget(spin_quantiter)

        position_label = QGroupBox("Position des objets")
        position_layout = QVBoxLayout(position_label)
        layout.addWidget(position_label)

        global box_min_x, box_max_x, box_min_y, box_max_y, box_min_z, box_max_z
        box_min_x = box_des_choix(-5)
        box_max_x = box_des_choix(5)
        box_min_y = box_des_choix(-5)
        box_max_y = box_des_choix(5)
        box_min_z = box_des_choix(-5)
        box_max_z = box_des_choix(5)    

        nom_des_box(position_layout, "Position X :", box_min_x, box_max_x)
        nom_des_box(position_layout, "Position Y :", box_min_y, box_max_y) 
        nom_des_box(position_layout, "Position Z :", box_min_z, box_max_z)

        ajouter_box = [("Position X", box_min_x, box_max_x), ("Position Y", box_min_y, box_max_y), ("Position Z", box_min_z, box_max_z)]
        

        #creer les box pour le scale
        scale_labelg = QGroupBox("Taille des objets")
        scale_layout = QFormLayout(scale_labelg)

        global box_min_scale, box_max_scale
        box_min_scale = box_des_choix(0.5)
        box_max_scale = box_des_choix(2.0)

        scale_layout.addWidget(QLabel("Taille minimale :"))
        scale_layout.addWidget(box_min_scale)

        scale_layout.addWidget(QLabel("Taille maximale :"))
        scale_layout.addWidget(box_max_scale)
        

        layout.addWidget(scale_labelg)


        button_generer = QPushButton("Générer les objets")
        button_generer.clicked.connect(generation_objets)
        layout.addWidget(button_generer)

cube= bpy.data.objects.get("Cube")
if cube:
    bpy.data.objects.remove(cube, do_unlink=True)  # Supprimer l'objet initial de la scène

window = Window()
window.show()




    
    