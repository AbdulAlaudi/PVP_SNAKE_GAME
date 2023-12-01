import turtle  # Import the turtle module
import random  # Import the random module
import time  # Import the time module


ANGLE = 15  # constant for the angle a snake can turn
SNAKE_SPEED = 40  # constant for the speed of the snake
BOUNCE_SPEED_MULTIPLIER = 1.25  # constant for the speed of the snake after bouncing off the wall

FOOD_COLLISION_DISTANCE = 40  # constant for the distance between the snake head and food for a collision to occur

SNAKE_HEAD_COLLISION_DISTANCE = 40  # constant for the distance between the snake head and body for a collision to occur

BLUE = "blue"  # constant for the color of the blue snake
RED = "red"  # constant for the color of the red snake

GOOD_FOOD_COLOR = "green"  # constant for the color of the good food
BAD_FOOD_COLOR = "white"  # constant for the color of the bad food


class CreateScreen:  # Class to create the screen
    def create_screen():  # Function to create the screen
        wn = turtle.Screen()  # use turtle module to create the screen
        wn.bgcolor("black")  # set its background color to black
        wn.title("Turtle PvP Snake Game")  # set its title to "Turtle PvP Snake Game"
        wn.setup(width=700, height=700)  # set its width and height to 700
        wn.tracer(0)  # when setting up turtle animations, you'll see each one being formed, this turns it off so you only see the end result when you manually update the screen later on
        return wn  # now return the screen so we can use it later on


class CollisionManager:  # Class to manage collisions
    @staticmethod  # static method to check for wall collisions
    def check_wall_collision(turt):  # function to check for wall collisions, pass in the turtle object
        bounced = False  # initialize the bounced variable to False

        if turt.xcor() > 340:  # if the turtle's x coordinate is greater than 340
            turt.setheading(180 - turt.heading())  # set the turtle's heading to 180 - the turtle's current heading to bounce it off the wall in the opposite direction
            turt.setx(340)  # then move the turtle's positive horizontal coordinate back within the screen
            bounced = True  # set the bounced variable to True
        elif turt.xcor() < -340:  # if the turtle's x coordinate is less than -340
            turt.setheading(180 - turt.heading())  # set the turtle's heading to 180 - the turtle's current heading to bounce it off the wall in the opposite direction
            turt.setx(-340)  # then move the turtle's negative horizontal coordinate back within the screen
            bounced = True  # set the bounced variable to True

        if turt.ycor() > 340:  # if the turtle's y coordinate is greater than 340
            turt.setheading(-turt.heading())  # set the turtle's heading to - the turtle's current heading to bounce it off the wall in the opposite direction
            turt.sety(340)  # then move the turtle's positive vertical coordinate back within the screen
            bounced = True  # set the bounced variable to True
        elif turt.ycor() < -340:  # if the turtle's y coordinate is less than -340
            turt.setheading(-turt.heading())  # set the turtle's heading to - the turtle's current heading to bounce it off the wall in the opposite direction
            turt.sety(-340)  # then move the turtle's negative vertical coordinate back within the screen
            bounced = True  # set the bounced variable to True

        if bounced:  # if the turtle bounced off the wall
            turt.forward(SNAKE_SPEED * BOUNCE_SPEED_MULTIPLIER)  # move the turtle forward at a faster speed, this adds a bit of a bounce effect, makes the game more interesting

    def collides_with(self, other_snake):  # method to check for collisions between the head of one snake and any other part of the other snake
        COLLISION_COOLDOWN = 0.05  # there must be at least 0.05 seconds between collisions, that way if a longer snake's head collides with a shorter snake's body multiple times, it will only count as one collision, giving the shorter snake a chance to survive

        for segment in other_snake.body:  # loop through each segment of the other snake's body
            if self.body[0].distance(segment) <= SNAKE_HEAD_COLLISION_DISTANCE:  # if the distance between the head of this snake and the current segment of the other snake is less than or equal to the collision distance
                current_time = time.time()  # get the current time
                if current_time - self.last_collision_time > COLLISION_COOLDOWN:  # now use that time to check if there has been enough time between collisions
                    self.last_collision_time = current_time  # if there has been enough time, set the last collision time to the current time, so it can be used to check for the next collision
                    return True  # return True to indicate a collision has occurred

        return False  # if no collision has occurred, return False


