field = [[" "] * 3 for i in range(3)]


def show():
    print(f"  0 1 2")
    for i in range(3):
        row_info = " ".join(field[i])
        print(f"{i} {row_info}")


def ask():
    while True:
        cords = input("Ваш ход: ").split()
        if len(cords) != 2:
            print("Введите 2 координаты!")
            continue
        x, y = cords
        if not (x.isdigit()) or not (y.isdigit()):
            print("Введите число!")
            continue
        x, y = int(x), int(y)
        if 0 > x or x > 2 or 0 > y or y > 2:
            print("Вне диапазона")
            continue
        if field[x][y] != " ":
            print("Занято")
            continue
        return x, y


def check_win():
    win_cord = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0))]
    for cord in win_cord:
        a = cord[0]
        b = cord[1]
        c = cord[2]
        if field[a[0]][a[1]] == field[b[0]][b[1]] == field[c[0]][c[1]] != " ":
            print(f"ПОБЕДА {field[c[0]][c[1]]}")
            return True
    return False


num = 0
while True:
    num += 1
    show()
    if num % 2 == 1:
        print("Ходит Крестик")
    else:
        print("Ходит Нолик")
    x, y = ask()
    if num % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"
    if num == 9:
        print("Ничья")

    if check_win():
        break