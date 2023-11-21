import pygame

from pygame.locals import *

from sys import exit

from random import randrange

pygame.init()

# clock = pygame.time.Clock()
# fps = 120

screen = pygame.display.set_mode((0, 0), FULLSCREEN, 32)
w = screen.get_width()

h = screen.get_height()


# PixelToScreenSize
def PSS(pixel):
    return int(w * (pixel / 1500))


pygame.mouse.set_visible(False)
loadBackground = pygame.image.load("Background.png").convert()
background = pygame.transform.scale(loadBackground, (w, h))
loadPlayer = pygame.image.load("Present.png").convert_alpha()
player = pygame.transform.scale(loadPlayer, (PSS(50), PSS(50)))
loadPresent = pygame.image.load("Present.png").convert_alpha()
present = pygame.transform.scale(loadPresent, (PSS(50), PSS(50)))
loadSledge = pygame.image.load("Sledge.png").convert_alpha()
sledgeImg = pygame.transform.scale(loadSledge, (PSS(330), PSS(85)))
loadObstacle = pygame.image.load("GreenPresent.png").convert_alpha()
obstaclePicture = pygame.transform.scale(loadObstacle, (PSS(50), PSS(50)))
loadResetButton = pygame.image.load("reset.png").convert_alpha()
ResetButtonPicture = pygame.transform.scale(loadResetButton, (PSS(100), PSS(100)))
loadPlayer2 = pygame.image.load("bluePresent.png").convert_alpha()
present2 = pygame.transform.scale(loadPlayer2, (PSS(50), PSS(50)))
pygame.mixer.init()
pygame.mixer.music.load("SchneeflöckchenWeißröckchen.mp3")
pygame.mixer.music.play(-1, 2.5)

singleplayer_rect = Rect(0, 0, 0, 0)
multiplayer_rect = Rect(0, 0, 0, 0)


def Startup():
    pygame.mouse.set_visible(True)
    screen.fill(0)
    font = pygame.font.Font(None, PSS(80))
    title = font.render("kleiner 3rd-person 2d-Shooter im Weihnachtsflair", True, (255, 255, 255))
    font = pygame.font.Font(None, PSS(50))
    authors = font.render("von Gabriel Endres und Philippe Zimmermann", True, (255, 255, 255))
    time_and_place = font.render("Schuljahr 2020/21 am Gymnasium Überlingen, Informatik", True, (255, 255, 255))

    title_rect = title.get_rect(center=(w / 2, h / 10))
    authors_rect = authors.get_rect(center=(w / 2, h / 4))
    time_and_place_rect = time_and_place.get_rect(center=(w / 2, h / 3))

    screen.blit(title, title_rect)
    screen.blit(authors, authors_rect)
    screen.blit(time_and_place, time_and_place_rect)

    choose_mode = font.render("bitte Spielmodus wählen", True, (255, 255, 255))
    singleplayer = font.render("ein Spieler", True, (255, 255, 255))
    multiplayer = font.render("zwei Spieler", True, (255, 255, 255))

    choose_mode_rect = choose_mode.get_rect(center=(w / 2, h / 1.5))
    global singleplayer_rect
    singleplayer_rect = singleplayer.get_rect(center=(w / 2 - PSS(200), h / 1.2))
    global multiplayer_rect
    multiplayer_rect = multiplayer.get_rect(center=(w / 2 + PSS(200), h / 1.2))

    screen.blit(choose_mode, choose_mode_rect)
    screen.blit(singleplayer, singleplayer_rect)
    screen.blit(multiplayer, multiplayer_rect)


def Instructions(position):
    t = ""
    text_rect = Rect(0, 0, 0, 0)
    if position == 1:
        t = "Einzelspieler: Steuere mit der Maus und schieße per Links- bzw. Rechtsklick."
    if position == 2:
        t = "Zwei Spieler benötigt: Lokales Duell um den höheren Punktestand! Spieler 1 steuert mit WASD, " \
            "Spieler 2 mit den Pfeiltasten."
    font = pygame.font.Font(None, PSS(25))
    text = font.render(t, True, (255, 255, 255))
    if position == 1:
        text_rect = text.get_rect(center=(w / 2 - PSS(200), h / 1.2 + PSS(50)))
    if position == 2:
        text_rect = text.get_rect(center=(w / 2 + PSS(200), h / 1.2 + PSS(50)))
    screen.blit(text, text_rect)


