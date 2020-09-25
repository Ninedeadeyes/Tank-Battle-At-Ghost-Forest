import turtle
import math
import random
import winsound
import time 

images=["rock.gif","tree.gif","health.gif","ghost.gif","fire1.gif","background.gif"]

for image in images:
    turtle.register_shape(image)

#Hide the default turtle
turtle.ht()
turtle.setup(950,950)
turtle.title("Tank Battle at Ghost Forest")
turtle.bgcolor("black")
turtle.bgpic("background.gif")
#This saves memory
turtle.setundobuffer(1)
#This speeds up drawing
turtle.tracer(0)


class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        

    def blue_win(self):
        self.ht()
        self.up()
        self.goto(-100,450)
        self.color("white")
        msg = ("Blue has won")       
        self.write(msg, font=("Arial", 16, "normal"))

    def yellow_win(self):
        self.ht()
        self.up()
        self.goto(-100,450)
        self.color("white")
        msg = ("Yellow has won")        
        self.write(msg, font=("Arial", 16, "normal"))

    def show_rules(self):
        msg = ("Controls: BLUE: W,A,S,D, Fire=Spacebar YELLOW: Arrowkeys, Fire= ' / '")
        self.penup()
        self.goto(-350, -450)
        self.color("white")
        self.write(msg, font=("Arial", 16, "normal"))
        self.pendown()
        self.penup()
     
        

    def show_lives1(self):
        self.ht()
        self.up()
        self.goto(-410,450)
        self.color("white")
        msg = " Yellow Armour:%s" %(player1.health)        
        self.write(msg, font=("Arial", 16, "normal"))
    
    def update_lives1(self):
        self.undo()
        self.ht()
        self.up()
        self.goto(-410,450)
        self.color("white")
        msg = "Yellow Armour:%s" %(player1.health)        
        self.write(msg, font=("Arial", 16, "normal"))



    def show_lives2(self):
        self.ht()
        self.up()
        self.goto(250,450)
        self.color("white")
        msg = " Blue Armour:%s" %(player2.health)        
        self.write(msg, font=("Arial", 16, "normal"))
    
    def update_lives2(self):
        self.undo()
        self.ht()
        self.up()
        self.goto(250,450)
        self.color("white")
        msg = "Blue Armour:%s" %(player2.health)        
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
            self.rt(90)
        
        if self.xcor() < -390:
            self.setx(-390)
            self.rt(90)
        
        if self.ycor() > 390:
            self.sety(390)
            self.rt(90)
        
        if self.ycor() < -390:
            self.sety(-390)
            self.rt(90)
            
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
        

    def turn_left(self):
        self.lt(45)
        
        
    def turn_right(self):
        self.rt(45)
       

    def accelerate(self):
        self.speed = 1 
        
    def decelerate(self):
        self.speed = 0


        
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 2
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

            
    def fire2(self):
        if self.status == "ready":            
            self.goto(player2.xcor(), player2.ycor())
            self.setheading(player2.heading())
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

        if self.frame > 15:
            self.frame = 0
            self.goto(-1000, -1000)



class Shield(Sprite):
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


maxtree = random.randint(20,30)
tree = []
    
for tre in range (maxtree):
    tree.append(turtle.Turtle())
    tree[tre].color("Darkgreen")
    tree[tre].shape("tree.gif")
    tree[tre].penup()
    tree[tre].speed(0)
    tree[tre].setposition(random.randint(-360,360),random.randint(-360,360))

maxrock = random.randint(12,20)
rock = []
    
for roc in range (maxrock):
    rock.append(turtle.Turtle())
    rock[roc].color("grey")
    rock[roc].shape("rock.gif")
    rock[roc].penup()
    rock[roc].speed(0)
    rock[roc].setposition(random.randint(-360,360),random.randint(-360,360))



maxshield = random.randint(12,15)
shield=[]

    
for shi in range (maxshield):
    shield.append(Shield("health.gif","red",random.randint(-360,370),random.randint(-360,370)))
   
maxenemies= random.randint(6,12)

enemies =[]
for i in range(maxenemies):
    enemies.append(Enemy("ghost.gif", "white",0, 0))

particles = []               
for i in range(10):
        particles.append(Particle("circle", "red", 0, 0))
        
for i in range(10):
        particles.append(Particle("circle", "yellow", 0, 0))


particles2 = []         # 2nd player sparkles 
for i in range(10):
        particles2.append(Particle("circle", "red", 0, 0))

for i in range(10):
        particles2.append(Particle("circle", "yellow", 0, 0))



    
#Create game object
game = Game()


#Draw the game border
game.draw_border()



#Create my sprites
player1 = Player("turtle", "yellow",-380, -380)
player2 = Player("turtle", "blue",380, 380)
missile1= Missile("fire1.gif", "yellow", 0, 0)
missile2= Missile("fire1.gif", "blue", 0, 0)      # Two different class becasue functions will be different 


