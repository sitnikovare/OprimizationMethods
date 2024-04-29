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

def bitwise_search_method(x, coord):
    alpha = 0.25
    eps = 0.01

    if coord == 1:
        # поиск по х1
        x_to_find = [x[0], x[1]]
        alpha_x = [x[0] + alpha, x[1]]
        f_x = func11(x_to_find)
        f_alpha_x = func11(alpha_x)
        while(abs(f_alpha_x - f_x) >= eps):
            if (f_alpha_x > f_x and alpha > 0) or (f_alpha_x > f_x and alpha < 0):
                if abs(alpha) < eps:
                    break
                alpha_x = [alpha_x[0] - alpha, x[1]]
                alpha /= -4
                alpha_x = [alpha_x[0] + alpha, x[1]]
                f_alpha_x = func11(alpha_x)
                continue
            f_x = f_alpha_x
            alpha_x = [alpha_x[0] + alpha, x[1]]
            f_alpha_x = func11(alpha_x)
        x1 = alpha_x[0] - alpha
        x2 = x[1]
    else:
        # поиск по х2
        x_to_find = [x[0], x[1]]
        alpha_x = [x[0], x[1] + alpha]
        f_x = func11(x_to_find)
        f_alpha_x = func11(alpha_x)
        while(abs(f_alpha_x - f_x) >= eps):
            if (f_alpha_x > f_x and alpha > 0) or (f_alpha_x > f_x and alpha < 0):
                if abs(alpha) < eps:
                    break
                alpha_x = [x[0], alpha_x[1] - alpha]
                alpha /= -4
                alpha_x = [x[0], alpha_x[1] + alpha]
                f_alpha_x = func11(alpha_x)
                continue
            f_x = f_alpha_x
            alpha_x = [x[0], alpha_x[1] + alpha]
            f_alpha_x = func11(alpha_x)
        x1 = x[0]
        x2 = alpha_x[1] - alpha
    return [x1, x2]

# расстояние между двумя точками
def p(x1, x2):
    return math.sqrt((x1[0] - x2[0]) * (x1[0] - x2[0]) + (x1[1] - x2[1]) * (x1[1] - x2[1]))
        

# Метод циклического покоординатного спуска
def cyclic_coordinate_descent(eps_x, eps_f, x):
    #--- Шаг 1
    f_x = func11(x)
    j = 1
    n = 2
    while(True):
        #--- Шаг 2. Решение задачи одномерной минимизации
        x_ = bitwise_search_method(x, j)
        f_ = func11(x_)
        #--- Шаг 3. Проверка условий
        if j < n:
            x = x_
            f_x = f_
            j += 1
            #--- Переход на Шаг 2 к решению задачи одномерной минимизации
            continue
        else:
            #--- Шаг 4. Проверка условия достижения точности
            if p(x, x_) < eps_x or abs(f_x - f_) < eps_f:
                # условие останова достигнуто
                x_min = x_
                f_min = f_
                break
            else:
                x = x_
                f_x = f_
                j = 1
    return x_min, f_min



#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    # критерий достижения точности по x
    eps_x = 0.001
    # критерий достижения точности по f
    eps_f = 0.001
    # начальная точка
    x = [-0.2, 2]
    
    x_min, f_min = cyclic_coordinate_descent(eps_x, eps_f, x)
    print(x_min, f_min)
    check_answer(x_min, f_min)