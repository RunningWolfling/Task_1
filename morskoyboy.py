from random import randint

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел вне доски!!!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "В этой клетке выстрел уже был."

class BoardShipException(BoardException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, l, b):
        self.bow = bow
        self.l = l
        self.b = b
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            curs_x = self.bow.x
            curs_y = self.bow.y

            if self.b == 0:
                curs_x += i
            elif self.b == 1:
                curs_y += i

            ship_dots.append(Dot(curs_x, curs_y))
        return ship_dots

    def shooting(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.count = 0

        self.field = [["0"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        doska = ""
        doska += "  | 1 | 2 | 3 | 4 | 5 | 6|"
        for i, row in enumerate(self.field):
            doska += f"\n{i + 1} | " + " |".join(row) + "|"
        if self.hid:
            doska = doska.replace("@", "0")
        return doska

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                curs = Dot(d.x + dx, d.y + dy)
                if not (self.out(curs)) and curs not in self.busy:
                    if verb:
                        self.field[curs.x][curs.y] = "+"
                    self.busy.append(curs)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "@"
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)
        for ship in self.ships:
            if ship.shooting(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Убит!")
                    return False
                else:
                    print("Ранен.")
                    return True
        self.field[d.x][d.y] = "."
        print("Мимо!")

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, foe):
        self.board = board
        self.foe = foe

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.foe.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print("Введите 2 координаты!")
                continue

            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print("Нужны числа!")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_boards()
        computer = self.random_boards()
        computer.hid = True
        self.ai = AI(computer, player)
        self.user = User(player, computer)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), 1, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardShipException:
                    pass
        board.begin()
        return board

    def random_boards(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print(" Добро пожаловать ")
        print("      в игру      ")
        print("   Морской Бой!   ")
        print("формат ввода: x, y")
        print("х - строка        ")
        print("у - столбец.      ")

    def loop(self):
        counts = 0
        while True:
            print("-" * 20)
            print("Доска игрока:")
            print(self.user.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if counts % 2 == 0:
                print("Ходит игрок!")
                repeat = self.user.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                counts -= 1

            if self.ai.board.count == len(self.ai.board.ships):
                print("-" * 20)
                print("выиграл Игрок!!!")
                break
            if self.user.board.count == 7:
                print("-" * 20)
                print("выиграл Компьютер!!!")
                break
            counts += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()