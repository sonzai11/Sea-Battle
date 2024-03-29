import random as r

class Dot:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class OutOfBounds(Exception):
    pass

class Collision(Exception):
    pass

class BadAttempt(Exception):
    pass

class Ship:
    def __init__(self,size,x,y,rotation):
        self.size = size
        self.position = Dot(x,y)
        # Если True, то корабль расположен вертикально
        self.rotation = rotation
        self.hp = size

    def get_size(self):
        return self.size

    def get_position(self):
        return self.position

    def get_rotation(self):
        return self.rotation

    def get_hp(self):
        return self.hp

    def got_hit(self):
        self.hp -= 1



    def get_ship(self):
        dots = [self.get_position()]
        for i in range(1,self.get_size()):
            if self.get_rotation():
                dots.append(Dot(self.get_position().get_x()+i,self.get_position().get_y()))
            else:
                dots.append(Dot(self.get_position().get_x(), self.get_position().get_y()+i))
        return dots

class Field:
    def __init__(self,hid):
        self.field = [['O','O','O','O','O','O'],
                      ['O','O','O','O','O','O'],
                      ['O','O','O','O','O','O'],
                      ['O','O','O','O','O','O'],
                      ['O','O','O','O','O','O'],
                      ['O','O','O','O','O','O'],]
        self.ships = []
        self.hid = hid
        self.alive = 0

    def get_field(self):
        return self.field

    def get_ships(self):
        return self.ships

    def get_hid(self):
        return self.hid

    def get_alive(self):
        return self.alive

    def add_ship(self,size,rotation,dot):
       x = dot.get_x()
       y = dot.get_y()
       self.get_ships().append(Ship(size,x,y,rotation))
       for dot in Ship(size,x,y,rotation).get_ship():
           x1,y1 = dot.get_x(), dot.get_y()
           self.get_field()[x1-1][y1-1] = '■'


    def collision(self, ship):
        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1),(0,0)]
        check_up = 0
        for d in directions:
            for dot in ship.get_ship():
                x,y = dot.get_x() + d[0], dot.get_y() + d[1]

                for ship_in_field in self.get_ships():
                    if Dot(x,y) in ship_in_field.get_ship():
                        check_up = 1
                        break
        if check_up:
            return True
        else:
            return False

    def contour(self, ship):
        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        for d in directions:
            for dot in ship.get_ship():
                x, y = dot.get_x() + d[0], dot.get_y() + d[1]
                if not(self.out(Dot(x, y))):
                    check_up = 0
                    for ship_in_field in self.get_ships():
                        if Dot(x, y) in ship_in_field.get_ship():
                            check_up = 1
                            break
                    if not check_up:
                        self.get_field()[x-1][y-1] = "T"

    def print_board(self):
        print('\033[32m  | 1 | 2 | 3 | 4 | 5 | 6 |\033[39m')
        if self.get_hid():
            for i in range(1,7):
                print(f'\033[32m{i}\033[39m |',end='')
                for j in range(1,7):
                    if self.get_field()[i-1][j-1] == '■':
                        print(' O |',end='')
                    else:
                        print(f' {self.get_field()[i-1][j-1]} |',end='')
                print('',end='\n')
        else:
            for i in range(1,7):
                print(f'\033[32m{i}\033[39m | {self.get_field()[i-1][0]} | {self.get_field()[i-1][1]} | {self.get_field()[i-1][2]} | {self.get_field()[i-1][3]} | {self.get_field()[i-1][4]} | {self.get_field()[i-1][5]} |')

    def out(self,dot):
        return not((0 < dot.get_x() <= 6) and (0 < dot.get_y() <= 6))

    def shot(self,dot):
        x = dot.get_x()
        y = dot.get_y()
        shot = Dot(x,y)

        for ship in self.get_ships():
            for dot in ship.get_ship():
        #        if self.get_field()[x-1][y-1] == '■':
                if shot == dot:
                    print('Зафиксировано попадание!\n')
                    self.get_field()[x-1][y-1] = 'X'
                    for ship in self.get_ships():
                        if shot in ship.get_ship():
                            ship.got_hit()
                            if not ship.get_hp():
                                print('Корабль уничтожен!\n')
                                self.contour(ship)
                                self.get_ships().remove(ship)
                    return True

        print('Мимо!\n')
        self.get_field()[x-1][y-1] = 'T'
        return False

    def reset_board(self):
        self.field = [['O' for _ in range(6)] for _ in range(6)]
        self.ships = []
