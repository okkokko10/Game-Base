from ShapeDraw import *
import random
class PhysicsParticle(ShapeObject):
    def __init__(self, posTr, mass, velVec):
        self.posTr,self.mass,self.velVec=posTr,mass,velVec
        self.shape=Circle(self.posTr)
        self.color=(
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255))
        self.acceleration=V(0,0)
    def Update(self, scene):
        for o in scene.objects:
            if isinstance(o,PhysicsParticle) and not o == self:
                self.Attract(o)
        self.Move(scene.deltaTime)
        return super().Update(scene)
    def Accelerate(self,amount):
        self.acceleration+=amount
    def Attract(self,other):
        d=other.posTr.attach(self.posTr)
        o=d.pos*other.mass*self.mass/(d.pos.lengthSq())
        self.Accelerate(o)
        pass
    def Move(self,deltaTime):
        self.velVec+=self.acceleration*deltaTime/1000
        self.acceleration=V(0,0)
        self.posTr.pos+=self.velVec/self.mass*deltaTime/1000


if __name__=='__main__':
    tr=Transform(V(0,0),V(1/100,0))
    a=Scene(TrCanvas(V(800,800),tr))
    b=Display(V(800,800))
    col=(100,100,100)
    
    a.AddObject(PhysicsParticle(Transform(V(-1,1),V(1,0)),1,V(2,1)))
    a.AddObject(PhysicsParticle(Transform(V(1,0),V(1,0)),1,V(0,0)))
    a.AddObject(MoveCamera())

    b.Loop(a.ScreenUpdate)        
        