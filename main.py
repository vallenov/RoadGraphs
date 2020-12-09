# python C:\Prog\Python\NIR\P\Road_Graphs-0.6.py

import os
import random
import math
from tkinter import *
import numpy as np
import time

# Размеры окна
HEIGHT = 500
WIDTH = 1000

root = Tk()  # Инициализация окна
root.title("Road Graph")  # Название окна
mainmenu = Menu(root)
root.config(menu=mainmenu)
c = Canvas(root, width=WIDTH, height=HEIGHT, background="white")  # Создание окна с белым фоном


class Point:  # Класс перекрестков

    def __init__(self, name_of_point):  # Инициализация точки прекрестка
        self.name_of_point = name_of_point  # Название перекрестка
        self.RAD = 10  # Радиус точки перекрестка
        self.coordx = 0  # None
        self.coordy = 0  # None
        self.bonds = {}  # Имена перекрестко, связанных дорогами
        self.number_of_bonds = random.randint(2, 5)  # количество связанных перекрестков
        self.available_bonds = self.number_of_bonds  # Доступное количество связей
        self.met = -1
        self.was = False

    def point_drow(self):
        # Прорисовка точки перекрестка
        self.point = c.create_oval(self.coordx - self.RAD / 2, self.coordy - self.RAD / 2, self.coordx + self.RAD / 2,
                                   self.coordy + self.RAD / 2, fill="brown", tag="web")
        # Прорисовка имени перекрестка
        self.text = c.create_text(self.coordx, self.coordy - self.RAD * 1.5, text=self.name_of_point, fill="black",
                                  font="Verdana 10", tag="web")

    def point_print(self):  # Печать информации по перекрестку
        print("=====")
        print("Name: {}".format(self.name_of_point))
        print("Bonds: {}".format(self.bonds))
        print("Count of bonds: {}".format(self.number_of_bonds))
        print("Available bonds: {}".format(self.available_bonds))
        print("=====")


