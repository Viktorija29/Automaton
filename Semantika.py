from copy import copy

import Leks_analiz
from enum import Enum


class Tree:
    def __init__(self):
        self.ListNodes = []
        self.stekVarConst = []
        self.stekAo = []
        self.level = 0
        self.flPrevVarConst = False
        self.flRange = False

    def clear(self):
        self.__init__()

    def printTree(self):
        print("\n\nДерево:")
        if not self.ListNodes:
            print("Не может быть построено")
        else:
            for n in self.ListNodes:
                print("Лексема {0} на уровне {1}".format(n[0].lex, n[1]))

    def addArithExpr(self):
        self.flRange = False
        lev = []
        if len(self.stekAo):
            for ao in self.stekAo:
                self.ListNodes.append([ao, self.level])
                lev.append(self.level)
                self.level += 1
            lev = [l + 1 for l in lev]
            self.stekAo = []
        if len(lev):
            for vc in range(0, len(self.stekVarConst) - 1):
                self.ListNodes.append([self.stekVarConst[vc], lev[vc]])
            self.ListNodes.append([self.stekVarConst[len(self.stekVarConst) - 1], lev[len(lev) - 1]])
        else:
            self.ListNodes.append([self.stekVarConst[0], self.level])
        self.stekVarConst = []
        self.flPrevVarConst = False

    def addNode(self, node):
        if node.lex_type == Leks_analiz.ELexType.lFor:
            self.level = 1
            self.ListNodes.append([node, self.level])
        elif node.lex_type == Leks_analiz.ELexType.lTo or node.lex_type == Leks_analiz.ELexType.lNext:
            self.addArithExpr()
            self.level = 2
            self.ListNodes.append([node, self.level])
            self.level = 3
            self.flPrevVarConst = False
            self.flRange = True
        elif node.lex_type == Leks_analiz.ELexType.lVar or node.lex_type == Leks_analiz.ELexType.lConst:
            if not self.flRange:
                self.level = 3
            if self.flPrevVarConst:
                self.addArithExpr()
            else:
                self.flPrevVarConst = True
            self.stekVarConst.append(node)
        elif node.lex_type == Leks_analiz.ELexType.lAs:
            self.level = 2
            self.ListNodes.append([node, self.level])
            self.level = 3
            self.ListNodes.append([self.stekVarConst[0], self.level])
            self.stekVarConst = []
            self.flPrevVarConst = False
        elif node.lex_type == Leks_analiz.ELexType.lAo:
            self.stekAo.append(node)
            self.flPrevVarConst = False


# тип содержимого в ПОЛИЗе
class EEntryType(Enum):
    etCmd = "Cmd"  # команда
    etVar = "Var"  # переменная
    etConst = "Const"  # константа
    etCmdPtr = "CmdPtr"  # адрес


# тип команды
ECmd = ['JMP', 'JZ', 'SET', 'ADD', 'SUB', 'CMPE', 'CMPNE', 'CMPL', 'CMPLE']


# элемент ПОЛИЗа
class PostfixEntry:
    def __init__(self, etype, index):
        self.etype = etype
        self.index = index  # описывает содержимое