class Snake(CollisionManager):  # Class to create the snake, pass in the CollisionManager class so we can use its methods
    def __init__(self, color, x, y, heading):  # function to initialize the snake, pass in the color, x and y coordinates, and heading
        self.snake_speed = SNAKE_SPEED  # set the snake speed to the constant SNAKE_SPEED
        self.body = []  # initialize the body list
        self.color = color  # set the color of the snake to the color passed in
        self.segment_spacing = 0  # Set the spacing between segments
        self.last_segment_loss_time = 0  # Timestamp of the last segment loss
        self.last_collision_time = 0  # Timestamp of the last collision

        self.create_head(x, y, heading)  # now call the create_head function to create the head of the snake
        self.create_body()  # then call the create_body function to create the body of the snake

    def create_head(self, x, y, heading):  # method to create the head of the snake, pass in the x and y coordinates, and the direction the snake is facing
        head = turtle.Turtle()  # create a turtle object for the head
        head.shape("triangle")  # set the shape of the head to a triangle
        head.shapesize(2, 2)  # set the size ratio of the head to 1:1, altering this ratio will warp the shape of the head
        head.color(self.color)  # set the color of the head to the color passed in in the __init__ function
        head.speed(0)  # set the speed of the head to 0, this is the fastest speed, prevents animation of the head, so it moves instantly to the starting position
        head.penup()  # set the penup, this prevents the turtle from drawing a line when moving
        head.goto(x, y)  # set the position of the head to the x and y coordinates passed in
        head.setheading(heading)  # set the heading of the head to the heading passed in
        head.forward(self.segment_spacing)  # Create space for the first segment, otherwise it will be placed on top of the body
        self.body.append(head)  # then append the head to the body list

    def create_body(self):  # method to create the body of the snake
        for _ in range(2):  # each snake is going to start off with a head and two segments, that's why we loop through twice, one for each segment body segment
            segment = turtle.Turtle()  # create a turtle object for the body segment
            segment.shape("circle")  # set the shape of the body segment to a circle
            segment.shapesize(2, 2)  # set the size ratio of the body segment to 1:1, altering this ratio will warp the shape of the body segment
            segment.color(self.color)  # set the color of the body segment to the color passed in in the __init__ function
            segment.speed(0)  # set the speed of the body segment to 0, this is the fastest speed, prevents animation of the body segment, so it moves instantly to the starting position
            segment.penup()  # set the penup, this prevents the turtle from drawing a line when moving
            segment.goto(self.body[-1].position())  # Set segment behind the previous segment or head
            segment.setheading(self.body[-1].heading())  # Set the segment to face the same direction as the previous segment or head
            segment.backward(self.segment_spacing)  # Move it backward to create space otherwise it will be placed on top of the previous segment or head
            self.body.append(segment)  # then append the body segment to the body list

    def add_segment(self):  # Method to add a segment to the snake when it eats food or eats a segment of the other snake
        segment = turtle.Turtle()  # create a turtle object for the segment
        segment.shape("circle")  # set the shape of the segment to a circle
        segment.shapesize(2, 2)  # set the size ratio of the segment to 1:1, altering this ratio will warp the shape of the segment
        segment.color(self.color)  # set the color of the segment to the color passed in in the __init__ function
        segment.speed(0)  # set the speed of the segment to 0, this is the fastest speed, prevents animation of the segment, so it moves instantly to the starting position
        segment.penup()  # set the penup, this prevents the turtle from drawing a line when moving
        segment.goto(self.body[-1].position())  # Set segment behind the last segment
        segment.setheading(self.body[-1].heading())  # Set the segment to face the same direction as the last segment
        segment.backward(self.segment_spacing)  # Move it backward to create space, otherwise it will be placed on top of the last segment
        self.body.append(segment)  # then append the segment to the body list

    def remove_segment(self):  # Method to remove a segment from the snake when it eats bad food or collides with the other snake
        if len(self.body) > 1:  # Ensure we don't remove the head
            segment_to_remove = self.body.pop()  # Remove the last segment
            segment_to_remove.hideturtle()  # Hide the turtle segment that was removed
            del segment_to_remove  # Delete the turtle object so there's no more reference to it

    def can_lose_segment(self, cooldown_period=0.2):  # Method to check if the snake can lose a segment
        current_time = time.time()  # Get the current time to check if there has been enough time between segment losses
        if current_time - self.last_segment_loss_time > cooldown_period:  # If there has been enough time between segment losses
            self.last_segment_loss_time = current_time  # Set the last segment loss time to the current time so it can be used to check for the next segment loss
            return True  # Return True to indicate a segment can be lost
        return False  # If no segment can be lost, return False

    def is_longer_than(self, other_snake):  # Method to check if the snake is longer than the other snake, this will be used to check if the snake can eat the other snake in the game loop
        return len(self.body) > len(other_snake.body)  # Return True if the snake is longer than the other snake, otherwise return False

    def move(self):  # Method to move the snake
        for i in range(len(self.body) - 1, 0, -1):  # Loop through the body list in reverse order, starting at the last segment
            self.body[i].goto(self.body[i - 1].pos())  # Set the current segment to the position of the previous segment that way each segment follows the previous segment

        self.body[0].forward(self.snake_speed)  # Move the head forward at the snake speed
        self.check_wall_collision(self.body[0])  # now check if that movement caused the snake to collide with the wall

    def left(self):  # Method to turn the snake left
        self.body[0].left(ANGLE)  # Turn the head left by the angle constant

    def right(self):  # Method to turn the snake right
        self.body[0].right(ANGLE)  # Turn the head right by the angle constant


