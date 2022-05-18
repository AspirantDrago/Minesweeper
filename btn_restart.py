import pygame
from config import *
from functions import load_image


class ButtonRestart(pygame.sprite.Sprite):
    SCALE = 0.8
    BORDER_WIDTH = 3
    BORDER_COLOR = '#333333'
    SMILE_NORMAL = 0
    SMILE_OMG = 1
    SMILE_WIN = 2
    SMILE_DEAD = 3
    OMG_DELAY = 0.25

    def __init__(self, *args):
        super().__init__(*args)
        size = PADDING_TOP - 2 * BUTTON_PADDING
        self.rect = pygame.Rect((WIDTH - size) / 2, BUTTON_PADDING, size, size)
        image_temp = load_image('smiles.png')
        smile_size = min(image_temp.get_size()) // 2
        self.smiles = []
        for row in range(2):
            for col in range(2):
                sub_img = image_temp.subsurface((col * smile_size, row * smile_size, smile_size, smile_size))
                sub_img = pygame.transform.scale(sub_img, (size * self.SCALE, size * self.SCALE))
                self.smiles.append(pygame.Surface((size, size)))
                self.smiles[-1].fill('white')
                self.smiles[-1].blit(sub_img, (size * (1 - self.SCALE) / 2, size * (1 - self.SCALE) / 2))
                border_rect = self.rect.copy()
                border_rect.topleft = 0, 0
                pygame.draw.rect(self.smiles[-1], self.BORDER_COLOR, border_rect, self.BORDER_WIDTH)
        self.image = self.smiles[self.SMILE_NORMAL]
        self.frame_count = 0

    def set_smile_normal(self):
        self.image = self.smiles[self.SMILE_NORMAL]

    def set_smile_dead(self):
        self.image = self.smiles[self.SMILE_DEAD]

    def set_smile_win(self):
        self.image = self.smiles[self.SMILE_WIN]

    def set_smile_omg(self):
        self.image = self.smiles[self.SMILE_OMG]

    def update(self, event):
        if self.image == self.smiles[self.SMILE_OMG]:
            self.frame_count += 1
            if self.frame_count / FPS > self.OMG_DELAY:
                self.set_smile_normal()
                self.frame_count = 0
        if event.type == pygame.MOUSEBUTTONDOWN and \
                event.button == pygame.BUTTON_LEFT and \
                self.rect.collidepoint(*event.pos):
            self.restart()

    def restart(self):
        self.set_smile_normal()
        from main import new_board
        new_board()