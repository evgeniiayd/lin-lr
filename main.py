import numpy as np
from scipy.optimize import linprog
import json

# Загрузка данных из JSON
with open('data/problem_data.json', 'r') as f:
    data = json.load(f)

# 1.1 Математическая модель
# Переменные решения:
# x₁ — количество смартфонов
# x₂ — количество планшетов

# Целевая функция: максимизация прибыли
# P(x₁, x₂) = 8000x₁ + 12000x₂

# Ограничения:
# Процессорное время: 2x₁ + 3x₂ ≤ 240
# Оперативная память: 4x₁ + 6x₂ ≤ 480
# Аккумуляторы: x₁ + 2x₂ ≤ 150
# Неотрицательность: x₁ ≥ 0, x₂ ≥ 0

# 1.3 Решение на Python
# Коэффициенты целевой функции (для минимизации берём с минусом)
c = [-data['profit']['smartphone'], -data['profit']['tablet']]

# Матрица ограничений A_ub @ x <= b_ub
A_ub = [
    [data['resources']['processor_time']['smartphone'], data['resources']['processor_time']['tablet']],  # процессор
    [data['resources']['ram']['smartphone'], data['resources']['ram']['tablet']],  # память
    [data['resources']['batteries']['smartphone'], data['resources']['batteries']['tablet']]  # аккумуляторы
]

# Вектор правых частей
b_ub = [
    data['resources']['processor_time']['total'],
    data['resources']['ram']['total'],
    data['resources']['batteries']['total']
]

# Границы переменных (неотрицательность)
bounds = [(0, None), (0, None)]

# Решение задачи
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

# Вывод результатов
print("=== Задача оптимизации производства электроники ===")
print(f"!Статус: {result.message}")

if result.success:
    x1_opt = round(result.x[0])  # смартфоны
    x2_opt = round(result.x[1])  # планшеты
    max_profit = -round(result.fun)  # максимальная прибыль

    print(f"Оптимальное количество смартфонов: {x1_opt} шт.")
    print(f"Оптимальное количество планшетов: {x2_opt} шт.")
    print(f"Максимальная прибыль: {max_profit} руб.")

    # Анализ использования ресурсов
    print("\n--- Анализ использования ресурсов ---")
    cpu_used = 2 * x1_opt + 3 * x2_opt
    ram_used = 4 * x1_opt + 6 * x2_opt
    batt_used = x1_opt + 2 * x2_opt

    print(f"Процессорное время: использовано {cpu_used}/{b_ub[0]} часов ({cpu_used / b_ub[0] * 100:.1f}%)")
    print(f"Оперативная память: использовано {ram_used}/{b_ub[1]} ГБ ({ram_used / b_ub[1] * 100:.1f}%)")
    print(f"Аккумуляторы: использовано {batt_used}/{b_ub[2]} шт. ({batt_used / b_ub[2] * 100:.1f}%)")
else:
    print("Решение не найдено!")



import numpy as np
from scipy.optimize import linprog

# Целевая функция: минимизировать транспортные расходы
# Переменные: [x_11, x_12, x_13, x_21, x_22, x_23]
c = [8, 6, 10, 9, 7, 5]

# Ограничения-равенства A_eq @ x = b_eq
A_eq = [
    [1, 1, 1, 0, 0, 0],  # Склад 1: x_11 + x_12 + x_13 = 150
    [0, 0, 0, 1, 1, 1],  # Склад 2: x_21 + x_22 + x_23 = 250
    [1, 0, 0, 1, 0, 0],  # База Альфа: x_11 + x_21 = 120
    [0, 1, 0, 0, 1, 0],  # База Бета: x_12 + x_22 = 180
    [0, 0, 1, 0, 0, 1]   # База Гамма: x_13 + x_23 = 100
]
b_eq = [150, 250, 120, 180, 100]

# Границы переменных (все >= 0)
bounds = [(0, None) for _ in range(6)]

# Решение задачи
result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# Вывод результатов
print("=== Транспортная задача снабжения военных баз ===")
print(f"Статус: {result.message}")

if result.success:
    x = result.x
    x_11, x_12, x_13, x_21, x_22, x_23 = map(round, x)
    total_cost = round(result.fun)

    print(f"Оптимальный план перевозок:")
    print(f"  Склад 1 → Альфа: {x_11} т")
    print(f"  Склад 1 → Бета:  {x_12} т")
    print(f"  Склад 1 → Гамма: {x_13} т")
    print(f"  Склад 2 → Альфа: {x_21} т")
    print(f"  Склад 2 → Бета:  {x_22} т")
    print(f"  Склад 2 → Гамма: {x_23} т")
    print(f"Минимальная стоимость транспортировки: {total_cost} усл. ед.")
else:
    print("Решение не найдено!")
