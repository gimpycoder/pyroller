import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, NeonButton


class StatsMenu(tools._State):
    """
    This state allows the player to choose which game's stats they
    want to view or return to the lobby.
    """
    def __init__(self):
        super(StatsMenu, self).__init__()
        screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        self.font = prepare.FONTS["Saniretro"]
        self.title = Label(self.font, 64, "Statistics", "darkred",
                          {"midtop":(screen_rect.centerx, screen_rect.top+10)})
        self.games = ["Blackjack", "Bingo", "Craps", "Keno"]
        b_width = 318
        b_height = 101
        top = self.title.rect.bottom + 50
        self.game_buttons = []
        for game in self.games:
            label = Label(self.font, 48, game, "gold3", {"center": (0, 0)})
            button = NeonButton((screen_rect.centerx-(b_width//2), top), game)
            self.game_buttons.append(button)
            top += button.rect.height + 20
        self.done_button = NeonButton((screen_rect.centerx-(b_width//2),
                                      screen_rect.bottom - (b_height + 10)),
                                      "Lobby")

    def startup(self, current_time, persistent):
        self.start_time = current_time
        self.persist = persistent
        self.player = self.persist["casino_player"]

    def get_event(self, event, scale=(1,1)):
        if event.type == pg.QUIT:
            self.done = True
            self.next = "LOBBYSCREEN"
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = tools.scaled_mouse_pos(scale, event.pos)
            if self.done_button.rect.collidepoint(pos):
                self.done = True
                self.next = "LOBBYSCREEN"
            for button in self.game_buttons:
                if button.rect.collidepoint(pos):
                    self.persist["current_game_stats"] = button.payload
                    self.next = "STATSSCREEN"
                    self.done = True

    def draw(self, surface):
        surface.fill(prepare.BACKGROUND_BASE)
        self.title.draw(surface)
        for button in self.game_buttons:
            button.draw(surface)
        self.done_button.draw(surface)

    def update(self, surface, keys, current_time, dt, scale):
        mouse_pos = tools.scaled_mouse_pos(scale)
        for button in self.game_buttons:
            button.update(mouse_pos)
        self.done_button.update(mouse_pos)
        self.draw(surface)
