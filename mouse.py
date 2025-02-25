# interface to mouse events

from typing import Self, Tuple
from enum import Enum

import pygame

from statuspane import StatusPane

# from https://stackoverflow.com/a/36268899/104774
class MouseEventChecker:
    class Click(Enum):
        WAITING = 1
        SINGLE = 2
        DOUBLE = 3
        DRAG_START = 4
        DRAG = 5
        DRAG_STOP = 6
        RIGHT_BUTTON = 7
    def __init__(self: Self, status: StatusPane):
        self.status : StatusPane = status
        self.single_click_timer : pygame.event.Event = pygame.event.Event(pygame.USEREVENT + 10)
        self.double_click_timer : pygame.event.Event = pygame.event.Event(pygame.USEREVENT + 11)
        self.timer1: bool = False
        self.timer2: bool = False
        self.mouse_active: bool = False
        self.drag: bool = False
        self.mouse_pos = None


    def check(self: Self, event: pygame.event.Event) -> Click | None:
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if self.drag:
                self.mouse_pos = pygame.mouse.get_pos()
                return self.Click.DRAG

        if event.type == pygame.MOUSEBUTTONDOWN:
            presses = pygame.mouse.get_pressed()
            if not self.mouse_active and presses[0]:
                self.mouse_active = True
                self.timer1 = True
                pygame.time.set_timer(self.single_click_timer, 200)
                self.mouse_pos = pygame.mouse.get_pos()
            if presses[2]:
                return self.Click.RIGHT_BUTTON
        if event.type == pygame.MOUSEBUTTONUP:
            # return self.Click.SINGLE # for now as the timer doesn't seem to work
            if self.timer1:
                pygame.time.set_timer(self.single_click_timer, 0)
                self.timer1 = False
                pygame.time.set_timer(self.double_click_timer, 350)
                self.timer2 = True
                return self.Click.WAITING
            elif self.timer2:
                pygame.time.set_timer(self.double_click_timer, 0)
                self.timer2 = False
                self.mouse_active = False
                return self.Click.DOUBLE
            elif self.drag:
                self.drag = False
                self.mouse_active = False
                return self.Click.DRAG_STOP
        elif event == self.single_click_timer and self.timer1:
            pygame.time.set_timer(self.single_click_timer, 0)
            self.timer1 = False
            self.drag = True
            return self.Click.DRAG_START
        elif event == self.double_click_timer and self.timer2:
            # timer timed out
            pygame.time.set_timer(self.double_click_timer, 0)
            self.timer2 = False
            self.mouse_active = False
            return self.Click.SINGLE
        elif event == pygame.MOUSEMOTION and self.drag:
            self.mouse_pos = pygame.mouse.get_pos()
            return self.Click.DRAG

        return None

    def get_clicked_pos(self: Self) -> Tuple[int, int]:
        return self.mouse_pos
