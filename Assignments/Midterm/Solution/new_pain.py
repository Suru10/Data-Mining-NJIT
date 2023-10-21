import random
from itertools import chain, combinations
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Function to read a text file and return its content
def read_txt(file_name):
    content_file = []
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 1)
            number = int(parts[0])
            models = parts[1].split(', ')
            content_file.append({number: models})
    return content_file

# Function to generate transactions and write them to a file
def generate_transactions_and_write(item_list, upper_limit, file_path):
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

# Function to get all combinations of a given size from a dictionary
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

# Function to generate frequent itemsets from transactions
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

# Helper function to generate non-empty subsets of an itemset
def subsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, _ in enumerate(itemset)])

# Function to generate association rules from frequent itemsets
def generate_rules(frequent_itemsets, min_support, min_confidence):
    rules = []
    num_transactions = 20  # since we're generating 20 transactions
    for itemset, support_count in frequent_itemsets.items():
        if isinstance(itemset, str):  # Skip 1-item itemsets
            continue
        support = support_count / num_transactions
        for antecedent in subsets(itemset):
            antecedent = tuple(antecedent)
            consequent = tuple(set(itemset) - set(antecedent))
            if not consequent:
                continue
            if antecedent not in frequent_itemsets:
                continue
            antecedent_support = frequent_itemsets[antecedent] / num_transactions
            confidence = support / antecedent_support
            if confidence >= min_confidence:
                rules.append({
                    'antecedent': antecedent,
                    'consequent': consequent,
                    'support': support,
                    'confidence': confidence
                })
    return rules
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
    rules = association_rules(frequent_itemsets ,metric="confidence", min_threshold=minimum_confidence)

    print(rules)

# Generate transactions and frequent itemsets
electronic_file_path = "electronics_transactions.txt"  # Update the path as needed
electronics_items = ['Digital Camera', 'Desktop', 'Printer', 'Xbox', 'Scanner', 'PS5', 'Nintendo Switch', 'Gaming Mouse', 'SDD', 'HDD']
electronics_items_data = generate_transactions_and_write(electronics_items, 5, electronic_file_path)

# Generate frequent itemsets
frequent_itemsets_data = frequent_itemset_generator(electronics_items_data)
frequent_itemsets = {}
for table in frequent_itemsets_data:
    frequent_itemsets.update(table)

# Define min_support and min_confidence values and generate association rules
min_support = 0.1  # 10% of transactions
min_confidence = 0.6
rules = generate_rules(frequent_itemsets, min_support, min_confidence)
count = 0
for each_rule in rules:
    print(count)
    print(each_rule)
    count += 1
print("\n length", len(rules))

apriori_library(electronic_file_path, min_support, min_confidence)



