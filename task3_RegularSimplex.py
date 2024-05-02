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

# поиск симметричной точки
def get_symmetric_point(simplex, max_point=0):
    x_max_point = simplex[max_point]
    sum_x1_sym = 0
    sum_x2_sym = 0
    for x in simplex[1:]:
        sum_x1_sym += x[0]
        sum_x2_sym += x[1]
    n2 = 2 / (len(simplex) - 1)
    return [n2 * sum_x1_sym - x_max_point[0], n2 * sum_x2_sym - x_max_point[1]]    

# обновление симплекса после отражения вершины
def update_simplex(x_add, simplex):
    # удаление отраженной вершины из симплекса
    simplex.remove(simplex[0])
    # добавление отражения вершины в симплекс
    simplex.append(x_add)
    # соритровка симплкса
    simplex.sort(key=sort_by_func_value, reverse=True)
    return simplex

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

# вычисления значения для проверки услоавия останова
def stop_criteria(simplex, x0):
    f_x0 = func11(x0)
    simplex_sum = 0
    for xs in simplex:
        simplex_sum += (func11(xs) - f_x0) * (func11(xs) - f_x0)
    return 1 / (len(simplex)) * simplex_sum

# Минимизация по методу правильного симплекса
def regular_simplex(n, l, l_min, eps, x, delta):
    # построение симлекса
    simplex = build_simplex(x, l, n)
    print(f"Построен симплекс: {simplex}")
    # отражение вершины
    x_sym = get_symmetric_point(simplex)
    x = simplex[0]
    # индекс точки для отражения
    max_point = 0
    # счетчик итерации
    iter_count = 0
    while(l > l_min):
        # обновление счетчика итераций
        iter_count += 1
        # проверка условия останова
        f_sym = func11(x_sym)
        f_x = func11(x)
        stop_check = stop_criteria(simplex, x)
        if stop_check < eps * eps:
            print(f"Достигнут критерий останова по eps: {stop_check} < {eps}")
            break
        # проверка условия останова
        if f_sym < f_x:
            # обновление симплекса
            simplex = update_simplex(x_sym, simplex)
            print(f"Вершины симплекса обновлены: {simplex}")
            x = simplex[0]
            # индекс точки для отражения
            max_point = 0
            # обновление точки x 
            x_sym = get_symmetric_point(simplex, max_point)
        else:
            simplex, l = simplex_reduction(simplex, delta, l)
            print(f"Симплекс редуцирован: {simplex}")
            # отражение другой вершины
            if max_point < len(simplex):
                x_sym = get_symmetric_point(simplex, max_point)
                x = simplex[max_point]
    f_min = func11(x_sym)
    print(f"Количество произведенных итераций: {iter_count}")
    return simplex[-1], f_min


#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    # количество точек симплекса
    n = 3
    # длина ребра симплекса
    l = 2
    # минимальная длина ребра
    l_min = 0.0001
    # погрешность измерения
    eps = 0.0001
    # коэффициент редукции симплекса
    delta = 0.5
    # начальная точка
    x = [-0.2, 2]
    
    x_min, f_min = regular_simplex(n, l, l_min, eps, x, delta)
    check_answer(x_min, f_min)