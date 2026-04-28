import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('stats_mpi.csv')

sizes = df['Size'].unique()
processes = sorted(df['Processes'].unique())


plt.figure(figsize=(12, 6))
for size in sizes:
    data = df[df['Size'] == size]
    plt.plot(data['Processes'], data['Time_sec'], 'o-', linewidth=2, markersize=8, label=f'{size}x{size}')
plt.xlabel('Количество процессов', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.title('MPI: зависимость времени от количества процессов', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('mpi_time_graph.png', dpi=150)
plt.show()


plt.figure(figsize=(12, 6))
for size in sizes:
    data = df[df['Size'] == size].sort_values('Processes')
    base_time = data[data['Processes'] == 1]['Time_sec'].values[0]
    speedups = [base_time / t for t in data['Time_sec']]
    plt.plot(data['Processes'], speedups, 's-', linewidth=2, markersize=8, label=f'{size}x{size}')

plt.plot([1, max(processes)], [1, max(processes)], 'k--', alpha=0.5, label='Идеальное ускорение')
plt.xlabel('Количество процессов', fontsize=12)
plt.ylabel('Ускорение (Speedup)', fontsize=12)
plt.title('MPI: ускорение при параллельном умножении матриц', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('mpi_speedup_graph.png', dpi=150)
plt.show()

print("Графики сохранены: mpi_time_graph.png, mpi_speedup_graph.png")