class GUI:
    def __init__(self):
        self.startMenue = False
        self.gameRunning = False
        self.basic_font = pygame.font.Font(None, PSS(100))
        self.t = "Start"
        self.text = self.basic_font.render(self.t, True, (255, 0, 0))
        self.text_rect = self.text.get_rect(center=(w / 2, h / 2))
        self.scoreVarP1 = 0
        self.scoreVarP2 = 0
        self.win_counter = [0, 0]
        self.win_updated = False
        self.win_updater = False
        self.flights = 1
        self.level = 1
        self.highScore = 0
        self.players = 1
        self.Is_dead_p1 = False
        self.Is_dead_p2 = True

    def startMenueMethod(self):

        pygame.draw.rect(screen, (200, 200, 200), self.text_rect)
        screen.blit(self.text, self.text_rect)

    def deathScreen(self):
        if self.win_updater:
            self.win_updated = False

        if self.Is_dead_p1 and self.players == 1:
            font = pygame.font.Font(None, PSS(50))
            text = font.render("Dein Ergebnis : " + str(self.scoreVarP1), True, (255, 255, 255))

            if self.scoreVarP1 > self.highScore:
                high_score_text = font.render("Neuer Rekord!", True, (255, 255, 255))
            else:
                high_score_text = font.render("Bestleistung : " + str(self.highScore), True, (255, 255, 255))
            high_score_text_rect = high_score_text.get_rect(center=(w / 2, h / 5))
            text_rect = text.get_rect(center=(w / 2, h / 10))

            screen.blit(text, text_rect)
            screen.blit(high_score_text, high_score_text_rect)

            t = "Runde beendet."
            text = self.basic_font.render(t, True, (255, 0, 0))
            text_rect = text.get_rect(center=(w / 2, h / 2))
            screen.blit(text, text_rect)
            screen.blit(ResetButtonPicture, (w / 2 - ResetButtonPicture.get_width() / 2, h / 2 + PSS(50)))

        if self.Is_dead_p1 and self.players == 2 and not self.Is_dead_p2:
            font = pygame.font.Font(None, PSS(50))
            t = "Spieler 1 ist ausgeschieden."
            text = font.render(t, True, (255, 0, 0))
            text_rect = text.get_rect(center=(w / 2 - PSS(200), h / 10 + PSS(50)))
            screen.blit(text, text_rect)

        if self.Is_dead_p2 and not self.Is_dead_p1 and self.players == 2:
            font = pygame.font.Font(None, PSS(50))
            t = "Spieler 2 ist ausgeschieden."
            text = font.render(t, True, (0, 0, 255))
            text_rect = text.get_rect(center=(w / 2 + PSS(200), h / 10 + PSS(50)))
            screen.blit(text, text_rect)

        if self.Is_dead_p1 and self.Is_dead_p2 and self.players == 2:
            t = "Runde beendet."
            text = self.basic_font.render(t, True, (255, 0, 0))
            text_rect = text.get_rect(center=(w / 2, h / 2))
            screen.blit(text, text_rect)
            screen.blit(ResetButtonPicture, (w / 2 - ResetButtonPicture.get_width() / 2, h / 2 + PSS(50)))

            if self.scoreVarP1 > self.scoreVarP2:
                a = "Sieg Spieler 1!"
                ab = self.basic_font.render(a, True, (255, 0, 0))
                if not self.win_updated:
                    self.win_counter[0] += 1
                    self.win_updated = True
                    self.win_updater = False

            elif self.scoreVarP2 > self.scoreVarP1:
                a = "Sieg Spieler 2!"
                ab = self.basic_font.render(a, True, (0, 0, 255))
                if not self.win_updated:
                    self.win_counter[1] += 1
                    self.win_updated = True
                    self.win_updater = False

            else:
                a = "Unentschieden."
                ab = self.basic_font.render(a, True, 120)
            ab_rect = ab.get_rect(center=(w / 2, h / 3))
            screen.blit(ab, ab_rect)

    def Score(self):
        font = pygame.font.Font(None, PSS(100))
        text_p1 = font.render(str(self.scoreVarP1), True, (255, 255, 255))

        if self.players == 1:
            text_p1_rect = text_p1.get_rect(center=(w / 2, h / 10))
        else:
            text_p1_rect = text_p1.get_rect(center=(w / 2 - PSS(200), h / 10))
            text_p2 = font.render(str(self.scoreVarP2), True, (255, 255, 255))
            text_p2_rect = text_p2.get_rect(center=(w / 2 + PSS(200), h / 10))
            screen.blit(text_p2, text_p2_rect)

            font = pygame.font.Font(None, PSS(50))
            wins_p1 = font.render("Siege Rot : " + str(self.win_counter[0]), True, (255, 0, 0))
            wins_p2 = font.render("Siege Blau : " + str(self.win_counter[1]), True, (0, 0, 255))
            wins_p1_rect = wins_p1.get_rect(center=(PSS(110), h/10))
            wins_p2_rect = wins_p2.get_rect(center=(w - PSS(120), h/10))
            screen.blit(wins_p1, wins_p1_rect)
            screen.blit(wins_p2, wins_p2_rect)

        screen.blit(text_p1, text_p1_rect)

    def levels(self):
        if self.flights >= self.level * 2:
            self.level += 1