class Player:
    def __init__(self, player_field, enemy_field):
        self.player_field = player_field
        self.enemy_field = enemy_field

    def get_player_field(self):
        return self.player_field

    def get_enemy_field(self):
        return self.enemy_field

    def place_ship(self,size):
        pass

    def make_shot(self):
        pass

class User(Player):
    def place_ship(self,size):
        self.get_player_field().print_board()
        rotation = True
        while True and size != 1:
            try:
                temp = int(input('Выберите направление корабля \033[31m ( 1 - ВЕРТИКАЛЬНО, 2 - ГОРИЗОНТАЛЬНО )\033[39m\n'))
                if temp != 1 and temp != 2:
                    raise ValueError
            except ValueError:
                print('\033[31m!Введено неправильное значение!\nПовторите ввод\033[39m')
            else:
                if temp == 1:
                    rotation = True
                else:
                    rotation = False
                break
        while True:
            try:
                x = int(input('Введите координату начала корабля по вертикали \033[31m (X) \033[39m\n'))
                y = int(input('Введите координату начала корабля по горизонтали \033[31m (Y) \033[39m\n'))
                if self.get_player_field().out(Dot(x,y)) or (self.get_player_field().out(Dot(x+size-1,y)) if rotation else self.get_player_field().out(Dot(x,y+size-1))):
                    raise OutOfBounds
                if self.get_player_field().collision(Ship(size,x,y,rotation)):
                    raise Collision
            except ValueError:
                print('\033[31m!Введено неправильное значение!\nПовторите ввод\033[39m')
            except OutOfBounds:
                print('\033[31m!Корабль выходит за границы игрового поля!\nПовторите ввод\033[39m')
            except Collision:
                print('\033[31m!Корабль расположен слишком близко к другому кораблю!\nПовторите ввод\033[39m')
            else:
                break
        self.get_player_field().add_ship(size=size,dot=Dot(x,y),rotation=rotation)

    def make_shot(self):
        while True:
            try:
                x = int(input('Введите координату выстрела по вертикали \033[31m (X) \033[39m\n'))
                y = int(input('Введите координату выстрела по горизонтали \033[31m (Y) \033[39m\n'))
                if self.get_enemy_field().out(Dot(x,y)):
                    raise OutOfBounds
                if self.get_enemy_field().get_field()[x-1][y-1] != 'O' and self.get_enemy_field().get_field()[x-1][y-1] != '■':
                    raise Collision
            except ValueError:
                print('\033[31m!Введено неправильное значение!\nПовторите ввод\033[39m')
            except OutOfBounds:
                print('\033[31m!Выстрел мимо игрового поля!\nПовторите ввод\033[39m')
            except Collision:
                print('\033[31m!Выстрел в данную точку уже был совершен!\nПовторите ввод\033[39m')
            else:
                break
        if self.get_enemy_field().shot(Dot(x,y)):
            return True
        else:
            return False

