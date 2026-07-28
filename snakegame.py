# import required modules
import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0

# Creating a window screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("dark blue")
wn.setup(width=600, height=600)
wn.tracer(0)

# head of the snake
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# food in the game
food = turtle.Turtle()
colors = random.choice(['red', 'green', 'yellow', 'orange', 'cyan'])
shapes = random.choice(['square', 'triangle', 'circle'])
food.speed(0)
food.shape(shapes)
food.color(colors)
food.penup()
food.goto(0, 100)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score : 0  High Score : 0", align="center", font=("candara", 24, "bold"))


# assigning key directions
def goup():
	if head.direction != "down":
		head.direction = "up"


def godown():
	if head.direction != "up":
		head.direction = "down"


def goleft():
	if head.direction != "right":
		head.direction = "left"


def goright():
	if head.direction != "left":
		head.direction = "right"


def move():
	if head.direction == "up":
		y = head.ycor()
		head.sety(y + 20)
	if head.direction == "down":
		y = head.ycor()
		head.sety(y - 20)
	if head.direction == "left":
		x = head.xcor()
		head.setx(x - 20)
	if head.direction == "right":
		x = head.xcor()
		head.setx(x + 20)


# Listen for keyboard input
wn.listen()

# Register movement controls (Arrow keys and W/A/S/D case-insensitive)
for k in ["w", "W", "Up"]:
	wn.onkey(goup, k)
	wn.onkeypress(goup, k)

for k in ["s", "S", "Down"]:
	wn.onkey(godown, k)
	wn.onkeypress(godown, k)

for k in ["a", "A", "Left"]:
	wn.onkey(goleft, k)
	wn.onkeypress(goleft, k)

for k in ["d", "D", "Right"]:
	wn.onkey(goright, k)
	wn.onkeypress(goright, k)

segments = []

# Main Gameplay Loop
try:
	while True:
		wn.update()

		# Check collision with border
		if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
			time.sleep(1)
			head.goto(0, 0)
			head.direction = "Stop"

			# Reset food
			colors = random.choice(['red', 'green', 'yellow', 'orange', 'cyan'])
			shapes = random.choice(['square', 'circle'])
			food.color(colors)
			food.shape(shapes)

			# Clear body segments
			for segment in segments:
				segment.hideturtle()
				segment.goto(1000, 1000)
			segments.clear()

			# Reset score and delay
			score = 0
			delay = 0.1
			pen.clear()
			pen.write("Score : {}  High Score : {}".format(score, high_score), align="center", font=("candara", 24, "bold"))

		# Check collision with food
		if head.distance(food) < 20:
			x = random.randint(-270, 270)
			y = random.randint(-270, 270)
			food.goto(x, y)

			# Change food color/shape on eating
			colors = random.choice(['red', 'green', 'yellow', 'orange', 'cyan'])
			shapes = random.choice(['square', 'triangle', 'circle'])
			food.color(colors)
			food.shape(shapes)

			# Adding new segment
			new_segment = turtle.Turtle()
			new_segment.speed(0)
			new_segment.shape("square")
			new_segment.color("orange")
			new_segment.penup()
			segments.append(new_segment)

			# Speed up game
			delay -= 0.001
			delay = max(0.01, delay)

			# Increase score
			score += 10
			if score > high_score:
				high_score = score
			pen.clear()
			pen.write("Score : {}  High Score : {}".format(score, high_score), align="center", font=("candara", 24, "bold"))

		# Move tail segments in reverse order
		for index in range(len(segments) - 1, 0, -1):
			x = segments[index - 1].xcor()
			y = segments[index - 1].ycor()
			segments[index].goto(x, y)

		# Move segment 0 to head position
		if len(segments) > 0:
			x = head.xcor()
			y = head.ycor()
			segments[0].goto(x, y)

		move()

		# Check head collision with body segments
		for segment in segments:
			if segment.distance(head) < 20:
				time.sleep(1)
				head.goto(0, 0)
				head.direction = "Stop"

				colors = random.choice(['red', 'green', 'yellow', 'orange', 'cyan'])
				shapes = random.choice(['square', 'circle'])
				food.color(colors)
				food.shape(shapes)

				for seg in segments:
					seg.hideturtle()
					seg.goto(1000, 1000)
				segments.clear()

				score = 0
				delay = 0.1
				pen.clear()
				pen.write("Score : {}  High Score : {}".format(score, high_score), align="center", font=("candara", 24, "bold"))
				break

		time.sleep(delay)
except (turtle.Terminator, Exception):
	pass
