import pygame
import sys

pygame.init()

from board import Board
from random import randint
from btn_restart import ButtonRestart
from functions import load_image, set_color
from config import *
from segment_table import CountSegmentTable, TimeSegmentTable


class Minesweeper(Board):
    font = pygame.font.Font('data/FreeSansBold.ttf', FONT_SIZE)

    def __init__(self, width, height):
        super().__init__(width, height)
        self.cell_color = BACK_COLOR
        hsva = self.cell_color.hsva
        self.cell_color_light = pygame.Color(self.cell_color)
        self.cell_color_dark = pygame.Color(self.cell_color)
        self.cell_color_light.hsva = (
            hsva[0], hsva[1], min(100, hsva[2] + LIGHT_COEFF), hsva[3]
        )
        self.cell_color_dark.hsva = (
            hsva[0], hsva[1], max(0, hsva[2] - LIGHT_COEFF), hsva[3]
        )
        self.margin = self.grid_width + CELL_OUTSET_WIDTH // 2
        self.show_mines = False
        self.gaming = True
        self.generated = False
        self.closed_cells = width * height - COUNT_MINES
        self.image_mine = self._resize_image('mine.png')
        self.image_mine_saved = self._resize_image('mine_saved.png')
        self.image_flag = self._resize_image('flag.png')

    def _generate(self, click_row, click_col):
        count_table.set_number(COUNT_MINES)
        count_last_mines = COUNT_MINES
        while count_last_mines:
            row = randint(0, self.height - 1)
            col = randint(0, self.width - 1)
            if row == click_row and col == click_col:
                continue
            if self.board[row][col] == EMPTY:
                self.board[row][col] = MINE
                count_last_mines -= 1
        self.generated = True
        time_table.start()

    def _resize_image(self, filename):
        return pygame.transform.scale(
            load_image(filename),
            (CELL_SIZE, CELL_SIZE)
        )

    def boom(self):
        self.show_mines = True
        self.gaming = False
        btn_restart.set_smile_dead()
        time_table.stop()

    def win(self):
        self.gaming = False
        btn_restart.set_smile_win()
        time_table.stop()

    def check_cell(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row,
                    self.cell_size,
                    self.cell_size
                )
                if self.board[row][col] & MASK_FLAG:
                    if self.board[row][col] & MINE and self.show_mines:
                        screen.blit(self.image_mine_saved, rect)
                    else:
                        # Отрисовка флага
                        screen.blit(self.image_flag, rect)
                elif self.board[row][col] & MASK_QUESTION:
                    # Отрисовка вопроса
                    text = self.font.render('?', True, 'black')
                    screen.blit(text, (
                        rect.centerx - text.get_width() / 2,
                        rect.centery - text.get_height() / 2
                    ))
                elif self.board[row][col] & MINE and self.show_mines:
                    # Отрисовка мин
                    screen.blit(self.image_mine, rect)
                elif 1 <= self.board[row][col] <= 8:
                    # Отрисовка чисел
                    text = self.font.render(
                        str(self.board[row][col]), True,
                        TEXT_COLOR[self.board[row][col]]
                    )
                    screen.blit(text, (
                        rect.centerx - text.get_width() / 2,
                        rect.centery - text.get_height() / 2
                    ))
                elif self.board[row][col] in (EMPTY, MINE):
                    pygame.draw.lines(
                        screen, self.cell_color_light, False,
                        [
                            (rect.left + self.margin,
                             rect.bottom - self.margin),
                            (rect.left + self.margin, rect.top + self.margin),
                            (rect.right - self.margin, rect.top + self.margin)
                        ], CELL_OUTSET_WIDTH
                    )
                    pygame.draw.lines(
                        screen, self.cell_color_dark, False,
                        [
                            (rect.right - self.margin, rect.top + self.margin),
                            (rect.right - self.margin,
                             rect.bottom - self.margin),
                            (
                                rect.left + self.margin,
                                rect.bottom - self.margin)
                        ], CELL_OUTSET_WIDTH
                    )
        super().render(screen)

    def cell(self, row, col):
        if self.check_cell(row, col):
            return self.board[row][col]
        return EMPTY

    def _count_mask(self, row, col, mask):
        count = 0
        for row2 in range(row - 1, row + 2):
            for col2 in range(col - 1, col + 2):
                if self.cell(row2, col2) & mask:
                    count += 1
        return count

    def count_mines(self, row, col):
        return self._count_mask(row, col, MINE)

    def count_flags(self, row, col):
        return self._count_mask(row, col, MASK_FLAG)

    def mark_click(self, row, col):
        if self.gaming and self.generated:
            if self.board[row][col] > 8:
                if self.board[row][col] & MASK_FLAG:
                    self.board[row][col] -= MASK_FLAG
                    self.board[row][col] |= MASK_QUESTION
                    count_table.inc()
                elif self.board[row][col] & MASK_QUESTION:
                    self.board[row][col] -= MASK_QUESTION
                else:
                    self.board[row][col] |= MASK_FLAG
                    count_table.dec()

    def on_click(self, row, col, recursive=False):
        if self.check_cell(row, col) and self.gaming:
            if not self.generated:
                self._generate(row, col)
            if self.board[row][col] == EMPTY:
                btn_restart.set_smile_omg()
                self.closed_cells -= 1
                if self.closed_cells == 0:
                    self.win()
                val = self.count_mines(row, col)
                self.board[row][col] = val
                if self.board[row][col] == 0:
                    for row2 in range(row - 1, row + 2):
                        for col2 in range(col - 1, col + 2):
                            if not (row2 == row and col2 == col):
                                self.on_click(row2, col2)
            elif self.board[row][col] == self.count_flags(row,
                                                          col) and not recursive:
                for row2 in range(row - 1, row + 2):
                    for col2 in range(col - 1, col + 2):
                        if not (row2 == row and col2 == col):
                            self.on_click(row2, col2, True)
            elif self.board[row][col] == MINE:
                self.boom()


def new_board():
    global board
    board = Minesweeper(N_COLS, N_ROWS)
    board.set_view(PADDING, PADDING_TOP, CELL_SIZE)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
new_board()
pygame.display.set_caption('САПЁР')
pygame.display.set_icon(pygame.image.load('data/mine.png'))
all_sprites = pygame.sprite.Group()
btn_restart = ButtonRestart(all_sprites)
count_table = CountSegmentTable(all_sprites)
time_table = TimeSegmentTable(all_sprites)
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event)
            if event.button == 4:
                time_table.inc()
            elif event.button == 5:
                time_table.dec()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
                btn_restart.restart()
                count_table.reset()
                time_table.reset()
    screen.fill(BACK_COLOR)
    board.render(screen)
    all_sprites.draw(screen)
    all_sprites.update(event)
    pygame.display.flip()
    clock.tick(FPS)
sys.exit(0)
