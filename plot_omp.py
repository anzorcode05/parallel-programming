import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('stats_omp.csv')

sizes = df['Size'].unique()
threads = sorted(df['Threads'].unique())

# График 1: Время от количества потоков
plt.figure(figsize=(12, 6))
for size in sizes:
    data = df[df['Size'] == size]
    plt.plot(data['Threads'], data['Time_sec'], 'o-', linewidth=2, markersize=8, label=f'{size}x{size}')
plt.xlabel('Количество потоков', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.title('Зависимость времени от количества потоков', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('omp_time_graph.png', dpi=150)
plt.show()

# Вычисляем ускорение
plt.figure(figsize=(12, 6))
for size in sizes:
    data = df[df['Size'] == size].sort_values('Threads')
    base_time = data[data['Threads'] == 1]['Time_sec'].values[0]
    speedups = [base_time / t for t in data['Time_sec']]
    plt.plot(data['Threads'], speedups, 's-', linewidth=2, markersize=8, label=f'{size}x{size}')

plt.plot([1, max(threads)], [1, max(threads)], 'k--', alpha=0.5, label='Идеальное ускорение')
plt.xlabel('Количество потоков', fontsize=12)
plt.ylabel('Ускорение (Speedup)', fontsize=12)
plt.title('Ускорение при параллельном умножении матриц', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('omp_speedup_graph.png', dpi=150)
plt.show()

print("Графики сохранены: omp_time_graph.png, omp_speedup_graph.png")