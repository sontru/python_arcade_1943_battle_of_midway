"""
This program shows how to:
  * Have one or more instruction screens
  * Show a 'Game over' text and halt the game
  * Allow the user to restart the game


If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.instruction_and_game_over_screens
"""

import arcade
import random
import os

SPRITE_SCALING = 1.0

SCREEN_WIDTH = 568
SCREEN_HEIGHT = 650
SCREEN_TITLE = "1943 Battle of Midway"

# These numbers represent "states" that the game can be in.
START_SCREEN = 0
INSTRUCTIONS = 1
GAME_RUNNING = 2
GAME_OVER = 3

ENEMY_COUNT = 5
MOVEMENT_SPEED  = 5
PLAYER_LIVES = 3

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, screen_width, screen_height, title):
        """ Constructor """
        # Call the parent constructor. Required and must be the first line.
        super().__init__(screen_width, screen_height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Start 'state' will be showing the first page of instructions.
        self.current_state = START_SCREEN

        self.player_list = None
        self.coin_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None

        # STEP 1: Put each instruction page in an image. Make sure the image
        # matches the dimensions of the window, or it will stretch and look
        # ugly. You can also do something similar if you want a page between
        # each level.
        self.instructions = []
        texture = arcade.load_texture("images/midway/Logo1.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/midway/Logo2.png")
        self.instructions.append(texture)

    def setup(self):
        """
        Set up the game.
        """
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite("images/midway/Plane1.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(ENEMY_COUNT):

            # Create the coin instance
            coin = arcade.Sprite("images/midway/Fighters.png", SPRITE_SCALING / 3)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

    # STEP 2: Add this function.
    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)


    # STEP 3: Add this function
    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        self.draw_instructions_page(1)

        output = "Game Over"
        arcade.draw_text(output, 150, 322, arcade.color.BLACK, 44)

        output = "Press SPACE to restart"
        arcade.draw_text(output, 145, 40, arcade.color.BLACK, 24)


    # STEP 4: Take the drawing code you currently have in your
    # on_draw method AFTER the start_render call and MOVE to a new
    # method called draw_game.
    def draw_game(self):
        """
        Draw all the sprites, along with the score.
        """
        # Draw all the sprites.
        self.player_list.draw()
        self.coin_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    # STEP 5: Update the on_draw function to look like this. Adjust according
    # to the number of instruction pages you have.
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.current_state == START_SCREEN:
            self.draw_instructions_page(0)
            logo_1943 = arcade.Sprite("images/midway/1943Logo.png")
            logo_1943.center_x  = SCREEN_WIDTH // 2
            logo_1943.center_y  = 500
            arcade.Sprite.draw(logo_1943)
            output = "The Battle of Midway"
            arcade.draw_text(output, 40, 360, arcade.color.BLACK, 44, bold=True)
            arcade.draw_text(output, 45, 365, arcade.color.WHITE, 44, bold=True)
            output = "Press Enter for Keys"
            arcade.draw_text(output, 275, 120, arcade.color.WHITE, 24)
            output = "Press SPACE to play"
            arcade.draw_text(output, 275, 90, arcade.color.BLACK, 24)

        elif self.current_state == INSTRUCTIONS:
            self.draw_instructions_page(1)
            output = "W: up, S: down, A: left, D: right, J: fire"
            arcade.draw_text(output, 50, 342, arcade.color.BLACK, 24)
            output = "Press SPACE to play"
            arcade.draw_text(output, 150, 40, arcade.color.BLACK, 24)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        else:
            self.draw_game()
            self.draw_game_over()

    # STEP 6: Do something like adding this to your on_mouse_press to flip
    # between instruction pages.
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == START_SCREEN:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS
        elif self.current_state == INSTRUCTIONS:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        # Only move the user if the game is running.
        if self.current_state == GAME_RUNNING:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y

    # STEP 7: Only update if the game state is GAME_RUNNING like below:
    def update(self, delta_time):
        """ Movement and game logic """

        # Only move and do things if the game is running.
        if self.current_state == GAME_RUNNING:
            # Call update on all sprites (The sprites don't do much in this
            # example though.)
            self.coin_list.update()
            self.player_list.update()

            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

            # Loop through each colliding sprite, remove it, and add to the
            # score.
            for coin in hit_list:
                coin.kill()
                self.score += 1

            # If we've collected all the games, then move to a "GAME_OVER"
            # state.
            if len(self.coin_list) == 0:
                self.current_state = GAME_OVER
                self.set_mouse_visible(True)


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
