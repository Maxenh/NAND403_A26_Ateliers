import bpy
import sys

#MISE A JOUR POSSIBLE
#j'ai manqué de temps, mais le code aurait pu être relié a pySide6 pour créer une interface qui nous permettraient d'entrer 
#la quantitée de section que nous voulons afin de régler la longueur de la cloture automatiquement. la hauteur des poteaux 
#pourraient elle aussi etre ajustable depuis l'interface. 









#Variables pour sa taille
longueur = 2
hauteur = 2
epaisseur = 0.12
qty_sections = 5

#supprimer le cube initial
bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)

#créer un groupe pour stocker tous les items qui seront créer
groupe = bpy.data.collections.get("fence")
#permet de mettre les objets qui sont necessaire a la scene mais pas de fence dans un autre groupe
#si je le met pas j'ai une erreur
if groupe is None:
    groupe=bpy.data.collections.new("fence")
    bpy.context.scene.collection.children.link(groupe)

#cree les pieces des différents items
def creer_piece(nom, position, dimensions):

    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    piece = bpy.context.object
    piece.name = nom
    piece.dimensions = dimensions

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    for obj in list(piece.users_collection):
        obj.objects.unlink(piece)
    groupe.objects.link(piece)

    return piece


for i in range(qty_sections):
    decal_x = i*longueur

    creer_piece(f"poteau{i}",(decal_x,0,hauteur/2),(epaisseur,epaisseur,hauteur))
    #faire les barreaux
    for j in (hauteur*0.50,hauteur*0.75):
        creer_piece(f"barreaux_{j}_{j:.2f}",(decal_x+longueur/2,0,j),(longueur,epaisseur,epaisseur))












