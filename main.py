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
