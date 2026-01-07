import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Входные данные (можно импортировать из main.py, но для автономности повторяем)
RESOURCES = {
    'processor_time': {'smartphone': 2, 'tablet': 3, 'total': 240},
    'ram': {'smartphone': 4, 'tablet': 6, 'total': 480},
    'batteries': {'smartphone': 1, 'tablet': 2, 'total': 150}
}

PROFIT = {'smartphone': 8000, 'tablet': 12000}

# Оптимальное решение (из результатов main.py)
X1_OPT = 30  # смартфоны
X2_OPT = 60  # планшеты
MAX_PROFIT = 960000


def get_constraint_line(resource, x1_range):
    """Возвращает значения x2 для ограничения по ресурсу"""
    a = RESOURCES[resource]['smartphone']
    b = RESOURCES[resource]['tablet']
    total = RESOURCES[resource]['total']
    return (total - a * x1_range) / b


def find_intersection(res1, res2):
    """Находит точку пересечения двух ограничений"""
    a1, b1 = RESOURCES[res1]['smartphone'], RESOURCES[res1]['tablet']
    a2, b2 = RESOURCES[res2]['smartphone'], RESOURCES[res2]['tablet']
    c1, c2 = RESOURCES[res1]['total'], RESOURCES[res2]['total']

    # Решаем систему: a1*x1 + b1*x2 = c1; a2*x1 + b2*x2 = c2
    A = np.array([[a1, b1], [a2, b2]])
    B = np.array([c1, c2])
    try:
        return np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        return None


# Подготовка данных для визуализации
x1_range = np.linspace(0, 100, 400)

# Вычисляем линии ограничений
x2_cpu = get_constraint_line('processor_time', x1_range)
x2_ram = get_constraint_line('ram', x1_range)
x2_bat = get_constraint_line('batteries', x1_range)

# Находим вершины допустимой области
vertices = []

# Пересечения пар ограничений
for res1, res2 in [('processor_time', 'ram'),
                   ('processor_time', 'batteries'),
                   ('ram', 'batteries')]:
    point = find_intersection(res1, res2)
    if point is not None and all(point >= 0):
        vertices.append(point)

# Точки на осях (где одна из переменных = 0)
vertices.append([0, min(RESOURCES['processor_time']['total'] / RESOURCES['processor_time']['tablet'],
                        RESOURCES['ram']['total'] / RESOURCES['ram']['tablet'],
                        RESOURCES['batteries']['total'] / RESOURCES['batteries']['tablet'])])
vertices.append([min(RESOURCES['processor_time']['total'] / RESOURCES['processor_time']['smartphone'],
                     RESOURCES['ram']['total'] / RESOURCES['ram']['smartphone'],
                     RESOURCES['batteries']['total'] / RESOURCES['batteries']['smartphone']), 0])

# Фильтруем точки, которые удовлетворяют всем ограничениям
valid_vertices = []
for point in vertices:
    x1, x2 = point
    if (2 * x1 + 3 * x2 <= 240 and
            4 * x1 + 6 * x2 <= 480 and
            x1 + 2 * x2 <= 150 and
            x1 >= 0 and x2 >= 0):
        valid_vertices.append(point)

# Сортируем вершины по углу для правильного построения многоугольника
valid_vertices = np.array(valid_vertices)
center = np.mean(valid_vertices, axis=0)
angles = np.arctan2(valid_vertices[:, 1] - center[1],
                    valid_vertices[:, 0] - center[0])
valid_vertices = valid_vertices[np.argsort(angles)]

# Создаём график
fig, ax = plt.subplots(figsize=(12, 10))

# Рисуем линии ограничений
ax.plot(x1_range, x2_cpu, 'r-', linewidth=2, label='Процессорное время (240 ч)')
ax.plot(x1_range, x2_ram, 'g-', linewidth=2, label='Оперативная память (480 ГБ)')
ax.plot(x1_range, x2_bat, 'b-', linewidth=2, label='Аккумуляторы (150 шт.)')

# Закрашиваем допустимую область
polygon = Polygon(valid_vertices, closed=True, facecolor='lightblue',
                  edgecolor='blue', alpha=0.5, label='Допустимая область')
ax.add_patch(polygon)

# Отмечаем оптимальное решение
ax.plot(X1_OPT, X2_OPT, 'ro', markersize=10, label=f'Оптимальное решение\n({X1_OPT}, {X2_OPT})')
ax.annotate(f'Прибыль: {MAX_PROFIT} руб.',
            xy=(X1_OPT, X2_OPT), xytext=(X1_OPT + 5, X2_OPT + 3),
            arrowprops=dict(arrowstyle='->', color='red'), fontsize=12)

# Линии уровня целевой функции (изопрофиты)
profit_levels = [600000, 720000, 840000, 960000]
for level in profit_levels:
    x2_iso = (level - PROFIT['smartphone'] * x1_range) / PROFIT['tablet']
    ax.plot(x1_range, x2_iso, 'k--', alpha=0.7, linewidth=1)
    # Подпись уровня
    if level == 960000:
        ax.text(x1_range[-1] - 10, x2_iso[-1] + 2, f'{level // 1000} тыс. руб.',
                color='black', fontsize=10)

# Оформление графика
ax.set_xlabel('Количество смартфонов ($x_1$)', fontsize=14)
ax.set_ylabel('Количество планшетов ($x_2$)', fontsize=14)
ax.set_title('Задача оптимизации производства электроники\nГеометрическое представление',
             fontsize=16, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 80)
ax.set_ylim(0, 80)

# Добавляем подписи к ограничениям
ax.text(70, 50, 'Недопустимая\nобласть', fontsize=12, color='red',
        bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()

# Дополнительная информация
print("=== Визуализация задачи оптимизации ===")
print(f"Вершины допустимой области: {valid_vertices}")
print(f"Оптимальное решение: x₁={X1_OPT}, x₂={X2_OPT}")
print(f"Максимальная прибыль: {MAX_PROFIT} руб.")
