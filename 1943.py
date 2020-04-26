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

SCREEN_WIDTH = 562
SCREEN_HEIGHT = 644
SCREEN_TITLE = "1943: The Battle of Midway"

# "states" of the game 
START_SCREEN = 0
INSTRUCTIONS = 1
GAME_RUNNING = 2
GAME_OVER = 3

ENEMY_COUNT = 50
MOVEMENT_SPEED  = 5
PLAYER_LIVES = 3

class Background(arcade.Sprite):

    def __init__(self,image):
        super().__init__(image)
        self.change_y = -10

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.top <= 0 : self.bottom = SCREEN_HEIGHT

class Furniture(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image)
        self.center_x = 0
        self.center_y = SCREEN_HEIGHT

    def update(self):
        if self.top<=0:self.kill()

class RedFighter(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image)
        self.center_x = 0
        self.center_y = 0

    def update(self):
        if self.top<=0:self.kill()

class Enemy(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image)
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT,SCREEN_HEIGHT*30)

    def update(self):
        if self.top<=0:self.kill()

class Enemy1(arcade.Sprite):
    def __init__(self,image):
        self = arcade.AnimatedTimeSprite("images/midway/Enemy1.png",0.8)
        self.textures.append(arcade.load_texture("images/midway/Enemy2.png"))
        self.textures.append(arcade.load_texture("images/midway/Enemy3.png"))
        self.scale = 1.0
        self.center_x = 0
        self.center_y = 0

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        if self.top<=0:self.kill()


class Explosion(arcade.Sprite):
    """ create explosion sprite"""
    def __init__(self, texture_list,x,y):
        """texture_list load"""
        super().__init__()
        self.center_x = x
        self.center_y = y
        # 第一帧
        self.current_texture = 0      # 这是造型索引号
        self.textures = texture_list  # 这是每帧图片列表
        self.set_texture(self.current_texture)

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()

