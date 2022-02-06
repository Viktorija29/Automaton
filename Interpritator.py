import Leks_analiz
import Sint_analiz
import Semantika


class Interpritator:
    def __init__(self, poliz, ListID, ListConst):
        self.stek = []
        self.POLIZ = poliz
        self.tmp = -1
        self.ListID = self.initVars(ListID)
        self.ListConst = ListConst

    # Инициализация переменных при запуске интерпритатора
    def initVars(self, ListID):
        new_list = []
        for v in ListID:
            new_list.append([v, input('Инициализируйте переменную ' + v.lex + ': ')])
        print()
        return new_list

    # Вывести список инициализированных переменных
    def showInitVars(self):
        s = 'Переменные: '
        for v in self.ListID:
            s += v[0].lex + ' = ' + str(v[1]) + ', '
        return s[0:-2]

    def showStek(self):
        ss = ''
        for s in self.stek:
            if isinstance(s, Semantika.PostfixEntry):
                if s.etype == Semantika.EEntryType.etVar:
                    ss += self.ListID[s.index][0].lex + ' '
                elif s.etype == Semantika.EEntryType.etConst:
                    ss += self.ListConst[s.index].lex + ' '
                elif s.etype == Semantika.EEntryType.etCmdPtr:
                    ss += str(s.index) + ' '
            else:
                ss += str(s) + ' '
        return 'Текущий стек: ' + ss

    # Извлечь значение константы или переменной из вершины стека
    def PopVal(self) -> int:
        val = self.stek[-1]
        self.stek = self.stek[0:-1]
        if isinstance(val, Semantika.PostfixEntry):
            if val.etype == Semantika.EEntryType.etVar:
                return int(self.ListID[val.index][1])
            elif val.etype == Semantika.EEntryType.etConst:
                return int(self.ListConst[val.index].lex)
            elif val.etype == Semantika.EEntryType.etCmdPtr:
                return val.index
        else:
            return val

    # Поместить значение в вершину стека
    def PushVal(self, val) -> None:
        self.stek.append(val)

    # Поместить элемент ПОЛИЗа (переменную, константу или адрес) в вершину стека
    def PushElm(self, elm) -> None:
        self.stek.append(elm)

    # Установить значение переменной, лежащей в вершине стека и извлечь ее
    def SetVarAndPop(self, val) -> None:
        var = self.stek[-1]
        for v in self.ListID:
            if v[0].lex == self.ListID[var.index][0].lex:
                self.ListID[var.index][1] = str(val)
        self.stek = self.stek[0:-1]

    def startInterp(self):
        iter = 0
        pos_POLIZ = 0
        while pos_POLIZ < len(self.POLIZ):
            info = self.showStek() + '  ' + self.showInitVars()
            if self.POLIZ[pos_POLIZ].etype == Semantika.EEntryType.etCmd:
                cmd = Semantika.ECmd[self.POLIZ[pos_POLIZ].index]
                if cmd == 'JMP':
                    print(info + "  |  Итерация " + str(iter) + ': Команда ' + 'JMP')
                    pos_POLIZ = self.PopVal()
                elif cmd == 'JZ':
                    print(info + "  |  Итерация " + str(iter) + ': Команда ' + 'JZ')
                    self.tmp = self.PopVal()
                    if self.PopVal() != 0:
                        pos_POLIZ += 1
                    else:
                        pos_POLIZ = self.tmp
                elif cmd == 'SET':
                    print(info + "  |  Итерация " + str(iter) + ': Команда ' + 'SET')
                    self.SetVarAndPop(self.PopVal())
                    pos_POLIZ += 1
                elif cmd == 'ADD':
                    print(info + "  |  Итерация " + str(iter) + ': Команда ' + 'ADD')
                    self.PushVal(self.PopVal() + self.PopVal())
                    pos_POLIZ += 1
                elif cmd == 'SUB':
                    print(info + "  |  Итерация " + str(iter) + ': Команда ' + 'SUB')
                    self.PushVal((-1) * self.PopVal() + self.PopVal())
                    pos_POLIZ += 1
                elif cmd == 'CMPL':
                    print(info + "  |  Итерация " + str(iter) + ': Команда ' + 'CMPL')
                    fl = self.PopVal() > self.PopVal()
                    if fl:
                        self.PushVal(1)
                    else:
                        self.PushVal(0)
                    pos_POLIZ += 1
            else:
                print(info + "  |  Итерация " + str(iter) + ': Внести в стек элемент ПОЛИЗа')
                self.PushElm(self.POLIZ[pos_POLIZ])
                pos_POLIZ += 1
            iter += 1
        print('\n------------------------------------\nРезультат: ' + self.showInitVars())
