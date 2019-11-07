
import random
import uwebsockets.client


class App():
    """
    Pong Battle Royal
    """

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Pong BR"

    def drawPlayer(self, x, y, w, h, status):
        for i in range(h*2 +1):
            for j in range(w):
                self.badge.screen.oled.pixel(int(x+j), int(y+i-h), status)
        return


    def run(self):
        if not self.badge.net.online():
            self.badge.show_text("No Internet")
            return

        websocket = uwebsockets.client.connect("ws://villagrasa.ch:8081/")
        

        sh, sw = 64, 128

        HEIGHT = 8

        player_x = 0
        player_y = int(sh/2)

        player2_x = sw-2
        player2_y = int(sh/2)

        key = "RIGHT"
        BALL_SPEED = 3

        ball_x = sw/2
        ball_y = sh/2

        self.badge.screen.oled.fill(0)
        self.badge.screen.oled.text("    Waiting", 1, 33)
        self.badge.screen.oled.show()

        side = websocket.recv()
        self.badge.screen.oled.fill(0)
        self.badge.screen.oled.show()

        if side == "LEFT":
            v = 1
        else:
            v = -1
        ball_vector = [
            v * BALL_SPEED,
            -BALL_SPEED
        ]

        while True:
            next_key = self.badge.buttons.get_button()
            key = key if next_key is None else next_key
            if key is None:
                continue
            if key == 'LEFT':
                return
            if key == 'DOWN':
                if player_y < (64-HEIGHT):
                    self.drawPlayer(player_x, player_y, 2, HEIGHT, 0)
                    player_y += 2
            if key == 'UP':
                if player_y > HEIGHT:
                    self.drawPlayer(player_x, player_y, 2, HEIGHT, 0)
                    player_y -= 2

            self.drawPlayer(player2_x, player2_y, 2, HEIGHT, 0)

            websocket.send(str(player_y))
            try:
                player2_y = int(websocket.recv())
                websocket.settimeout(5)
            except:
                self.badge.screen.oled.fill(0)
                self.badge.show_text("\n\n   TIMED OUT")
                return
            
            
            self.drawPlayer(player_x, player_y, 2, HEIGHT, 1)

            self.drawPlayer(player2_x, player2_y, 2, HEIGHT, 1)

            self.badge.screen.oled.pixel(int(ball_x), int(ball_y), 0)
            #Simulate ball
            ball_x += ball_vector[0]
            ball_y += ball_vector[1]

            #check sides

            if ball_x < 0:
                self.badge.screen.oled.fill(0)
                self.badge.show_text("\n\n   GAME OVER")
                return

            if ball_x > sw-1:
                websocket.send("END")
                self.badge.screen.oled.fill(0)
                self.badge.show_text("\n\n    YOU WIN")
                return

            if (ball_x < 5  and ball_y < player_y+HEIGHT and ball_y > player_y-HEIGHT) or (ball_x > sw-6 and ball_y < player2_y+HEIGHT and ball_y > player2_y-HEIGHT):
                ball_vector[0] = -ball_vector[0]

            #check sides
            if ball_y < 1 or ball_y > sh-1:
                ball_vector[1] = -ball_vector[1]

            self.badge.screen.oled.pixel(int(ball_x), int(ball_y), 1)
            
            #draw the raquet
            self.badge.screen.oled.show()