class Player:

    def __init__(self, user):
        if gui.players == 1:
            self.x = w / 2
        else:
            self.x = w / 2 - PSS(25)
        self.y = (h / 10) * 9
        self.user = user
        self.moveleft = False
        self.moveright = False
        if self.user == 1:
            self.pic = player
        else:
            self.pic = present2

    def show(self):
        screen.blit(self.pic, (self.x, self.y))

    def move(self):
        if gui.players == 1:
            mouse_x_y = pygame.mouse.get_pos()
            if PSS(25) <= mouse_x_y[0] <= w:
                self.x = mouse_x_y[0] - PSS(25)
            if mouse_x_y[0] > w - PSS(25):
                self.x = w - PSS(50)

    def move_left(self):
        self.x -= PSS(10)
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += PSS(10)
        if self.x > w - PSS(50):
            self.x = w - PSS(50)


class Projectile:
    def __init__(self, initiator, direction):
        self.PresentClock = pygame.time.Clock()
        self.belonging = initiator
        self.x = p[self.belonging - 1].x
        self.y = p[self.belonging - 1].y
        self.d = direction
        self.s = PSS(-1400)
        self.g = PSS(1400)
        self.bounce = 1
        for e in range(3):
            if self.d == e:
                self.vel = [(e - 1) * -1 * self.s * 0.5, self.s]
        self.collision_active = False
        if self.belonging == 1:
            self.pic = present
        else:
            self.pic = present2

    def show(self):
        screen.blit(self.pic, (self.x, self.y))

    def move(self):

        if self.x <= 0:
            self.vel[0] *= -1
            self.x = 1

        if self.x + 50 >= w:
            self.vel[0] *= -1
            self.x = w - 51

        if self.y <= 0 and self.bounce == 1 or self.y >= h - PSS(40) and self.bounce == 1:
            self.vel[1] *= -1
            self.bounce = 0

        time_passed = self.PresentClock.tick()
        time_passed_seconds = time_passed / 1000.0
        distance_moved_x = time_passed_seconds * self.vel[0]
        distance_moved_y = time_passed_seconds * self.vel[1]
        distance_moved_grav = time_passed_seconds * self.g

        self.vel[1] += distance_moved_grav
        self.x += distance_moved_x
        self.y += distance_moved_y

        if self.y <= h / 2:
            self.collision_active = True


class Snowflake:

    def __init__(self):
        self.SnowflakeClock = pygame.time.Clock()
        self.x = randrange(20, w - 20)
        self.y = PSS(-100)
        self.r = PSS(10)
        self.vel = PSS(400)

    def show(self):
        pygame.draw.ellipse(screen, (255, 255, 255), (self.x, self.y, self.r * 2, self.r * 2))

    def move(self):
        time_passed = self.SnowflakeClock.tick()
        time_passed_seconds = time_passed / 1000.0
        distance_moved_y = time_passed_seconds * self.vel

        self.y += distance_moved_y


