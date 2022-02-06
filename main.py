import Leks_analiz
import Sint_analiz
import Semantika
import Interpritator

A = Leks_analiz.LexAnalyzer()
x = input("Введите строку: ")
res = A.startAnalysis(x)
if res:
    print("Лексический анализ проведен успешно")
else:
    print("Что-то пошло не так")

print("\nСписок лексем")
print(A.getListLex())
print("\nСписок идентификаторов")
print(A.getListID())
print("\nСписок констант")
print(A.getListConst())

print("\n----------------------------------")

B = Semantika.SintAnalyzer(A.ListLex, A.ListID, A.ListConst)
nor_err = B.startSimAnalysis()
if nor_err:
    print("\nСинтаксический анализ:\nКорректно")
else:
    print("\nСинтаксический анализ:\nЧто-то пошло не так")
B.T.printTree()

print("\n----------------------------------")

if nor_err:
    B.PrintPOLIZ()
else:
    print('\nПОЛИЗ невозможно сформировать, ошибка\n')

print("\n----------------------------------")

if nor_err:
    C = Interpritator.Interpritator(B.POLIZ, B.ListID, B.ListConst)
    C.startInterp()
