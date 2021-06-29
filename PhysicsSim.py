from ShapeDraw import *
import random
class PositionComponent(Component):
    def __init__(self,transform:Transform):
        self.transform=transform
    def TranslateVector(self,vec):
        self.transform.TranslateVector(vec)
class PhysicsComponent(Component):
    def __init__(self, velVec):
        self.velVec=velVec
        self.acceleration=V(0,0)
    def Update(self, gameObject, scene):
        self.UpdatePos(gameObject,scene.deltaTime)
        return super().Update(scene)
    def AccelerateVector(self,amount):
        self.acceleration+=amount
    def AccelerateTransform(self,tr):
        self.AccelerateVector(tr.detach().pos)
    def UpdatePos(self,gameObject,deltaTime):
        self.velVec+=self.acceleration*deltaTime/1000
        self.acceleration=V(0,0)
        gameObject.components[PositionComponent].TranslateVector(self.velVec*deltaTime/1000)
class testPhysicsParticle(PhysicsComponent):#not ready
    def __init__(self, posTr, mass, velVec):
        super().__init__(posTr, velVec)
        self.mass=mass
        shape=Circle(Transform(V(0,0),V(0.5,0),self.posTr))
        color=(
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255))
        self.visual=ShapeObject(shape,color)
    def Init(self, scene:Scene):
        scene.AddObject(self.visual)
        return super().Init(scene)
    def Update(self, scene:Scene):
        for o in scene.objects:
            if isinstance(o,PhysicsComponent) and not o == self:
                self.Attract(o)
        return super().Update(scene)
    def Attract(self,other):
        d=other.posTr.attach(self.posTr)
        o=d.pos*other.mass*self.mass/(d.pos.lengthSq())
        self.Accelerate(o/self.mass)
        pass

if __name__=='__main__':
    tr=Transform(V(0,0),V(1/100,0))
    a=Scene(TrCanvas(V(800,800),tr))
    b=Display(V(800,800))
    col=(100,100,100)
    
    a.AddObject(testPhysicsParticle(Transform(V(-1,1),V(1,0)),1,V(2,1)))
    a.AddObject(testPhysicsParticle(Transform(V(1,0),V(1,0)),1,V(0,0)))
    a.AddObject(MoveCamera())

    b.Loop(a.ScreenUpdate)        
        