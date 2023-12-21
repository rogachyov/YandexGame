import pygame
import os
import sys

pygame.init()
SIZE = WIDTH, HEIGHT = 1920, 1080
FPS = 60
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найдена')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def cut_sheet(sheet, columns, rows, x, y):
    pass


class MenuBack(pygame.sprite.Sprite):
    img = load_image('menu.png')

    def __init__(self, *args):
        super().__init__(*args)
        self.image = MenuBack.img
        self.rect = self.image.get_rect()


class MenuButtons(pygame.sprite.Sprite):
    img = pygame.transform.scale(load_image('button_start.png'), (400, 160))
    img1 = pygame.transform.scale(load_image('button_info.png'), (400, 160))
    img2 = pygame.transform.scale(load_image('button_exit.png'), (400, 160))

    def __init__(self, x, y, type, *args):
        super().__init__(*args)
        self.image = [MenuButtons.img, MenuButtons.img1, MenuButtons.img2][type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.rect.width = 400
        self.rect.height = 160

    def update(self, *args):
        global start, menu_active, running, info
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) and \
                self.image == MenuButtons.img:
            start = True
            menu_active = False
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) and \
                self.image == MenuButtons.img2:
            running = False
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) and \
                self.image == MenuButtons.img1:
            info = True
            menu_active = False


class Hero(pygame.sprite.Sprite):
    img = load_image('cat.png')
    frame_walk_up = []


    def __init__(self, board):
        super().__init__(hero_sprite)
        self.x = 1
        self.y = 1
        self.board = board
        self.image = pygame.Surface((board.width, board.height), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x = board.left + self.x * board.width
        self.rect.y = board.top + self.y * board.height
        pygame.draw.rect(screen, 'red', self.rect)

    def move(self, key):
        if key.scancode == 81:
            self.y += self.rect.size
        elif key.scancode == 79:
            self.x += self.rect.size
        elif key.scancode == 80:
            self.x -= self.rect.size
        elif key.scancode == 82:
            self.y -= self.rect.size


class StartGame(pygame.sprite.Sprite):
    img = pygame.transform.scale(load_image('game.png'), (1920, 1080))

    def __init__(self, *args):
        super().__init__(*args)
        self.image = StartGame.img
        self.rect = self.image.get_rect()


class Info(pygame.sprite.Sprite):
    img = load_image('info.png')

    def __init__(self, *args):
        super().__init__(*args)
        self.image = Info.img
        self.rect = self.image.get_rect()
        self.rect.y = 100


class BackButton(pygame.sprite.Sprite):
    img = load_image('button_back.png')

    def __init__(self, *args):
        super().__init__(*args)
        self.image = BackButton.img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

    def update(self, *args):
        global menu_active, running, info, start
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            info = False
            start = False
            menu_active = True


class DungeonButton(pygame.sprite.Sprite):
    img = load_image('dungeon_button.png')

    def __init__(self):
        super().__init__(game_sprite)
        self.image = DungeonButton.img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2 - self.rect.w / 2
        self.rect.y = HEIGHT - self.rect.h

    def update(self, event):
        global n_dungeon
        if self.rect.collidepoint(event.pos):
            n_dungeon = 1


class Board(pygame.sprite.Sprite):
    def __init__(self, left, top, x, y, width, height):
        super().__init__(board_sprites)
        self.left = left
        self.top = top
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.board = [[0] * x for _ in range(y)]
        self.image = pygame.Surface((x * width + left, y * height + top), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        for i in range(x):
            for j in range(y):
                if self.board[j][i] == 0:
                    pygame.draw.rect(self.image, 'black', (left + width * i, top + height * j, width, height))
                pygame.draw.rect(self.image, 'white', (left + width * i, top + height * j, width, height), 1)

    def update(self, *args, **kwargs):
        pass


def start_screen():
    intro_text = ['Cat and dungeon']

    fon = pygame.transform.scale(load_image('game.png'), SIZE)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 250)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

n_dungeon = 0

board_sprites = pygame.sprite.Group()
board = Board(200, 200, 15, 8, 80, 80)

menu_sprite = pygame.sprite.Group()
MenuBack(menu_sprite)

menu_buttons = pygame.sprite.Group()
for i in range(3):
    MenuButtons(760, 400 + i * 160, i, menu_buttons)

game_sprite = pygame.sprite.Group()
StartGame(game_sprite)
DungeonButton()

info_sprite = pygame.sprite.Group()
Info(info_sprite)

back_to_menu = pygame.sprite.Group()
BackButton(back_to_menu)

hero_sprite = pygame.sprite.Group()
# hero = Hero(board)

running = True
menu_active = True
start = False
info = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            menu_buttons.update(event)
            game_sprite.update(event)
            back_to_menu.update(event)
    screen.fill('white')
    if menu_active:
        menu_sprite.draw(screen)
        menu_buttons.draw(screen)
    elif start:
        menu_active = False
        game_sprite.draw(screen)
        if n_dungeon:
            board_sprites.draw(screen)
            hero_sprite.draw(screen)
    elif info:
        menu_active = False
        info_sprite.draw(screen)
    if not menu_active:
        back_to_menu.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
