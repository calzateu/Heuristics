lista = [[0, 46, 0, 32, 1, 22, 28, 31, 3, 20, 35, 36, 2, 0], [0, 27, 0, 6, 48, 8, 26, 7, 23, 24, 14, 0, 10, 45, 0], [0, 12, 0, 11, 38, 5, 49, 9, 50, 16, 29, 21, 0], [0, 47, 4, 17, 37, 15, 44, 42, 19, 41, 13, 40, 0]]

lista_set = []
for l in lista:
    lista_set.extend(l)

lista_set = list(set(lista_set))

print(lista_set)