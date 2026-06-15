from turtle import Turtle


class Paddle(Turtle):
    
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)

    def go_up(self):
        # Eğer raket henüz üst sınıra (250) dayanmadıysa yukarı gitmesine izin ver kanka
        if self.ycor() < 250:
            new_y = self.ycor() + 20
            self.goto(self.xcor(), new_y)

    def go_down(self):
        # Eğer raket henüz alt sınıra (-250) dayanmadıysa aşağı gitmesine izin ver aga
        if self.ycor() > -250:
            new_y = self.ycor() - 20
            self.goto(self.xcor(), new_y)