from ShapeDraw import *
import random
class C_Inertia(Component):
    def __init__(self, velVec):
        self.velVec=velVec
        self.acceleration=V(0,0)
        self.accelerationGradual=V(0,0)
    def O_OnUpdate(self):
        self.UpdatePos()
        return super().O_OnUpdate()
    def AccelerateVector(self,amount):
        self.acceleration+=amount
    def AccelerateTransform(self,tr):
        self.AccelerateVector(tr.detach().pos)
    def AccelerateVectorGradual(self,amount):
        self.accelerationGradual+=amount
    def AccelerateTransformGradual(self,tr):
        self.AccelerateVectorGradual(tr.detach().pos)
    def UpdatePos(self):
        deltaTime=self.gameObject.scene.deltaTime
        self.velVec+=self.accelerationGradual*deltaTime/1000+self.acceleration
        self.acceleration=V(0,0)
        self.accelerationGradual=V(0,0)
        self.gameObject.GetComponent(C_Position).TranslateVector(self.velVec*deltaTime/1000)
# class testPhysicsParticle(C_Inertia):#not ready
#     def __init__(self, posTr, mass, velVec):
#         super().__init__(posTr, velVec)
#         self.mass=mass
#         shape=Circle(Transform(V(0,0),V(0.5,0),self.posTr))
#         color=(
#         random.randint(0,255),
#         random.randint(0,255),
#         random.randint(0,255))
#         self.visual=ShapeObject(shape,color)
#     def Init(self, scene:Scene):
#         scene.AddObject(self.visual)
#         return super().O_OnInit(scene)
#     def Update(self, scene:Scene):
#         for o in scene.objects:
#             if isinstance(o,C_Inertia) and not o == self:
#                 self.Attract(o)
#         return super().Update(scene)
#     def Attract(self,other):
#         d=other.posTr.attach(self.posTr)
#         o=d.pos*other.mass*self.mass/(d.pos.lengthSq())
#         self.Accelerate(o/self.mass)
#         pass

# if __name__=='__main__':
#     tr=Transform(V(0,0),V(1/100,0))
#     a=Scene(TrCanvas(V(800,800),tr))
#     b=Display(V(800,800))
#     col=(100,100,100)
    
#     a.AddObject(testPhysicsParticle(Transform(V(-1,1),V(1,0)),1,V(2,1)))
#     a.AddObject(testPhysicsParticle(Transform(V(1,0),V(1,0)),1,V(0,0)))
#     a.AddObject(MoveCamera())

#     b.Loop(a.ScreenUpdate)        
        