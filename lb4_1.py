# Предметы: обозначение -> (размер в ячейках, очки выживания)
ITEMS = {
    'r': (3, 25),  # Винтовка
    'p': (2, 15),  # Пистолет
    'a': (2, 15),  # Боекомплект
    'm': (2, 20),  # Аптечка
    'i': (1, 5),   # Ингалятор (обязателен при астме)
    'k': (1, 15),  # Нож
    'x': (3, 20),  # Топор
    't': (1, 25),  # Оберег
    'f': (1, 15),  # Фляжка
    'd': (1, 10),  # Антидот
    's': (2, 20),  # Еда
    'c': (2, 20),  # Арбалет
}


def solve_knapsack(items, capacity, start_points, item0=None):
    total_points = sum(val for size, val in items.values())

    taken = []
    free_capacity = capacity
    other_items = []

    for code, (size, val) in items.items():
        if code == item0:
            taken.append(code)
            free_capacity -= size
        else:
            other_items.append((code, size, val))

    n = len(other_items)
    dp = [[0] * (free_capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        code, size, val = other_items[i - 1]
        for w in range(1, free_capacity + 1):
            if size <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - size] + val)
            else:
                dp[i][w] = dp[i - 1][w]

    w = free_capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            code, size, val = other_items[i - 1]
            taken.append(code)
            w -= size

    taken_points = sum(items[code][1] for code in taken)
    missed_points = total_points - taken_points
    final_score = start_points + taken_points - missed_points

    return taken, final_score

# Основное задание (8 ячеек, старт 20, обязателен 'i')
best_items, best_score = solve_knapsack(ITEMS, 8, 20, 'i')

cells = []
for code in best_items:
    size = ITEMS[code][0]
    for j in range(size):
        cells.append('[' + code + ']')

print(cells[0], cells[1], cells[2], cells[3], sep=',')
print(cells[4], cells[5], cells[6], cells[7], sep=',')
print('Итоговые очки выживания:', best_score)

# Допзадание (7 ячеек)
items_7, score_7 = solve_knapsack(ITEMS, 7, 20, 'i')
print('Максимум очков для 7 ячеек:', score_7)


