import itertools
import random
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Data Generation and Reading Functions
# Data Generation and Reading Functions
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
            output_str += str(key) + " " + ", ".join(value) + "\\n"
    with open(file_path, "w") as file:
        file.write(output_str)
    return transactions


# Frequent Itemset Generator
# Frequent Itemset Generator
def get_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        items_in_transaction = list(transaction.values())[0]
        if set(itemset).issubset(set(items_in_transaction)):
            count += 1
    return count / len(transactions)


def frequent_itemset_generator(transactions, min_support):
    frequent_itemsets = []
    items = set(item for transaction in transactions for item in list(transaction.values())[0])
    
    # Generate 1-item itemsets
    k_itemsets = [[item] for item in items]
    
    while k_itemsets:
        valid_itemsets = []
        for itemset in k_itemsets:
            support = get_support(itemset, transactions)
            if support >= min_support:
                valid_itemsets.append(itemset)
                frequent_itemsets.append((itemset, support))
        
        # Generate next level itemsets from current valid itemsets
        next_level_itemsets = set()
        for combo in itertools.combinations(valid_itemsets, 2):
            possible_itemset = sorted(list(set(itertools.chain(*combo))))
            if len(possible_itemset) == len(combo[0]) + 1:
                next_level_itemsets.add(tuple(possible_itemset))
        k_itemsets = []
        for itemset in next_level_itemsets:
            k_itemsets.append(list(itemset))
    
    return frequent_itemsets


# Association Rule Generator
# Association Rule Generator
def get_confidence(antecedent, consequent, transactions):
    antecedent_support = get_support(antecedent, transactions)
    both_support = get_support(antecedent + consequent, transactions)
    return both_support / antecedent_support


def association_rule_generator(frequent_itemsets, transactions, min_confidence):
    rules = []
    for itemset, support in frequent_itemsets:
        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                consequent = list(set(itemset) - set(antecedent))
                confidence = get_confidence(list(antecedent), consequent, transactions)
                if confidence >= min_confidence:
                    rules.append((list(antecedent), consequent, support, confidence))
    return rules
def apriori_library(electronics_items_data, minimum_support, minimum_confidence):
    # Extracting items from the transactions
    transactions = []
    for transaction in electronics_items_data:
        transaction_values = list(transaction.values())
        first_value = transaction_values[0]
        transactions.append(first_value)

    # Transforming data into one-hot encoded DataFrame
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Generating frequent itemsets
    frequent_itemsets_mlxtend = apriori(df, min_support=minimum_support, use_colnames=True)

    # Generating association rules
    rules_mlxtend = association_rules(frequent_itemsets_mlxtend, metric="confidence", min_threshold=minimum_confidence)

    # Displaying the rules
    print(rules_mlxtend)

# Sample Execution
electronics_items = ['Digital Camera', 'Desktop', 'Printer', 'Xbox', 'Scanner', 'PS5', 'Nintendo Switch', 'Gaming Mouse', 'SDD', 'HDD']
electronic_file_path = "electronics_transactions.txt"
electronics_items_data = generate_transactions_and_write(electronics_items, 5, electronic_file_path)
min_support = 0.1
frequent_itemsets = frequent_itemset_generator(electronics_items_data, min_support)
min_confidence = 0.5
association_rules_ = association_rule_generator(frequent_itemsets, electronics_items_data, min_confidence)
# print(len(association_rules))
count = 0
for each_rule in association_rules_:
    print(count)
    print(each_rule)
    count += 1
apriori_library(electronics_items_data, min_support, min_confidence)





