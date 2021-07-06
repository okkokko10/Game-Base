from ComplexVector import CompVec
from PhysicsSim import *
import GetTextures
class C_Health(Component):
    def __init__(self,hp,defense=0,damageResistance=0) -> None:
        super().__init__()
        self.hp=hp
        self.defense=defense
        self.damageResistance=damageResistance
        self.buffs=[]
    def TakeTrueDamage(self,amount):
        self.hp-=amount
        return
    def Heal(self,amount):
        self.hp+=amount
        return
    def O_OnUpdate(self):
        if self.hp<=0:
            self.gameObject.Remove()
        return super().O_OnUpdate()
class C_Hitbox(Component):
    shape:Shape
    touching:dict
    def __init__(self,shape) -> None:
        super().__init__()
        self.shape=shape
        self.touching={}
    def O_OnPreUpdate(self):
        self.updateTouching()
        return super().O_OnPreUpdate()
    def updateTouching(self):
        self.touching={}
        for o in self.gameObject.scene.objects:
            assert(isinstance(o,GameObject))
            if C_Hitbox in o.components:
                if True:
                    otherShape=o.components[C_Hitbox].shape
                    intersection=self.shape.Intersect(otherShape)
                    if intersection:
                        self.touching[o]=intersection
    def GetTouching(self):
        return self.touching
class C_ContactDamage(Component):
    def __init__(self,amount) -> None:
        super().__init__()
        self.amount=amount
    def O_OnUpdate(self):
        hitbox=self.gameObject.GetComponent(C_Hitbox)
        hits=hitbox.GetTouching()
        for h in hits:
            assert(isinstance(h,GameObject))
            if h.HasComponent(C_Health):
                h.GetComponent(C_Health).TakeTrueDamage(self.amount)
        return super().O_OnUpdate()


class Entity(GameObject):
    def __init__(self, posTr,hp,shape):
        super().__init__()
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_Inertia(V0))
        self.AddComponent(C_Hitbox(shape))
        self.AddComponent(C_Health(hp))
class Projectile(GameObject):
    def __init__(self, posTr, velVec, size, owner=None,maxAge=2000):
        super().__init__()
        self.owner=owner
        self.AddComponent(C_Position(posTr))
        self.AddComponent(C_Inertia(velVec))
        color=(100,0,0)
        #shape=LineSegment(Transform(V0,V(size,0),posTr))
        self.maxAge=maxAge
        #self.AddComponent(C_Hitbox(shape))
        #self.AddComponent(C_ContactDamage(1))
    def O_OnUpdate(self):
        if self.GetAge()>self.maxAge>=0:
            self.Remove()
        return super().O_OnUpdate()
class Player(Entity):
    def __init__(self, posTr, hp):
        shape=Circle(Transform(V0,V1/2,posTr))
        super().__init__(posTr, hp, shape)
        self.AddComponent(C_DrawTexture(Transform(V0,V1/20,posTr),2))
    def O_OnUpdate(self):
        for i in range(1):
            amb=AmbientParticle(self.GetComponent(C_Position).transform.copy())
            self.scene.AddObject(amb)
        selfPos=self.GetComponent(C_Position).transform.detach().pos
        k=self.scene.inputs.GetMousePos().detach().pos-selfPos
        k=k.normalize()
        trTx=self.GetComponent(C_DrawTexture).transform
        trTx.rot=Transform(V0,k).attach(tr).rot/20
        if self.scene.inputs.IsKeyDown(pygame.K_LSHIFT):
            self.GetComponent(C_Inertia).velVec=V0
            self.GetComponent(C_Inertia).AccelerateVector(k*20)
            posTr=Transform(selfPos,k).attach(self.GetComponent(C_Position).transform)
            p=Projectile(posTr,k*0 ,1,self,200)
            Transform(V1*0,V1/20,posTr)
            p.AddComponent(C_DrawTexture(self.GetComponent(C_DrawTexture).transform,3))
            self.scene.AddObject(p)
        selfPos=self.GetComponent(C_Position).transform.detach().pos
        v=self.GetComponent(C_Inertia).velVec
        maxspeed=10
        acceleration=25
        moved=False
        if self.scene.inputs.IsKeyPressed(pygame.K_a) and v.x>-maxspeed:
            self.GetComponent(C_Inertia).AccelerateVectorGradual(V(-acceleration,0))
            moved=True
        if self.scene.inputs.IsKeyPressed(pygame.K_d) and v.x<maxspeed:
            self.GetComponent(C_Inertia).AccelerateVectorGradual(V(acceleration,0))
            moved=True
        if self.scene.inputs.IsKeyPressed(pygame.K_s) and v.y<maxspeed:
            self.GetComponent(C_Inertia).AccelerateVectorGradual(V(0,acceleration))
            moved=True
        if self.scene.inputs.IsKeyPressed(pygame.K_w) and v.y>-maxspeed:
            self.GetComponent(C_Inertia).AccelerateVectorGradual(V(0,-acceleration))
            moved=True
        if self.scene.inputs.IsKeyDown(pygame.K_SPACE):
            self.GetComponent(C_Inertia).velVec=V0
        # if selfPos.y>0:
        #     self.GetComponent(C_Inertia).velVec=V(v.x,0*v.y)
        #     self.GetComponent(C_Position).TranslateVector(V(0,-selfPos.y))
        # elif selfPos.y<0:
        #     self.GetComponent(C_Inertia).AccelerateVectorGradual(V(0,10))
        # if self.scene.inputs.IsKeyDown(pygame.K_SPACE) and self.GetComponent(C_Position).transform.detach().pos.y==0:
        #     self.GetComponent(C_Inertia).AccelerateVector(V(0,-10))
        
        return super().O_OnUpdate()
