from itertools import combinations


ITEMS = {
    'r': (3, 25),  # Винтовка
    'p': (2, 15),  # Пистолет
    'a': (2, 15),  # Боекомплект
    'm': (2, 20),  # Аптечка
    'i': (1, 5),   # Ингалятор 
    'k': (1, 15),  # Нож
    'x': (3, 20),  # Топор
    't': (1, 25),  # Оберег
    'f': (1, 15),  # Фляжка
    'd': (1, 10),  # Антидот
    's': (2, 20),  # Еда
    'c': (2, 20),  # Арбалет
}


def solve_knapsack(items, capacity, start_points, required_item=None):
    total_points = sum(val for size, val in items.values())

    taken = []
    free_capacity = capacity
    other_items = []

   
    for code, (size, val) in items.items():
        if code == required_item:
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


def print_inventory(taken, items, rows, cols):
  
    taken_sorted = sorted(taken, key=lambda code: items[code][0], reverse=True)

    cells = []
    for code in taken_sorted:
        size = items[code][0]
        for _ in range(size):
            cells.append(f'[{code}]')

    while len(cells) < rows * cols:
        cells.append('[ ]')

    for r in range(rows):
        row = cells[r * cols:(r + 1) * cols]
        print(','.join(row))


def find_all_positive(items, capacity, start_points, required_item=None):
    total_points = sum(val for size, val in items.values())
    other_codes = [code for code in items if code != required_item]

    req_size, req_val = items[required_item] if required_item else (0, 0)
    results = []

    for count in range(len(other_codes) + 1):
        for combo in combinations(other_codes, count):
            size = req_size + sum(items[c][0] for c in combo)
            if size <= capacity:
                taken_points = req_val + sum(items[c][1] for c in combo)
                score = start_points + taken_points - (total_points - taken_points)
                if score > 0:
                    full_set = ([required_item] if required_item else []) + list(combo)
                    results.append((full_set, score))

    return results


if __name__ == '__main__':

    rows, cols = 2, 4
    start_points = 20
    required = 'i'

    best_items, best_score = solve_knapsack(ITEMS, rows * cols, start_points, required)

    if best_score > 0:
        print('Оптимальный инвентарь (Вариант 5):')
        print_inventory(best_items, ITEMS, rows, cols)
        print(f'\nИтоговые очки выживания: {best_score}')
    else:
        print(f'Положительного решения нет (максимум: {best_score})')

    #Допзадание 1: инвентарь на 7 ячеек
    print('\n--- Допзадание: 7 ячеек ---')
    items_7, score_7 = solve_knapsack(ITEMS, 7, start_points, required)
    if score_7 > 0:
        print(f'Решение найдено: {items_7}, очки: {score_7}')
    else:
        print(f'Решения нет. Максимально возможный счёт для 7 ячеек: {score_7} (набор: {items_7})')

    #Допзадание 2: все комбинации с положительным счётом 
    print('\n--- Допзадание: все подходящие комбинации (8 ячеек) ---')
    all_solutions = find_all_positive(ITEMS, rows * cols, start_points, required)
    print(f'Всего найдено комбинаций: {len(all_solutions)}')
    for combo, score in all_solutions:
        print(f'{combo} -> очки: {score}')