class AI(Player):
    def place_ship(self,size):

        temp = r.randint(1,2)
        if temp == 1:
            rotation = True
        else:
            rotation = False
        try:
            x = r.randint(0,5)
            y = r.randint(0,5)
            if self.get_player_field().out(Dot(x,y)) or (self.get_player_field().out(Dot(x+size-1,y)) if rotation else self.get_player_field().out(Dot(x,y+size-1))):
                raise OutOfBounds
            if self.get_player_field().collision(Ship(size,x,y,rotation)):
                raise Collision
        except OutOfBounds:
            return False
        except Collision:
            return False
        else:
            self.get_player_field().add_ship(size,dot=Dot(x,y),rotation=rotation)
            return True

    def make_shot(self):
        try:
            x = r.randint(1,6)
            y = r.randint(1,6)
            if self.get_enemy_field().out(Dot(x,y)):
                raise OutOfBounds
            if self.get_enemy_field().get_field()[x-1][y-1] == 'T' and self.get_enemy_field().get_field()[x-1][y-1] == 'X':
                raise Collision
        except OutOfBounds:
            pass
        except Collision:
            pass
        else:
            if self.get_enemy_field().shot(Dot(x,y)):
                return True
            else:
                return False

class Game:
    def __init__(self,user,player_field,bot,bot_field):
        self.user = user
        self.player_field = player_field
        self.bot = bot
        self.bot_field = bot_field

    def get_user(self):
        return self.user

    def get_player_field(self):
        return self.player_field

    def get_bot(self):
        return self.bot

    def get_bot_field(self):
        return self.bot_field

    def greet(self):
        print('\033[31m ИГРА МОРСКОЙ БОЙ\033[39m\n\n'
              'Пользователь играет против компьютера. Перед началом игры пользователь расставляет корабли на своем поле.\n'
              'После игрок и компьютер совершают ходы, называя координаты поля соперника, вводя координаты по горизонтали\n'
              'и вертикали. Если у врага в клетке с этими координатами имеется корабль, то корабль или его палуба уничтожается,\n'
              'попавший делает еще один ход. Цель игрока: первым убить все корабли противника.\n\n')

    def random_board(self):
        ship_sizes = [3, 2, 2, 1, 1, 1, 1]

        self.get_bot().get_player_field().reset_board()
        self.get_bot_field().reset_board()

        for size in ship_sizes:
            attempts = 0
            while attempts < 1000:
                try:
                    if self.get_bot().place_ship(size):
                        break
                except (OutOfBounds, Collision):
                    pass
                attempts += 1

            if attempts >= 1000:
                return False

        return True

    def start_game(self):
        self.greet()
        print('\033[31mПримечание: если не удается разместить все корабли на доске, перезапустите игру.\033[39m\n\n')
        print('Разместите 3-х палубных корабль')
        self.get_user().place_ship(3)
        print('Разместите два 2-х палубных корабля')
        self.get_user().place_ship(2)
        self.get_user().place_ship(2)
        print('Разместите четыре однопалубных корабля')
        self.get_user().place_ship(1)
        self.get_user().place_ship(1)
        self.get_user().place_ship(1)
        self.get_user().place_ship(1)
        while True:
            if self.random_board():
                break

        players = [self.get_user(), self.get_bot()]
        move = 0
        while not self.end_of_game():
            for ship in self.get_bot().get_player_field().get_ships():
                print(ship.get_hp())
            if not move:
                print('Ваш ход')
                players[0].get_enemy_field().print_board()
            else:
                print('Ход компьютера')
                players[0].get_player_field().print_board()
            if not players[move].make_shot():
                if not move:
                    move = 1
                else:
                    move = 0



    def end_of_game(self):
        players = [self.get_user().get_player_field(), self.get_user().get_enemy_field()]
        count = 0
        win = 0
        for index in range(0,2):
            count = 0
            if not players[index].get_ships():
                count = 1
            if count == 1:
                if index == 0:
                    print('\n\nПОБЕДА КОМПЬЮТЕРА!')
                    win = 1
                else:
                    print('\n\nПОБЕДА ИГРОКА')
                    win = 2
                break
        return win

user_field = Field(False)
bot_field = Field(True)
user = User(user_field,bot_field)
bot = AI(bot_field,user_field)
game = Game(user,user_field,bot,bot_field)
game.start_game()