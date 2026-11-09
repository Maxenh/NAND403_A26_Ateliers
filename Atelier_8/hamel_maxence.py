#Eric a testé mon outil suivant et j'ai testé le siens, qui était super clair. 

#Voici mes instructions

#comment faire par soi-même l'atelier #8 
#1. Ouvrir maya
#2. Sélectionner l'engrenage en haut a gauche près des outils et cliquer sur new shelf.
#3. Nommer le shelf à convenance
#4. Ouvrir l'éditeur script en bas a droit ( icone ; )
#5. Copier coller le code joint plus bas.
#6. Avec CTRL+A prendre tout le code et le glisser dans le nouveau shelf créer précédement à l'aide du clique de la roulette de la souris.
#7. Click droit sur l'icone créer et sélectionner open.
#8. Cliquer sur l'icone du dossier, à coté de Icon name
#9. Vous pouvez ainsi choisir une image qui vous aidera a mieux identifier l'utilité de l'outil créer.
#10. Maintenant, en cliquant sur l'icone qui affiche votre super image, vous pouvez repousser l'ennemi sans crainte et en toute facilité.

#Voici le code

cmds.select(all=True)

ennemies= cmds.polyCube(
    name="Cavalerie",
    width=5,
    height=2,
    depth=3
)
cmds.move(0,1,0, ennemies[0])

cmds.cutKey(ennemies, clear=True)
cmds.playbackOptions(minTime=0,maxTime=100)

cmds.setKeyframe(ennemies,attribute=["translateX","translateZ"],value=0, time=10 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=1, time=10 )


cmds.setKeyframe(ennemies,attribute=["translateY"],value=8, time=12 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=9, time=13 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=9.5, time=15 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=9.5, time=30 )
cmds.setKeyframe(ennemies,attribute=["translateZ"],value=0, time=72 )

cmds.setKeyframe(ennemies,attribute=["translateX"],value=0, time=30 )
temps=0
position=-20
while temps <=35:
    cmds.setKeyframe(ennemies,attribute=["translateX"],value=position, time=temps+30 )
    temps+=7
    position *= -1

cmds.setKeyframe(ennemies,attribute=["translateX"],value=0, time=72 )


cmds.setKeyframe(ennemies,attribute=["translateY"],value=9.5, time=79 )
cmds.setKeyframe(ennemies,attribute=["translateZ"],value=-110, time=85 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=-90, time=100 )
cmds.setKeyframe(ennemies,attribute=["rotateX"],value=0, time=72 )
cmds.setKeyframe(ennemies,attribute=["rotateX"],value=-900, time=100)