from turtle import Screen, Turtle
from snake import Snake
import time
import random
from Food import food
screen = Screen()
screen.setup(width=900, height=550)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)


snake = Snake()
# burada klavyede w,a,s,d tuşlarına basınca snake'in hareket etmesini sağlıyoruz ve
# oyunun her 0.1 saniyede güncellenmesini sağlıyoruz 

screen.listen()
screen.onkey(snake.up, "w")
screen.onkey(snake.left, "a")
screen.onkey(snake.down, "s")
screen.onkey(snake.right, "d")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    SnakeXcor = snake.head.xcor()
    FoodXcor = food.xcor()
    if(SnakeXcor == FoodXcor):
        food.refresh()
    snake.move()


screen.exitonclick()