import matplotlib.pyplot as plt
import pandas as pd

# Твои данные (немного отличаются от его)
sizes = [10, 50, 100, 500, 1000]
times = [0.0002, 0.0016, 0.0131, 2.4512, 20.183]
operations = [1000, 125000, 1000000, 125000000, 1000000000]

# График 1: Зависимость времени от размера
plt.figure(figsize=(10, 5))
plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Размер матрицы (N)', fontsize=12)
plt.ylabel('Время вычисления (сек)', fontsize=12)
plt.title('Зависимость времени умножения матриц от размера', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('time_graph.png', dpi=150)
plt.show()

# График 2: Зависимость объёма задачи от размера
plt.figure(figsize=(10, 5))
plt.plot(sizes, [x/1e9 for x in operations], 'rs-', linewidth=2, markersize=8)
plt.xlabel('Размер матрицы (N)', fontsize=12)
plt.ylabel('Объём задачи (млрд операций)', fontsize=12)
plt.title('Зависимость объёма задачи от размера матрицы', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('operations_graph.png', dpi=150)
plt.show()

print("Графики сохранены как time_graph.png и operations_graph.png")