# import required modules
import turtle
import random

# Initial game speed (60ms = ~16.6 updates per second for super snappy responsiveness)
INITIAL_DELAY = 90
delay_ms = INITIAL_DELAY
score = 0
high_score = 0
can_change_direction = True

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


# assigning key directions with instant responsiveness check
def goup():
	global can_change_direction
	if head.direction != "down" and can_change_direction:
		head.direction = "up"
		can_change_direction = False


def godown():
	global can_change_direction
	if head.direction != "up" and can_change_direction:
		head.direction = "down"
		can_change_direction = False


def goleft():
	global can_change_direction
	if head.direction != "right" and can_change_direction:
		head.direction = "left"
		can_change_direction = False


def goright():
	global can_change_direction
	if head.direction != "left" and can_change_direction:
		head.direction = "right"
		can_change_direction = False


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

# Bind movement controls cleanly using onkeypress
for k in ["w", "W", "Up"]:
	wn.onkeypress(goup, k)

for k in ["s", "S", "Down"]:
	wn.onkeypress(godown, k)

for k in ["a", "A", "Left"]:
	wn.onkeypress(goleft, k)

for k in ["d", "D", "Right"]:
	wn.onkeypress(goright, k)

segments = []


def reset_game():
	global score, delay_ms, can_change_direction
	head.goto(0, 0)
	head.direction = "Stop"
	can_change_direction = True

	colors = random.choice(['red', 'green', 'yellow', 'orange', 'cyan'])
	shapes = random.choice(['square', 'circle'])
	food.color(colors)
	food.shape(shapes)

	for segment in segments:
		segment.hideturtle()
		segment.goto(1000, 1000)
	segments.clear()

	score = 0
	delay_ms = INITIAL_DELAY
	pen.clear()
	pen.write("Score : {}  High Score : {}".format(score, high_score), align="center", font=("candara", 24, "bold"))


# Main Gameplay Loop via ontimer
def game_loop():
	global score, high_score, delay_ms, can_change_direction

	try:
		wn.update()
	except turtle.Terminator:
		return

	# Reset direction lock so next keypress is registered immediately for next tick
	can_change_direction = True

	# Check collision with border
	if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
		reset_game()

	# Check collision with food
	elif head.distance(food) < 20:
		x = random.randint(-270, 270)
		y = random.randint(-270, 270)
		food.goto(x, y)

		colors = random.choice(['red', 'green', 'yellow', 'orange', 'cyan'])
		shapes = random.choice(['square', 'triangle', 'circle'])
		food.color(colors)
		food.shape(shapes)

		new_segment = turtle.Turtle()
		new_segment.speed(0)
		new_segment.shape("square")
		new_segment.color("orange")
		new_segment.penup()
		segments.append(new_segment)

		# Gradually speed up game
		delay_ms = max(25, delay_ms - 1)

		score += 10
		if score > high_score:
			high_score = score
		pen.clear()
		pen.write("Score : {}  High Score : {}".format(score, high_score), align="center", font=("candara", 24, "bold"))

	# Move body segments
	for index in range(len(segments) - 1, 0, -1):
		x = segments[index - 1].xcor()
		y = segments[index - 1].ycor()
		segments[index].goto(x, y)

	if len(segments) > 0:
		x = head.xcor()
		y = head.ycor()
		segments[0].goto(x, y)

	move()

	# Check collision with body
	for segment in segments:
		if segment.distance(head) < 20:
			reset_game()
			break

	# Schedule next frame with faster tick rate
	try:
		wn.ontimer(game_loop, delay_ms)
	except turtle.Terminator:
		pass


# Start game loop and main event loop
game_loop()
wn.mainloop()