class WormSegment(Entity):
    def __init__(self, posTr, head:GameObject, nextSegment:GameObject):
        super().__init__(posTr,1,Circle(Transform(V0,V1/3,posTr)))
        self.head=head
        self.next=nextSegment
        
        self.components[C_Health]=head.components[C_Health]
        self.AddComponent(C_DrawTexture(Transform(V0,V1/30,posTr),4))
    def Direction(self):
        nextpos=self.next.GetComponent(C_Position).transform.detach().pos
        selfpos=self.GetComponent(C_Position).transform.detach().pos
        return nextpos-selfpos
    def SpringForce(self):
        d=self.Direction()
        if abs(d)>1:
            f=d*(1-1/abs(d))
            self.GetComponent(C_Position).TranslateVector(f)
        #self.GetComponent(C_Inertia).AccelerateVectorGradual(d.normalize())
        if d!=V0:
            b=d.normalize()
            tr=self.GetComponent(C_Position).transform
            tr.rot=Transform(V0,b).attach(tr).detachOnce().rot
    def Shoot(self,atVec):
        tr=self.GetComponent(C_Position).transform.detach()
        atPos=atVec#atTr.detach().pos
        vel=atPos-tr.pos
        vel=vel.normalize()
        #vel=self.Direction()*V(0,1)
        tr.rot=vel
        projectile=Projectile(tr,vel*10,1,self,4000)
        projectile.AddComponent(C_DrawTexture(Transform(V0,V1/20,tr),6))
        self.scene.AddObject(projectile)
    def O_OnDraw(self, canvas) -> None:
        return #super().O_OnDraw(canvas)
