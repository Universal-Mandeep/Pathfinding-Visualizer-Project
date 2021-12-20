import pygame
import Commons.Constants as const


class Button:
    def __init__(self, pos, size, text):
        self.x_cor = pos[0]
        self.y_cor = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.bg_color = const.BUTTON_BG_COLOR
        self.text = text
        self.text_color = const.FONT_COLOR
        self.text_x_cor = self.x_cor + 50    # 50px margin in left
        self.text_y_cor = self.y_cor + 15    # 15px margin at top

    def get_pos(self):
        return self.x_cor, self.y_cor

    def get_text(self):
        return self.text

    def is_selected(self):
        return self.text_color == const.BUTTON_SELECTED_FONT_COLOR

    def make_selected(self):
        self.text_color = const.BUTTON_SELECTED_FONT_COLOR

    def make_unselected(self):
        self.text_color = const.FONT_COLOR

    def draw_button(self, win):
        pygame.draw.rect(
            win, self.bg_color, (self.x_cor, self.y_cor, self.width, self.height))
        button_label = const.MAIN_FONT.render(self.text, 1, self.text_color)
        win.blit(button_label, (self.text_x_cor, self.text_y_cor))


