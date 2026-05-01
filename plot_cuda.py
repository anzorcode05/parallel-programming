import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('stats_cuda.csv')

sizes = df['Size'].unique()
block_sizes = sorted(df['BlockSize'].unique())

# График 1: Время от размера блока для каждого размера матрицы
plt.figure(figsize=(12, 6))
for size in sizes:
    data = df[df['Size'] == size]
    plt.plot(data['BlockSize'], data['Time_sec'], 'o-', linewidth=2, markersize=8, label=f'{size}x{size}')
plt.xlabel('Размер блока (threads per block)', fontsize=12)
plt.ylabel('Время выполнения (сек)', fontsize=12)
plt.title('CUDA: зависимость времени от размера блока', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('cuda_time_graph.png', dpi=150)
plt.show()

# График 2: Ускорение относительно блока 8x8
plt.figure(figsize=(12, 6))
for size in sizes:
    data = df[df['Size'] == size].sort_values('BlockSize')
    base_time = data[data['BlockSize'] == 8]['Time_sec'].values[0]
    speedups = [base_time / t for t in data['Time_sec']]
    plt.plot(data['BlockSize'], speedups, 's-', linewidth=2, markersize=8, label=f'{size}x{size}')

plt.plot([8, 32], [1, 4], 'k--', alpha=0.5, label='Идеальное масштабирование')
plt.xlabel('Размер блока', fontsize=12)
plt.ylabel('Ускорение (Speedup)', fontsize=12)
plt.title('CUDA: ускорение при увеличении размера блока', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('cuda_speedup_graph.png', dpi=150)
plt.show()

print("Графики сохранены: cuda_time_graph.png, cuda_speedup_graph.png")