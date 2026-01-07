import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 10))

# Координаты узлов
warehouses = {'Склад 1': (2, 8), 'Склад 2': (2, 3)}
bases = {'Альфа': (10, 10), 'Бета': (10, 5.5), 'Гамма': (10, 1)}

# Рисуем склады (прямоугольники)
for name, (x, y) in warehouses.items():
    patch = FancyBboxPatch(
        (x - 0.8, y - 0.4), width=1.6, height=0.8,
        boxstyle="round, pad=0.1",
        facecolor="lightblue", edgecolor="black", linewidth=2
    )
    ax.add_patch(patch)
    ax.text(x, y, name, ha="center", va="center", fontsize=12, fontweight="bold")

# Рисуем базы (прямоугольники)
for name, (x, y) in bases.items():
    patch = FancyBboxPatch(
        (x - 0.6, y - 0.35), width=1.2, height=0.7,
        boxstyle="round, pad=0.1",
        facecolor="lightgreen", edgecolor="darkgreen", linewidth=2
    )
    ax.add_patch(patch)
    ax.text(x, y, f"База {name}", ha="center", va="center", fontsize=11, fontweight="bold")

# Оптимальные потоки (подставьте значения из решения linprog)
flows = [
    ('Склад 1', 'Альфа', 0, 8),
    ('Склад 1', 'Бета', 150, 6),
    ('Склад 1', 'Гамма', 0, 10),
    ('Склад 2', 'Альфа', 120, 9),
    ('Склад 2', 'Бета', 30, 7),
    ('Склад 2', 'Гамма', 100, 5)
]

# Рисуем потоки (стрелки)
for wh, base, volume, cost in flows:
    if volume > 0:  # Рисуем только ненулевые потоки
        x1, y1 = warehouses[wh]
        x2, y2 = bases[base]

        # Стрелка с толщиной, пропорциональной объёму
        arrow = FancyArrowPatch(
            (x1 + 0.8, y1), (x2 - 0.6, y2),
            arrowstyle='->', mutation_scale=20,
            lw=volume / 20,  # Толщина стрелки
            color='darkred', alpha=0.7
        )
        ax.add_patch(arrow)

        # Подпись объёма и стоимости
        mid_x = (x1 + 0.8 + x2 - 0.6) / 2
        mid_y = (y1 + y2) / 2
        ax.text(
            mid_x, mid_y, f"{volume} т\n({cost} у.е./т)",
            ha="center", va="bottom", fontsize=9,
            bbox=dict(facecolor="white", alpha=0.8, boxstyle="round,pad=0.3")
        )

# Оформление графика
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Оптимальный план снабжения военных баз', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.show()