class Food:  # Class to create the food
    def __init__(self, food_color):  # initialize the food, pass in the food color
        self.food = turtle.Turtle()  # create a turtle object for the food
        self.food.speed(0)  # set the speed of the food to 0, this is the fastest speed, prevents animation of the food, so it moves instantly to the starting position
        self.food.shapesize(2, 2)  # set the size ratio of the food to 0.5:0.5, altering this ratio will warp the shape of the food
        self.food.shape("circle")  # set the shape of the food to a circle
        self.food.color(food_color)  # set the color of the food to the food color passed in the __init__ function
        self.food.penup()  # set the penup, this prevents the turtle from drawing a line when moving
        self.place_food_randomly()  # first food placement

    def place_food_randomly(self):  # method to place the food randomly
        x = random.randint(-290, 290)  # create an x coordinate for the food between -290 and 290
        y = random.randint(-290, 290)  # create a y coordinate for the food between -290 and 290
        self.food.goto(x, y)  # set the position of the food to the x and y coordinates


class KeyHandler:  # Class to handle keyboard events
    def __init__(self, screen):  # initialize the key handler, pass in the screen
        self.screen = screen  # set the screen to the screen passed in
        self.active_keys_red = set()  # initialize the active keys set for the red snake
        self.active_keys_blue = set()  # initialize the active keys set for the blue snake
        self.bind_keys_to_screen()  # now call the bind_keys_to_screen function to bind the keys to the screen

    def press_key_red_left(self):  # method to handle the red snake turning left
        self.active_keys_red.add("left")  # add the left key to the active keys set for the red snake

    def release_key_red_left(self):  # method to handle the red snake releasing the left key
        self.active_keys_red.remove("left")  # remove the left key from the active keys set for the red snake

    def press_key_red_right(self):  # method to handle the red snake turning right
        self.active_keys_red.add("right")  # add the right key to the active keys set for the red snake

    def release_key_red_right(self):  # method to handle the red snake releasing the right key
        self.active_keys_red.remove("right")  # remove the right key from the active keys set for the red snake

    def press_key_blue_left(self):  # method to handle the blue snake turning left
        self.active_keys_blue.add("left")  # add the left key to the active keys set for the blue snake

    def release_key_blue_left(self):  # method to handle the blue snake releasing the left key
        self.active_keys_blue.remove("left")  # remove the left key from the active keys set for the blue snake

    def press_key_blue_right(self):  # method to handle the blue snake turning right
        self.active_keys_blue.add("right")  # add the right key to the active keys set for the blue snake

    def release_key_blue_right(self):  # method to handle the blue snake releasing the right key
        self.active_keys_blue.remove("right")  # remove the right key from the active keys set for the blue snake

    def bind_keys_to_screen(self):  # method to bind the keys to the screen
        self.screen.listen()  # tell the screen to listen for key presses
        self.screen.onkeypress(self.press_key_red_left, "a")  # bind the a key to the press_key_red_left function
        self.screen.onkeyrelease(self.release_key_red_left, "a")  # bind the a key to the release_key_red_left function
        self.screen.onkeypress(self.press_key_red_right, "d")  # bind the d key to the press_key_red_right function
        self.screen.onkeyrelease(self.release_key_red_right, "d")  # bind the d key to the release_key_red_right function
        self.screen.onkeypress(self.press_key_blue_left, "Left")  # bind the Left arrow key to the press_key_blue_left function
        self.screen.onkeyrelease(self.release_key_blue_left, "Left")  # bind the Left arrow key to the release_key_blue_left function
        self.screen.onkeypress(self.press_key_blue_right, "Right")  # bind the Right arrow key to the press_key_blue_right function
        self.screen.onkeyrelease(self.release_key_blue_right, "Right")  # bind the Right arrow key to the release_key_blue_right function