class SintAnalyzer:
    def __init__(self, ListLex, ListID, ListConst):
        self.ListLex = ListLex
        self.ListID = ListID
        self.ListConst = ListConst
        self.curr_lex_pos = 0
        self.curr_lex = ListLex[0]
        self.prev_lex = None
        self.flErr = False
        self.T = Tree()
        self.POLIZ = []

    # функции для формирования ПОЛИЗа
    def WriteCmd(self, cmd) -> int:
        self.POLIZ.append(PostfixEntry(EEntryType.etCmd, ECmd.index(cmd)))
        return len(self.POLIZ) - 1

    def WriteVar(self, ind) -> int:
        self.POLIZ.append(PostfixEntry(EEntryType.etVar, ind))
        return len(self.POLIZ) - 1

    def WriteConst(self, ind) -> int:
        self.POLIZ.append(PostfixEntry(EEntryType.etConst, ind))
        return len(self.POLIZ) - 1

    def WriteCmdPtr(self, ptr) -> int:
        self.POLIZ.append(PostfixEntry(EEntryType.etCmdPtr, ptr))
        return len(self.POLIZ) - 1

    def SetCmdPtr(self, ind, ptr) -> None:
        self.POLIZ[ind].index = ptr

    def PrintPOLIZ(self):
        c = 0
        print('\nPOLIZ:')
        for p in self.POLIZ:
            s = str(c) + ": "
            if p.etype == EEntryType.etCmd:
                s += ECmd[p.index]
            elif p.etype == EEntryType.etVar:
                s += self.ListID[p.index].lex
            elif p.etype == EEntryType.etConst:
                s += self.ListConst[p.index].lex
            else:
                s += '(' + str(p.index) + ')'
            print(s)
            c += 1

    def FindIndexByObjectInListID(self, obj):
        name = obj.lex
        ind = 0
        for var in self.ListID:
            if var.lex == name:
                return ind
            ind += 1

    def FindIndexByObjectInListConst(self, obj):
        name = obj.lex
        ind = 0
        for var in self.ListConst:
            if var.lex == name:
                return ind
            ind += 1

    def printError(self, msg, pos) -> None:
        self.T.clear()
        print("ОШИБКА: {0} ПОЗИЦИЯ: {1}".format(msg, str(pos)))
        self.flErr = True

    def next_lexem(self) -> None:
        self.prev_lex = self.curr_lex
        if len(self.ListLex) > self.curr_lex_pos + 1:
            self.curr_lex_pos += 1
            self.curr_lex = self.ListLex[self.curr_lex_pos]
            self.T.addNode(self.curr_lex)
        else:
            self.curr_lex_pos = -1
            self.curr_lex = None

    def Operand(self) -> bool:
        if not self.curr_lex:
            self.printError("Ожидается переменная или константа", self.prev_lex.pos + len(self.prev_lex.lex))
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lVar and self.curr_lex.lex_type != Leks_analiz.ELexType.lConst:
            self.printError("Ожидается переменная или константа", self.curr_lex.pos)
            return False
        # тип лексемы - переменная
        if self.curr_lex.lex_type == Leks_analiz.ELexType.lVar:
            self.WriteVar(self.FindIndexByObjectInListID(self.curr_lex))
        # тип лексемы - константа
        else:
            self.WriteConst(self.FindIndexByObjectInListConst(self.curr_lex))
        self.next_lexem()
        return True

    def ArithExpr(self) -> bool:
        if not self.Operand():
            return False
        # сформирована часть ПОЛИЗа для операнда
        while self.curr_lex and self.curr_lex.lex_type == Leks_analiz.ELexType.lAo:
            # определение типа операции
            if self.curr_lex.lex == '+':
                cmd = 'ADD'
            else:
                cmd = 'SUB'
            self.next_lexem()
            if not self.Operand():
                return False
            # сформирована часть ПОЛИЗа для операнда
            self.WriteCmd(cmd)  # заносим операцию в ПОЛИЗ
        return True

    def Statement(self) -> bool:
        if not self.curr_lex:
            self.printError("Ожидается переменная", self.prev_lex.pos + len(self.prev_lex.lex) + 1)
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lVar:
            self.printError("Ожидается переменная", self.curr_lex.pos)
            return False
        # заносим в ПОЛИЗ переменную
        if self.curr_lex.lex_type == Leks_analiz.ELexType.lVar:
            self.WriteVar(self.FindIndexByObjectInListID(self.curr_lex))
        self.next_lexem()
        if not self.curr_lex:
            self.printError("Ожидается присваивание", self.prev_lex.pos + len(self.prev_lex.lex))
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lAs:
            self.printError("Ожидается присваивание", self.curr_lex.pos)
            return False
        self.next_lexem()
        if not self.ArithExpr():
            return False
        # ПОЛИЗ для выражения уже сформирован
        self.WriteCmd('SET')  # заносим в ПОЛИЗ команду присваивания
        return True

    def Range(self, indCMPL) -> bool:
        if not self.curr_lex:
            self.printError("Ожидается переменная", self.prev_lex.pos + len(self.prev_lex.lex) + 1)
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lVar:
            self.printError("Ожидается переменная", self.curr_lex.pos)
            return False
        # заносим переменную в ПОЛИЗ и запоминаем ее для дальнейшего сравнения
        buf_var = copy(self.curr_lex)
        self.WriteVar(self.FindIndexByObjectInListID(self.curr_lex))
        self.next_lexem()
        if not self.curr_lex:
            self.printError("Ожидается присваивание", self.prev_lex.pos + len(self.prev_lex.lex))
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lAs:
            self.printError("Ожидается присваивание", self.curr_lex.pos)
            return False
        self.next_lexem()
        if not self.ArithExpr():
            return False
        # сформирована часть ПОЛИЗа для условия
        self.WriteCmd('SET')  # заносим в ПОЛИЗ команду присваивания
        if not self.curr_lex:
            self.printError("Ожидается to", self.prev_lex.pos + len(self.prev_lex.lex) + 1)
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lTo:
            self.printError("Ожидается to", self.curr_lex.pos + 1)
            return False
        indCMPL[0] = len(self.POLIZ)
        indCMPL[1] = buf_var
        self.WriteVar(self.FindIndexByObjectInListID(buf_var))
        self.next_lexem()
        if not self.ArithExpr():
            return False
        self.WriteCmd('CMPL')  # заносим в ПОЛИЗ команду сравнения
        return True

    def ForStatement(self) -> bool:
        if not self.curr_lex or self.curr_lex.lex_type != Leks_analiz.ELexType.lFor:
            self.printError("Ожидается for", self.curr_lex.pos)
            return False
        self.T.addNode(self.curr_lex)
        self.next_lexem()
        paramToCMPL = [-1, '']
        if not self.Range(paramToCMPL):
            return False
        # сформирована часть ПОЛИЗа, вычисляющая условие цикла
        indJmp = self.WriteCmdPtr(-1)  # заносим фиктивное значение адреса условного перехода
        self.WriteCmd('JZ')  # заносим команду условного перехода
        if not self.Statement():
            return False
        while self.curr_lex and self.curr_lex.lex_type != Leks_analiz.ELexType.lNext:
            if not self.Statement():
                return False
        # сформирована часть ПОЛИЗа для тела цикла
        if not self.curr_lex:
            self.printError("Ожидается next", self.prev_lex.pos + len(self.prev_lex.lex) + 1)
            return False

        # увеличение счетчика на 1
        self.ListConst.append(Leks_analiz.Lex(Leks_analiz.ELexType.lConst, 10000, '1'))
        self.WriteVar(self.FindIndexByObjectInListID(paramToCMPL[1]))
        self.WriteVar(self.FindIndexByObjectInListID(paramToCMPL[1]))
        self.WriteConst(len(self.ListConst)-1)
        self.WriteCmd('ADD')
        self.WriteCmd('SET')

        self.WriteCmdPtr(paramToCMPL[0])  # заносим адрес проверки условия
        indLast = self.WriteCmd('JMP')  # заносим команду безусловного перехода и сохраняем ее адрес
        self.SetCmdPtr(indJmp, indLast + 1)  # изменяем фиктивное значение адреса условного перехода
        return True

    def startSimAnalysis(self) -> bool:
        return self.ForStatement()
