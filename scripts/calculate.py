import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import time

logging.info("Waiting for db container up...")
time.sleep(5)

from itertools import combinations
import pandas as pd
from deuces import Card, Evaluator
import time
import random
from multiprocessing import Pool, cpu_count
import concurrent.futures
import db

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

    if db.is_record_exists(row['First'], row['Second']):
        logging.info(f'{idx:.2f} - Skip')
        return

    first_hand = [Card.new(card) for card in row['First'].split()]
    second_hand = [Card.new(card) for card in row['Second'].split()]
    ev_hand = calculate_all_in_ev_full_enumeration(first_hand, second_hand, sample_percentage)

    db.insert(row['First'], row['Second'], row['A'], row['B'], row['C'], row['D'], row['E'], row['F'], row['Concat'], str(ev_hand))

    logging.info(f'{idx:.2f} Calculated')


def main(max_iterations=None, sample_percentage=100):
    logging.info(f'Start')
    start_time = time.time()

    input_path = './input.xlsx'
    output_path = './output.xlsx'
    df = pd.read_excel(input_path)

    rows_to_process = df[df['Equity'].isna()]
    rows_to_process = rows_to_process.reset_index(drop=True)

    if max_iterations:
        rows_to_process = rows_to_process.head(max_iterations)

    logging.info(f'Executing...')

    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count() - 1) as executor:
        executor.map(process_row, [(idx, row, sample_percentage) for idx, row in rows_to_process.iterrows()])

    elapsed_time = time.time() - start_time
    logging.info(f'equity calculation took {elapsed_time:.2f} sec or {elapsed_time / 60:.2f} min')

    logging.info(f'Saving results...')
    result_df = db.sql_to_dataframe()

    result_df.to_excel(output_path, index=False)


if __name__ == "__main__":
    main(max_iterations=None, sample_percentage=100)
