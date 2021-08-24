# 21,21
# 21,25
# 46,25
# 46,25
import os.path
import pygame
pygame.init()

def GetImage(name):
    return pygame.image.load(os.path.join('Textures',name))
atlas=GetImage('TextureAtlas.png')

a=2
atlas=pygame.transform.scale2x(atlas)

def GetSub(rect):
    return atlas.subsurface(rect)

sizes=(21,21),(21,25),(46,25),(46,25),(36,31),(21,21),(20,13)
locations=[]
y=0
for s in sizes:
    s=s[0]*a,s[1]*a
    locations.append(pygame.Rect((0,y),s))
    y+=s[1]

images=[GetSub(l) for l in locations]
def ConvertImages(surface):
    global images
    i = images.copy()
    images = [
        #pygame.transform.scale2x
        (img.convert(surface)) for img in i]
def images1():
    global images
    return images
def setImages(value):
    global images 
    images = value
def GetTexture(i):
    return images1()[i]

if pygame.display.get_surface():
    images=ConvertImages(pygame.display.get_surface())