import pygame
from config import *
import time


class SegmentTable(pygame.sprite.Sprite):
    def __init__(self, x, y, *args):
        super().__init__(*args)
        self.x = x
        self.text_width = SEGMENT_TABLE_MIN_WIDTH_TEXT
        self.aligin = SEGMENT_TABLE_ALIGING_LEGT
        self.rect = pygame.Rect(x, y, 0, 0)

    def reset(self):
        self.set_number(0)

    def set_number(self, number):
        self.number = number
        self.render()

    def render(self):
        text = str(self.number).zfill(self.text_width)
        self.text_width = len(text)
        rendered_text = SEGMENT_TABLE_FONT.render(text,
                                                  SEGMENT_TABLE_ANTIALIAS,
                                                  SEGMENT_TABLE_COLOR_TEXT)
        w_text = rendered_text.get_width()
        h_text = rendered_text.get_height()
        pad = 2 * SEGMENT_TABLE_BORDER_WIDTH + 2 * SEGMENT_TABLE_PADDING
        pad2 = 2 * SEGMENT_TABLE_PADDING
        self.rect = pygame.Rect(self.rect.left, self.rect.top, w_text + pad,
                                h_text + pad)
        inner_rect = pygame.Rect(SEGMENT_TABLE_BORDER_WIDTH,
                                 SEGMENT_TABLE_BORDER_WIDTH, w_text + pad2,
                                 h_text + pad2)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(SEGMENT_TABLE_COLOR_BORDER)
        self.image.fill(SEGMENT_TABLE_COLOR_BACK, inner_rect)
        self.image.blit(rendered_text, (
        SEGMENT_TABLE_BORDER_WIDTH + SEGMENT_TABLE_PADDING,) * 2)
        if self.aligin == SEGMENT_TABLE_ALIGING_LEGT:
            self.rect.left = self.x
        elif self.aligin == SEGMENT_TABLE_ALIGING_RIGHT:
            self.rect.right = self.x
        elif self.aligin == SEGMENT_TABLE_ALIGING_CENTER:
            self.rect.centerx = self.x

    def inc(self):
        self.set_number(self.number + 1)

    def dec(self):
        self.set_number(self.number - 1)


class CountSegmentTable(SegmentTable):
    def __init__(self, *args):
        super().__init__(SEGMENT_TABLE_LEFT_MARGIN, SEGMENT_TABLE_TOP_MARGIN,
                         *args)
        self.aligin = SEGMENT_TABLE_ALIGING_LEGT
        self.reset()


class TimeSegmentTable(SegmentTable):
    def __init__(self, *args):
        super().__init__(WIDTH - SEGMENT_TABLE_LEFT_MARGIN,
                         SEGMENT_TABLE_TOP_MARGIN, *args)
        self.aligin = SEGMENT_TABLE_ALIGING_RIGHT
        self.reset()
        self.active = False
        self.schet = 0

    def start(self):
        self.active = True
        self.schet = 0
        self.timer = time.time()

    def stop(self):
        self.active = False
        self.schet = int(round((time.time() - self.timer) * 100))

    def get_schet(self):
        return self.schet

    def update(self, *args, **kwargs):
        if self.active:
            secs = int(time.time() - self.timer)
            self.set_number(secs)
