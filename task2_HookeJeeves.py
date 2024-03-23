import numpy as np
import math

# функция для 11 варианта
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

# получение случайного вектора и его нормы
def get_E():
    # вектор из двух случайных чисел из [0, 1)
    E = np.random.rand(2)
    # случайное домножение на -1
    E[0] = E[0] * np.random.choice([-1, 1])
    E[1] = E[1] * np.random.choice([-1, 1])
    # вычисление нормы
    norm = math.sqrt(E[0] * E[0] + E[1] * E[1])
    return E, norm

# метод покоординатного поиска
def coordinate_search(x, delta, e_basis):
    #--- Шаг 1. Задание параметров
    xc = x
    j = 0
    while(True):
        #--- Шаг 2. Пробный шаг и вычисление функции
        y = (xc[0] - delta[j] * e_basis[j][0], xc[1] - delta[j] * e_basis[j][1])
        f_xc = func11(xc)
        f_y = func11(y)
        # Проверка функции
        if f_xc <= f_y:
            #--- Шаг 3. Пробный шаг
            y = (xc[0] + delta[j] * e_basis[j][0], xc[1] + delta[j] * e_basis[j][1])
            f_y = func11(y)
            # Проверка функции
            if f_xc <= f_y:
                #--- Шаг 5.
                j += 1
                if j == len(e_basis):
                    return y
            else:
                #--- Шаг 4.
                xc = y
                #--- Шаг 5.
                j += 1
                if j == len(e_basis):
                    return y
        else:
            #--- Шаг 4.
            xc = y
            #--- Шаг 5.
            j += 1
            if j == len(e_basis):
                return y

# Метод Хука-Дживса
def hooke_jeeves(e_basis):
    #--- Шаг 1. Задание параметров
    # начальная точка
    x = (-0.2, 2)
    print(f"Начальная точка: x({x[0]}, {x[1]})")
    # dектор приращений
    delta, delta_n = get_E()
    print(f"delta = {delta}, ||delta|| = {delta_n}")
    # коэффициент приращения шага
    gamma = 1.5
    print(f"Коэффициент приращения шага: {gamma}")
    # параметр окончания поиска
    e = 0.05
    print(f"Параметр окончания поиска: {e}")
    while(True):
        #--- Шаг 2. Исследующий координатный поиск
        xc = coordinate_search(x, delta, e_basis)
        fc = func11(xc)
        # проверка
        if xc != x:
            #--- Шаг 4. Перемещение в направлении убывания
            xd = (2 * xc[0] - x[0], 2 * xc[1] - x[1])
            xe = coordinate_search(xd, delta, e_basis)
            fe = func11(xe)
            while (fe < fc):
                x = xc
                xc = xe
                fc = fe
                xd = (2 * xc[0] - x[0], 2 * xc[1] - x[1])
                xe = coordinate_search(xd, delta, e_basis)
                fe = func11(xe)
            else:
                #--- Шаг 3. Проверка окончания поиска
                if delta_n < e:
                    return xc
                else:
                    delta = [delta[0] / gamma, delta[1] / gamma]
                    delta_n = math.sqrt(delta[0] * delta[0] + delta[1] * delta[1])
                    #--- далее будет переход на Шаг 2
        else:
            #--- Шаг 3. Проверка окончания поиска
            if delta_n < e:
                return xc
            else:
                delta = [delta[0] / gamma, delta[1] / gamma]
                delta_n = math.sqrt(delta[0] * delta[0] + delta[1] * delta[1])
                #--- далее будет переход на Шаг 2

#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    # базисные векторы пространства
    e_basis = [[1, 0], [0, 1]]

    x_min = hooke_jeeves(e_basis)
    f_min = func11(x_min)

    check_answer(x_min, f_min)