class Web:
    # new_dict = {}
    def __init__(self, value):  # Инициализация графа дорог

        self.value = value  # Количество перекрестков
        self.web = []  # Список, хранящий все точки перекрестков
        self.line_base = []  # Список, хранящий все дороги
        for i in range(0, self.value - 1):  # Заполнение списка перекрестков
            p = Point(i)
            self.web.append(p)
            del p
        #self.invalid_lines = {}
        self.graf = {}
        self.glen = 0
        # self.t = []  # список посещённых вершин
        # self.p = {}  # словарь {открытая вершина : её метка}
        # self.b = {}  # словарь для отслеживания короткого пути

    def web_init_random(self):  # Алгоритм случайной генерации графа дорог
        c.delete("web")
        #random.seed(random.randint(self.web[1].RAD * 3, WIDTH - self.web[1].RAD * 3))
        for j in range(0, self.value - 1):  # Проход по всем элементам
            self.web[j].coordx = random.randint(self.web[j].RAD * 3,
                                                WIDTH - self.web[j].RAD * 3)  # Случайные координаты по х и у
            self.web[j].coordy = random.randint(self.web[j].RAD * 3,
                                                HEIGHT - self.web[j].RAD * 3)  # Случайные координаты по х и у
            #self.web[j].number_of_bonds = random.randint(2, 5)  # количество связанных перекрестков
            for k in range(1, self.web[j].number_of_bonds + 1):  # Проход по количеству связей элемента
                if self.web[j].available_bonds > 0:  # Если остались доступные связи
                    num_buff = []  # Хранение попыток связи с другими перекрестками
                    while True:
                        number = random.randint(0, self.value - 2)  # Случайное имя перекрестка
                        if number not in num_buff:  # Если в буфере еще нет текущего имени, то добавить
                            num_buff.append(number)
                            if len(num_buff) >= self.value - 1:  # Если буфер переполен,
                                # то прервать цикл прохода по связям
                                break
                            else:
                                continue
                        # Если перекресток не пытается создать связь с самим
                        # собой, либо привязать себя к другому перекреску дважды
                        # и ели у него остались свободные связи, то связать перекрестки
                        if ((number != j) and (number not in self.web[j].bonds.keys()) and (
                                self.web[number].available_bonds > 0)):
                            if randomize(30):
                                rand = random.randint(100, 101)
                            else:
                                rand = random.randint(3, 10)
                            self.web[number].bonds[
                                j] = rand  # Добавление веса текущего связи
                            self.web[
                                number].available_bonds -= 1  # Уменьшение количества связей у случайно выбранного
                            # перекрестка на 1
                            self.web[j].bonds[
                                number] = rand  # Добавление имени случайно выбранного перекрестка
                            # в список связей текущего перекрестка
                            self.web[j].available_bonds -= 1  # Уменьшение количества связей у текущего перекрестка на 1
                            break
        for i in range(self.value - 1):
            self.graf[i] = self.web[i].bonds
        self.glen = len(self.web)
        #self.inv_lines()
        for l in self.graf:
            print(l, ':', self.graf[l])
        self.web_drow()


    def web_drow(self):  # Прорисовка сети дорог между перекрестками
        for l in range(0, self.value - 1):
            print(self.web[l].name_of_point, ':', self.web[l].bonds)
        for i in range(0, self.value - 1):  # Проход по всем перекресткам
            self.web[i].point_drow()
            for j in self.web[i].bonds.keys():  # Проход по всем связам перекрестка
                if self.web[i].bonds.get(j) >= 100:
                    line = c.create_line(self.web[i].coordx, self.web[i].coordy, self.web[j].coordx, self.web[j].coordy,
                                         fill='red', tag="web")
                else:
                    line = c.create_line(self.web[i].coordx, self.web[i].coordy, self.web[j].coordx, self.web[j].coordy,
                                         fill='green', tag="web")
                self.line_base.append(line)  # Добавить в список дорог
            #time.sleep(1)
            # self.web[i].point_print()

    def press_key(self, press):  #
        if press.keysym == "q":
            quit_prog()
        elif press.keysym == "h":
            c.delete("web")
            s = "g - генерация случайного графа дорог\n" \
                "f - поиск кратчайшего пути\n" \
                "h - помощь\n" \
                "q - выход"
            text = c.create_text(WIDTH / 2, HEIGHT / 2, text=s, fill="black",
                                      font="Verdana 20", tag="web")
        elif press.keysym == "g":
            self.web_init_random()
        elif press.keysym == "f":
            # print("Пожалуйста, введите имя начальной точки >: ")
            # self.start = input()
            # print("Пожалуйста, введите имя конечной точки >: ")
            # self.finish = input()
            dijkstra(self.graf, 0, 9, self.glen)


def randomize(percent):  # С заданной вероятностью (0-100%) выдает значение True
    i = random.randint(1, 101)
    if (i > 0) and (i < percent):
        return True
    else:
        return False


def quit_prog():
    quit()


W = Web(11)  # Инициализация точек (количество указано в скобках)
G = W.graf
N = W.glen
t = []  # список посещённых вершин
p = {}  # словарь {открытая вершина : её метка}
b = {}  # словарь для отслеживания короткого пути
s = []