life1=Pen()
life2=Pen()
life1.show_lives1()
life2.show_lives2()
win=Pen()
win.show_rules()


winsound.PlaySound("intro.wav", winsound.SND_ASYNC)
time.sleep(3)



#Keyboard bindings
turtle.onkey(player1.turn_left, "Left")
turtle.onkey(player1.turn_right, "Right")
turtle.onkey(player1.accelerate, "Up")
turtle.onkey(player1.decelerate, "Down")
turtle.onkey(player2.turn_left, "a")
turtle.onkey(player2.turn_right, "d")
turtle.onkey(player2.accelerate, "w")
turtle.onkey(player2.decelerate, "s")
turtle.onkey(missile1.fire1, "/")
turtle.onkey(missile2.fire2, "space")

turtle.listen()

#Main game loop
while True:
    player1.move()
    player2.move()
    missile1.move()
    missile2.move()

    for particle in particles:
        particle.move()

    for particle in particles2:
        particle.move()  
    
    for enemy in enemies:
        enemy.move()
    
        if player1.is_collision(enemy):
            player1.health-=1
            life1.update_lives1()
            winsound.PlaySound("gasp.wav", winsound.SND_ASYNC)

            for particle in particles:
                particle.explode(player1.xcor(), player1.ycor())
           
         

        if player2.is_collision(enemy):
            player2.health-=1
            life2.update_lives2()
            winsound.PlaySound("gasp.wav", winsound.SND_ASYNC)

            for particle in particles2:
                particle.explode(player2.xcor(),player2.ycor())
            

        if missile1.is_collision(enemy):
            missile1.status = "ready"
            #enemy.destroy() ( If want to get rid of enemy of screen )
            x = random.randint(-430, 430)
            y = random.randint(-430, 430)
            enemy.goto(x, y)
            winsound.PlaySound("bang.wav", winsound.SND_ASYNC)
            
            for particle in particles:
                particle.explode(missile1.xcor(), missile1.ycor())
            
                
        if missile2.is_collision(enemy):
            missile2.status = "ready"
            #enemy.destroy() ( If want to get rid of enemy of screen )
            x = random.randint(-430, 430)
            y = random.randint(-430, 430)
            enemy.goto(x, y)
            winsound.PlaySound("bang.wav", winsound.SND_ASYNC)
            
            for particle in particles2:
                particle.explode(missile2.xcor(), missile2.ycor())
                
        


 



    for tre in range (maxtree):
        if player1.is_collision(tree[tre]):
            player1.left(180)

        if player2.is_collision(tree[tre]):
            player2.left(180)

        if missile1.is_collision(tree[tre]):
            missile1.status = "ready"
            missile1.goto(-1000,1000)

        if missile2.is_collision(tree[tre]):
            missile2.status = "ready"
            missile2.goto(-1000,1000)
            



    for roc in range (maxrock):
        if player1.is_collision(rock[roc]):
            player1.left(180)

        if player2.is_collision(rock[roc]):
            player2.left(180)

        if missile1.is_collision(rock[roc]):
            missile1.status = "ready"
            missile1.goto(-1000,1000)

        if missile2.is_collision(rock[roc]):
            missile2.status = "ready"
            missile2.goto(-1000,1000)
            
            
            

    for shi in range (maxshield):
        if player1.is_collision(shield[shi]):
           shield[shi].destroy()
           player1.health+=30
           life1.update_lives1()
           winsound.PlaySound("health.wav", winsound.SND_ASYNC)

            

        if player2.is_collision(shield[shi]):
           shield[shi].destroy()
           player2.health+=30
           life2.update_lives2()
           winsound.PlaySound("health.wav", winsound.SND_ASYNC)


    if missile1.is_collision(player2):
        missile1.status = "ready"
        player2.health-=20
        life2.update_lives2()
        winsound.PlaySound("bang.wav", winsound.SND_ASYNC)
        
        for particle in particles:
            particle.explode(missile1.xcor(), missile1.ycor())
        
            
    if missile2.is_collision(player1):
        missile2.status = "ready"
        player1.health-=20
        life1.update_lives1()
        winsound.PlaySound("bang.wav", winsound.SND_ASYNC)
        
        for particle in particles2:
            particle.explode(missile2.xcor(), missile2.ycor())
            


    if player2.health<=0:       
        player2.destroy()
        player1.destroy()
        win.yellow_win()
        player1.speed=0
        for enemy in enemies:
            enemy.speed=0
        winsound.PlaySound("intro.wav", winsound.SND_ASYNC)
        time.sleep(5)
        break
  
        

    if player1.health<=0:
        player1.destroy()
        player2.destroy()
        win.blue_win()
        player2.speed=0
        for enemy in enemies:
            enemy.speed=0
        winsound.PlaySound("intro.wav", winsound.SND_ASYNC)
        time.sleep(5)
        break

       

    

    turtle.update()
    
    #https://github.com/Ninedeadeyes/Tank-Battle-At-Ghost-Forest

