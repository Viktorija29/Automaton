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
#print(Table)

lz = len(Z)
lq = len(Q)
print('  '.join(Z))
print("----"*lz)
str = ""
for i in range(0, lq):
    for j in range(0, lz):
        str += Table[i*lz+j][2] + "  "
    str += "| " + Q[i]
    print(str)
    str = ""

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

    curState = beginState

    def find_next_state():
        global curState, s
        for el in Table:
            if el[0] == curState and el[1] == s:
                return el[2]


    for s in W:
        newState = find_next_state()
        print("Переход из состояния {} в состояние {} по символу {}".format(curState, newState, s))
        curState = newState
        if newState == "-":
            break

    print("--------------------------Конец работы автомата--------------------------")
    if curState in F:
        print("Цепочка {} допускается".format(w))
    else:
        print("Цепочка {} не допускается".format(w))

    print("Напишите 'yes' без кавычек, чтобы проверить новую цепочку")
    go = input().rstrip()
