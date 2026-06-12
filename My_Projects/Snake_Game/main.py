from turtle import Screen, position
from snake import Snake
import time
from Food import Food
from turtle import Turtle


screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()

screen.listen()
screen.onkey(snake.up, "w")
screen.onkey(snake.left, "a")
screen.onkey(snake.down, "s")
screen.onkey(snake.right, "d")


tabela = Turtle()
tabela.hideturtle()
tabela.penup()
tabela.color("white")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    
    if snake.head.distance(food) < 15:
        snake.add_segment(snake.segments[-1].position())
        food.refresh()
    if snake.head.xcor() == 300 or snake.head.xcor() == -300 or snake.head.ycor() == 300 or snake.head.ycor() == -300:
        game_is_on = False


    snake.move()
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        game_is_on = False
        tabela.goto(0, 0)
        tabela.write("GAME OVER", align="center", font=("Arial", 24, "normal"))
        
    # Kendi kuyruğuna çarpma kontrolü
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            tabela.goto(0, 0)
            tabela.write("GAME OVER", align="center", font=("Arial", 24, "normal"))
    
    for Cor in snake.segments[1:]:
        if snake.head.distance(Cor) < 10: 
            game_is_on = False
            tabela.goto(0, 0)
            tabela.write("GAME OVER", align="center", font=("Arial", 24, "normal"))

screen.exitonclick()