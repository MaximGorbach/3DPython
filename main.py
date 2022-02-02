import pygame as p;
from Camera import *;


class Player:
    def __init__(self,pos,screenSize,display,angle = Vector(0,0)):
        self.camera = Camera(screenSize,pos,display,angle)
        self.pos = pos
        self.i = Vector(1,0,0)
        self.j = Vector(0,1,0)
        self.k = Vector(0,0,1)

    #moves the player fps style
    def move(self,dir):
        change = self.i * dir.x + self.j * dir.y + self.k * dir.z
        self.pos += change
        self.camera.move(change)

    #rotates the way the player is facing
    def rotate(self,angle):
        self.i.rotate(angle.x,self.j)
        self.k.rotate(angle.x,self.j)
        self.camera.rotate(angle)

#displays the current ijk vectors of the camera
def showVectors(camera,display):
    p.draw.line(display,(255,0,0),(100,100),(100+camera.i.z*40,100+camera.i.x*-40),5)
    p.draw.line(display,(0,255,0),(100,100),(100+camera.j.z*40,100+camera.j.x*-40),5)
    p.draw.line(display,(0,0,255),(100,100),(100+camera.k.z*40,100+camera.k.x*-40),5)

#define screen size
screen_w = 1500
screen_h = 800

objects = []

#defining a cube
p1 = Vector(500,0,0)
p2 = Vector(500,50,0)
p3 = Vector(500,50,50)
p4 = Vector(500,0,50)
p5 = Vector(550,0,0)
p6 = Vector(550,50,0)
p7 = Vector(550,50,50)
p8 = Vector(550,0,50)
ts =           [Triangle([Point(p1),Point(p2),Point(p3)]), Triangle([Point(p1),Point(p3),Point(p4)]),
               Triangle([Point(p2),Point(p6),Point(p7)]), Triangle([Point(p2),Point(p7),Point(p3)]),
               Triangle([Point(p5),Point(p1),Point(p4)]), Triangle([Point(p5),Point(p4),Point(p8)]),
               Triangle([Point(p1),Point(p5),Point(p6)]), Triangle([Point(p1),Point(p6),Point(p2)]),
               Triangle([Point(p4),Point(p3),Point(p7)]), Triangle([Point(p4),Point(p7),Point(p8)]),
               Triangle([Point(p8),Point(p7),Point(p6)]), Triangle([Point(p8),Point(p6),Point(p5)])]

cube = Object(ts)

obj = Object()
obj.fromObjFile("shape.obj")
# for tri in obj.triangles:
#     for point in tri.points:
#         point.pos *= 20

objects.append(obj)

p.init()
display = p.display.set_mode((screen_w,screen_h))
clock = p.time.Clock()
p.mouse.set_visible(False)

player = Player(Vector(0,0,0),Vector(screen_w,screen_h),display)
moveSpeed = 1
mouseSens = 0.2

running = True

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_ESCAPE:
                running = False
    
    display.fill((255,255,255))

    # check movement
    keys = p.key.get_pressed() 
    if keys[p.K_UP]:
        player.rotate(Vector(0,math.pi/100))
    if keys[p.K_DOWN]:
        player.rotate(Vector(0,-math.pi/100))
    if keys[p.K_RIGHT]:
        player.rotate(Vector(-math.pi/100,0))
    if keys[p.K_LEFT]:
        player.rotate(Vector(math.pi/100,0))
    if keys[p.K_w]:
        player.move(Vector(moveSpeed,0,0))
    if keys[p.K_s]:
        player.move(Vector(-moveSpeed,0,0))
    if keys[p.K_d]:
        player.move(Vector(0,0,moveSpeed))
    if keys[p.K_a]:
        player.move(Vector(0,0,-moveSpeed))
    if keys[p.K_SPACE]:
        player.move(Vector(0,moveSpeed,0))
    if keys[p.K_LCTRL]:
        player.move(Vector(0,-moveSpeed,0))


    player.camera.show(objects)
    showVectors(player.camera,display)

    p.display.update()
    #print(clock.get_fps())
    clock.tick(30)

p.quit()
quit