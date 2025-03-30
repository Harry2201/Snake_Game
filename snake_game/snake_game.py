import turtle  # Import turtle graphics module
import random  # Import random module

# Define program constants
width = 500
height = 500
delay = 200  # Reduced delay for smooth movement
food_size = 32

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0),
}


#highscore
high_score = 0

try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass



def update_high_score():
    global high_score
    if score> high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))

def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")


def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":
            snake_direction = "up"

    elif direction == "down":
        if snake_direction != "up":
            snake_direction = "down"
    elif direction == "right":
        if snake_direction != "left":
            snake_direction = "right"
    elif direction == "left":
        if snake_direction != "right":
            snake_direction = "left"


def game_loop():
    if not running:
        return

    # Move the snake forward
    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check for collisions
    if (
        new_head in snake
        or new_head[0] < -width / 2
        or new_head[0] > width / 2
        or new_head[1] < -height / 2
        or new_head[1] > height / 2
    ):
        reset()
    else:
        snake.append(new_head)

        if not food_collision():
            snake.pop(0)  # Keep the snake length the same unless fed

    # Clear old stamps and redraw
    stamper.clearstamps()

    for segment in snake:
        stamper.goto(segment[0], segment[1])
        stamper.stamp()

    screen.title(f"Harry's Snake Game. Score: {score} High Score: {high_score}")
    screen.update()

    # Schedule the next move
    screen.ontimer(game_loop, delay)


def get_random_food_pos():
    x = random.randint(-width // 2 + food_size, width // 2 - food_size)
    y = random.randint(-height // 2 + food_size, height // 2 - food_size)
    return (x, y)


def food_collision():
    global food_pos, score
    if get_distance(snake[-1], food_pos) < 20:
        score += 1
        update_high_score()
        food_pos = get_random_food_pos()  # ✅ Call the function to get new coordinates
        food.goto(food_pos)  # ✅ Move the food to new position
        return True
    return False


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # Pythagorean theorem


def reset():
    global snake, score, food_pos, snake_direction
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    snake_direction = "up"
    score = 0
    food_pos = get_random_food_pos()  # ✅ Call the function
    food.goto(food_pos)


# Set up the screen
screen = turtle.Screen()
screen.setup(width, height)
screen.title("Snake Game")
screen.bgpic("assets/background.gif")
screen.register_shape("assets/head2.gif")
screen.register_shape("assets/food3.gif")
screen.tracer(0)  # Turns off automatic animation

# Event listener for keyboard input
screen.listen()
bind_direction_keys()

# Create a turtle for the snake
stamper = turtle.Turtle()
stamper.shape("square")
stamper.color("green")
stamper.penup()


# Create food
food = turtle.Turtle()
food.shape("assets/food3.gif")
food.shapesize(food_size / 20)
food.penup()
game_loop


screen.update()

# Global flag to prevent infinite recursion
running = True

# Start moving the snake
screen.ontimer(game_loop, delay)


reset()

turtle.done()
