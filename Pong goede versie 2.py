import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Pong"

STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
#Dit zijn 3 statussen.
#State_Menu, die gebruik je als je in het menu bent.
#state_Playing die gebruik je als je aan het spelen bent.
#State_game_over die gebruik je als je game over bent.

class scoreboard():

    def __init__(self):
        self.position_x = None
        self.position_y = None
        self.font_side = None
        self.color = None
        self.score = None

    def setup(self, position_x, position_y, font_side, color, score):

        self.position_x = position_x
        self.position_y = position_y
        self.font_side = font_side
        self.color = color
        self.score = score 

    def on_draw(self):
        arcade.draw_text(f" Score: {self.score}" , self.position_x, self.position_y, self.color, self.font_side)
        

    def on_update(self):
        arcade.draw_text(f" Score: {self.score}" , self.position_x, self.position_y, self.color, self.font_side)
        

class ball():

    def __init__(self):
        self.position_x = None
        self.position_y = None
        self.radius = None
        self.color = None

        self.delta_x = None
        self.delta_y = None

    def setup(self, position_x, position_y, radius, color, delta_x, delta_y):

        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.color = color

        self.delta_x = delta_x
        self.delta_y = delta_y

    def on_draw(self):
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def on_update(self, delta_time, paddle_a, paddle_b, score_board, score_board2):
        self.position_x = self.position_x + self.delta_x
        self.position_y = self.position_y + self.delta_y

        # als we de bovenkant raken, zet de beweegrihting naar beneden
        if self.position_y + self.radius >= SCREEN_HEIGHT:
            self.delta_y = self.delta_y * -1
            
        if self.position_y - self.radius <= 0:
            self.delta_y = self.delta_y * -1

        # als onze rechterkant groter of gelijk is aan paddle a zijn linkerkant EN ... etc.
        if self.position_x + self.radius >= paddle_a.position_x - paddle_a.width // 2 and \
            self.position_x - self.radius <= paddle_a.position_x + paddle_a.width // 2 and \
            self.position_y + self.radius >= paddle_a.position_y - paddle_a.height // 2 and \
            self.position_y - self.radius <= paddle_a.position_y + paddle_a.height // 2:
            self.delta_x *= -1 

        if self.position_x + self.radius >= paddle_b.position_x - paddle_b.width // 2 and \
            self.position_x - self.radius <= paddle_b.position_x + paddle_b.width // 2 and \
            self.position_y + self.radius >= paddle_b.position_y - paddle_b.height // 2 and \
            self.position_y - self.radius <= paddle_b.position_y + paddle_b.height // 2:
            self.delta_x *= -1


        if self.position_x >= 1000:
                self.position_x = SCREEN_WIDTH/2
                self.position_y = SCREEN_HEIGHT/2
                self.delta_x = self.delta_x * -1
                score_board.score += 1
        
        if self.position_x <= 0:
                score_board2.score += 1
                self.position_x = SCREEN_WIDTH/2
                self.position_y = SCREEN_HEIGHT/2
                self.delta_x = self.delta_x * -1
         
                

        #if self.position_x > 1000:
            #self.position_x(500, 400)
        
        #als de bal de rechterkant raakt, stuitert de bal terug
        #if  self.position_x + self.radius >= SCREEN_WIDTH:
            #self.delta_x = self.delta_x -1
        #als de bal de linkerkant van het scherm raakt gaat hij weer naar rechts. Het scherm loopt van 0 naar screen width. Dus de linkerkant heeft een 0 waarde    
        #if  self.position_x - self.radius <= 0:
            #self.delta_x = self.delta_x +1

class rectangle():

    def __init__(self):
        self.position_x = None
        self.position_y = None
        self.width = None
        self.height = None
        self.color = None
        self.tilt_angle = None
        self.change_y = None
        self.change_x = None
        #chang y & change x = hetzelfde als delta y & delta x. Delta = verschil & changes = veranderen. 
        #Staat voor de rectangle van plek veranderen

    def setup(self, position_x, position_y, width, height, color, change_y, change_x):

        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.color = color
        self.change_y = change_y
        self.change_x = change_x

    def on_draw(self):
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.height, self.color,)

    def on_update(self, delta_time):
        self.position_y += self.change_y * delta_time
        self.position_x += self.change_x * delta_time

        # Kijk of de paddle de top of de bodem van het scherm raakt.
        if self.position_y < self.height/2:
            self.position_y = self.height/2
        if self.position_y > SCREEN_HEIGHT - self.height/2:
            self.position_y = SCREEN_HEIGHT - self.height/2
        
