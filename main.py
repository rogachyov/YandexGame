import pygame
from os import path
import sys

from random import randint, choice


SIZE_BOARD = 25, 25
pygame.init()
SIZE = WIDTH, HEIGHT = 1920, 1080
FPS = 60
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = path.join('data', name)
    if not path.isfile(fullname):
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
    img = pygame.transform.scale(load_image('cat.png'), (800, 800))
    frame_walk = []

    def __init__(self):
        super().__init__(hero_sprite)
        self.x = 1
        self.y = 1
        self.walk = False
        self.images = self.cut_sheet()
        self.cur_image = 0
        self.image = self.images[int(self.walk)][1][self.cur_image]
        self.rect = pygame.Rect(0, 0, 200, 200)
        self.rect.x = 800
        self.rect.y = 400
        self.turn = 1
        self.tick = 1

    def cut_sheet(self):
        result = [[[], [], [], []], [[], [], [], []]]
        result[1][0].append(Hero.img.subsurface(pygame.Rect(0, 0, 200, 200)))
        result[1][0].append(Hero.img.subsurface(pygame.Rect(0, 200, 200, 200)))  # walk up
        result[1][1].append(Hero.img.subsurface(pygame.Rect(200, 0, 200, 200)))
        result[1][1].append(Hero.img.subsurface(pygame.Rect(200, 200, 200, 200)))  # walk right
        result[1][2].append(Hero.img.subsurface(pygame.Rect(400, 0, 200, 200)))
        result[1][2].append(Hero.img.subsurface(pygame.Rect(400, 200, 200, 200)))  # walk down
        result[1][3].append(Hero.img.subsurface(pygame.Rect(600, 0, 200, 200)))
        result[1][3].append(Hero.img.subsurface(pygame.Rect(600, 200, 200, 200)))  # walk left

        result[0][0].append(Hero.img.subsurface(pygame.Rect(0, 400, 200, 200)))
        result[0][0].append(Hero.img.subsurface(pygame.Rect(0, 600, 200, 200)))  # stay up
        result[0][1].append(Hero.img.subsurface(pygame.Rect(200, 400, 200, 200)))
        result[0][1].append(Hero.img.subsurface(pygame.Rect(200, 600, 200, 200)))  # stay right
        result[0][2].append(Hero.img.subsurface(pygame.Rect(400, 400, 200, 200)))
        result[0][2].append(Hero.img.subsurface(pygame.Rect(400, 600, 200, 200)))  # stay down
        result[0][3].append(Hero.img.subsurface(pygame.Rect(600, 400, 200, 200)))
        result[0][3].append(Hero.img.subsurface(pygame.Rect(600, 600, 200, 200)))  # stay left
        return result

    def update(self, *args, **kwargs):
        self.tick += 1
        if self.tick == 10:
            self.cur_image = (self.cur_image + 1) % 2
            self.tick = 0
        self.image = self.images[int(self.walk)][self.turn][self.cur_image]


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(hero_sprite)
        self.x, self.y = randint(1, SIZE_BOARD[0] - 1), randint(1, SIZE_BOARD[1] - 1)
        while board.board[self.y][self.x]:
            self.x, self.y = randint(1, SIZE_BOARD[0] - 1), randint(1, SIZE_BOARD[1] - 1)
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, 'red', (0, 0, 200, 200))
        self.rect = pygame.Rect(0, 0, 200, 200)
        self.rect.x = 600 + self.x * 200
        self.rect.y = 200 + self.y * 200


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
        global board
        if self.rect.collidepoint(event.pos):
            board = Board()


