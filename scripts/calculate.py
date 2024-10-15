from itertools import combinations
import pandas as pd
from deuces import Card, Evaluator
import time
import logging
import random
from multiprocessing import Pool, cpu_count
import concurrent.futures

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_all_in_ev_full_enumeration(hand1, hand2, sample_percentage=100):
    evaluator = Evaluator()

    all_cards = set(Card.new(rank + suit) for rank in '23456789TJQKA' for suit in 'shdc')

    remaining_cards = all_cards - set(hand1 + hand2)

    needed_cards = 5
    wins_hand1 = 0
    wins_hand2 = 0
    ties = 0
    total_combinations = 0

    all_combinations = list(combinations(remaining_cards, needed_cards))

    # Випадковий вибір комбінацій на основі sample_percentage
    if sample_percentage < 100:
        sample_size = int(len(all_combinations) * sample_percentage / 100)
        if sample_size > 0:
            all_combinations = random.sample(all_combinations, sample_size)

    for combination in all_combinations:
        final_board = list(combination)

        score1 = evaluator.evaluate(hand1, final_board)
        score2 = evaluator.evaluate(hand2, final_board)

        if score1 < score2:
            wins_hand1 += 1
        elif score1 > score2:
            wins_hand2 += 1
        else:
            ties += 1

        total_combinations += 1

    ev_hand1 = (wins_hand1 + ties / 2) / total_combinations

    return ev_hand1


def process_row(row_data):
    idx, row, sample_percentage = row_data
    first_hand = [Card.new(card) for card in row['First'].split()]
    second_hand = [Card.new(card) for card in row['Second'].split()]

    # Обчислення еквіті повним перебором або за випадковими комбінаціями
    ev_hand = calculate_all_in_ev_full_enumeration(first_hand, second_hand, sample_percentage)

    return idx, ev_hand


def main(max_iterations=None, sample_percentage=100):
    start_time = time.time()

    input_path = './input.xlsx'
    output_path = './output.xlsx'
    df = pd.read_excel(input_path)

    rows_to_process = df[df['Equity'].isna()]
    rows_to_process = rows_to_process.reset_index(drop=True)

    if max_iterations:
        rows_to_process = rows_to_process.head(max_iterations)

    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        results = list(
            executor.map(process_row, [(idx, row, sample_percentage) for idx, row in rows_to_process.iterrows()]))

    for idx, ev_hand in results:
        df.at[idx, 'Equity'] = ev_hand

    df.to_excel(output_path, index=False)

    elapsed_time = time.time() - start_time
    logging.info(f'Скрипт завершено за {elapsed_time:.2f} секунд (або {elapsed_time / 60:.2f} хвилин).')


if __name__ == "__main__":
    main(max_iterations=None, sample_percentage=100)