class WormHead(Entity):
    def __init__(self, posTr, hp, segments):
        super().__init__(posTr, hp, Circle(Transform(V0,V1/2,posTr)))
        self.segments=[WormSegment(posTr.copy(),self,self)]
        for i in range(segments):
            self.segments.append(WormSegment(posTr.copy(),self,self.segments[-1]))
        self.AddComponent(C_DrawTexture(Transform(V0,V1/30,posTr),5))
        self.shots=0
    def O_OnInit(self):
        for i in range(len(self.segments)):
            self.scene.AddObject(self.segments[i])
        return super().O_OnInit()
    def O_OnRemove(self):
        for o in self.segments:
            o.Remove()
        return super().O_OnRemove()
    def O_OnUpdate(self):
        super().O_OnUpdate()
        player=None
        for o in self.scene.objects:
            if isinstance(o,Player):
                player=o
        if player:
            playerPos=player.GetComponent(C_Position).transform.detach().pos
            selfPos=self.GetComponent(C_Position).transform.detach().pos
            d=playerPos-selfPos
            f=d.normalize()
            self.ShootOne(playerPos)
            #self.ShootOne(playerPos)
            self.GetComponent(C_Inertia).AccelerateVectorGradual(d)
            if True:
                segPos=self.segments[0].GetComponent(C_Position).transform.detach().pos
                b=-(segPos-selfPos).normalize()
                if b!=V0:
                    tr=self.GetComponent(C_Position).transform
                    tr.rot=Transform(V0,b).attach(tr).detachOnce().rot
                self.GetComponent(C_Inertia).AccelerateVectorGradual(self.GetComponent(C_Position).transform.detach().rot)
            v=self.GetComponent(C_Inertia).velVec
            if v.lengthSq()>100:
                self.GetComponent(C_Inertia).AccelerateVectorGradual(-v/10)
            if abs(d)>15:
                #self.ShootAll(player.GetComponent(C_Position).transform)
                #self.GetComponent(C_Position).TranslateVector(f*(abs(d)-15))
                #self.GetComponent(C_Inertia).velVec=V0
                pass
            if abs(d.x)>10:
                pass#self.GetComponent(C_Inertia).AccelerateVectorGradual(V(d.x,15))
            if abs(d.x)<10 and False:
                v=self.GetComponent(C_Inertia).velVec
                a=0.95
                if f.y*v.y>0:
                    a=1.05
                self.GetComponent(C_Inertia).velVec=V(v.x*1,v.y*a)
            if selfPos.y<0:
                #self.GetComponent(C_Inertia).AccelerateVectorGradual(V(0,15))
                pass
            else:
                f=V(f.x,f.y*5)
            #self.GetComponent(C_Inertia).AccelerateVectorGradual(f*5)
            if self.scene.inputs.IsKeyDown(pygame.K_e):
                self.ShootAll(playerPos)
        self.UpdateTail()
    def ShootAll(self,atVec):
        for o in self.segments:
            o.Shoot(atVec)
    def UpdateTail(self):
        for i in range(len(self.segments)):
            self.segments[i].SpringForce()
    def O_OnDraw(self, canvas) -> None:
        for i in range(len(self.segments)):
            super(Entity,self.segments[i]).O_OnDraw(canvas)
            
        return super().O_OnDraw(canvas)
    def ShootOne(self,atVec):
        self.shots-=1
        self.shots%=len(self.segments)
        if self.shots==0:
            self.ShootAll(atVec)
        else:
            self.segments[self.shots].Shoot(atVec)
class AmbientParticle(Projectile):
    def __init__(self, posTr):
        velVec=V0
        size=1
        owner=None
        maxAge=2000
        randVec=(V(random.random(),random.random())*2-V(1,1))*20
        tr=Transform(randVec,randVec*randVec/randVec.lengthSq(),posTr)
        super().__init__(tr, velVec, size, owner=owner, maxAge=maxAge)
        self.AddComponent(C_DrawTexture(Transform(V0,V1/40,tr),0))
    
if __name__=='__main__':
    a=Scene()
    display=Display((1600,800))
    p=Player(Transform(V(0,0),V(1,0)),5)
    a.AddObject(Projectile(Transform(V(-4,-8),V(1,0)),V0,8,p))
    a.AddObject(Projectile(Transform(V(4,-4),V(0,1)),V0,8,p))
    a.AddObject(Projectile(Transform(V(4,4),V(-1,0)),V0,8,p))
    a.AddObject(Projectile(Transform(V(-4,4),V(0,-1)),V0,8,p))
    tr=p.GetComponent(C_Position).transform
    t=Transform(V(0,0),V(1/50,0),tr)
    #trCanvas=TrCanvas(V(1600,800),t)
    p.AddComponent(C_Camera(t,(1600,800)))
    a.AddObject(p)
    w=WormHead(tr.copy(),10,50)
    #w.GetComponent(C_Inertia).AccelerateVector(V(0,1))
    a.AddObject(w)
    ta=Transform(V0,V1)
    a.AddObject(Entity(ta,1,LineSegment(Transform(V0,V1*5,ta))))
    def getTime(self):
        print(self.deltaTime)
    a.globalMethods.add(getTime)
    display.Loop(a.ScreenUpdate,50)        