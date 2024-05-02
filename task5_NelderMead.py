import numpy as np
import math


def func11(x):
    return 76 * x[0] * x[0] - 141 * x[0] * x[1] + 76 * x[1] * x[1] - 17 * x[0] + 49 * x[1] + 14

# функция для проверки,
# ответ получен с помощью нахождения производных 
# и решения системы уравнений
def check_answer(x, fx):
    z = (- 4325 / 32223, - 5051 / 3223)
    fz = - 41865 / 3223
    print(f"Приблизительный ответ:\n\tточка минимума z({z[0]}, {z[1]})\n\tf(z) = {fz}")
    print(f"Ответ, полученный программой:\n\tточка минимума x({x[0]}, {x[1]})\n\tf(x) = {fx}")
    print(f"Погрешность: |f(x) - f(z)| = {abs(fx - fz)}")
    
# функция для соритровки симплекса
# согласно правильной нумерации
def sort_by_func_value(input):
    return func11(input)

# Функция построения симплекса
# x - заданная базовая точка, 
# l - длина ребра, 
# n - количество точек симплекса
# возвращает n точек построенного симплекса
def build_simplex(x, l, n):
    # массив, содержащий точки симплекса
    simplex = [x]
    n_rest = n - 1
    for i in range(2, n_rest + 2):
        xi = [0, 0]
        for j in range (1, n_rest + 1):
            if i == j + 1:
                xi[j-1] = x[0] + (math.sqrt(n_rest + 1) - 1) / (n_rest * math.sqrt(2)) * l
            else:
                xi[j-1] = x[1] + (math.sqrt(n_rest + 1) + n_rest - 1) / (n_rest * math.sqrt(2)) * l
        simplex.append(xi)
    # сортировка для правильной нумерации вершин
    simplex.sort(key=sort_by_func_value, reverse=True)
    return simplex

# получение середины отрезка между первыми двумя точками в симплексе
def get_middle(simplex):
    x1 = 0
    x2 = 0
    n = len(simplex)
    for x in simplex:
        x1 += x[0]
        x2 += x[1]
    return [x1 / n, x2 / n]

# операция отражения худшей точки
def reflect(simplex, xc, alpha):
    xh = simplex[0]
    return [(1 + alpha) * xc[0] - alpha * xh[0], (1 + alpha) * xc[1] - alpha * xh[1]]

# операция растяжения
def extention(xr, ghamma):
    return [(1 + ghamma) * xr[0] + alpha * xr[0], (1 + ghamma) * xr[1] + alpha * xr[1]]

# операция сжатия
def contraction(xh, xc, beta):
    return [beta * xh[0] + (1 - beta) * xc[0], beta * xh[0] + (1 - beta) * xc[0]]

# обновление симплекса после отражения вершины
def update_simplex(x_add, simplex):
    # удаление отраженной вершины из симплекса
    simplex.remove(simplex[-1])
    # добавление отражения вершины в симплекс
    simplex.append(x_add)
    # соритровка симплкса
    simplex.sort(key=sort_by_func_value, reverse=True)
    return simplex

# вычисления значения для проверки услоавия останова
def stop_criteria(simplex):
    x0 = simplex[0]
    f_x0 = func11(x0)
    simplex_sum = 0
    for xs in simplex:
        simplex_sum += (func11(xs) - f_x0) * (func11(xs) - f_x0)
    return 1 / (len(simplex)) * simplex_sum

# редукция симплекса
def simplex_reduction(simplex, delta, l):
    l *= delta
    # точка симплекса с наименьшим значением функции
    xk1 = simplex[-1]
    new_simplex = [xk1]
    for x in simplex[:len(simplex)-1]:
        x1_new = xk1[0] + delta * (x[0] - xk1[0])
        x2_new = xk1[1] + delta * (x[1] - xk1[1])
        new_simplex.append([x1_new, x2_new])
    new_simplex.sort(key=sort_by_func_value, reverse=True)
    print(f"--- Произведена редукция симплекса, новая длина ребра: {l}")
    return new_simplex, l

def nelder_mead(n, l, l_min, eps, x, max_iter, alpha, beta, ghamma, delta):
    # построение симлекса
    simplex = build_simplex(x, l, n)
    print(f"Построен симплекс: {simplex}")
    iteration = 0
    while(True):
        iteration += 1
        if stop_criteria(simplex) < eps * eps  or max_iter == iteration or l < l_min:
            print("Достигнут критерий останова")
            break
        # точка с наибольшим значением функции
        xh = simplex[0]
        # центр тяжести
        xc = get_middle(simplex)
        # отражение точки
        xr = reflect(simplex, xc, alpha)
        # значение функции в отраженной точке
        f_xr = func11(xr)
        # наименьшее значение функции по симплексу
        f_xl = func11(simplex[-1])
        # среднее значение функции по симплексу
        f_xg = func11(simplex[1])
        # наибольшее значение функции по симплексу
        f_xh = func11(simplex[0])
        # можно попробовать растяжение
        if f_xr < f_xl:
            # точка, полученная с помощью операции растяжения
            xe = extention(xr, ghamma)
            # значение функции в этой точке
            f_xe = func11(xe)
            # можно попробовать обновить симплекс
            if f_xe < f_xr:
                simplex = update_simplex(xe, simplex)
                print(f"Симплекс обновлен точкой растяжения: {simplex}")
                continue
            # иначе переместились слишком далеко
            else:
                # обновление симплекса
                simplex = update_simplex(xr, simplex)
                print(f"Симплекс обновлен точкой отражения, f_xe >= f_xr: {simplex}")
                continue
        # новая точка лучше двух прежних
        elif f_xl < f_xr and f_xr < f_xg:
            # обновление симплекса
            simplex = update_simplex(xr, simplex)
            print(f"Симплекс обновлен точкой отражения, f_xl < f_xr and f_xr < f_xg: {simplex}")
            continue
        # заменяем xh на xr
        elif f_xg < f_xr and f_xr < f_xh:
            # обновление симплекса
            simplex = update_simplex(xr, simplex)
            print(f"Симплекс обновлен точкой отражения, f_xg < f_xr and f_xr < f_xh: {simplex}")
            # примение операции сжатия
            xs = contraction(xh, xc, beta)
            f_xs = func11(xs)
            # проверяем точки после сжатия
            if f_xs < f_xh:
                # обновление симплекса точкой сжатия
                simplex = update_simplex(xs, simplex)
                print(f"Симплекс обновлен точкой сжатия: {simplex}")
                continue
        simplex, l = simplex_reduction(simplex, delta, l)
        print(f"Симплекс редуцирован: {simplex}")
    # точка минимума функции
    x_min = simplex[-1]
    # значение функции в точке минимума
    f_min = func11(x_min)
    print(f"Количество итераций: {iteration}")
    return x_min, f_min


#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    # количество точек симплекса
    n = 3
    # длина ребра симплекса
    l = 2
    # минимальная длина ребра
    l_min = 0.001
    # погрешность измерения
    eps = 0.0001
    # максимальное количество итераций
    max_iter = 1000
    # начальная точка
    x = [-0.2, 2]
    # коэффициент отражения
    alpha = 1
    # коэффициент сжатия
    beta = 0.5
    # коэффициент отражения
    ghamma = 2
    # коэффициент редукции симплекса
    delta = 0.5
    
    x_min, f_min = nelder_mead(n, l, l_min, eps, x, max_iter, alpha, beta, ghamma, delta)
    check_answer(x_min, f_min)