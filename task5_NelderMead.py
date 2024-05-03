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
def build_simplex():
    # массив, содержащий точки симплекса
    simplex = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]
    simplex.sort(key=sort_by_func_value)
    return simplex

# Функция построения симплекса
# x - заданная базовая точка, 
# l - длина ребра, 
# n - количество точек симплекса
# возвращает n точек построенного симплекса
# def build_simplex(x=[0.0, 0.0], l=2, n=3):
#     # массив, содержащий точки симплекса
#     simplex = [x]
#     n_rest = n - 1
#     for i in range(2, n_rest + 2):
#         xi = [0, 0]
#         for j in range (1, n_rest + 1):
#             if i == j + 1:
#                 xi[j-1] = x[0] + (math.sqrt(n_rest + 1) - 1) / (n_rest * math.sqrt(2)) * l
#             else:
#                 xi[j-1] = x[1] + (math.sqrt(n_rest + 1) + n_rest - 1) / (n_rest * math.sqrt(2)) * l
#         simplex.append(xi)
#     # сортировка для правильной нумерации вершин
#     simplex.sort(key=sort_by_func_value, reverse=True)
#     return simplex

# получение середины отрезка между первыми двумя точками в симплексе
def get_middle(simplex):
    return [simplex[0][0] + simplex[1][0] / 2, simplex[0][1] + simplex[1][1] / 2]

# получение середины отрезка
def get_center(a, b):
    return [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]

# операция отражения точки
def reflect(mid, alpha, w):
    return [mid[0] + alpha * (mid[0] - w[0]), mid[1] + alpha * (mid[1] - w[1])]

# операция растяжения
def extention(mid, gamma, xr):
    return [mid[0] + gamma * (xr[0] - mid[0]), mid[1] + gamma * (xr[1] - mid[1])]

# операция сжатия
def contraction(mid, beta, w):
    return [mid[0] + beta * (w[0] - mid[0]), mid[1] + beta * (w[1] - mid[1])]

def nelder_mead(alpha, beta, ghamma, maxiter):
    # построение симлекса
    simplex = build_simplex()
    print(f"Построен симплекс: {simplex}")

    for _ in range(maxiter):
        # переобозначение точек симплекса
        b = simplex[0]
        g = simplex[1]
        w = simplex[2]
        # получение середины отрезка между двумя лучшими точками симплекса
        mid = get_center(g, b)
        # отражение точки симплекса
        xr = reflect(mid, alpha, w)
        # проверка для замены точек
        if func11(xr) < func11(g):
            w = xr
        else:
            if func11(xr) < func11(w):
                w = xr
            c = get_center(w, mid)
            if func11(c) < func11(w):
                w = c
        if func11(xr) < func11(b):
            # растяжение
            xe = extention(mid, ghamma, xr)
            if func11(xe) < func11(xr):
                w = xe
            else:
                w = xr
        if func11(xr) > func11(g):
            # сжатие
            xc = contraction(mid, beta, w)
            if func11(xc) < func11(w):
                w = xc
        simplex = [w, g, b]
        print(f"Cимплекс обновлен {simplex}")
        simplex.sort(key=sort_by_func_value)

    # точка минимума функции
    x_min = simplex[-1]
    # значение функции в точке минимума
    f_min = func11(x_min)
    return x_min, f_min


#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    # коэффициент отражения
    alpha = 1
    # коэффициент сжатия
    beta = 0.5
    # коэффициент отражения
    ghamma = 2
    # коэффициент редукции симплекса
    delta = 0.5
    # максимальное количество итераций
    maxiter = 50
    
    x_min, f_min = nelder_mead(alpha, beta, ghamma, maxiter)
    check_answer(x_min, f_min)