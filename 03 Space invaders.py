
# Space Ivaders
# Game
# First try
import turtle
import winsound
import os
import math
import random
import platform

# set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Ivaders")
wn.bgpic("space/space_invader_background.gif")
wn.tracer(0)

# Register the shape
turtle.register_shape("space/invaders.gif")
turtle.register_shape("space/player.gif")

# Draw a border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set the score to 0
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle 
player = turtle.Turtle()
player.color("blue")
player.shape("space/player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90) 
player.speed = 0

# Choose a number of enemy
number_of_enemies = 30
# Creat a emty list of enemies 
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

for enemy in enemies:    
    enemy.color("red")
    enemy.shape("space/invaders.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y 
    enemy.setposition(x, y)
    #Update the enemy number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 30
        enemy_number = 0
    

enemyspeed = 0.2


# Creat the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 10

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"

        
#  Move the player left and right
def move_left():
    player.speed = -2
    
def move_right():
    player.speed = 2

def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # Declare bulletstate as a global if it nedds changed
    global bulletstate
    if bulletstate == "ready":
        winsound.PlaySound("space/shoot.wav", winsound.SND_ASYNC)
        bulletstate = "fire"
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2) + math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False
# Create keybord blindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# Main game loop
while True:
    wn.update()
    move_player()
    
    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280:
            for e in enemies:
                # Move all enemies down
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= -1
             
        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= -1

        # Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            winsound.PlaySound("space/enemy.wav", winsound.SND_ASYNC)
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            
            # Reset the enemy 
            enemy.setposition(0, 10000)
            
            # Update the score
            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
             
        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
