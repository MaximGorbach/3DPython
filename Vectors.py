from Matrix import *;
import math;

class Vector:
    def __init__(self,x,y,z=0):
        self.x = x
        self.y = y
        self.z = z

    def rotate(self,angle,axis):
        rotM = Matrix(3,3)
        sin = math.sin(angle)
        cos = math.cos(angle)
        x = axis.x
        y = axis.y
        z = axis.z
        data = [cos+(x**2)*(1-cos),x*y*(1-cos)-z*sin,x*z*(1-cos)+y*sin,y*x*(1-cos)+z*sin,cos+(y**2)*(1-cos),y*x*(1-cos)-x*sin,z*x*(1-cos)-y*sin,z*y*(1-cos)+x*sin,cos+(z**2)*(1-cos)]
        rotM.dataFromArray(data)
        vectorM = Matrix(3,1)
        vectorM.dataFromArray([self.x,self.y,self.z])
        res = rotM * vectorM
        self.x = res.data[0][0]
        self.y = res.data[1][0]
        self.z = res.data[2][0]

    def unit(self):
        mag = self.x**2 + self.y**2 + self.z **2
        mag = math.sqrt(mag)
        if mag == 0:
            return None
        return self * (1/mag)

    def __add__(self,other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self,other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self,num):
        return Vector(self.x * num, self.y * num, self.z * num)
    
    def __repr__(self):
        return "(%s,%s,%s)" %(self.x,self.y,self.z)
    
    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

class Line:
    def __init__(self,p,v):
        self.p = p
        self.v = v
    
    def __repr__(self):
        return "%s + a%s" %(self.p,self.v)

class Plane:
    def __init__(self,p,v1,v2):
        self.p = p
        self.v1 = v1
        self.v2 = v2

    def __repr__(self):
        return "%s + a%s + b%s" %(self.p,self.v1,self.v2)

def crossProduct(v1,v2):
    resV = Vector(v1.y*v2.z-v1.z*v2.y,v1.z*v2.x-v1.x*v2.z,v1.x*v2.y-v1.y*v2.x)
    return resV

def dotProduct(v1,v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z