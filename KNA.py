print("--------------------------Инициализация автомата--------------------------")
Z = input("Введите алфавит через пробел:\n").rstrip().split(" ")


def init_auto():
    global Q, F, err
    Q = input("Введите состояния автомата через пробел:\n").rstrip().split(" ")
    F = input("Введите конечные состояния автомата через пробел:\n").rstrip().split(" ")
    err = False

    for f in F:
        if f not in Q:
            err = True
            print("Финальные состояния должны принадлежать множеству состояний, ")
            break


init_auto()
while err:
    init_auto()

print("--------------------------Составление таблицы переходов--------------------------")
print("Если перехода нет, введите символ '-'")
print("Список состояний вводите через пробел")


def add():
    global q, z, d, err
    err = False
    # не текущее состояние, а множество текущих
    d = input("Переходы из состояния {0} на символе {1}: ".format(q, z)).rstrip().split(" ")
    for d_1 in d:
        if d_1 not in Q and d_1 != "-":
            print("Какого-то состояния не существует")
            err = True
            break


maxCountStates = [[z, 0] for z in Z]
Table = []
for q in Q:
    for z in Z:
        add()
        while err:
            add()
        Table.append([q, z, d])
        for el in maxCountStates:
            if el[0] == z:
                el[1] = max(el[1], len(d))
# print(maxCountStates)

print("--------------------------Таблица переходов--------------------------")
# print(Table)
for el in Table:
    print("Для состояния {0} и символа {1} переходы: {2}".format(el[0], el[1], ' '.join(el[2])))

beginState = input("\nВведите начальное состояние: ").rstrip()
if beginState not in Q:
    print("Такого состояния не существует")
    err = True
while err:
    beginState = input("Введите начальное состояние").rstrip()
    err = False
    if beginState not in Q:
        print("Такого состояния не существует")
        err = True

########################################################################################################

print("\nНапишите 'yes' без кавычек, чтобы начать алгоритм")
go = input().rstrip()
stop = False

while go == "yes":

    print("--------------------------Начало работы автомата--------------------------")

    w = input("Введите строку символов: ").rstrip()
    W = list(w)

    # глобальный список цепочек
    listOfChain = []


    def check_chain(pos, chain, curState, prev):
        global W, Table, listOfChain
        if curState == '-':
            return
        if pos != 0:
            chain.insert(len(chain), [prev, W[pos - 1], curState])
        if pos == len(W):
            listOfChain.insert(len(listOfChain), chain)
        else:
            # выделение символа
            symb = W[pos]
            # поиск множества следующих состояний
            for el in Table:
                if el[0] == curState and el[1] == symb:
                    list_next_states = el[2]
                    break
            for q in list_next_states:
                check_chain(pos + 1, chain.copy(), q, curState)


    check_chain(0, [], beginState, "")

    for ls in listOfChain:
        print(ls)
    fl = False
    for ls in listOfChain:
        if ls[len(ls)-1][2] in F:
            print("Цепочка {} допускается".format(w))
            fl = True
            break

    if not fl:
        print("Цепочка {} не допускается".format(w))

    print("--------------------------Конец работы автомата--------------------------")
    # if curState in F:
    #     print("Цепочка {} допускается".format(w))
    # else:
    #     print("Цепочка {} не допускается".format(w))

    print("Напишите 'yes' без кавычек, чтобы проверить новую цепочку")
    go = input().rstrip()
