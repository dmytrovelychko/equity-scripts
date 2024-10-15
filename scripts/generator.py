import pandas as pd
from itertools import combinations

# Визначимо значення номіналу кожної карти
card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
               '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
suits = ['d', 's', 'h', 'c']
deck = [f'{rank}{suit}' for rank in card_values for suit in suits]

# Всі можливі комбінації карт для 2 гравців
player_combinations = list(combinations(deck, 2))

# Унікальні пари гравців, незалежно від їх порядку
unique_pairs = set()

for p1 in player_combinations:
    remaining_deck = [card for card in deck if card not in p1]
    for p2 in combinations(remaining_deck, 2):
        # Створюємо пару гравців, де порядок гравців не має значення
        sorted_p1 = tuple(sorted(p1, key=lambda x: -card_values[x[0]]))
        sorted_p2 = tuple(sorted(p2, key=lambda x: -card_values[x[0]]))

        # Сортуємо пари гравців незалежно від порядку
        if sorted_p1 > sorted_p2:
            pair = (sorted_p1, sorted_p2)
        else:
            pair = (sorted_p2, sorted_p1)

        unique_pairs.add(pair)

# Функція для визначення, чи схожі масті карт (s - так, o - ні)
def suited_indicator(cards):
    return 's' if cards[0][1] == cards[1][1] else 'o'

# Функція для створення назви руки (наприклад, AKo)
def hand_name(cards):
    ranks = ''.join(sorted([cards[0][0], cards[1][0]], key=lambda x: -card_values[x]))
    return f"{ranks}{suited_indicator(cards)}"

# Функція для перевірки схожості мастей між картами різних гравців
def is_suited(card1, card2):
    return card1[1] == card2[1]

# Перетворимо результати в DataFrame
data = [{'First': ' '.join(pair[0]),
         'Second': ' '.join(pair[1]),
         'A': hand_name(pair[0]),
         'B': hand_name(pair[1]),
         'C': 's' if is_suited(pair[0][0], pair[1][0]) else 'o',
         'D': 's' if is_suited(pair[0][0], pair[1][1]) else 'o',
         'E': 's' if is_suited(pair[0][1], pair[1][0]) else 'o',
         'F': 's' if is_suited(pair[0][1], pair[1][1]) else 'o',
         'Player 1 Value': sum(card_values[card[0]] for card in pair[0]),
         'Player 2 Value': sum(card_values[card[0]] for card in pair[1])}
        for pair in unique_pairs]

df = pd.DataFrame(data)

# Відсортуємо DataFrame за сумарним номіналом гравця 1, а потім гравця 2
df = df.sort_values(by=['Player 1 Value', 'Player 2 Value'], ascending=False)

# Видалимо колонки 'Player 1 Value' і 'Player 2 Value' перед збереженням
df = df.drop(columns=['Player 1 Value', 'Player 2 Value'])

# Записуємо DataFrame у файл Excel
df.to_excel('D:\\Poker\\Documents\\Evolution\\Two_players_equity.xlsx', index=False)

print(f"Results saved")


