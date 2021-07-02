from PhysicsSim import *

class Entity(GameObject):
    def __init__(self, posTr):
        super().__init__()
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_Inertia(V0))
class Projectile(GameObject):
    def __init__(self, posTr, velVec, size):
        super().__init__()
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_Inertia(velVec))
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_Inertia(velVec))
        color=(100,0,0)
        shape=LineSegment(Transform(V0,V(size,0),posTr))
        self.AddComponent(C_Shape(shape,color))
class Player(Projectile):
    def Update(self):
        if self.scene.inputs.IsKeyPressed(pygame.K_LSHIFT):
            k=self.scene.inputs.GetMousePos().detach().pos-self.GetComponent(C_Position).transform.detach().pos
            self.GetComponent(C_Inertia).AccelerateVectorGradual(k.normalize()*10)
        
        return super().Update()



if __name__=='__main__':
    a=Scene()
    
    a.AddObject(Projectile(Transform(V(-4,-4),V(1,0)),V0,8))
    a.AddObject(Projectile(Transform(V(4,-4),V(0,1)),V0,8))
    a.AddObject(Projectile(Transform(V(4,4),V(-1,0)),V0,8))
    a.AddObject(Projectile(Transform(V(-4,4),V(0,-1)),V0,8))
    p=Player(Transform(V(0,0),V(1,0)),V(0,0),1)
    tr=p.GetComponent(C_Position).transform
    t=Transform(V(0,0),V(1/100,0),tr)
    trCanvas=TrCanvas(V(800,800),t)
    p.AddComponent(C_Camera(trCanvas))
    a.AddObject(p)

    Display().Loop(a.ScreenUpdate)        