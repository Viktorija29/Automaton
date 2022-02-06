import Leks_analiz

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
            for vc in range(0, len(self.stekVarConst)-1):
                self.ListNodes.append([self.stekVarConst[vc], lev[vc]])
            self.ListNodes.append([self.stekVarConst[len(self.stekVarConst)-1], lev[len(lev)-1]])
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


class SintAnalyzer:
    def __init__(self, ListLex):
        self.ListLex = ListLex
        self.curr_lex_pos = 0
        self.curr_lex = ListLex[0]
        self.prev_lex = None
        self.flErr = False
        self.T = Tree()

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
        self.next_lexem()
        return True

    def ArithExpr(self) -> bool:
        if not self.Operand():
            return False
        while self.curr_lex and self.curr_lex.lex_type == Leks_analiz.ELexType.lAo:
            self.next_lexem()
            if not self.Operand():
                return False
        return True

    def Statement(self) -> bool:
        if not self.curr_lex:
            self.printError("Ожидается переменная", self.prev_lex.pos + len(self.prev_lex.lex) + 1)
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lVar:
            self.printError("Ожидается переменная", self.curr_lex.pos)
            return False
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
        return True

    def Range(self) -> bool:
        if not self.curr_lex:
            self.printError("Ожидается переменная", self.prev_lex.pos + len(self.prev_lex.lex) + 1)
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lVar:
            self.printError("Ожидается переменная", self.curr_lex.pos)
            return False
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
        if not self.curr_lex:
            self.printError("Ожидается to", self.prev_lex.pos + len(self.prev_lex.lex) + 1)
            return False
        if self.curr_lex.lex_type != Leks_analiz.ELexType.lTo:
            self.printError("Ожидается to", self.curr_lex.pos + 1)
            return False
        self.next_lexem()
        if not self.ArithExpr():
            return False
        return True

    def ForStatement(self) -> bool:
        if not self.curr_lex or self.curr_lex.lex_type != Leks_analiz.ELexType.lFor:
            self.printError("Ожидается for", self.curr_lex.pos)
            return False
        self.T.addNode(self.curr_lex)
        self.next_lexem()
        if not self.Range():
            return False
        if not self.Statement():
            return False
        while self.curr_lex and self.curr_lex.lex_type != Leks_analiz.ELexType.lNext:
            if not self.Statement():
                return False
        if not self.curr_lex:
            self.printError("Ожидается next", self.prev_lex.pos + len(self.prev_lex.lex) + 1)
            return False
        return True

    def startSimAnalysis(self) -> bool:
        return self.ForStatement()