class Sledge:

    def __init__(self):
        self.SledgeClock = pygame.time.Clock()
        self.x = PSS(-699)
        self.y = h / 4 + randrange(PSS(300))
        self.vel = [PSS(1000), 0]
        self.RL = 0
        self.s = pygame.transform.flip(sledgeImg, True, False)

    def show(self):
        screen.blit(self.s, (self.x, self.y))

    def move(self):
        if self.x >= w + PSS(400):
            self.x = w + PSS(399)
            self.RL = 1
            self.s = pygame.transform.flip(sledgeImg, False, False)
            self.y = h / 4 + randrange(PSS(300))
            gui.flights += 1
            for f in range(gui.level + 1):
                obs.append(Obstacle(self.RL))

        if self.x <= PSS(-700):
            self.x = PSS(-699)
            self.RL = 0
            self.s = pygame.transform.flip(sledgeImg, True, False)
            self.y = h / 4 + randrange(PSS(300))
            gui.flights += 1
            for f in range(gui.level + 1):
                obs.append(Obstacle(self.RL))

        if self.RL == 0:
            time_passed = self.SledgeClock.tick()
            time_passed_seconds = time_passed / 1000.0
            distance_moved_x = time_passed_seconds * self.vel[0]

            self.x += distance_moved_x

        if self.RL == 1:
            time_passed = self.SledgeClock.tick()
            time_passed_seconds = time_passed / 1000.0
            distance_moved_x = time_passed_seconds * self.vel[0]

            self.x -= distance_moved_x

    def get_sledge_y(self):
        return self.y

    def get_sledge_RL(self):
        return self.RL

    def get_sledge_x(self):
        return self.x


def playerPresent():
    present_rects_p1 = []
    present_rects_p2 = []
    player1_rect = Rect(p[0].x, p[0].y, PSS(50), PSS(50))

    for g in range(len(ProP1)):
        present_rects_p1.append(Rect(ProP1[g].x, ProP1[g].y, PSS(50), PSS(50)))

# player 1 with presents player 1
    for g in range(len(present_rects_p1)):
        if player1_rect.colliderect(present_rects_p1[g]) and ProP1[g].collision_active is True:
            gui.Is_dead_p1 = True

    if gui.players == 2:
        player2_rect = Rect(p[1].x, p[1].y, PSS(50), PSS(50))
        for g in range(len(ProP2)):
            present_rects_p2.append(Rect(ProP2[g].x, ProP2[g].y, PSS(50), PSS(50)))

# player 2 with presents player 1
        for g in range(len(present_rects_p1)):
            if player2_rect.colliderect(present_rects_p1[g]) and ProP1[g].collision_active is True:
                gui.Is_dead_p2 = True

# player 2 with presents player 2
        for g in range(len(present_rects_p2)):
            if player2_rect.colliderect(present_rects_p2[g]) and ProP2[g].collision_active is True:
                gui.Is_dead_p2 = True

# player 1 with presents player 2
        for g in range(len(present_rects_p2)):
            if player1_rect.colliderect(present_rects_p2[g]) and ProP2[g].collision_active is True:
                gui.Is_dead_p1 = True


def playerObstacle():
    obst_rect = []
    for i in range(len(obs)):
        obst_rect.append(Rect(obs[i].x, obs[i].y, PSS(50), PSS(50)))

    player1_rect = Rect(p[0].x, p[0].y, PSS(50), PSS(50))

    for j in range(len(obst_rect)):
        if player1_rect.colliderect(obst_rect[j]):
            gui.Is_dead_p1 = True

    if gui.players == 2:
        player2_rect = Rect(p[1].x, p[1].y, PSS(50), PSS(50))
        for j in range(len(obst_rect)):
            if player2_rect.colliderect(obst_rect[j]):
                gui.Is_dead_p2 = True


def presentSledge():
    sledge_rect = None
    if s.RL == 0:
        sledge_rect = Rect(s.x, s.y, PSS(330 / 4), PSS(85))
    if s.RL == 1:
        sledge_rect = Rect(s.x + PSS(330) - PSS(330 / 4), s.y, PSS(330 / 4), PSS(85))

    # pygame.draw.rect(screen,(100, 0, 200), sledge_rect)

    present_rects_1 = []
    present_rects_2 = []
    for t in range(len(ProP1)):
        present_rects_1.append(Rect(ProP1[t].x, ProP1[t].y, PSS(50), PSS(50)))

    if gui.players == 2:
        for t in range(len(ProP2)):
            present_rects_2.append(Rect(ProP2[t].x, ProP2[t].y, PSS(50), PSS(50)))

    len_p1 = len(present_rects_1)
    for t in range(len_p1):
        if sledge_rect.colliderect(present_rects_1[len_p1 - t - 1]):
            gui.scoreVarP1 += 1
            ProP1.pop(len_p1 - t - 1)

    if gui.players == 2:
        len_p2 = len(present_rects_2)
        for t in range(len_p2):
            if sledge_rect.colliderect(present_rects_2[len_p2 - t - 1]):
                gui.scoreVarP2 += 1
                ProP2.pop(len_p2 - t - 1)