class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.ball = None
        self.rectangle = None
        self.rectangle2 = None
        self.paddlespeed = 300
        self.score_board = None
        self.score_board2 = None
        self.game_state = None
        #De game state geeft aan in welke status je zit


    def setup(self):
        self.ball = ball()
        self.ball.setup(185, 185, 30, arcade.color.WHITE, 15, 15)

        self.rectangle = rectangle()
        self.rectangle.setup(40, 400, 50, 200, arcade.color.WHITE, 0, 0)

        self.rectangle2 = rectangle()
        self.rectangle2.setup(960, 400, 50, 200, arcade.color.WHITE, 0, 0)

        self.score_board = scoreboard()
        self.score_board.setup(SCREEN_WIDTH//7, 700, 40, arcade.color.LIGHT_GRAY, 0)
        
        self.score_board2 = scoreboard()
        self.score_board2.setup(658, 700, 40, arcade.color.LIGHT_GRAY, 0)
        self.game_state = 0

    def on_draw(self):
        arcade.start_render()
        #arcade render zorgt ervoor dat alles begint met tekenen. Dat hoeft maar 1x, en het hoeft niet gestopt te worden.
        
        if self.game_state == STATE_MENU:
            arcade.draw_text(f" PRESS SPACE TO PLAY" , SCREEN_WIDTH//10, 350, arcade.color.WHITE_SMOKE, 70, bold=True)

        if self.game_state == STATE_PLAYING:
            point_list = ((SCREEN_WIDTH//2, 800),
              (SCREEN_WIDTH//2, 780),
              (SCREEN_WIDTH//2, 740),
              (SCREEN_WIDTH//2, 720),
              (SCREEN_WIDTH//2, 680),
              (SCREEN_WIDTH//2, 660),
              (SCREEN_WIDTH//2, 620),
              (SCREEN_WIDTH//2, 600),
              (SCREEN_WIDTH//2, 560),
              (SCREEN_WIDTH//2, 540),
              (SCREEN_WIDTH//2, 500),
              (SCREEN_WIDTH//2, 480),
              (SCREEN_WIDTH//2, 440),
              (SCREEN_WIDTH//2, 420),
              (SCREEN_WIDTH//2, 380),
              (SCREEN_WIDTH//2, 360),
              (SCREEN_WIDTH//2, 320),
              (SCREEN_WIDTH//2, 300),
              (SCREEN_WIDTH//2, 260),
              (SCREEN_WIDTH//2, 240),
              (SCREEN_WIDTH//2, 200),
              (SCREEN_WIDTH//2, 180),
              (SCREEN_WIDTH//2, 140),
              (SCREEN_WIDTH//2, 120),
              (SCREEN_WIDTH//2, 80),
              (SCREEN_WIDTH//2, 60),
              (SCREEN_WIDTH//2, 20),
              (SCREEN_WIDTH//2, 0))
            arcade.draw_points(point_list, arcade.color.LIGHT_GRAY, 20)
            self.score_board.on_draw()
            self.score_board2.on_draw()
            self.ball.on_draw()
            self.rectangle.on_draw()
            self.rectangle2.on_draw()

        if self.game_state == STATE_GAME_OVER:
            arcade.draw_text(f" GAME OVER" , SCREEN_WIDTH//5, 350, arcade.color.WHITE_SMOKE, 80, bold=True)
        

    def on_update(self, delta_time):

        if self.game_state == STATE_PLAYING:
            self.ball.on_update(delta_time, self.rectangle, self.rectangle2, self.score_board, self.score_board2)
            self.rectangle.on_update(delta_time)
            self.rectangle2.on_update(delta_time)
            self.score_board2.on_update()
            self.score_board.on_update()

            if self.score_board.score == 3 or self.score_board2.score == 3:
                self.game_state = STATE_GAME_OVER
                

        if self.game_state == STATE_MENU:
            pass 

    def on_key_press(self, key, key_modifiers):
        if self.game_state == STATE_PLAYING:
            if key == arcade.key.UP:
                self.rectangle2.change_y = self.paddlespeed
            elif key == arcade.key.DOWN:
                self.rectangle2.change_y = -self.paddlespeed

            if key == arcade.key.W:
                self.rectangle.change_y = self.paddlespeed
            elif key == arcade.key.S:
                self.rectangle.change_y = -self.paddlespeed

        if self.game_state != STATE_PLAYING:
            if key == arcade.key.SPACE:
                self.game_state = STATE_PLAYING

        if self.game_state == STATE_GAME_OVER:
            if key == arcade.key.ENTER:
                self.game_state = STATE_MENU
        
            #Als je op spatie klikt, start de game
            # != Betekend is niet
            #Dat doe je zodat je niet midden in de game op spatie kan drukken
 
        

        #if(als) key = arcade.key.up: dan weet het programma dat je een toets aanslaat
        #elif(maar) key = arcade.key.dwon: dan weet het programma dat je een toets aanslaat naar beneden


    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.rectangle2.change_y = 0
        if key == arcade.key.W or key == arcade.key.S:
            self.rectangle.change_y = 0

        
        #Als je de toets los laat, is hij bezig met of omhoog via up of bezig met down via down, dan gaat hij staat hij stil(self.rectangle2.change_y=0)

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()
    #arcade run zorgt ervoor dat alle vensters worden getekend en dat is de loop. Hij blijft alles tekenen.

if __name__ == "__main__":
    main()
