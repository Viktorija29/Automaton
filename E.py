print("--------------------------Инициализация автомата--------------------------")
Z = input("Введите алфавит через пробел: \n").rstrip().split(" ")
eps = input("Введите символ обозначения Эпсилон: \n")
# Z = ['0', '1']
# eps = 'E'
Z += eps


def init_auto():
    global Q, F, err
    Q = input("Введите состояния автомата через пробел: \n").rstrip().split(" ")
    F = input("Введите конечные состояния автомата через пробел: \n").rstrip().split(" ")
    err = False

    for f in F:
        if f not in Q:
            err = True
            print("Финальные состояния должны принадлежать множеству состояний, ")
            break


init_auto()
while err:
    init_auto()


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

#
# Q = ['q0', 'q1', 'q2', 'q3', 'q4']
# F = ['q1']

print("--------------------------Составление таблицы переходов--------------------------")
print("Если перехода нет, введите символ '-'")


def add():
    global q, z, d, err
    err = False
    d = input("Переход из состояния {0} на символе {1}: ".format(q, z)).rstrip()
    if d not in Q and d != "-":
        print("Такого состояния не существует")
        err = True


Table = []
for q in Q:
    for z in Z:
        add()
        while err:
            add()
        Table.append([q, z, d])

print("--------------------------Таблица переходов--------------------------")
# print(Table)

lz = len(Z)
lq = len(Q)
print('  '.join(Z))
print("----" * lz)
str_temp = ""
for i in range(0, lq):
    for j in range(0, lz):
        str_temp += Table[i * lz + j][2] + "  "
    str_temp += "| " + Q[i]
    print(str_temp)
    str_temp = ""

########################################################################################################

print("\nНапишите 'yes' без кавычек, чтобы начать алгоритм")
go = input().rstrip()
stop = False

while go == "yes":

    print("--------------------------Начало работы автомата--------------------------")

    w = input("Введите строку символов: ").rstrip()
    W = list(w)


    def find_next_state(curS, sym):
        for el in Table:
            if el[0] == curS and el[1] == sym:
                return el[2]


    listOfChain = []

    def find_next_state(state, sym):
        for el in Table:
            if el[0] == state and el[1] == sym:
                return el[2]


    def get_eps_perehod(state, list_eps):
        for el in Table:
            if el[0] == state and el[1] == eps and el[2] != '-':
                list_eps.insert(len(list_eps), el[2])
                get_eps_perehod(el[2], list_eps)


    def check_chain(pos, chain, curState, prevState, prevSym):
        global W, Table, listOfChain
        if curState == '-':
            chain.insert(len(chain), [prevState, prevSym, curState])
            listOfChain.insert(len(listOfChain), chain)
            return
        # если есть E-переход - получаем все возможные состояния, в которые переходим
        list_eps = []
        if find_next_state(curState, eps) != '-':
            get_eps_perehod(curState, list_eps)
            # print(list_eps)
        # продолжение основного алгоритма
        if pos != 0 or prevSym == eps:
            chain.insert(len(chain), [prevState, prevSym, curState])
        if pos == len(W):
            listOfChain.insert(len(listOfChain), chain)
        else:
            # выделение символа
            symb = W[pos]
            # поиск следующего состояния
            q_next = find_next_state(curState, symb)
            check_chain(pos + 1, chain.copy(), q_next, curState, symb)
            for e in list_eps:
                check_chain(pos, chain.copy(), e, curState, eps)


    check_chain(0, [], beginState, "", "")

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

    print("Напишите 'yes' без кавычек, чтобы проверить новую цепочку")
    go = input().rstrip()