class Obstacle:
    def __init__(self, direction):
        self.ObstacleClock = pygame.time.Clock()
        self.o_p = obstaclePicture
        self.vel = [PSS(40), PSS(-60)]
        self.grav = PSS(500)
        self.RL = direction
        if direction == 0:
            self.x = randrange(PSS(10), w - PSS(10))
        else:
            self.x = randrange(PSS(-300), w - PSS(340))
        self.y = 0
        self.lost = False

    def show(self):
        if self.lost:
            screen.blit(self.o_p, (self.x, self.y))

    def throw_out_check(self):
        if self.RL == 0:
            if self.x < s.get_sledge_x() and self.lost is False:
                self.lost = True
                self.x = s.get_sledge_x() + PSS(40)
                self.y = s.get_sledge_y() + PSS(40)
        if self.RL == 1:
            if self.x > s.get_sledge_x() and self.lost is False:
                self.lost = True
                self.x = s.get_sledge_x() + PSS(270)
                self.y = s.get_sledge_y() + PSS(40)

    def move(self):
        if self.lost:
            time_passed = self.ObstacleClock.tick()
            time_passed_seconds = time_passed / 1000.0
            distance_moved_x = time_passed_seconds * self.vel[0]
            distance_moved_y = time_passed_seconds * self.vel[1]
            distance_moved_grav = time_passed_seconds * self.grav

            if self.RL == 1:
                self.x += distance_moved_x
            if self.RL == 0:
                self.x -= distance_moved_x

            self.y += distance_moved_y
            self.vel[1] += distance_moved_grav

            if self.vel[0] >= 0.5:
                self.vel[0] -= 0.5


keys = pygame.key.get_pressed()
Startup()
gui = GUI()
ProP1 = []
ProP2 = []
flakes = []
s = Sledge()
p = []
firstShot = False
start_screen = True
obs = []
for z in range(2):
    obs.append(Obstacle(0))


def spawn_snow():
    r = randrange(PSS(60))
    if r <= 30:
        flakes.append(Snowflake())
    if len(flakes) > 1:
        if flakes[0].y >= h - PSS(200):
            flakes.pop(0)

    for g in range(len(flakes)):
        flakes[g].show()
        flakes[g].move()


