import maya.cmds as cmds

cmds.select(all=True)
cmds.delete()
#créer le cube et le place au point d'origine sur le sol
ennemies= cmds.polyCube(
    name="Cavalerie",
    width=5,
    height=2,
    depth=3
)
cmds.move(0,1,0, ennemies[0])

cmds.cutKey(ennemies, clear=True)
cmds.playbackOptions(minTime=0,maxTime=100)

#wait 
cmds.setKeyframe(ennemies,attribute=["translateX","translateZ"],value=0, time=10 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=1, time=10 )

#floating

cmds.setKeyframe(ennemies,attribute=["translateY"],value=8, time=12 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=9, time=13 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=9.5, time=15 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=9.5, time=30 )
cmds.setKeyframe(ennemies,attribute=["translateZ"],value=0, time=72 )

#left right swing
cmds.setKeyframe(ennemies,attribute=["translateX"],value=0, time=30 )
temps=0
position=-20
while temps <=35:
    cmds.setKeyframe(ennemies,attribute=["translateX"],value=position, time=temps+30 )
    temps+=7
    position *= -1

cmds.setKeyframe(ennemies,attribute=["translateX"],value=0, time=72 )



#throwing

cmds.setKeyframe(ennemies,attribute=["translateY"],value=9.5, time=79 )
cmds.setKeyframe(ennemies,attribute=["translateZ"],value=-110, time=85 )
cmds.setKeyframe(ennemies,attribute=["translateY"],value=-90, time=100 )
cmds.setKeyframe(ennemies,attribute=["rotateX"],value=0, time=72 )
cmds.setKeyframe(ennemies,attribute=["rotateX"],value=-900, time=100 )