def dijkstra_step(graf, v, p, t, b, e, N, s):
    #global s
    print('\n  Обходим всех соседей текущей вершины')
    # print(graf[v])
    for x in graf[v]:  # для каждого соседа (х) текущей вершины (v)
        xm = p[v] + graf[v][x]  # новая метка соседа (xm) =
        # метка текущей вершины (p[v]) +
        # значение ребра vx (G[v][x])

        if not x in p:  # если соседа (x) нет в словаре (p)
            p[x] = xm  # записываем новую метку (xm) в словарь с ключем (x)
            b[x] = v  # как только метка пересчитывается, запоминаем
            # (следующая вершина: предыдущая вершина) в словаре (b)
        elif not x in t:  # иначе если (x) не в (t)
            if p[x] > xm:  # если старая метка соседа больше новой метки
                p[x] = xm  # новую метку записываем на место старой
                b[x] = v  # как только метка пересчитывается, запоминаем
                # (следующая вершина: предыдущая вершина) в словаре (b)

        #print('текущей вершины v =', v, ' сосед x =', x, 'c меткой xm =', xm)

    #print('p =', p)

    #print('\n  Добавляем текущую вершину в список посещенных')
    t.append(v)
    #print('t =', t)
    #print(N)
    #print(len(t))
    if N <= len(t):  # Условие выхода из функции
        #print('\nВсё!\nВершины и их метки =', p)
        #print('Словарь для отслеживания пути =', b)

        #s = []  # кратчайший путь
        s.insert(0, e)  # вставляем (е) в список (s) по индексу (0)

        while True:
            if b[e] == -1:  # значение ключа (-1) имеет начальная вершина
                # вот её и ищем в словаре (b)
                print('Кратчайший путь от начальной до конечной вершины =', s)
                break  # выходим из цикла
            e = b[e]  # теперь последней вершиной будет предыдущая
            s.insert(0, e)  # вставляем (е) в список (s) по индексу (0)

        return 0

    #print('\n  Находим вершину с минимальной меткой за исключением тех, что уже в t')
    for d in p:  # вершина (d) с минимальной меткой из словаря (p)
        if d not in t:
            dm = p[d]  # метка вершины (d)
            break  # пусть это будет первая вершина из словаря (p)

    for y in p:  # для каждой вершины (y) из словаря (p)
        if p[y] < dm and not y in t:  # если метка вершины (y) <
            # метки вершины (d) & (y) нет в (t)
            dm = p[y]  # метку вершины (y) записываем в (dm)
            d = y  # вершину (y) записываем в (d)
            #print('Вершина y =', y, 'с меткой dm =', dm)

    #print('Вершина d =', d, 'имеет минимальную метку dm =', dm, \
    #      '\nтеперь текущей вершиной v будет вершина d')
    v = d  # теперь текущей вершиной v будет вершина d

   #print('\n  Рекурсивно вызываем функцию Дейкстры с параметрами v, p, t, b, e')
    dijkstra_step(graf, v, p, t, b, e, N, s)


def dijkstra(graf, start, end, N):
    global v, p, b, e, s
    s = []
    # print(graf)
    #for l in graf:
    #    print(l, ':', graf[l])
    if len(graf) > 0:
        v = start
        e = end
        p[v] = 0
        b[v] = -1
        print('\n Начальная текущая вершина v =', v)
        dijkstra_step(graf, v, p, t, b, e, N, s)
        print("Кратчайший путь {}".format(s))
        path = ""
        for cur in range(len(s) - 1):
            line = c.create_line(W.web[s[cur]].coordx - W.web[s[cur]].RAD / 3,
                                 W.web[s[cur]].coordy - W.web[s[cur]].RAD / 3,
                                 W.web[s[cur+1]].coordx - W.web[s[cur+1]].RAD / 3,
                                 W.web[s[cur+1]].coordy - W.web[s[cur+1]].RAD / 3,
                                 fill='blue', tag="web")
            path = path + str(W.web[s[cur]].name_of_point) + " -> "
        path = path + str(W.web[s[len(s) - 1]].name_of_point)
        text = c.create_text(len(path) * 5, HEIGHT - 15, text=path, fill="black",
                                  font="Verdana 10", tag="web")
    else:
        text = c.create_text(WIDTH / 2, HEIGHT / 2, text="Сначала требуется сгенерировать граф дорог!", fill="black",
                             font="Verdana 20", tag="web")

c.bind("<KeyPress>", W.press_key)

c.pack()  # Открытие окна
c.focus_set()  # Перемещает фокус на окно
root.mainloop()  # Запуск отображения окна в цикле