# hiscore: add, store/load, display

from dataclasses import dataclass
from typing import Self
import json
from datetime import datetime
import os

import pygame
from config import Config

@dataclass
class Score:
    points: int
    highest_tile: int
    user: str
    datetime: str

    def to_json(self: Self):
        return { 'points': self.points, 'tile': self.highest_tile, 'user': self.user, 'datetime': self.datetime }

    def from_json(self: Self, js):
        self.points = js['points']
        self.highest_tile = js['tile']
        self.user = js['user']
        self.datetime = js['datetime']

class HiScore:
    MAX_SCORES = 10

    def __init__(self: Self, user: str, screen: pygame.Surface):
        self.__scores = []
        self.__read()
        self.user = user
        self.screen = screen

    @staticmethod
    def __get_filename() -> str:
        Config.make_datapath()
        return os.path.join(Config.get_datapath(), 'hiscore.json')

    def __read(self: Self) -> None:
        self.__scores = []
        p = self.__get_filename()
        try:
            with open(p, 'r') as f:
                js = json.load(f)
                for j in js:
                    sc = Score(int(j['points']), int(j['tile']), j['user'], j['datetime'])
                    self.__scores.append(sc)
            self.__scores.sort(key=lambda s: s.points, reverse = True)
        except (KeyError, ValueError):
            self.__scores = []
            os.remove(p)
        except FileNotFoundError:
            pass # file will be created, __scores can't be filled in


    def __write(self: Self) -> None:
        p = self.__get_filename()
        try:
            with open(p, 'w') as f:
                json.dump([s.to_json() for s in self.__scores], f)
        except Exception as e:
            print(e)

    #return whether the score is part of the hiscore
    def add_score(self: Self, in_points: int, in_tile: int) -> bool:
        self.__scores.sort(key=lambda s: s.points, reverse = True)

        if len(self.__scores) >= HiScore.MAX_SCORES:
            if in_points <= self.__scores[-1].points:
                return False
        now = datetime.utcnow()
        str_now = current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        score = Score(points = in_points, highest_tile = in_tile, user = self.user, datetime = str_now)

        self.__scores.append(score)
        self.__scores.sort(key=lambda s: s.points, reverse = True)
        self.__scores = self.__scores[0: HiScore.MAX_SCORES]
        self.__write()
        self.display(score)
        return True

    def display(self: Self, new_score: Score | None = None) -> None:
        print("Hiscore top 10")
        for i, s in enumerate(self.__scores):
            print(f'{i+1:2} - score: {s.points:15n}, tile: {s.highest_tile:2}, time: {s.datetime}, user: {s.user}')
        self.screen.fill("yellow")
        font = pygame.font.Font(None, 30)
        text: pygame.Surface = font.render("Hiscore Top 10:", True, "black")
        text_rect: pygame.Rect = text.get_rect()
        text_rect.top = 5
        text_rect.left = 5
        self.screen.blit(text, text_rect)
        top = 22
        for i, s in enumerate(self.__scores):
            font = pygame.font.Font(None, 24)
            text: pygame.Surface = font.render(f'{i+1:2} - score: {s.points:15n}, tile: {s.highest_tile:2}', True, "red" if new_score and new_score == s else "darkblue")
            text_rect: pygame.Rect = text.get_rect()
            top += 24
            text_rect.top = top
            text_rect.left = 5
            self.screen.blit(text, text_rect)
            font = pygame.font.Font(None, 22)
            text: pygame.Surface = font.render(f'        time: {s.datetime}, user: {s.user}', True, "blue")
            text_rect: pygame.Rect = text.get_rect()
            top += 26
            text_rect.top = top
            text_rect.left = 5
            self.screen.blit(text, text_rect)

        top += 30
        font = pygame.font.Font(None, 26)
        text: pygame.Surface = font.render("Time is UTC, not local time", True, "grey")
        text_rect: pygame.Rect = text.get_rect()
        text_rect.top = top
        text_rect.left = 5
        self.screen.blit(text, text_rect)
        top += 30
        font = pygame.font.Font(None, 26)
        text: pygame.Surface = font.render("Press a key or mouse button to continue...", True, "grey")
        text_rect: pygame.Rect = text.get_rect()
        text_rect.top = top
        text_rect.left = 5
        self.screen.blit(text, text_rect)



        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False






