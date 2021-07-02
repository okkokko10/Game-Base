from Screen import *
class Transform:
    def __init__(self,pos:cv,rot:cv,parent=None):
        self.parent=parent
        self.pos=pos
        self.rot=rot
        self.world=None
    def detachFrom(self,parent):
        return Transform(parent.pos+self.pos*parent.rot,self.rot*parent.rot,parent.parent)
    def detachOnce(self):
        return self.detachFrom(self.parent)
    def detach(self,until=None): #probably needs optimization idk
        'gets the transform\'s world coordinates'
        c = self
        while c.parent!=until:
            c = c.detachOnce()
        return c.copy()
    def getWorld(self):
        'deprecated, use detach() \n\n gets the transform\'s world coordinates. Also saves them for optimization purposes. \n WARNING: must be reset after an ancestor has moved.'
        if not self.world:
            if self.parent:
                self.world = self.detachFrom(self.parent.getWorld())
            else:
                self.world = self
        return self.world
    def Become(self,other):
        self.__dict__=other.__dict__
    def copy(self):
        return Transform(self.pos,self.rot,self.parent)
    def distance(self,other,ancestor=None):
        return abs(other.attach(self).pos)
    def attach(self,newParent,ancestor=None):
        'returns a new transform that has identical world coordinates but has newParent as parent'
        unattached=self.detach(ancestor)
        parent=newParent.detach(ancestor)
        # unattached.pos = parent.pos+self.pos*parent.rot
        # unattached.rot = self.rot*parent.rot
        # unattached.parent = parent.parent
        return Transform(
        (unattached.pos - parent.pos)/parent.rot,
        unattached.rot/parent.rot,
        newParent)
    def commonAncestor(self,other,until=None):
        sFT=self.familyTree(until)
        oFT=other.familyTree(until)
        for i in len(sFT):
            if sFT[i] in oFT:
                #oFT.index(sFT[i])
                return sFT[i]
    def familyTree(self,until=None):
        l=[self.parent]
        while l[-1]!=until:
            #assert c.parent!=None
            l.append(l[-1].parent)
        return l
    def Translate(self,tr,ancestor=None):
        self.pos+=tr.attach(self,ancestor).rot
    def Rotate(self,rotationCompVec):
        self.rot*=rotationCompVec
    def TranslateVector(self,vec):
        self.Translate(Transform(V(0,0),vec))
    @staticmethod
    def FromVector(vec):
        return Transform(vec,V(1,0))
