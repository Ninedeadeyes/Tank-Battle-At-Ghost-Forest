import turtle
import math
import random
import winsound
import time 

images=["rock.gif","tree.gif","health.gif","ghost.gif","fire1.gif","background.gif","diamond.gif"]

for image in images:
    turtle.register_shape(image)

#Hide the default turtle
turtle.ht()
turtle.setup(950,950)
turtle.title("Tank Battle at Ghost Forest")
turtle.bgcolor("black")
turtle.bgpic("background.gif")
#This saves memory
turtle.setundobuffer(0)
#This speeds up drawing
turtle.tracer(0)




class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        

    def blue_win(self):
        self.ht()
        self.up()
        self.goto(-170,450)
        self.color("white")
        msg = ("""
        You lose, final points:%s""") %(player1.points)       
        self.write(msg, font=("Arial", 16, "normal"))

    def show_rules(self):
        self.ht()
        self.up()
        msg = ("Controls: ArrowKeys, Fire=Spacebar ")
        self.goto(-200, -450)
        self.color("white")
        self.write(msg, font=("Arial", 16, "normal"))
        self.pendown()
        self.penup()
     
        

    def show_lives1(self):
        self.ht()
        self.up()
        self.goto(-400,450)
        self.color("white")
        msg = "Armour:%s" %(player1.health)        
        self.write(msg, font=("Arial", 16, "normal"))
    
    def update_lives1(self):
        self.undo()
        self.ht()
        self.up()
        self.goto(-400,450)
        self.color("white")
        msg = "Armour:%s" %(player1.health)        
        self.write(msg, font=("Arial", 16, "normal"))



    def show_points1(self):
        self.ht()
        self.up()
        self.goto(310,450)
        self.color("white")
        msg = " Points:%s" %(player1.points)        
        self.write(msg, font=("Arial", 16, "normal"))
    
    def update_points1(self):
        self.undo()
        self.ht()
        self.up()
        self.goto(310,450)
        self.color("white")
        msg = "Points:%s" %(player1.points)        
        self.write(msg, font=("Arial", 16, "normal"))


class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1
        
    def move(self):
        self.fd(self.speed)
        
        #Boundary detection
        if self.xcor() > 390:
            self.setx(390)
            self.rt(135)
        
        if self.xcor() < -390:
            self.setx(-390)
            self.rt (135)
        
        if self.ycor() > 390:
            self.sety(390)
            self.rt (135)
        
        if self.ycor() < -390:
            self.sety(-390)
            self.rt (135)
            
    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False

    def destroy(self):
        self.goto(9000,9000)
        self.hideturtle()
                
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed =1
        self.shapesize(.8,1,6)
        self.health = 500
        self.points=0

    def turn_left(self):
        self.lt(45)
        
        
    def turn_right(self):
        self.rt(45)
       

    def accelerate(self):
        if self.speed==2:
            pass
        else:
            self.speed += 1 
        
    def decelerate(self):
        if self.speed == -1:
            pass
        else:
            self.speed -= 1
            
            


        
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 3
        self.setheading(random.randint(0,360))


class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.status = "ready"
        self.goto(-1000, 1000)
        
    def fire1(self):
        if self.status == "ready":
            
                
            self.goto(player1.xcor(), player1.ycor())
            self.setheading(player1.heading())
            self.status = "firing"

        
                
            
    def move(self):
    
        if self.status == "ready":
            self.goto(-1000, 1000)
        
        if self.status == "firing":
            self.fd(self.speed) 
            
        #Border check
        if self.xcor() < -400 or self.xcor() > 400 or \
            self.ycor()< -400 or self.ycor()> 400:
            self.goto(-1000,1000)
            self.status = "ready"


