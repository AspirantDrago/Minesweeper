import pygame
from config import EMPTY

GRID_COLOR = '#333333'

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[EMPTY] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.grid_width = 1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(
                    self.left + self.cell_size * col,
                    self.top + self.cell_size * row,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, GRID_COLOR, rect, self.grid_width)

    def get_cell(self, mouse_pos):
        row = (mouse_pos[1] - self.top) // self.cell_size
        col = (mouse_pos[0] - self.left) // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            return row, col

    def on_click(self, row, col):
        pass

    def get_click(self, event):
        cell = self.get_cell(event.pos)
        if cell:
            if event.button == pygame.BUTTON_LEFT:
                self.on_click(*cell)
            elif event.button == pygame.BUTTON_RIGHT:
                self.mark_click(*cell)