class Popups:  # Class to display popups
    def display_winner(winner_color, callback):  # Function to display the winner
        announcement = turtle.Turtle()  # Create a turtle object for the announcement
        announcement.speed(0)  # set the speed of the announcement to 0, this is the fastest speed, prevents animation of the announcement, so it moves instantly to the starting position
        announcement.color(winner_color)  # set the color of the announcement to the winner color passed into this method
        announcement.hideturtle()  # hide the turtle so it doesn't show up on screen
        announcement.penup()  # set the penup, this prevents the turtle from drawing a line when moving

        announcement.goto(0, 100)  # Position the turtle at the top of the screen for the first line
        announcement.write(f"{winner_color.capitalize()} Snake Wins!", align="center", font=("Arial", 50, "bold"))  # Write the first line

        announcement.goto(0, -100)  # Position the turtle at the bottom of the screen for the second line
        announcement.write("Press ENTER to play again!", align="center", font=("Arial", 50, "normal"))  # Write the second line

        turtle.Screen().onkeypress(callback, "Return")  # Bind the Enter key to the callback function
        turtle.Screen().listen()  # Tell the screen to listen for key presses

        announcement.hideturtle()  # Hide the turtle after writing to prevent it from showing up on screen


class Game(CollisionManager):  # Class to create the game, inherits from the CollisionManager class
    def __init__(self, screen):  # initialize the game, pass in the screen
        self.instance = self  # set the instance to this instance of the game
        self.screen = screen  # set the screen to the screen passed in
        self.collision_manager = CollisionManager()  # create a collision manager object
        self.red_snake = Snake(RED, -100, 0, 0)  # create the red snake, put it on the left side of the screen
        self.blue_snake = Snake(BLUE, 100, 0, 180)  # create the blue snake, put it on the right side of the screen
        self.good_food_instance = Food(food_color=GOOD_FOOD_COLOR)  # create the gain segment food
        self.bad_food_instance = Food(food_color=BAD_FOOD_COLOR)  # create the lose segment food
        self.key_handler = KeyHandler(self.screen)  # create the key handler
        self.game_loop()  # now call the game loop function to start the game

    def restart_game(self):  # Method to restart the game if the user presses the Enter key after a game ends
        turtle.clearscreen()  # Clear the screen
        screen = CreateScreen.create_screen()  # Create a new screen
        game = Game(screen)  # Create a new game
        screen.mainloop()  # Start the main loop

    def game_loop(self):  # Method to run the game loop
        if "left" in self.key_handler.active_keys_red:  # if the left key is in the active keys set for the red snake
            self.red_snake.left()  # call the left method of the red snake
        if "right" in self.key_handler.active_keys_red:  # if the right key is in the active keys set for the red snake
            self.red_snake.right()  # call the right method of the red snake
        if "left" in self.key_handler.active_keys_blue:  # if the left key is in the active keys set for the blue snake
            self.blue_snake.left()  # call the left method of the blue snake
        if "right" in self.key_handler.active_keys_blue:  # if the right key is in the active keys set for the blue snake
            self.blue_snake.right()  # call the right method of the blue snake

        self.red_snake.move()  # move the red snake forward
        self.blue_snake.move()  # move the blue snake forward

        if (
            self.red_snake.body[0].distance(self.good_food_instance.food) <= FOOD_COLLISION_DISTANCE
        ):  # if the distance between the head of the red snake and the good food is less than or equal to the food collision distance
            self.good_food_instance.place_food_randomly()  # place the good food to a new random location
            self.red_snake.add_segment()  # add a segment to the red snake
            self.red_snake.snake_speed /= 1.01  # increase the speed of the red snake by 1% to make the game more challenging

        if (
            self.blue_snake.body[0].distance(self.good_food_instance.food) <= FOOD_COLLISION_DISTANCE
        ):  # if the distance between the head of the blue snake and the good food is less than or equal to the food collision distance
            self.good_food_instance.place_food_randomly()  # place the good food to a new random location
            self.blue_snake.add_segment()  # add a segment to the blue snake
            self.blue_snake.snake_speed /= 1.01  # increase the speed of the blue snake by 1% to make the game more challenging

        if (
            self.red_snake.body[0].distance(self.bad_food_instance.food) <= FOOD_COLLISION_DISTANCE
        ):  # if the distance between the head of the red snake and the bad food is less than or equal to the food collision distance
            if self.red_snake.can_lose_segment():  # check if the red snake can lose a segment
                if len(self.red_snake.body) > 1:  # check if the red snake has more than one segment
                    self.bad_food_instance.place_food_randomly()  # if it does, place the bad food to a new random location
                    self.red_snake.remove_segment()  # then remove a segment from the red snake
                    self.red_snake.snake_speed *= 1.01  # then decrease the speed of the red snake by 1% so you can move the snake closer to its original speed
                else:  # if the red snake only has one segment
                    Popups.display_winner(BLUE, self.restart_game)  # display the winner popup for the blue snake since that was the last segment the snake had to lose
                    return  # then return to exit the game loop

        if (
            self.blue_snake.body[0].distance(self.bad_food_instance.food) <= FOOD_COLLISION_DISTANCE
        ):  # if the distance between the head of the blue snake and the bad food is less than or equal to the food collision distance
            if self.blue_snake.can_lose_segment():  # check if the blue snake can lose a segment
                if len(self.blue_snake.body) > 1:  # check if the blue snake has more than one segment
                    self.bad_food_instance.place_food_randomly()  # if it does, place the bad food to a new random location
                    self.blue_snake.remove_segment()  # then remove a segment from the blue snake
                    self.blue_snake.snake_speed *= 1.01  # then decrease the speed of the blue snake by 1% so you can move the snake closer to its original speed
                else:  # if the blue snake only has one segment
                    Popups.display_winner(RED, self.restart_game)  # display the winner popup for the red snake since that was the last segment the snake had to lose
                    return  # then return to exit the game loop

        if self.blue_snake.collides_with(self.red_snake):  # if the blue snake collides with the red snake
            if self.blue_snake.is_longer_than(self.red_snake):  # check if the blue snake is longer than the red snake
                if self.red_snake.can_lose_segment():  # then check if the red snake can lose a segment
                    if len(self.red_snake.body) > 1:  # and if it has more than one segment
                        self.red_snake.remove_segment()  # if so, remove a segment from the red snake
                        self.red_snake.snake_speed *= 1.01  # then decrease the speed of the red snake by 1% so you can move the snake closer to its original speed
                        self.blue_snake.add_segment()  # then add a segment to the blue snake since it stole a segment from the red snake
                        self.blue_snake.snake_speed /= 1.01  # then increase the speed of the blue snake by 1% to make the game more challenging
                    else:  # if the red snake only has one segment
                        Popups.display_winner(BLUE, self.restart_game)  # display the winner popup for the blue snake since that was the last segment the red snake had to lose
                        return  # then return to exit the game loop

        if self.red_snake.collides_with(self.blue_snake):  # if the red snake collides with the blue snake
            if self.red_snake.is_longer_than(self.blue_snake):  # check if the red snake is longer than the blue snake
                if self.blue_snake.can_lose_segment():  # then check if the blue snake can lose a segment
                    if len(self.blue_snake.body) > 1:  # and if it has more than one segment
                        self.blue_snake.remove_segment()  # if so, remove a segment from the blue snake
                        self.blue_snake.snake_speed *= 1.01  # then decrease the speed of the blue snake by 1% so you can move the snake closer to its original speed
                        self.red_snake.add_segment()  # then add a segment to the red snake since it stole a segment from the blue snake
                        self.red_snake.snake_speed /= 1.01  # then increase the speed of the red snake by 1% to make the game more challenging
                    else:  # if the blue snake only has one segment
                        Popups.display_winner(RED, self.restart_game)  # display the winner popup for the red snake since that was the last segment the blue snake had to lose
                        return  # then return to exit the game loop

        self.screen.update()  # update the screen to show the changes made in the game loop
        self.screen.ontimer(self.game_loop, 50)  # call the game loop function again after 50 milliseconds to keep the game running smoothly


if __name__ == "__main__":  # if this file is being run directly
    screen = CreateScreen.create_screen()  # create the screen
    game = Game(screen)  # create the game and pass in the screen
    screen.mainloop()  # start the main loop