class Bullet(arcade.Sprite):
    """ Bullet class, inherited from the character class that comes with Arcade, it is shot from the coordinates of the aircraft """
    def __init__(self,image,plane):
        super().__init__(image)
        self.center_x = plane.center_x
        self.center_y = plane.center_y
        self.change_y = 20

    def update(self):
        """ update coordinates"""
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.bottom >  SCREEN_HEIGHT: self.kill()

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

        # Crate the explosion animation
        self.enemy_explosion_images = []
        columns = 4
        count = 16
        sprite_width = 64
        sprite_height = 64
        file_name = "images/midway/explode.png"
        # Load the explosions from a sprite sheet
        self.enemy_explosion_images = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

        # Load music sounds
        self.background_music = arcade.sound.load_sound("images/midway/background.wav")
        self.shoot_sound = arcade.sound.load_sound("images/midway/Shot.wav")
        self.explode_sound = arcade.sound.load_sound("images/midway/explode.wav")
        self.powerup_sound = arcade.sound.load_sound("images/midway/powerup.wav")
        self.gameover_sound = arcade.sound.load_sound("images/midway/gameover.wav")

        # Play background music
        arcade.sound.play_sound(self.background_music)
        
    # STEP 2: Add this function.
        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Start 'state' will be showing the first page of instructions.
        self.current_state = START_SCREEN

        #self.player_list = None
        #self.coin_list = None

        # Set up the player
        self.player_sprite = None

        # Set up the enemy
        self.enemy_sprite = None

        # Set up the POW
        self.power_sprite = None

        # STEP 1: Put each instruction page in an image. Make sure the image
        # matches the dimensions of the window, or it will stretch and look
        # ugly. You can also do something similar if you want a page between
        # each level.
        self.instructions = []
        texture = arcade.load_texture("images/midway/Logo1.png")
        self.instructions.append(texture)
        texture = arcade.load_texture("images/midway/Logo2.png")
        self.instructions.append(texture)

        self.player_sprite = arcade.AnimatedTimeSprite("images/midway/Plane1.png",0.8)
        self.player_sprite.textures.append(arcade.load_texture("images/midway/Plane2.png"))
        self.player_sprite.textures.append(arcade.load_texture("images/midway/Plane3.png"))
        self.player_sprite.scale = 1.0
        
        self.enemy_sprite = arcade.AnimatedTimeSprite("images/midway/Enemy1.png",0.8)
        self.enemy_sprite.textures.append(arcade.load_texture("images/midway/Enemy2.png"))
        self.enemy_sprite.textures.append(arcade.load_texture("images/midway/Enemy3.png"))
        self.enemy_sprite.scale = 1.0

        self.power_sprite = arcade.AnimatedTimeSprite("images/midway/Pow1a.png",0.8)
        self.power_sprite.textures.append(arcade.load_texture("images/midway/Pow1b.png"))
        self.power_sprite.textures.append(arcade.load_texture("images/midway/Pow1c.png"))
        self.power_sprite.scale = 1.0

    def setup(self):
        """
        Set up the game.
        """
        self.score = 0
        self.enemy_shot = 0
        self.power_col = False
        self.powerup = 1
        enemy_shot = False
        powerup = True

        # Sprite lists
        self.cloud_list = arcade.SpriteList()

        self.enemy_list = arcade.SpriteList()
        self.red_list = arcade.SpriteList()

        self.bullet_list = arcade.SpriteList()

        self.enemy_explosion_list = arcade.SpriteList()
        self.power_list = arcade.SpriteList()

        self.all_sprites_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite.health  = PLAYER_LIVES        # No of Lives
        self.player_sprite.center_x = SCREEN_WIDTH //2
        self.player_sprite.center_y = 50
        self.all_sprites_list.append(self.player_sprite)

        self.enemy_sprite.center_x = SCREEN_WIDTH+30
        self.enemy_sprite.center_y = SCREEN_HEIGHT+30
        self.all_sprites_list.append(self.enemy_sprite)

        self.power_sprite.center_x = SCREEN_WIDTH+30
        self.power_sprite.center_y = SCREEN_HEIGHT+30
        self.all_sprites_list.append(self.power_sprite)

        # Set up enemies
        for i in range(ENEMY_COUNT):
            # Create Enemies
            enemy = Enemy("images/midway/Fighter1.png")
            self.enemy_list.append(enemy)
            self.all_sprites_list.append(enemy)

        for i in range(5):
            redfighter = RedFighter("images/midway/Fighter2.png")
            redfighter.center_x = 0
            redfighter.center_y = SCREEN_HEIGHT-i*30
            self.red_list.append(redfighter)
            self.all_sprites_list.append(redfighter)

        for i in range(5):
            clouds = Furniture("images/midway/cloud-right.png")
            clouds.center_x = SCREEN_WIDTH - (10 * i + random.randrange(10,50))
            clouds.center_y = SCREEN_HEIGHT + (300 * i) + random.randrange(0,1000)
            self.cloud_list.append(clouds)
            self.all_sprites_list.append(clouds)

        for i in range(5):
            clouds = Furniture("images/midway/cloud-left.png")
            clouds.center_x = 10 * i + random.randrange(10,50)
            clouds.center_y = SCREEN_HEIGHT + (300 * i) + random.randrange(0,1000)
            self.cloud_list.append(clouds)
            self.all_sprites_list.append(clouds)

        sea_image = "images/midway/sea.png"
        # Setting a Fixed Background To cover up rolling background cracks
        self.background = arcade.Sprite(sea_image)
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.bottom = 0

        # Set the scrolling background, the two first drawn characters move down,
        # move to a certain coordinate and go to the top
        self.background1 = Background(sea_image)
        self.background1.center_x = SCREEN_WIDTH // 2
        self.background1.bottom = 0
        self.all_sprites_list.append(self.background1)

        self.background2 = Background(sea_image)
        self.background2.center_x = SCREEN_WIDTH // 2
        self.background2.bottom = SCREEN_HEIGHT
        self.all_sprites_list.append(self.background2)

        self.interval = 60
        self.interval_counter = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

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
        # Start rendering, this command must be before all redraw commands
        self.background.draw()    # Unmovable background to make up for
                                  # the problem of rolling background cracks
        self.background1.draw()   # Paint scroll background
        self.background2.draw()   # Paint scroll background

        self.cloud_list.draw()
        # Draw all the characters
        self.enemy_list.draw()
        self.red_list.draw()
        if self.player_sprite.health > 0:
           self.player_sprite.draw()
        self.bullet_list.draw()
        self.enemy_sprite.draw()
        self.power_sprite.draw()
        self.enemy_explosion_list.draw()

        # 画得分情况
        score = "Kills: " + str(self.score) + ", Lives: " + str(self.player_sprite.health)
        arcade.draw_text(score, 10, 20, arcade.color.WHITE, 14 )

        if self.player_sprite.health < 1:  # end of game
           self.interval_counter +=1
           if self.interval_counter % self.interval == 0: self.interval_counter = 0


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
            arcade.draw_text(output, 272, 117, arcade.color.BLACK, 24)
            arcade.draw_text(output, 275, 120, arcade.color.WHITE, 24)
            output = "Press SPACE to play"
            arcade.draw_text(output, 272, 87, arcade.color.BLACK, 24)
            arcade.draw_text(output, 275, 90, arcade.color.WHITE, 24)

        elif self.current_state == INSTRUCTIONS:
            self.draw_instructions_page(1)
            output = "W: up, S: down, A: left, D: right, J: fire"
            arcade.draw_text(output, 50, 342, arcade.color.BLACK, 24)
            arcade.draw_text(output, 48, 344, arcade.color.WHITE, 24)
            output = "Press SPACE to play"
            arcade.draw_text(output, 150, 286, arcade.color.BLACK, 24)
            arcade.draw_text(output, 148, 288, arcade.color.WHITE, 24)

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

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        # Only move the user if the game is running.
        #if self.current_state == GAME_RUNNING:
        #    self.player_sprite.center_x = x
        #    self.player_sprite.center_y = y

    def on_key_press(self, key, modifiers):
        """ Key button events """
        if key == arcade.key.ENTER:
            arcade.sound.play_sound(self.explode_sound)
            if self.current_state == START_SCREEN:
                self.current_state = INSTRUCTIONS
            elif self.current_state == INSTRUCTIONS:
                self.current_state = START_SCREEN
            elif self.current_state == GAME_OVER:
                self.current_state = INSTRUCTIONS
        if key == arcade.key.SPACE and self.current_state != GAME_RUNNING:
            self.current_state = GAME_RUNNING
            self.setup()

        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.J:
            arcade.sound.play_sound(self.shoot_sound)
            self.bullet = Bullet("images/midway/Shot1.png",self.player_sprite)
            self.bullet_list.append(self.bullet)
            self.all_sprites_list.append(self.bullet)

    def on_key_release(self, key, modifiers):
        """ Key release event """
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    # STEP 7: Only update if the game state is GAME_RUNNING like below:
    def update(self, delta_time):
        """ Movement and game logic """
        # Animate the player on the start screen
        if self.current_state == START_SCREEN:
            self.player_sprite.update()
            self.player_sprite.update_animation()

        # Only move and do things if the game is running.
        if self.current_state == GAME_RUNNING:
            # Update coordinates, etc.
            #print(self.background2.bottom - self.background1.top)
            distance = self.background2.bottom - self.background1.top
            if  distance < 0 and distance > -80:   # Fissure remedy
                self.background2.bottom = self.background1.top

            self.enemy_list.move(0, -5)
            self.red_list.move(1,-2)
            self.cloud_list.move(0,-2)
            self.player_sprite.update_animation()
            self.enemy_sprite.update_animation()
            self.power_sprite.update_animation()
            self.all_sprites_list.update()

            if self.player_sprite.health > 0:
                # Collision detection between players and all enemy aircraft.
                for enemy_list in [ self.enemy_list, self.red_list ]:
                    hit_list = arcade.check_for_collision_with_list(self.player_sprite,enemy_list)
                    # Traverse the list of enemy aircraft encountered
                    for enemy in hit_list:
                        enemy.kill()
                        self.player_sprite.health -= 1
                        if self.player_sprite.health < 0 :
                            e = Explosion(self.enemy_explosion_images)
                            e.center_x = self.player_sprite.center_x
                            e.center_y = self.player_sprite.center_y
                            e.update()
                            self.player_sprite.kill()

                        e = Explosion(self.enemy_explosion_images,enemy.center_x,enemy.center_y)
                        e.center_x = enemy.center_x
                        e.center_y = enemy.center_y
                        e.update()
                        arcade.sound.play_sound(self.explode_sound)
                        self.enemy_explosion_list.append(e)
                        self.all_sprites_list.append(e)

            # Is Powerup dropped?
            if self.powerup:
                self.power_sprite.top = self.power_sprite.top - 2
                self.power_sprite.update()
                # pickup power up
                power_col = arcade.check_for_collision(self.power_sprite,self.player_sprite)
                if power_col:
                    arcade.sound.play_sound(self.powerup_sound)
                    self.powerup = 0
                    self.power_sprite.kill()

            if not self.enemy_shot:
                enemy_hit = arcade.check_for_collision(self.enemy_sprite,self.player_sprite)
                if enemy_hit:
                    print(self.enemy_sprite.left,self.enemy_sprite.top)
                    self.enemy_shot = True
                    self.enemy_sprite.kill()
                    self.enemy_sprite.update()
                    es = Explosion(self.enemy_explosion_images,self.enemy_sprite.center_x,self.enemy_sprite.center_y)
                    es.center_x = self.enemy_sprite.center_x
                    es.center_y = self.enemy_sprite.center_y
                    es.update()
                    self.enemy_explosion_list.append(es)
                    self.all_sprites_list.append(es)

            print(self.player_sprite.left,self.player_sprite.top)

            if self.power_sprite.top < 0:
                self.power_sprite.kill()
                self.powerup = 0

            # Did we shoot the powerup enemy?
            if not self.enemy_shot:

               self.enemy_sprite.right = self.enemy_sprite.right - 1
               self.enemy_sprite.top = self.enemy_sprite.top - 1

               shot_enemy = arcade.check_for_collision_with_list(self.enemy_sprite,self.bullet_list)
               if len(shot_enemy) > 0:
                   arcade.sound.play_sound(self.explode_sound)
                   self.enemy_sprite.remove_from_sprite_lists()
                   self.enemy_sprite.kill()
                   es = Explosion(self.enemy_explosion_images,self.enemy_sprite.center_x,self.enemy_sprite.center_y)
                   es.center_x = self.enemy_sprite.center_x
                   es.center_y = self.enemy_sprite.center_y
                   es.update()
                   self.enemy_explosion_list.append(es)
                   self.all_sprites_list.append(es)
                   self.enemy_shot = 1
                   self.power_sprite.top = self.enemy_sprite.top
                   self.power_sprite.center_x = self.enemy_sprite.center_x
                   self.power_sprite.center_y = self.enemy_sprite.center_y
                   self.power_sprite.update_animation()
                   self.power_sprite.update()

            # Did each enemy hit the bullet
            for enemy_bullet in [ self.enemy_list, self.red_list ]:
                for enemy in enemy_bullet:
                    hit_list = arcade.check_for_collision_with_list(enemy,self.bullet_list)
                    if len(hit_list) > 0:
                        enemy.kill()
                        arcade.sound.play_sound(self.explode_sound)
                        [b.kill() for b in hit_list]   # Delete every bullet encountered
                        self.score += len(hit_list)
                        e = Explosion(self.enemy_explosion_images,enemy.center_x,enemy.center_y)
                        e.center_x = enemy.center_x
                        e.center_y = enemy.center_y
                        e.update()
                        self.enemy_explosion_list.append(e)
                        self.all_sprites_list.append(e)

            # If we've collected all the games, then move to a "GAME_OVER" state.
            if self.player_sprite.health <= 0:
                e = Explosion(self.enemy_explosion_images,self.player_sprite.center_x,self.player_sprite.center_y)
                e.center_x = self.player_sprite.center_x
                e.center_y = self.player_sprite.center_y
                e.update()
                self.enemy_explosion_list.append(e)
                self.all_sprites_list.append(e)
                self.power_sprite.update()
                self.current_state = GAME_OVER
                self.background_music.stop()
                arcade.sound.play_sound(self.gameover_sound)
                arcade.pause(3)
                self.set_mouse_visible(True)

            if self.player_sprite.left < 0:
                self.player_sprite.left = 0
            elif self.player_sprite.right > SCREEN_WIDTH - 1:
                self.player_sprite.right = SCREEN_WIDTH - 1

            if self.player_sprite.bottom < 60:
                self.player_sprite.bottom = 60
            elif self.player_sprite.top > SCREEN_HEIGHT - 1:
                self.player_sprite.top = SCREEN_HEIGHT - 1


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
