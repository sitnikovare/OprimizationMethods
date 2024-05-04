import matplotlib.pyplot as plt
import numpy as np

#  функция, максимальное значение которой нужно найти
def z_with_arg(x1, z):
    return 3 / 2 * x1 + z / 2

def z(x1, x2):
    return 3 * x1 + 2 * x2

# первое ограничение
def ogr1(x1):
    return 8 / 3 - 2 / 3 * x1

# второе ограничение
def ogr2(x1):
    return 4 - 2 * x1

# третье ограничение
def ogr3(x1):
    return 1 + 2 * x1

# получение двух точек для построения прямых
def get_points():
    z_arg = 2.75
    ogr1_points = [ogr1(0), ogr1(1)]
    ogr2_points = [ogr2(0), ogr2(1)]
    ogr3_points = [ogr3(0), ogr3(1)]
    z_points = [z_with_arg(0, z_arg), z_with_arg(1, z_arg)]
    return np.array(ogr1_points), np.array(ogr2_points), np.array(ogr3_points), np.array(z_points)

#  поиск пересечения двух функций
def find_corner(f1, f2, step):
    # поиск точки пересечения двух графиков с указанным шагом
    x1 = 0
    eps = 0.01
    while (abs(f1(x1) - f2(x1)) > eps):
        x2 = f1(x1)
        x1 += step
    x2 = f1(x1)
    return [x1, x2]

# поиск границ многоугольника решений
def get_corners():
    corner_o1o2 = find_corner(ogr1, ogr2, 0.2)
    corner_o1o3 = find_corner(ogr1, ogr3, 0.025)
    corner_o2o3 = find_corner(ogr2, ogr3, 0.25)
    return corner_o1o2, corner_o1o3, corner_o2o3


#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    # получение точек, необходимых для отрисовки графиков
    o1_p, o2_p, o3_p, z_p = get_points()
    # отрисовка прямых
    plt.plot(o1_p, label='2x1 + 3x2 = 8', color='g')
    plt.plot(o2_p, label='2x1 + x2 = 4', color='b')
    plt.plot(o3_p, label='-2x1 + x2 = 1', color='y')
    plt.plot(z_p, label='(z) 2.75 = 3x1 + 2x2', color='r', linestyle='--')
    
    c_o1o2, c_o1o3, c_o2o3 = get_corners()
    print(f"Границы многоугольника решений:")
    print(f"\tпересечение o1_o2 (зеленая и синяя прямые): {c_o1o2}")
    print(f"\tпересечение o1_o3 (зеленая и желтая прямые): {c_o1o3}")
    print(f"\tпересечение o2_o3 (синяя и желтая прямые): {c_o2o3}")

    print("Значения функции z в этих точках:")
    c_points = np.array([c_o1o2, c_o1o3, c_o2o3])
    z_points = []
    # вычисление значения функции на границах
    for c in c_points:
        z_c = z(c[0], c[1])
        z_points.append(z_c)
        print(f"\tz({c[0]}, {c[1]}) = {z_c}")
    # индекс максимального элемента
    z_points = np.array(z_points)
    z_max_idx = np.argmax(z_points)
    c_max = c_points[z_max_idx]
    print(f"Функция принимает максимальное значение {z_points[z_max_idx]} в точке ({c_max[0]}, {c_max[1]})")

    #  добавление легенды на график
    plt.legend()
    # добавление названий осей на график
    plt.xlabel('x1')
    plt.ylabel('x2')
    # отрисовка финального графика
    plt.show()