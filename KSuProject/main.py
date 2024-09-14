import pygame as pg
import json as js


HEIGHT = 500
WIDTH = 500

pg.init()

Window = pg.display.set_mode((HEIGHT, WIDTH))
clock = pg.time.Clock()

def MixCol(col0: pg.Color, col1: pg.Color):
    red = round((col0[0] + col1[0]) * 0.5)
    green = round((col0[1] + col1[1]) * 0.5)
    blue = round((col0[2] + col1[2]) * 0.5)

    return (red, green, blue)

class CircleTextButton:
    def __init__(self, text: str, radius) -> None:
        self.text = text
        self.radius = radius
    
    def GetSurface(self, color, background: pg.Color = pg.Color(0, 0, 0, 0)):
        Font = pg.font.SysFont('Comic Sans MS', 30)
        TextSurface = Font.render(self.text, False, color, background)

        surface = pg.Surface((self.radius * 2, self.radius * 2))
        surface.fill(background)
        pg.draw.circle(surface, background, (self.radius, self.radius), self.radius)
        pg.draw.circle(surface, color, (self.radius, self.radius), self.radius - 1, 5)
        surface.blit(pg.transform.scale(TextSurface, (self.radius / 2, self.radius)), (self.radius * 0.75, self.radius * 0.5))

        TransparentSurface = pg.Surface((self.radius * 2, self.radius * 2))
        TransparentSurface.blit(surface, (0, 0))
        TransparentSurface.set_alpha(64)

        surface.blits([
            (TransparentSurface, (-1, -1)),
            (TransparentSurface, (-1,  1)),
            (TransparentSurface, ( 1, -1)),
            (TransparentSurface, ( 1,  1)),
        ])
        return surface
    
    def draw(self, DrawAt, pos, color, background: pg.Color = pg.Color(0, 0, 0, 0)):
        surface = self.GetSurface(color, background)

        DrawAt.blit(surface, (pos[0] - self.radius, pos[1] - self.radius))

def DrawInGameUIAndMechanics(rectangles):

    DButtton = 0
    FButtton = 0
    JButtton = 0
    KButtton = 0

    global Error
    global GO
    global Time

    for Rectangle in rectangles:
        TopRelTime = Rectangle.top * 55 / Speed + Time * 5

        if TopRelTime > -55 / Speed and TopRelTime < 500:
            pg.draw.rect(Window, pg.Color(0, 255, 255), pg.Rect(Rectangle.left * 55 + 140, TopRelTime, 55.0, 55.0 / Speed + 1))

        if TopRelTime + 55.0 / Speed > 440 and TopRelTime < 440:
            if Rectangle.left == 0:
                DButtton += 1
            if Rectangle.left == 1:
                FButtton += 1
            if Rectangle.left == 2:
                JButtton += 1
            if Rectangle.left == 3:
                KButtton += 1
    if not GO:
        if DButtton == 1:
            if D == 1:
                Error -= Speed * 0.5
            else:
                Error += Speed * 2
        else:
            if D == 1:
                Error += Speed * 2

        if FButtton == 1:
            if F == 1:
                Error -= Speed * 0.5
            else:
                Error += Speed * 2
        else:
            if F == 1:
                Error += Speed * 2

        if JButtton == 1:
            if J == 1:
                Error -= Speed * 0.5
            else:
                Error += Speed * 2
        else:
            if J == 1:
                Error += Speed * 2

        if KButtton == 1:
            if K == 1:
                Error -= Speed * 0.5
            else:
                Error += Speed * 2
        else:
            if K == 1:
                Error += Speed * 2

    if Error < 0:
        Error = 0

    Error *= 0.99

    if Error > 100:
        GO = True
    
    if round(Time) == 0:
        GO = False

    if GO:
        Time *= 0.8
        Error *= 0.8

    pg.draw.rect(Window, BGcolor, pg.Rect(140, 440, 220, 60))

    ButtonD.draw(Window, (167.5, 470), (0, 255, 255 - 128 * D), BGcolor)
    ButtonF.draw(Window, (222.5, 470), (0, 255, 255 - 128 * F), BGcolor)
    ButtonJ.draw(Window, (277.5, 470), (0, 255, 255 - 128 * J), BGcolor)
    ButtonK.draw(Window, (332.5, 470), (0, 255, 255 - 128 * K), BGcolor)

    pg.draw.lines(Window, pg.Color(150, 150, 200), False, (
        (140, 0),
        (140, 500),
        (140, 440),
        (194.5, 440),
        (194.5, 500),
        (194.5, 0),
        (194.5, 440),
        (249, 440),
        (249, 500),
        (249, 0),
        (249, 440),
        (304, 440),
        (304, 500),
        (304, 0),
        (304, 440),
        (360, 440),
        (360, 500),
        (360, 0),
    ))

def LoadLevel(level: dict):
    Gameplay = level["gameplay"]

    Rectangles = []
    for row in range(Gameplay.__len__()):
        Row = Gameplay[row]
        for rect in range(Row.__len__()):
            Rect = Row[rect]

            if Rect == 1:
                Rectangles.append(pg.Rect(rect, -row, 1.0, 1.0))

    return Rectangles


BGcolor = pg.Color(10, 10, 20)

ButtonD = CircleTextButton("D", 25)
ButtonF = CircleTextButton("F", 25)
ButtonJ = CircleTextButton("J", 25)
ButtonK = CircleTextButton("K", 25)

InGame = True
GO = False

with open("levels.json") as file:
    LevelDict = js.loads(file.read())["levels"][0]

Rectangles = LoadLevel(LevelDict)

Time = 0
Error = 0

Speed = 0.75


running = True
while running:
    
    if InGame and not GO:
        try:
            Time += 60 / clock.get_fps()
        except ZeroDivisionError:
            print("Zero FPS")

    Keys = pg.key.get_pressed()

    D = int(Keys[pg.K_d])
    F = int(Keys[pg.K_f])
    J = int(Keys[pg.K_j])
    K = int(Keys[pg.K_k])


    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

    Window.fill(BGcolor + pg.Color(round(Error), 0, 0))

    if InGame:
        DrawInGameUIAndMechanics(Rectangles)
    
    pg.display.update()
    clock.tick(60)

pg.quit()