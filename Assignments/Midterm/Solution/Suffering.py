import random
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def read_txt(file_name):
    content_file = []
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 1)
            number = int(parts[0])
            models = parts[1].split(', ')
            content_file.append({number: models})
    return content_file
def generate_transactions_and_write(item_list, upper_limit, file_path):
    """
    Generate transactions based on a given item list and an upper limit for each transaction.
    Then, write the generated transactions to a file.
    
    Parameters:
    - item_list (list): List of items to choose from.
    - upper_limit (int): Maximum number of items in each transaction.
    - file_path (str): Path to the file where transactions should be written.
    
    Returns:
    - transactions (list): List of generated transactions.
    """
    if upper_limit > len(item_list):
        raise ValueError(f"Upper limit {upper_limit} is greater than the number of unique items in the list {len(item_list)}")
    
    transactions = []
    for i in range(1, 21):  # generating 20 transactions
        num_items = random.randint(1, upper_limit)
        chosen_items = random.sample(item_list, num_items)
        transactions.append({i: chosen_items})
    
    # Write the transactions to the file
    output_str = ""
    for transaction in transactions:
        for key, value in transaction.items():
            output_str += str(key) + " " + ", ".join(value) + "\n"

    with open(file_path, "w") as file:
        file.write(output_str)
    
    return transactions

def print_transactions(transactions):
    """
    Print transactions in a nicely formatted manner.
    
    Parameters:
    - transactions (list): List of generated transactions.
    """
    for transaction in transactions:
        for key, value in transaction.items():
            items_str = ", ".join(value)
            print(f"Transaction {key}: {items_str}")


def get_combinations(dictionary_data, combination_size):
    keys = list(dictionary_data.keys())
    if combination_size <= 0 or combination_size > len(keys):
        return []
    combinations_list = []

    def generate_combinations(current_combination, start_index, size):
        if size == 0:
            combinations_list.append(tuple(current_combination))
            return
        for i in range(start_index, len(keys)):
            new_combination = current_combination + [keys[i]]
            generate_combinations(new_combination, i + 1, size - 1)

    generate_combinations([], 0, combination_size)
    return combinations_list

def frequent_itemset_generator(data):
    i = 0
    flag = True
    tables = []
    while flag:
        current_trans = 1
        tables.append({})
        comb = get_combinations(tables[0], i + 1)
        if i == 0:
            for trans in data:
                if current_trans in trans:
                    number = tuple(trans[current_trans])
                    for item in number:
                        if item in tables[i]:
                            tables[i][item] += 1
                        else:
                            tables[i][item] = 1
                current_trans += 1
        else:
            for each_comb in comb:
                current_trans = 1
                for trans in data:
                    previous_item_tracker = True
                    transaction_numbers = trans.keys()
                    if current_trans not in transaction_numbers:
                        continue
                    for item in each_comb:
                        if (item in trans[current_trans]) and (previous_item_tracker):
                            previous_item_tracker = True
                        else:
                            previous_item_tracker = False
                    if previous_item_tracker:
                        if each_comb in tables[i]:
                            tables[i][each_comb] += 1
                        else:
                            tables[i][each_comb] = 1
                    current_trans += 1
        i += 1 
        if i == 10:
            flag = False
    return tables


def calculate_support_adjusted(itemset, num_transactions, tables):
    itemset_size = len(itemset)
    relevant_table = tables[itemset_size - 1]
    return relevant_table.get(itemset, 0) / num_transactions

def generate_all_rules(data, tables, min_support, min_confidence):
    num_transactions = len(data)
    rules = []
  
    for table in tables:
        for itemset, count in table.items():
            if isinstance(itemset, tuple) and len(itemset) > 1:
                itemset_support = count / num_transactions
                # Loop through all possible sizes of antecedents
                for i in range(1, len(itemset)):
                    from itertools import combinations
                    for subset in combinations(itemset, i):
                        antecedent = tuple(subset)
                        consequent = tuple(sorted(set(itemset) - set(antecedent)))
                        
                        
                        confidence_support = calculate_support_adjusted(antecedent, num_transactions, tables)
                        if confidence_support == 0:
                            continue
                        else:
                            confidence = itemset_support / calculate_support_adjusted(antecedent, num_transactions, tables)
                            if confidence >= min_confidence and itemset_support >= min_support:
                                rules.append((antecedent, consequent, itemset_support, confidence))
   
    return rules
# Apriori
def apriori_library(file_path, minimum_support, minimum_confidence):
    with open(file_path, 'r') as f:
        transactions = [line.strip().split() for line in f.readlines()]

    # Cleaning the data: Removing transaction IDs and trailing commas from item names
    cleaned_transactions = [ [item.replace(',', '') for item in transaction[1:]] for transaction in transactions]

    # Convert the transactions into a one-hot encoded DataFrame
    items = sorted(list(set(item for transaction in cleaned_transactions for item in transaction)))
    oht = pd.DataFrame([[item in transaction for item in items] for transaction in cleaned_transactions], columns=items)

    # Apply the Apriori algorithm
    frequent_itemsets = apriori(oht, min_support=minimum_support, use_colnames=True)

    # Generate association rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=minimum_confidence)

    print(rules)

def execute_brute_force(file_path, min_support_value, min_confidence_value):
    # Execution
    content = read_txt(file_path)
    tables = frequent_itemset_generator(content)
    # min_support_value = 0.1
    # min_confidence_value = 0.1
    all_rules = generate_all_rules(content, tables, min_support_value, min_confidence_value)

    # Print all the association rules
    count = 0
    for rule in all_rules:
        antecedent, consequent, support, confidence = rule
        print(f"{count} {antecedent} => {consequent} (Support: {support:.2f}, Confidence: {confidence:.2f})")
        count += 1






# Testing the function with writing capability
electronic_file_path = "electronics_items.txt"
electronics_items = ['Digital Camera', 'Desktop', 'Printer', 'Xbox', 'Scanner', 'PS5', 'Nintendo Switch', 'Gaming Mouse', 'SDD', 'HDD']
electronics_items_data = generate_transactions_and_write(electronics_items, 5, electronic_file_path)
print_transactions(electronics_items_data)
execute_brute_force(electronic_file_path, 0.3, 0.0)
apriori_library(electronic_file_path, 0.0000001, 0.0)