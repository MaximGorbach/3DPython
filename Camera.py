from Vectors import *;
from Matrix import *;
import pygame as p;

import time;

class Point:
    def __init__(self,pos):
        self.pos = pos
        self.screenPos = Vector(0,0,0)
        self.size = 10

    #checks whether the point is towards the normal of a boundary plane or not
    def inBoundary(self,boundary,camera):
        norm = crossProduct(boundary.v1,boundary.v2)
        pt = boundary.p
        #find d in equation ax + by + cz - d = 0
        d = dotProduct(pt,norm)
        res = dotProduct(self.pos,norm) - d >= 0
        #outPoint is a point thats on the 'outside' of the plane
        outPoint = pt + norm
        outPointRes = dotProduct(outPoint,norm) - d >= 0
        #return if both points are on the same side of the plane
        return res == outPointRes

    def __repr__(self):
        return  str(self.pos)

class Triangle:
    def __init__(self,points,col = (240,0,0)):
        self.points = points
        self.center = Vector(0,0,0)
        # work out the average position of the triangle
        self.updateCenter()
        self.col = col
        self.updateNormal()

    def updateNormal(self):
        v1 = self.points[2].pos - self.points[0].pos
        v2 = self.points[1].pos - self.points[0].pos
        self.normal = crossProduct(v1,v2)
        self.normal = self.normal.unit()
    
    def updateCenter(self):
        self.center = Vector(0,0)
        for point in self.points:
            self.center += point.pos
        self.center *= (1/3)

    # backface culling
    def checkVis(self,camera):
        return dotProduct(self.normal,(camera.pos-self.center)) > 0

    def __repr__(self):
        return "Triangle at: %s,%s,%s" %(self.points[0],self.points[1],self.points[2])

    #clip the current triangle into a list of triangles
    def clip(self,camera):
        clipped = [self]
        buffer = []
        #for each boundary find how many points are on the visible side of the boundary
        for bound in camera.boundary:
            for tri in clipped:
                pOut = []
                pIn = []
                for point in tri.points:
                    if point.inBoundary(bound,camera):
                        pIn.append(point)
                    else:
                        pOut.append(point)
                # if there are 3 visible do nothing
                if len(pIn) == 3:
                    buffer.append(tri)
                # if there are 1 then form a new triangle using the intersection points with the plane
                if len(pIn) == 1:
                    intersect1 = intersection(Line(pIn[0].pos,pOut[0].pos - pIn[0].pos),bound)
                    intersect2 = intersection(Line(pIn[0].pos,pOut[1].pos - pIn[0].pos),bound)
                    intersect1 = Point(intersect1)
                    intersect2 = Point(intersect2)
                    newTri = Triangle([intersect1,intersect2,pIn[0]],tri.col)
                    newTri.normal = tri.normal
                    buffer.append(newTri)
                # if there are 2 then form 2 new triangles using the intersection points
                if len(pIn) == 2:
                    intersect1 = intersection(Line(pOut[0].pos,pIn[0].pos - pOut[0].pos),bound)
                    intersect2 = intersection(Line(pOut[0].pos,pIn[1].pos - pOut[0].pos),bound)
                    intersect1 = Point(intersect1)
                    intersect2 = Point(intersect2)
                    newTri1 = Triangle([intersect1,intersect2,pIn[0]],tri.col)
                    newTri2 = Triangle([intersect2,pIn[0],pIn[1]],tri.col)
                    newTri1.normal = tri.normal
                    newTri2.normal = tri.normal
                    buffer.append(newTri1)
                    buffer.append(newTri2)
                # reset the buffer list and put new triangles in the clipped list to check against other boundaries
            clipped = buffer
            buffer = []
        return clipped
        
class Object:
    def __init__(self, triangles = []):
        self.triangles = triangles

    def fromObjFile(self,filepath):
        f = open(filepath, "r")
        # stores the list of indexed points
        ps = []
        #stores the triangles of the object
        ts = []
        for line in f:
            if line[0] == "v":
                # create new triangle position, the points need to be unique in-between triangles
                # so that when applying a function to each point, no points are affected twice
                coords = self.readFloats(line)
                x = coords[0]
                y = coords[1]
                z = coords[2]
                p = Vector(x,y,z)
                ps.append(p)
            elif line[0] == "f":
                # create new triangle
                indices = self.readInts(line)
                p1 = indices[0] - 1
                p2 = indices[1] - 1
                p3 = indices[2] - 1
                t = Triangle([Point(ps[p3]),Point(ps[p2]),Point(ps[p1])])
                ts.append(t)
        f.close()
        self.triangles = ts
        return True

    def readInts(self,line):
        intStr = ""
        res = []
        for char in line:
            if char != " ":
                intStr += char
            else:
                try:
                    res.append((int)(intStr))
                except Exception:
                    pass
                intStr = ""
        res.append((int)(intStr))
        return res
    
    def readFloats(self,line):
        fStr = ""
        res = []
        for char in line:
            if char != " ":
                fStr += char
            else:
                try:
                    res.append((float)(fStr))
                except Exception:
                    pass
                fStr = ""
        res.append((float)(fStr))
        return res

    #moves the position of an object by vector 'dir'
    #TODO doesnt work
    def move(self,dir):
        for tri in self.triangles:
            for pt in tri.points:
                pt.pos += dir

    def __repr__(self):
        outStr = ""
        for tri in self.triangles:
            outStr += str(tri) + "\n"
        return outStr


