from PhysicsSim import *

class Projectile(GameObject):
    def __init__(self, posTr, velVec):
        super().__init__()
        self.AddComponent(PositionComponent(posTr))
        self.AddComponent(PhysicsComponent(velVec))
        color=(100,0,0)
        shape=LineSegment(Transform(V(0,0),V(1,0),posTr))
        self.AddComponent(ShapeComponent(shape,color))


if __name__=='__main__':
    tr=Transform(V(0,0),V(1/100,0))
    a=Scene(TrCanvas(V(800,800),tr))
    b=Display(V(800,800))
    a.AddObject(MoveCamera())
    
    a.AddObject(Projectile(Transform(V(-1,-1),V(3,0)),V(5,0)))
    a.AddObject(Projectile(Transform(V(-1,0),V(1,0)),V(5,0)))

    b.Loop(a.ScreenUpdate)        