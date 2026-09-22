#Amélioration a faire dans le code: permettre de pouvoir ajouter une key de plus
import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem)

file_path = sys.argv[1]
print("json file", file_path)

try:
    file = open(file_path)
    data = json.load(file)
    print(type(data))

except: 
    print(f"could not load data from {file_path}")

print(data[0].keys())

app = QApplication([])

tableau = QTableWidget()

tableau.setColumnCount(3)

#viens chercher les noms placés dans les keys 0, 1, 2.... et les ajoutent a colonne
colonne = list(data[0].keys())
tableau.setHorizontalHeaderLabels(colonne) 

#prend le nombre d'items et le transforme en quantité avant de prendre le chiffre pour set le nombre de ranger
ranger = list(data[0].items())
item_quantity = len(data)
print(item_quantity)
tableau.setRowCount(item_quantity)

#rempli le tableau
for i, item in enumerate(data):
    for b, value in enumerate(colonne):
        valeur = item.get(value, "") #si je comprend bien, cette ligne va chercher la value de l'item et stock dans valeur ce pour chaque itération
        tableau.setItem(i, b, QTableWidgetItem(str(valeur)))

#test pour voir si le json est malléable
for b, ranger in enumerate(data):  
       
    print(ranger)

    

window = QMainWindow();
window.setCentralWidget(tableau)
window.show()
sys.exit(app.exec())