class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000,-1000)
        self.frame = 0
        
    def explode(self, startx, starty):
        self.goto(startx,starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame > 30:
            self.frame = 0
            self.goto(-1000, -1000)



class Shield(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 2


class Diamond(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 2
        

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3
        
    def draw_border(self):
        #Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-400, 400)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(800)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()


maxtree = random.randint(20,35)
tree = []
    
for tre in range (maxtree):
    tree.append(turtle.Turtle())
    tree[tre].color("Darkgreen")
    tree[tre].shape("tree.gif")
    tree[tre].penup()
    tree[tre].speed(0)
    tree[tre].setposition(random.randint(-360,360),random.randint(-360,360))

maxrock = random.randint(15,25)
rock = []
    
for roc in range (maxrock):
    rock.append(turtle.Turtle())
    rock[roc].color("grey")
    rock[roc].shape("rock.gif")
    rock[roc].penup()
    rock[roc].speed(0)
    rock[roc].setposition(random.randint(-360,360),random.randint(-360,360))


diamond=[]
    
for dia in range(1):
    diamond.append(Diamond("diamond.gif","red",random.randint(-370,370),random.randint(-370,370)))

maxshield = random.randint(2,4)
shield=[]
  
for shi in range (maxshield):
    shield.append(Shield("health.gif","red",random.randint(-370,370),random.randint(-370,370)))
   
maxenemies= random.randint(10,16)

enemies =[]
for i in range(maxenemies):
    enemies.append(Enemy("ghost.gif", "white",0, 0))
    enemies[i].setposition(random.randint(-300,300),random.randint(-300,300))

particles = []

for i in range(10):
        particles.append(Particle("circle", "red", 0, 0))
        
for i in range(10):
        particles.append(Particle("circle", "yellow", 0, 0))
    
#Create game object
game = Game()


#Draw the game border
game.draw_border()



#Create my sprites
player1 = Player("turtle", "blue",-380, -380)
missile1= Missile("fire1.gif", "blue", 0, 0)


life1=Pen()
points1=Pen()
life1.show_lives1()
points1.show_points1()
win=Pen()
win.show_rules()


winsound.PlaySound("intro.wav", winsound.SND_ASYNC)
time.sleep(3)



#Keyboard bindings
turtle.onkey(player1.turn_left, "Left")
turtle.onkey(player1.turn_right, "Right")
turtle.onkey(player1.accelerate, "Up")
turtle.onkey(player1.decelerate, "Down")
turtle.onkey(missile1.fire1, "space")


turtle.listen()

#Main game loop
while True:
    player1.move()
    missile1.move()

    for particle in particles:
        particle.move()  
    
    for enemy in enemies:
        enemy.move()
    
        if player1.is_collision(enemy):
            player1.health-=10
            life1.update_lives1()
            winsound.PlaySound("gasp.wav", winsound.SND_ASYNC)

            for particle in particles:
                particle.explode(player1.xcor(), player1.ycor())

        for shi in range (maxshield):
            if shield[shi].is_collision(enemy):
                enemy.rt(45)
           


        if missile1.is_collision(enemy):
            missile1.status = "ready"
            #enemy.destroy() ( If want to get rid of enemy of screen )
            x = random.randint(-390, 390)
            y = random.randint(-390, 390)
            enemy.goto(x, y)
            winsound.PlaySound("bang.wav", winsound.SND_ASYNC)
            player1.points+=10
            points1.update_points1()
            
            for particle in particles:
                particle.explode(missile1.xcor(), missile1.ycor())
            
            


    for tre in range (maxtree):
        if player1.is_collision(tree[tre]):
            player1.left(180)

        if missile1.is_collision(tree[tre]):
            missile1.status = "ready"
            missile1.goto(-1000,1000)



    for roc in range (maxrock):
        if player1.is_collision(rock[roc]):
            player1.left(180)

        if missile1.is_collision(rock[roc]):
            missile1.status = "ready"
            missile1.goto(-1000,1000)


    for shi in range (maxshield):
        if player1.is_collision(shield[shi]):
           #shield[shi].destroy()
           x = random.randint(-390, 390)
           y = random.randint(-390, 390)
           shield[shi].goto(x, y)
           player1.health+=100
           life1.update_lives1()
           winsound.PlaySound("health.wav", winsound.SND_ASYNC)

    for dia in range (1):
        if player1.is_collision(diamond[dia]):
           x = random.randint(-390, 390)
           y = random.randint(-390, 390)
           diamond[dia].goto(x, y)
           player1.points+=100
           points1.update_points1()
           winsound.PlaySound("win.wav", winsound.SND_ASYNC)


            
 

    if player1.health<=0:
        player1.destroy()
        win.blue_win()
        for enemy in enemies:
            enemy.speed=0
        winsound.PlaySound("intro.wav", winsound.SND_ASYNC)
        time.sleep(5)
        break


    turtle.update()

