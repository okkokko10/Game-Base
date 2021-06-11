class CompVec(complex):
    '''almost the same as complex()

    additions to complex():

    self[0] == self.x == self.real

    self[1] == self.y == self.imag

    x,y=self =>
        x == self.x and y == self.y

    self.normalize() = self/abs(self)
    
    making it so functions from the superclass return an instance of the subclass instead of the superclass took way too long, and I couldn't do it in a way I wanted to
    '''
    x:float
    y:float
    def normalize(self):
        return self/abs(self)
    def __new__(cls,x,y=None):
        if y:
            a=complex.__new__(cls,x,y)
        else:
            a=complex.__new__(cls,x)
        a.x=a.real
        a.y=a.imag
        return a
    def __iter__(self):
        return (self.x,self.y).__iter__()
    def __getitem__(self,i):
        if i==0:
            return self.x
        elif i==1:
            return self.y
def outer(func):
    def inner(*args,**kvargs):
        return CompVec(func(*args,**kvargs))
    return inner

_list_of_complex_methods_that_return_complex='__add__', '__mul__', '__ne__', '__neg__', '__pos__', '__pow__', '__radd__', '__rmul__', '__rpow__', '__rsub__', '__rtruediv__', '__sub__', '__truediv__', 'conjugate'
for fun in _list_of_complex_methods_that_return_complex:
    setattr(CompVec,fun,outer(getattr(CompVec,fun)))