class Camera:
    def __init__(self,screenSize,pos,display,angle = Vector(0,0)):
        self.pos = pos
        self.screenSize = screenSize
        self.fov = 50 * math.pi/180
        self.fov_scalar = (screenSize.x/2)/math.tan(self.fov)
        self.i = Vector(1,0,0)
        self.j = Vector(0,1,0)
        self.k = Vector(0,0,1)
        self.lightSource = Vector(1,0,1).unit()
        self.display = display
        self.rotate(angle)
        self.updateCanvas()
        
    #whenever the camera position or rotation is changed, the canvas needs to be updated
    def updateCanvas(self):
        self.canvas = Plane(self.pos + self.i * self.fov_scalar,self.j,self.k)
        self.topLeft = self.canvas.p + self.j * self.screenSize.y * (1/2) - self.k * self.screenSize.x * (1/2)
        topRight = self.canvas.p + self.j * self.screenSize.y * (1/2) + self.k * self.screenSize.x * (1/2)
        botRight = self.canvas.p - self.j * self.screenSize.y * (1/2) + self.k * self.screenSize.x * (1/2)
        botLeft = self.canvas.p - self.j * self.screenSize.y * (1/2) - self.k * self.screenSize.x * (1/2)
        #left boundary
        b1 = Plane(self.pos,self.pos - botLeft,self.pos - self.topLeft)
        #right boundary
        b2 = Plane(self.pos,self.pos - topRight,self.pos - botRight)
        #upper boundary
        b3 = Plane(self.pos,self.pos - self.topLeft,self.pos - topRight)
        #lower boundary
        b4 = Plane(self.pos,self.pos - botRight,self.pos - botLeft)
        #boundary stores 4 planes which define the borders of view
        self.boundary = [b1,b2,b3,b4]

    #calculates the position of a 3d point on the 2d canvas
    def setPointPos(self,point):
        toPoint = point.pos - self.pos
        onCanvas = intersection(Line(self.pos,toPoint),self.canvas)
        if onCanvas is None:
            return False
        toPoint = onCanvas - self.topLeft
        dBasis = convertToBasis(toPoint,self.i,self.j,self.k)
        x = dBasis.data[2][0]
        y = dBasis.data[1][0] *- 1
        point.screenPos = Vector(x,y)
        return True

    #draws a triangle from an object
    def drawTri(self,tri):
        if not tri.checkVis(self):
            return False
        #check if the triangle needs to be clipped, in which case draw all triangles
        triangles = tri.clip(self)
        for tri in triangles:
            pointsToDraw = []
            for point in tri.points:
                self.setPointPos(point)
                pointsToDraw.append((point.screenPos.x,point.screenPos.y))
            #work out new colour with illumination
            illum = (-dotProduct(self.lightSource,tri.normal) + 1)/2
            r = tri.col[0]
            g = tri.col[1]
            b = tri.col[2]
            colToDraw = (r*illum,g*illum,b*illum)
            p.draw.polygon(self.display,colToDraw,pointsToDraw)
            #draws outline of triangle for debugging
            p.draw.polygon(self.display,(0,0,0),pointsToDraw,3)
        return True

    #draws an object
    def drawObj(self,obj):
        for tri in obj.triangles:
            self.drawTri(tri)

    #draws every object in the given list
    def show(self,objects):
        for obj in objects:
            self.drawObj(obj)

    # input angle as 2D vector to rotate both both axes
    def rotate(self,angle):
        self.i.rotate(angle.y,self.k)
        self.i.rotate(angle.x,Vector(0,1,0))
        self.j.rotate(angle.x,Vector(0,1,0))
        self.j.rotate(angle.y,self.k)
        self.k.rotate(angle.x,Vector(0,1,0))
        self.updateCanvas()

    #moves the camera in the provided dir as a vector
    def move(self,dir):
        self.pos += dir
        self.updateCanvas()

# finds the point at which a plane intersects a line,
# returns none if the direction of the line is negative or there is no intersection
def intersection(line,plane):
    m1 = Matrix(3,1)
    m1.dataFromArray([plane.p.x-line.p.x,plane.p.y-line.p.y,plane.p.z-line.p.z])
    m2 = Matrix(3,3)
    m2.dataFromArray([line.v.x,-plane.v1.x,-plane.v2.x,line.v.y,-plane.v1.y,-plane.v2.y,line.v.z,-plane.v1.z,-plane.v2.z])
    m2 = m2.inverse()
    if m2 is None:
        return None
    res = m2 * m1
    if res.data[0][0] < 0:
        return None
    return line.p + line.v*res.data[0][0]

#converts from universal basis to basis ijk
def convertToBasis(point,i,j,k):
    pointM = Matrix(3,1)
    pointM.dataFromArray([point.x,point.y,point.z])
    M = Matrix(3,3)
    M.dataFromArray([i.x,j.x,k.x,i.y,j.y,k.y,i.z,j.z,k.z])
    M = M.inverse()
    res = M * pointM
    return res
