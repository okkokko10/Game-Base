import QuickDirectory
from pygame import Vector2
from ComplexVector import CompVec
from TransformCanvas import *
import GetTextures
import Screen
import TransformCanvas
class Quaternion:
    r:float
    i:float
    j:float
    k:float
    def __init__(self,r,i,j,k):
        self.r=r
        self.i=i
        self.j=j
        self.k=k
    def mul(self,other):
        a=self
        b=other
        r=a.r*b.r-a.i*b.i-a.j*b.j-a.k*b.k
        i=a.i*b.r+a.r*b.i-a.k*b.j+a.j*b.k
        j=a.j*b.r+a.k*b.i+a.r*b.j-a.i*b.k
        k=a.k*b.r-a.j*b.i+a.i*b.j+a.r*b.k
        return Quaternion(r,i,j,k)
    pass
class Vector3(Quaternion):
    def __init__(self, i, j, k):
        super().__init__(0, i, j, k)
    def __add__(self,other):
        return Vector3(self.i+other.i,self.j+other.j,self.k+other.k)
class C_RaycastCamera(Component):
    pass

if __name__=='__main__':
    scene=Screen.Scene()
    cam=GameObject()
    cam.AddComponent(C_Camera(Transform(V0,V1/30),V1*800))
    scene.AddObject(cam)
    
    
    Screen.Display(V1*800).Loop(scene.ScreenUpdate)