class Board:
    def first_nears(self):
        wal = set()
        for i in range(4, SIZE_BOARD[0] - 1):
            wal.add((i, 1))
        for i in range(4, SIZE_BOARD[1] - 1):
            wal.add((1, i))
        for i in range(1, SIZE_BOARD[0] - 1):
            wal.add((SIZE_BOARD[0] - 1, i))
        for i in range(1, SIZE_BOARD[1] - 1):
            wal.add((SIZE_BOARD[1] - 1, i))
        return wal

    @staticmethod
    def nears_group(array, group):
        result = list()
        for i in range(SIZE_BOARD[0]):
            for j in range(SIZE_BOARD[1]):
                if not array[i][j]:
                    a = False
                    for x, y in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                        if (i + x, j + y) in group:
                            a = True
                            break
                    n = 0
                    for x, y in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                        if array[x + i][y + j]:
                            n += 1
                            if (i + x, y + j) not in group:
                                a = False
                    if a and n < 4:
                        result.append((i, j))
        return result

    @staticmethod
    def find_clear_cells(array):
        result = list()
        for i in range(1, SIZE_BOARD[0] - 1):
            for j in range(1, SIZE_BOARD[1] - 1):
                if array[i][j] == 0 and not any([any(x[j - 1:j + 2])
                                                 for x in array[i - 1:i + 2]]):
                    result.append((i, j))
        return result

    @staticmethod
    def bfs(array):
        delta = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        d = [[1e9] * SIZE_BOARD[0] for _ in range(SIZE_BOARD[1])]
        d[1][1] = 0
        q = [(1, 1), ]
        mmax = 0
        while q:
            x, y = q.pop()
            for dx, dy in delta:
                nx, ny = dx + x, dy + y
                if d[nx][ny] == 1e9 and array[nx][ny] != 1:
                    d[nx][ny] = d[x][y] + 1
                    mmax = max(d[nx][ny], mmax)
                    q.insert(0, (nx, ny))
        return d

    @staticmethod
    def bfs_yes_no(distant):
        mmax = 0
        mmax_coord = (1, 1)
        for i in range(SIZE_BOARD[0]):
            for j in range(SIZE_BOARD[1]):
                if distant[i][j] < 1e9:
                    if mmax < distant[i][j]:
                        mmax = distant[i][j]
                        mmax_coord = (i, j)
        if mmax > SIZE_BOARD[0] * 2:
            return mmax_coord
        else:
            return False

    def create_board(self):
        board = [[0] * SIZE_BOARD[0] for _ in range(SIZE_BOARD[1])]
        board[1][1] = 2
        for i in range(SIZE_BOARD[0]):
            board[i][0] = 1
            board[i][-1] = 1
        for i in range(SIZE_BOARD[1]):
            board[0][i] = 1
            board[-1][i] = 1

        n_wals = randint(5, 7)
        for i in range(n_wals):
            walls = set()
            b = self.first_nears()
            if len(b) < min(*SIZE_BOARD) // 4:
                break
            c = choice(list(b))
            walls.add(c)
            board[c[0]][c[1]] = 1
            for _ in range(randint(30, 70)):
                try:
                    cur_cell = choice(self.nears_group(board, walls))
                    board[cur_cell[0]][cur_cell[1]] = 1
                    walls.add(cur_cell)
                except Exception:
                    break

        while True:
            walls = set()
            b = self.find_clear_cells(board)
            if len(b) < min(*SIZE_BOARD) // 4:
                break
            c = choice(b)
            walls.add(c)
            board[c[0]][c[1]] = 1
            for _ in range(randint(30, 70)):
                try:
                    cur_cell = choice(self.nears_group(board, walls))
                    board[cur_cell[0]][cur_cell[1]] = 1
                    walls.add(cur_cell)
                except Exception:
                    break
        a = self.bfs_yes_no(self.bfs(board))
        if a:
            board[a[0]][a[1]] = 3
            return board
        else:
            return self.create_board()

    def __init__(self):
        self.end_pos = self.new_board()

    def new_board(self):
        self.board = self.create_board()
        end_pos = (0, 0)
        for i in range(SIZE_BOARD[0]):
            for j in range(SIZE_BOARD[1]):
                if self.board[i][j] == 2:
                    self.board[i][j] = 0
                elif self.board[i][j] == 3:
                    end_pos = (i, j)
                Cells((i, j), self.board[i][j])
        return end_pos


class Cells(pygame.sprite.Sprite):
    img = pygame.transform.scale(load_image('cat.png'), (800, 800))
    img_unde = pygame.transform.scale(load_image('ground.jpg'), (200, 200))
    img_wall = pygame.transform.scale(load_image('wall.png'), (200, 200))
    img_port = pygame.transform.scale(load_image('portal.jpg'), (200, 200))

    def __init__(self, pos, type):
        super().__init__(board_sprites)
        color = 'white'
        if type == 1:
            self.image = Cells.img_wall
        elif type == 0:
            self.image = Cells.img_unde
        else:
            self.image = Cells.img_port
        self.rect = pygame.Rect(pos[0] * 200 + 600, pos[1] * 200 + 200, 200, 200)


def start_screen():
    intro_text = ['The dungeon cat']

    fon = pygame.transform.scale(load_image('game.png'), SIZE)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 250)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
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


def move(turn, hero, board, real_m):
    global step
    if board.board[hero.x + turn[0]][hero.y - turn[1]] != 1 and not real_m:
        real_m = True
        step = 20
        hero.walk = True
        real_move(turn)
        if turn == (0, 1):
            hero.turn = 0
        elif turn == (0, -1):
            hero.turn = 2
        elif turn == (1, 0):
            hero.turn = 1
        elif turn == (-1, 0):
            hero.turn = 3
        if board.board[hero.x][hero.y] == 3:
            exit(0)  # ToDo
    return real_m


def real_move(turn_h):
    global step, turn, real_m
    if step:
        turn = turn_h
        for i in board_sprites:
            i.rect.x -= turn[0] * 10
            i.rect.y += turn[1] * 10
        enemy.rect.x -= turn[0] * 10
        enemy.rect.y += turn[1] * 10
        step -= 1
    else:
        hero.walk = False
        real_m = False
        hero.x += turn[0]
        hero.y -= turn[1]
        turn = tuple()


start_screen()

n_dungeon = 0

board_sprites = pygame.sprite.Group()

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
hero = Hero()

running = True
menu_active = True
start = False
info = False
board = Board()
enemy = Enemy()
real_m = False
step = 0
turn = tuple()
while running:
    if real_m:
        real_move(turn)
        screen.fill('white')
        if start:
            menu_active = False
            game_sprite.draw(screen)
            if board:
                board_sprites.draw(screen)
                hero_sprite.update()
                hero_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                real_m = move((-1, 0), hero, board, real_m)
            elif event.key == pygame.K_RIGHT:
                real_m = move((1, 0), hero, board, real_m)
            elif event.key == pygame.K_UP:
                real_m = move((0, 1), hero, board, real_m)
            elif event.key == pygame.K_DOWN:
                real_m = move((0, -1), hero, board, real_m)

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
        if board:
            hero_sprite.update()
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
