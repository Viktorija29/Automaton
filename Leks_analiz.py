from enum import Enum


class ELexType(Enum):
    lFor = "for"
    lTo = "to"
    lNext = "next"
    # lAnd = "and"
    # lOr = "or"
    lRel = "rel"
    lAs = "as"
    lAo = "ao"
    lVar = "var"
    lConst = "const"

    def __str__(self):
        return str(self.value)


class EState(Enum):
    S = "S"  # начальное
    Ai = "Ai"  # идентификатор
    Ac = "Ac"  # константа
    As1 = "As1"  # >
    As2 = "As2"  # <
    Bs = "Bs"  # =
    Cs = "Cs"  # +-
    Ds = "Ds"  # >=, <=, <>,
    Gs = "Gs"  # ==
    E = "E"  # ошибочное состояние
    F = "F"  # финальное


class Lex:
    def __init__(self, lex_type, pos, lex):
        self.lex_type = lex_type
        self.pos = pos
        self.lex = lex

    def __str__(self):
        return ' '.join(["Тип:", str(self.lex_type), "Позиция:", str(self.pos), "Лексема", self.lex])


class LexAnalyzer:
    def __init__(self):
        # список считанных лексем
        self.ListLex = []
        self.ListID = []
        self.ListConst = []

    def getListLex(self):
        return "\n".join([str(el) for el in self.ListLex])

    def getListID(self):
        return "\n".join([str(el) for el in self.ListID])

    def getListConst(self):
        return "\n".join([str(el) for el in self.ListConst])

    def startAnalysis(self, source_text):
        curr_state = EState.S
        curr_symb = source_text[0]
        curr_lexem = ""
        index = 1
        add = None

        while curr_state != EState.E and curr_state != EState.F:
            # prevState = curr_state
            add = True

            if curr_state == EState.S:
                if curr_symb == " ":
                    pass
                elif curr_symb.isalpha():
                    curr_state = EState.Ai
                elif curr_symb.isdigit():
                    curr_state = EState.Ac
                elif curr_symb == "+" or curr_symb == "-":
                    curr_state = EState.Cs
                elif curr_symb == ">":
                    curr_state = EState.As1
                elif curr_symb == "<":
                    curr_state = EState.As2
                elif curr_symb == "=":
                    curr_state = EState.Bs
                elif curr_symb == "1a":
                    curr_state = EState.F
                else:
                    curr_state = EState.E
                add = False
            elif curr_state == EState.Ai:
                if curr_symb == " ":
                    curr_state = EState.S
                elif curr_symb.isalpha() or curr_symb.isdigit():
                    add = False
                elif curr_symb == "+" or curr_symb == "-":
                    curr_state = EState.Cs
                elif curr_symb == ">":
                    curr_state = EState.As1
                elif curr_symb == "<":
                    curr_state = EState.As2
                elif curr_symb == "=":
                    curr_state = EState.Bs
                elif curr_symb == "1a":
                    curr_state = EState.F
                else:
                    curr_state = EState.E
                    add = False
            elif curr_state == EState.Ac:
                if curr_symb == " ":
                    curr_state = EState.S
                elif curr_symb.isdigit():
                    add = False
                elif curr_symb == "+" or curr_symb == "-":
                    curr_state = EState.Cs
                elif curr_symb == ">":
                    curr_state = EState.As1
                elif curr_symb == "<":
                    curr_state = EState.As2
                elif curr_symb == "=":
                    curr_state = EState.Bs
                elif curr_symb == "1a":
                    curr_state = EState.F
                else:
                    curr_state = EState.E
                    add = False
            elif curr_state == EState.As1 or curr_state == EState.As2:
                if curr_symb == " ":
                    curr_state = EState.S
                elif curr_symb.isalpha():
                    curr_state = EState.Ai
                elif curr_symb.isdigit():
                    curr_state = EState.Ac
                elif curr_symb == "=" or (curr_state == EState.As2 and curr_symb == ">"):
                    curr_state = EState.Ds
                    add = False
                elif curr_symb == "1a":
                    curr_state = EState.F
                else:
                    curr_state = EState.E
                    add = False
            elif curr_state == EState.Bs:
                if curr_symb == " ":
                    curr_state = EState.S
                elif curr_symb.isalpha():
                    curr_state = EState.Ai
                elif curr_symb.isdigit():
                    curr_state = EState.Ac
                elif curr_symb == "=":
                    curr_state = EState.Gs
                    add = False
                elif curr_symb == "1a":
                    curr_state = EState.F
                else:
                    curr_state = EState.E
                    add = False
            elif curr_state == EState.Cs or curr_state == EState.Ds or curr_state == EState.Gs:
                if curr_symb == " ":
                    curr_state = EState.S
                elif curr_symb.isalpha():
                    curr_state = EState.Ai
                elif curr_symb.isdigit():
                    curr_state = EState.Ac
                elif curr_symb == "1a":
                    curr_state = EState.F
                else:
                    curr_state = EState.E
                    add = False

            if add:
                self.addLex(curr_lexem, index)
                curr_lexem = ""

            if curr_state == EState.Ai or curr_state == EState.Ac or curr_state == EState.As1 or \
                    curr_state == EState.As2 or curr_state == EState.Bs or curr_state == EState.Cs \
                    or curr_state == EState.Ds:
                curr_lexem = curr_lexem + curr_symb

            if index < len(source_text) and curr_state != EState.E and curr_state != EState.F:
                curr_symb = source_text[index]
            else:
                curr_symb = '1a'
            index += 1

        return curr_state == EState.F

    def addLex(self, strLex, pos):
        if strLex == "<" or strLex == ">" or strLex == "<" or strLex == "<=" or strLex == ">=" \
                or strLex == "<>" or strLex == "==":
            typeLex = ELexType.lRel
        elif strLex == "=":
            typeLex = ELexType.lAs
        elif strLex == "+" or strLex == "-":
            typeLex = ELexType.lAo
        elif strLex == "for":
            typeLex = ELexType.lFor
        elif strLex == "to":
            typeLex = ELexType.lTo
        elif strLex == "next":
            typeLex = ELexType.lNext
        # elif strLex == "and":
        #     typeLex = ELexType.lAnd
        # elif strLex == "or":
        #     typeLex = ELexType.lOr
        elif strLex.isdigit():
            typeLex = ELexType.lConst
            self.addConst(strLex, pos - len(strLex) - 1)
        else:
            typeLex = ELexType.lVar
            self.addID(strLex, pos - len(strLex) - 1)
        self.ListLex.append(Lex(typeLex, pos - len(strLex) - 1, strLex))

    def addID(self, strID, pos):
        for l in self.ListID:
            if l.lex == strID:
                return
        self.ListID.append(Lex(ELexType.lVar, pos, strID))

    def addConst(self, strConst, pos):
        self.ListConst.append(Lex(ELexType.lConst, pos, strConst))
