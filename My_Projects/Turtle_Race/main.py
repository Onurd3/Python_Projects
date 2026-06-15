from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
colors = ["red", "orange", "yellow", "green", "blue", "purple"] # renklerini ayarlioz 
y_positions = [-70, -40, -10, 20, 50, 80]
all_turtles = []

#Create 6 turtles
for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle") # turtle şekli veriyoruz
    new_turtle.penup()
    new_turtle.color(colors[turtle_index]) # renklerini atioz
    new_turtle.goto(x=-230, y=y_positions[turtle_index]) # başlangıç noktalarını ayarlioz
    all_turtles.append(new_turtle) # oluşturduğumuz kaplumbağaları bir listeye atıyoruz

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles: # bu iki satır foreach e benziyor. tüm kaplumbağalar için bu işlemi yapacağız.
        #230 is 250 - half the width of the turtle.
        if turtle.xcor() > 230: # eğer herhangi bir kaplumbağa x ekseninde 230 u geçerse yarış biter
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet: # bizim kaplumbağamız kazanırsa
                print(f"You've won! The {winning_color} turtle is the winner!")
            else: # bizim kaplumbağamız kaybederse
                print(f"You've lost! The {winning_color} turtle is the winner!")

        #Make each turtle move a random amount.
        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)

screen.exitonclick()