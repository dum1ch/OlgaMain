def symbol(num):
    if num == 0:
        return '-'
    if num == 1:
        return 'x'
    return 'o'


def first_choice():  # Определяем очередность первого хода
    print('Кто ходит первым? Если вы, введите 1, если компьютер, любой другой символ ')
    return input() != '1'


def show_board(dict_b):  # Выводим доску на экран
    print('  0 1 2')
    print('0', symbol(dict_b[(0, 0)]), symbol(dict_b[(0, 1)]), symbol(dict_b[(0, 2)]))
    print('1', symbol(dict_b[(1, 0)]), symbol(dict_b[(1, 1)]), symbol(dict_b[(1, 2)]))
    print('2', symbol(dict_b[(2, 0)]), symbol(dict_b[(2, 1)]), symbol(dict_b[(2, 2)]))
    print()


def status(dict_b):  # Проверка статуса и выбор следующего хода
    sums = [dict_b[(0, 0)] + dict_b[(0, 1)] + dict_b[(0, 2)],  # Список сумм по всем возможным линиям
            dict_b[(1, 0)] + dict_b[(1, 1)] + dict_b[(1, 2)],
            dict_b[(2, 0)] + dict_b[(2, 1)] + dict_b[(2, 2)],
            dict_b[(0, 0)] + dict_b[(1, 0)] + dict_b[(2, 0)],
            dict_b[(0, 1)] + dict_b[(1, 1)] + dict_b[(2, 1)],
            dict_b[(0, 2)] + dict_b[(1, 2)] + dict_b[(2, 2)],
            dict_b[(0, 0)] + dict_b[(1, 1)] + dict_b[(2, 2)],
            dict_b[(0, 2)] + dict_b[(1, 1)] + dict_b[(2, 0)]]

    if 12 in sums:
        return [12, ()]  # Игрок победил. Есть линия, в которой игроком занято 3 клетки

    for i in range(8):  # Поиск победного хода. Есть линия, в которой компьютером занято 2 клетки
        if sums[i] == 2:
            if i < 3:
                for j in range(3):
                    if dict_b[(i, j)] == 0:
                        return [2, (i, j)]

            elif i < 6:
                for j in range(3):
                    if dict_b[(j, i - 3)] == 0:
                        return [2, (j, i - 3)]

            elif i == 6:
                for j in range(3):
                    if dict_b[(j, j)] == 0:
                        return [2, (j, j)]

            elif i == 7:
                for j in range(3):
                    if dict_b[(j, 2 - j)] == 0:
                        return [2, (j, 2 - j)]

    for i in range(8):  # Поиск спасительного хода. Есть линия, в которой игроком занято 2 клетки
        if sums[i] == 8:
            if i < 3:
                for j in range(3):
                    if dict_b[(i, j)] == 0:
                        return [8, (i, j)]

            elif i < 6:
                for j in range(3):
                    if dict_b[(j, i - 3)] == 0:
                        return [8, (j, i - 3)]

            elif i == 6:
                for j in range(3):
                    if dict_b[(j, j)] == 0:
                        return [8, (j, j)]

            elif i == 7:
                for j in range(3):
                    if dict_b[(j, 2 - j)] == 0:
                        return [8, (j, 2 - j)]

    return [11, ()]


print('Здравствуйте, я компьютер, умею играть в крестики-нолики')

while True:
    print('Чтобы начать новую игру, нажмите 1. Если вы больше не хотите играть, нажмите любую другую клавишу ')
    if input() != '1':
        break

    draw = True  # Индикатор ничьей

    next_move = first_choice()  # Переменная для активного игрока

    list_moves = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (2, 1), (1, 2)]
    board = {(0, 0): 0, (0, 1): 0, (0, 2): 0,
             (1, 0): 0, (1, 1): 0, (1, 2): 0,
             (2, 0): 0, (2, 1): 0, (2, 2): 0}

    while list_moves:  # Пока есть ходы

        if next_move:  # Ход компьютера

            st = status(board)

            if st[0] == 12:
                print('Поздравляю! Вы выиграли!')
                draw = False
                break

            elif st[0] == 2:
                print('Ура! Я победил!')
                board[st[1]] = 1
                show_board(board)
                draw = False
                break

            elif st[0] == 8:
                board[st[1]] = 1  # Ход компьютера записывает 1 по ключу клетки
                list_moves.remove(st[1])

            else:
                board[list_moves[0]] = 1
                del list_moves[0]

        else:  # Ход человека
            while True:
                print('Ваш ход:')

                x = int(input('Номер строки '))
                y = int(input('Номер столбца '))

                flag = False  # Индикатор корректности хода человека

                for i in range(len(list_moves)):
                    if list_moves[i] == (x, y):
                        board[list_moves[i]] = 4  # Ход человека записывает 4 по ключу клетки
                        del list_moves[i]
                        flag = True
                        break

                if not flag:
                    print('Некорректный ход')
                else:
                    break

        show_board(board)

        next_move = not next_move  # Переход хода сопернику

    if draw:
        print('Ничья')

print('До свидания')