def despawn_presents_and_obstacles():
    if len(ProP1) > 0:
        if ProP1[0].y >= h:
            ProP1.pop(0)

    if len(ProP2) > 0:
        if ProP2[0].y >= h:
            ProP2.pop(0)

    if len(obs) > 0:
        length_obs = len(obs)
        for v in range(len(obs)):
            if obs[length_obs - v - 1].y > h:
                obs.pop(length_obs - v - 1)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                print("Spiel beendet. \nAuf Wiedersehen!")
                exit()

        if start_screen and event.type == MOUSEBUTTONUP:
            mouse_xy = pygame.mouse.get_pos()
            if singleplayer_rect.collidepoint(mouse_xy[0], mouse_xy[1]):
                p = [Player(1)]
                gui.startMenue = True
                start_screen = False
            elif multiplayer_rect.collidepoint(mouse_xy[0], mouse_xy[1]):
                p = [Player(1), Player(2)]
                gui.startMenue = True
                gui.Is_dead_p2 = False
                start_screen = False
                gui.players = 2

        if gui.startMenue:
            if event.type == MOUSEBUTTONUP:
                mouse_xy = pygame.mouse.get_pos()
                if gui.text_rect.collidepoint(mouse_xy[0], mouse_xy[1]):
                    gui.startMenue = False
                    gui.gameRunning = True
                    s = Sledge()
                    gui.level = 1
                    gui.flights = 1
                    obs.clear()
                    for z in range(2):
                        obs.append(Obstacle(0))

        if gui.gameRunning:
            if event.type == pygame.KEYDOWN:
                # player 1
                if not gui.Is_dead_p1 and gui.players == 2:
                    if event.key == K_w:
                        ProP1.append(Projectile(1, 0))
                    if event.key == K_s:
                        ProP1.append(Projectile(1, 2))
                    if event.key == K_a:
                        p[0].moveleft = True
                    if event.key == K_d:
                        p[0].moveright = True
                # player 2
                if not gui.Is_dead_p2 and gui.players == 2:
                    if event.key == K_UP:
                        ProP2.append(Projectile(2, 0))
                    if event.key == K_DOWN:
                        ProP2.append(Projectile(2, 2))
                    if event.key == K_LEFT:
                        p[1].moveleft = True
                    if event.key == K_RIGHT:
                        p[1].moveright = True

            if event.type == pygame.KEYUP:
                if event.key == K_a:
                    p[0].moveleft = False
                if event.key == K_d:
                    p[0].moveright = False

                if gui.players == 2:
                    if event.key == K_LEFT:
                        p[1].moveleft = False
                    if event.key == K_RIGHT:
                        p[1].moveright = False

            if firstShot and gui.players == 1 and not gui.Is_dead_p1:
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        ProP1.append(Projectile(1, 0))
                    if event.button == 3:
                        ProP1.append(Projectile(1, 2))
            firstShot = True

        if gui.Is_dead_p1 and gui.Is_dead_p2:
            if event.type == MOUSEBUTTONUP:
                mouse_xy = pygame.mouse.get_pos()
                reset_rect = Rect((w / 2 - ResetButtonPicture.get_width() / 2, h / 2 + PSS(50), PSS(100), PSS(100)))
                if reset_rect.collidepoint(mouse_xy[0], mouse_xy[1]):
                    gui.gameRunning = True
                    obs.clear()
                    ProP1.clear()
                    ProP2.clear()
                    gui.level = 1
                    gui.flights = 1
                    s = Sledge()
                    for z in range(2):
                        obs.append(Obstacle(0))
                    if gui.scoreVarP1 > gui.highScore and gui.players == 1:
                        gui.highScore = gui.scoreVarP1
                    gui.scoreVarP1 = 0
                    gui.scoreVarP2 = 0
                    gui.Is_dead_p1 = False
                    p[0].moveright = False
                    p[0].moveleft = False
                    p[0].x = w/2
                    if gui.players == 2:
                        gui.Is_dead_p2 = False
                        p[1].moveright = False
                        p[1].moveleft = False
                        p[1].x = w/2
                        gui.win_updater = True

    screen.fill((255, 255, 255))

    screen.blit(background, (0, 0))
    spawn_snow()

    if start_screen:
        Startup()
        mouse_xy = pygame.mouse.get_pos()
        if singleplayer_rect.collidepoint(mouse_xy[0], mouse_xy[1]):
            Instructions(1)
        elif multiplayer_rect.collidepoint(mouse_xy[0], mouse_xy[1]):
            Instructions(2)

    if gui.startMenue:
        pygame.mouse.set_visible(True)
        gui.startMenueMethod()

    if gui.gameRunning:
        pygame.mouse.set_visible(False)
        despawn_presents_and_obstacles()

        if not gui.Is_dead_p1:
            p[0].move()
            p[0].show()
            if p[0].moveleft:
                p[0].move_left()
            if p[0].moveright:
                p[0].move_right()

        if gui.players == 2 and not gui.Is_dead_p2:
            p[1].show()
            if p[1].moveleft:
                p[1].move_left()
            if p[1].moveright:
                p[1].move_right()

        s.move()
        s.show()

        if len(obs) > 0:
            for x in range(len(obs)):
                obs[x].throw_out_check()
                obs[x].move()
                obs[x].show()

        for x in range(len(ProP1)):
            ProP1[x].move()
            ProP1[x].show()
        for x in range(len(ProP2)):
            ProP2[x].move()
            ProP2[x].show()

        playerPresent()
        presentSledge()
        playerObstacle()
        gui.deathScreen()
        gui.Score()
        gui.levels()

    if gui.Is_dead_p1 and gui.Is_dead_p2:
        pygame.mouse.set_visible(True)
        if gui.players == 2:
            gui.Score()
        gui.deathScreen()
        gui.gameRunning = False

    pygame.display.update()
    # clock.tick(fps)
