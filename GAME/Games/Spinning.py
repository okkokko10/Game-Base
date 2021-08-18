import quickDirectory

from BC.PhysicsSim import *
from BC.ComplexVector import CompVec
import BC.GetTextures

class C_SpinnerInertia(Component):
    def __init__(self,startVel,lock=None) -> None:
        super().__init__()
        self.velVec=startVel
        self.lock=lock
    def O_OnPreUpdate(self):
        self.LockToClosest()
        if self.lock:
            self.Lock(self.lock)
        self.gameObject.GetComponent(C_Position).transform.TranslateVector(self.velVec)
        return super().O_OnPreUpdate()
    def Lock(self,lockVec):
        length=abs(self.velVec)
        if length==0:
            return
        tr=self.gameObject.GetComponent(C_Position).transform
        if False:
            direction=Transform(lockVec,V1).attach(tr).pos
            if direction==V0:
                return
            facing=Transform(V0,direction,tr)
            towards=Transform(V0,self.velVec).attach(facing)
            towards.rot=V(0,towards.rot.y)
            self.velVec=towards.detach().rot.normalize()*length
        else:
            pos=tr.detach().pos
            diff=lockVec-pos
            a=self.velVec/diff
            b=V(0,a.y)*diff
            self.velVec=b.normalize()*length
    def LockToClosest(self):
        pos=self.gameObject.GetComponent(C_Position).transform.detach().pos
        l=self.gameObject.scene.GetAllComponents(C_SpinnerInertia)
        positions=[]
        for i in range(len(l)):
            positions.append(l[i].gameObject.GetComponent(C_Position).transform.detach().pos)
        closestD=0
        closest=None
        for i in range(len(l)):
            d=(positions[i]-pos).lengthSq()
            if (d<closestD or closestD==0) and d!=0:
                d=closestD
                closest=i
        if closest:
            self.lock=l[closest].gameObject.GetComponent(C_Position).transform.detach().pos

class Spinner(GameObject):
    def __init__(self, posTr,velVec):
        super().__init__()
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_SpinnerInertia(velVec))
        self.AddComponent(C_DrawTexture(Transform(V0,V1/30,posTr),0))


class C_Spinners(Component):
    def __init__(self) -> None:
        super().__init__()


if __name__=='__main__':
    scene=Scene()
    display=Display((800,800))
    cam=GameObject()
    cam.AddComponent(C_Camera(Transform(V0,V1/50),(800,800)))
    scene.AddObject(cam)
    scene.AddObject(Spinner(Transform(-V1*2,V1),-2*V1))
    scene.AddObject(Spinner(Transform(V1,V1),V1))
    scene.AddObject(Spinner(Transform(V(1,3),V1),V1))
    scene.AddObject(Spinner(Transform(V(0,1),V1),V1))

    display.Loop(scene.ScreenUpdate,50)        