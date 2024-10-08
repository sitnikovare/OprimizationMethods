import numpy as np
import math

# функция для 11 варианта
def func11(x):
    return 76 * x[0] * x[0] - 141 * x[0] * x[1] + 76 * x[1] * x[1] - 17 * x[0] + 49 * x[1] + 14

# функция для проверки,
# ответ получен с помощью нахождения производных 
# и решения системы уравнений
def checkAnswer(x, fx):
    z = (- 4325 / 32223, - 5051 / 3223)
    fz = - 41865 / 3223
    print(f"\nПриблизительный ответ:\n\tточка минимума z({z[0]}, {z[1]})\n\tf(z) = {fz}")
    print(f"Ответ, полученный программой:\n\tточка минимума x({x[0]}, {x[1]})\n\tf(x) = {fx}")
    print(f"Погрешность: |f(x) - f(z)| = {abs(fx - fz)}")

# получение случайного вектора и его нормы
def getE():
    # вектор из двух случайных чисел из [0, 1)
    E = np.random.rand(2)
    # случайное домножение на -1
    E[0] = E[0] * np.random.choice([-1, 1])
    E[1] = E[1] * np.random.choice([-1, 1])
    # вычисление нормы
    norm = math.sqrt(E[0] * E[0] + E[1] * E[1])
    return E, norm

# получение пробной точки y 
def probY(x, a, E, normE):
    y1 = x[0] + a * E[0] / normE
    y2 = x[1] + a * E[1] / normE
    return (y1, y2) 

#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    #--- Шаг 1. Задание параметров
    # начальная точка
    x = (-0.2, 2)
    # параметр точности
    e = 0.05
    # начальный шаг
    a = 1.0
    # коэффициент уменьшения шага
    ghamma = 1.5
    # количество попыток
    M = 5
    # вычисление f(x) для начальной точки
    fx = func11(x)

    print("--- Шаг 1. Задание параметров ---")
    print(f"Начальная точка: x({x[0]}, {x[1]})")
    print(f"Параметр точности: e = {e}")
    print(f"Начальный шаг: a = {a}")
    print(f"Коэффициент уменьшения шага: {ghamma}")
    print(f"Максимальное количество неудачных попыток: M = {M}")
    print(f"f(x) для начальной точки ({x[0]}, {x[1]}): {fx}")

    #--- Шаг 2. Cчетчик неудачных попыток
    j = 1
    print(f"--- Шаг 2. Обновлен счетчик неудачных попыток: j = {j} ---")

    #--- Шаг 3. Случайный вектор из двух величин, 
    # равномерно распределенных на отрезке [-1, 1]
    E, normE = getE()
    print(f"--- Шаг 3. Обновлен случайный вектор: E = ({E[0]}, {E[1]}) ---")

    while(True):
        #--- Шаг 4. Получение пробной точки y и вычисление f(y)
        y = probY(x, a, E, normE)
        fy = func11(y)
        print(f"--- Шаг 4. Пробный y = ({y[0]}, {y[1]}), f(y) = {fy} ---")

        #--- Шаг 5. Проверка пробы
        if fy < fx:
            x = y
            fx = fy
            print(f"--- Шаг 5. Обновление x = ({x[0]}, {x[1]}), f(x) = {fx} ---")
            # --- далее будет переход на шаг 4
        else:
            #--- Шаг 6. Увеличение количества неудачных попыток
            j += 1
            print(f"--- Шаг 6. Обновлен счетчик неудачных попыток: j = {j} ---")
            if j <= M:
                #--- Шаг 3. Получение нового случайного вектора из двух величин
                E, normE = getE()
                print(f"--- Шаг 3. Обновлен случайный вектор: E = ({E[0]}, {E[1]}) ---")
                # --- далее будет переход на шаг 4
            else:
                #--- Шаг 7. Проверка критерия завершения поиска
                if a < e:
                    print(f"--- Шаг 7. Достигнуто условие выхода: a = {a} < e = {e}.")
                    print(f"--- Результат. Минимум функции: x = ({x[0]}, {x[1]}), f(x) = {fx}")
                    #--- выход из цикла 
                    break
                else: 
                    a = a / ghamma
                    print(f"--- Шаг 7. Обновлено значение: a = {a}")
                    #--- Шаг 2. Cчетчик неудачных попыток
                    j = 1
                    print(f"--- Шаг 2. Обновлен счетчик неудачных попыток: j = {j} ---")
                    #--- Шаг 3. Получение нового случайного вектора из двух величин
                    E, normE = getE()
                    print(f"--- Шаг 3. Обновлен случайный вектор: E = ({E[0]}, {E[1]}) ---")
                    # --- далее будет переход на шаг 4
    checkAnswer(x, fx)