import pygame as pg


class Button:
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
