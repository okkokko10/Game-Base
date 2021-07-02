from PhysicsSim import *
class C_Health(Component):
    def __init__(self,hp,defense=0,damageResistance=0) -> None:
        super().__init__()
        self.hp=hp
        self.defense=defense
        self.damageResistance=damageResistance
        self.buffs=[]
    def TakeDamage(self,amount):
        self.hp-=amount
        return
    def Heal(self,amount):
        self.hp+=amount
        return
    def O_OnUpdate(self):
        if self.hp<=0:
            self.gameObject
        return super().O_OnUpdate()

class Entity(GameObject):
    def __init__(self, posTr,hp):
        super().__init__()
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_Inertia(V0))
        self.AddComponent(C_Health(hp))
class Projectile(GameObject):
    def __init__(self, posTr, velVec, size, owner):
        super().__init__()
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_Inertia(velVec))
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_Inertia(velVec))
        color=(100,0,0)
        shape=LineSegment(Transform(V0,V(size,0),posTr))
        self.AddComponent(C_Shape(shape,color))
class Player(Entity):
    def O_OnUpdate(self):
        if self.scene.inputs.IsKeyPressed(pygame.K_LSHIFT):
            k=self.scene.inputs.GetMousePos().detach().pos-self.GetComponent(C_Position).transform.detach().pos
            self.GetComponent(C_Inertia).AccelerateVectorGradual(k.normalize()*10)
        
        return super().O_OnUpdate()
    

if __name__=='__main__':
    a=Scene()
    
    p=Player(Transform(V(0,0),V(1,0)),5)
    a.AddObject(Projectile(Transform(V(-4,-4),V(1,0)),V0,8,p))
    a.AddObject(Projectile(Transform(V(4,-4),V(0,1)),V0,8,p))
    a.AddObject(Projectile(Transform(V(4,4),V(-1,0)),V0,8,p))
    a.AddObject(Projectile(Transform(V(-4,4),V(0,-1)),V0,8,p))
    tr=p.GetComponent(C_Position).transform
    t=Transform(V(0,0),V(1/100,0),tr)
    trCanvas=TrCanvas(V(800,800),t)
    p.AddComponent(C_Camera(trCanvas))
    a.AddObject(p)

    Display().Loop(a.ScreenUpdate)        