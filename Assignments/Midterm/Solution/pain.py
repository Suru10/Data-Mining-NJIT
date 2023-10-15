def read_txt(file_name):
    content_file = []
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 1)
            number = int(parts[0])
            models = parts[1].split(', ')
            content_file.append({number: models})
    return content_file

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

def corrected_brute_force_v2(data):
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

def calculate_support_adjusted(itemset, num_transactions, single_item_itemsets, two_item_itemsets):
    if len(itemset) == 1:
        return single_item_itemsets.get(itemset[0], 1e-9) / num_transactions
    elif len(itemset) == 2:
        return two_item_itemsets.get(itemset, 1e-9) / num_transactions
    return 1e-9

def generate_all_rules(data, tables, min_support, min_confidence):
    num_transactions = len(data)
    rules = []

    for table in tables:
        for itemset, count in table.items():
            if isinstance(itemset, tuple) and len(itemset) > 1:
                itemset_support = count / num_transactions
                for i in range(1, len(itemset)):
                    from itertools import combinations
                    for subset in combinations(itemset, i):
                        antecedent = tuple(subset)
                        consequent = tuple(sorted(set(itemset) - set(antecedent)))
                        
                        confidence = itemset_support / calculate_support_adjusted(antecedent, num_transactions, tables[0], tables[1])
                        if confidence >= min_confidence and itemset_support >= min_support:
                            rules.append((antecedent, consequent, itemset_support, confidence))
    return rules

# Execution
content = read_txt("transaction1.txt")
tables = corrected_brute_force_v2(content)
min_support_value = 0.1
min_confidence_value = 0.1
all_rules = generate_all_rules(content, tables, min_support_value, min_confidence_value)

# Print all the association rules
for rule in all_rules:
    antecedent, consequent, support, confidence = rule
    print(f"{antecedent} => {consequent} (Support: {support:.2f}, Confidence: {confidence:.2f})")
