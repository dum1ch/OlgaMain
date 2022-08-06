from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"


class BoardWrongShipException(BoardException):
    pass


class Dot:  # Точки на доске
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, l_s, o):
        self.bow = bow
        self.l_s = l_s
        self.o = o
        self.lives = l_s

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l_s):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, size=6):

        self.size = size
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d, flag):  # Выстрел
        if d in self.busy:  # Выстрел в использованную клетку
            raise BoardUsedException

        if self.out(d):  # Выстрел мимо доски
            raise BoardOutException

        if not flag:
            print(f"Ход компьютера: {d.x + 1} {d.y + 1}")

        self.busy.append(d)

        for ship in self.ships:  # Проверка на попадание в один из кораблей
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен")
                    return False
                else:
                    print("Корабль ранен")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо")
        return False

    def begin(self):
        self.busy = []


class Monitor:
    def __init__(self, l_b, r_b, size):
        self.l_b = l_b
        self.r_b = r_b
        self.size = size
        left = [["O"] * self.size for _ in range(self.size)]
        right = [["O"] * self.size for _ in range(self.size)]
        self.field = [left, right]

        for i in range(self.size):
            self.field[0][i] = self.l_b.field[i]
            self.field[1][i] = self.r_b.field[i]

    def __str__(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[1][i][j] == "■":
                    self.field[1][i][j] = "0"

        res = ""
        res += "     Доска пользователя:                   Доска компьютера:   "
        res += "\n  | 1 | 2 | 3 | 4 | 5 | 6 |            | 1 | 2 | 3 | 4 | 5 | 6 |"
        row = [self.field[0], self.field[1]]

        for i in range(self.size):
            res += f"\n{i + 1} | " + " | ".join(row[0][i]) + f" |          {i + 1} | " + " | ".join(row[1][i]) + " |"

        return res


class Player:  # Класс игрока
    def __init__(self, board, enemy, size):
        self.board = board
        self.enemy = enemy
        self.size = size

    def ask(self):
        raise NotImplementedError()

    def move(self, flag=True):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target, flag)

                return repeat
            except BoardException as e:
                if flag:
                    print(e)


class AI(Player):  # Класс игрока-компьютера
    def ask(self):
        d = Dot(randint(0, self.size - 1), randint(0, self.size - 1))

        return d


class User(Player):  # Класс игрока-человека
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите две координаты!")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()

        self.ai = AI(co, pl, self.size)
        self.us = User(pl, co, self.size)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for i in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size - 1), randint(0, self.size - 1)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("-----------------------------------------------------------------")
        print("                        Приветствуем вас                         ")
        print("                             в игре                              ")
        print("                           морской бой                           ")
        print("-----------------------------------------------------------------")
        print("                        формат ввода:  x y                       ")
        print("                         x - номер строки                        ")
        print("                         y - номер столбца                       ")

    def loop(self):
        num = 0
        while True:
            print("-" * 65)
            m = Monitor(self.us.board, self.ai.board, self.size)
            print(m)
            print("-" * 65)

            if num % 2 == 0:
                print("Ходит пользователь")
                repeat = self.us.move()
            else:
                print("Ходит компьютер")
                repeat = self.ai.move(False)
            if repeat:
                num -= 1

            if self.ai.board.count == len(self.ai.board.ships):
                print("-" * 65)
                print("Вы выиграли!")
                break

            if self.us.board.count == len(self.us.board.ships):
                print("-" * 65)
                print("Компьютер выиграл!")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
