#22201145_Assignment01
#TASK 01
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
WINDOW_WIDTH, WINDOW_HEIGHT=500,500
NUM_RAIN=200
rain_positions=[]
rain_speed=0.2
rain_tilt=0.0
bg_color=0.2  #dark age

def init_rain():
    global rain_positions
    rain_positions=[]
    for _ in range(NUM_RAIN):
        x=random.uniform(-250,250)
        y=random.uniform(-250,250)
        rain_positions.append([x,y])

def draw_house():
    #House
    glColor3f(0.8, 0.6, 0.4)
    glBegin(GL_TRIANGLES)
    glVertex2f(-100,-100)
    glVertex2f(100,-100)
    glVertex2f(100,50)
    glVertex2f(-100,-100)
    glVertex2f(100,50)
    glVertex2f(-100,50)
    glEnd()
    #Roof 
    glColor3f(0.5,0.2,0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-120,50)
    glVertex2f(120,50)
    glVertex2f(0,150)
    glEnd()
    #Ground
    glColor3f(0.4,0.25,0.1)  
    glBegin(GL_QUADS)
    glVertex2f(-250,-250)
    glVertex2f(250,-250)
    glVertex2f(250,-100)
    glVertex2f(-250,-100)
    glEnd()
    #Door 
    glColor3f(0.3, 0.3, 0.6)
    glBegin(GL_TRIANGLES)
    glVertex2f(-30,-100)
    glVertex2f(30,-100)
    glVertex2f(30,-20)
    glVertex2f(-30,-100)
    glVertex2f(30,-20)
    glVertex2f(-30,-20)
    glEnd()

def draw_rain():
    glColor3f(0.5, 0.7,1.0)
    glBegin(GL_LINES)
    for (x,y) in rain_positions:
        glVertex2f(x,y)
        glVertex2f(x+rain_tilt*10,y-10)
    glEnd()

def display():
    global bg_color
    glClearColor(bg_color,bg_color,bg_color+0.1,1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_house()
    draw_rain()
    glutSwapBuffers()

def animate():
    global rain_positions
    for drop in rain_positions:
        drop[0]+=rain_tilt*1.5
        drop[1]-=rain_speed
        if drop[1]<-250:
            drop[1]=250
            drop[0]=random.uniform(-250,250)
    glutPostRedisplay()

def setup_projection():
    glViewport(0,0,WINDOW_WIDTH,WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250,250,-250,250,0,1)
    glMatrixMode(GL_MODELVIEW)

def special_keys(key, x, y):
    global rain_tilt
    if key==GLUT_KEY_LEFT:
        rain_tilt-=0.05
    elif key==GLUT_KEY_RIGHT:
        rain_tilt+=0.05
    glutPostRedisplay()

def normal_keys(key, x, y):
    global bg_color
    if key in [b'd',b'D']:  #Din
        bg_color=min(bg_color + 0.05, 0.8)
    elif key in [b'n',b'N']:  #Raat
        bg_color=max(bg_color - 0.05, 0.1)
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Building a House with Rain")
    setup_projection()
    init_rain()
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(normal_keys)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if __name__ == "__main__":
    main()


#TASK 02
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
BOUND = 250
points = []  
speed = 0.1
frozen = False
blink = False
last_blink_time = 0
show_color = True

def random_color():
    return random.random(), random.random(), random.random()

def random_direction():
    dx=random.choice([-1,1])
    dy=random.choice([-1,1])
    return dx,dy
def convert_coordi(x, y):
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b
def mouse_listener(button,state, x, y):
    global blink
    if frozen:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        px,py=convert_coordi(x, y) #new random point hoilo
        dx,dy=random_direction()
        color=random_color()
        points.append([px, py, dx, dy, color])
    elif button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
        blink=not blink
def keyboard_listener(key, x, y):
    global frozen
    if key==b' ':
        frozen = not frozen  #pause hobe
def special_key_listener(key, x, y):
    global speed
    if frozen:
        return
    if key==GLUT_KEY_DOWN:
        speed*=0.5
    elif key==GLUT_KEY_UP:
        speed=max(0.2,speed/0.5)
def draw_box():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-BOUND, -BOUND)
    glVertex2f(BOUND, -BOUND)
    glVertex2f(BOUND, BOUND)
    glVertex2f(-BOUND, BOUND)
    glEnd()

def draw_points():
    global show_color
    glPointSize(8)
    glBegin(GL_POINTS)
    for p in points:
        x, y, dx, dy, color = p
        if blink and not show_color:
            glColor3f(0.0, 0.0, 0.0)  #black during blink 
        else:
            glColor3f(*color)
        glVertex2f(x, y)
    glEnd()
def animate():
    global last_blink_time, show_color
    if frozen:
        glutPostRedisplay()
        return
    for p in points:
        p[0] += p[2]*speed
        p[1] += p[3]*speed
        if p[0]>BOUND or p[0]<-BOUND: #deyal e bounce
            p[2]*=-1
        if p[1] >BOUND or p[1]<-BOUND:
            p[3]*=-1
    if blink: #for blink
        current_time = time.time()
        if current_time-last_blink_time > 0.5:
            show_color=not show_color
            last_blink_time=current_time
    glutPostRedisplay()

def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-300, 300, -300, 300, 0, 1)
    glMatrixMode(GL_MODELVIEW)
def display():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_box()
    draw_points()
    glutSwapBuffers()
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Building the Amazing Box")
    setup_projection()
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMainLoop()
if __name__ == "__main__":
    main()
