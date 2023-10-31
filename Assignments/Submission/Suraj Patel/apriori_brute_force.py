
import time
import itertools
import random
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# read file function
def read_txt(file_name):
    content_file = [] # saving all content in this list
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 1) # splitting up the line according to written format
            number = int(parts[0]) # first is number of tranasction
            models = parts[1].split(', ') # rest is content sperated by comma
            content_file.append({number: models})
    return content_file

# function which takes in list of items and generate random transactions. At the end write it to file
def generate_transactions_and_write(item_list, upper_limit, file_path):
    if upper_limit > len(item_list): # just a check if I put in number which is greater than number of items in list. 
        print("Number of items is less than generation, try lesser number")
        return 
    transactions = []  # all transactions
    for i in range(1, 21):  # generating 20 transactions
        num_items = random.randint(1, upper_limit) # randomly choose a number for each trans
        chosen_items = random.sample(item_list, num_items) # sample the tiems randonly using the number
        transactions.append({i: chosen_items}) # adding it to list
    # Write the transactions to the file
    output_str = ""
    for transaction in transactions: # pre formatting to write in the file with format NUMBER itmes1, itmes2, etc.
        for key, value in transaction.items():
            output_str += str(key) + " " + ", ".join(value) + "\\n"
    with open(file_path, "w") as file: # writing to file
        file.write(output_str)
    return transactions

# function to print contents of transactions table
def print_transactions(transactions):
    print("\nTHIS IS TABLE CONTENTS\n")
    for transaction in transactions:
        for key, value in transaction.items():
            items_str = ", ".join(value)
            print(f"Transaction {key}: {items_str}")

# a function which is used to calcualte support for frequent itemset genrations
def get_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        items_in_transaction = list(transaction.values())[0] # get the transaction
        if set(itemset).issubset(set(items_in_transaction)): # check the transaction in itemset for counts
            count += 1 # increment count
    return count / len(transactions) # returnt the support

# Frequent Itemset Generator
def frequent_itemset_generator(transactions, min_support):
    frequent_itemsets = [] # list for frequent itemset
    items = set()
    # for loop to add transc items to the set. I made use of set approach for the pair like view.(a,b)
    
    for transaction in transactions:
        for item in list(transaction.values())[0]:
            items.add(item)

    
    # Generate 1-item itemsets
    k_itemsets = []
    for item in items:
        k_itemsets.append([item])

    # start generating 2 onwards item itemsets
    while k_itemsets:
        valid_itemsets = []
        for itemset in k_itemsets:
            support = get_support(itemset, transactions) # calcuating support for item
            if support >= min_support: # if the thershold passes, than they are valid itemset so we need to add it to valid_itemset
                valid_itemsets.append(itemset)
                frequent_itemsets.append((itemset, support))
        
        # Generate next level itemsets from current valid itemsets for the next k itemset
        next_level_itemsets = set()
        for combo in itertools.combinations(valid_itemsets, 2): # go over each combination two at a time
            possible_itemset = sorted(list(set(itertools.chain(*combo)))) # create itemset and using set removes duplicates
            if len(possible_itemset) == len(combo[0]) + 1: # basically check if it has one more itemset genrated. example from 2 tiemset to 3 itemset
                next_level_itemsets.add(tuple(possible_itemset)) # this is essentially an early stop mechanic,
        k_itemsets = [] # reset k_itemset for the next itemsets
        for itemset in next_level_itemsets: # if there isnt any k -itemset it will remain empty result in early stop
            k_itemsets.append(list(itemset)) # casting with list to keep up the format
    
    return frequent_itemsets # return the final frequent itemsets



#  A function to calculate confidence
def get_confidence(antecedent, consequent, transactions):
    antecedent_support = get_support(antecedent, transactions) # getting upper part of the formula
    both_support = get_support(antecedent + consequent, transactions) # this is lower part of the fomula 
    return both_support / antecedent_support # calculate confidence

# fucntion to generate assocaiton rules using frequent itemset generated.
def association_rule_generator(frequent_itemsets, transactions, min_confidence):
    rules = [] # all rules
    for itemset, support in frequent_itemsets: # go over the itemsets
        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i): # generate all possible combinations
                consequent = list(set(itemset) - set(antecedent)) # gets the consequent from the list
                confidence = get_confidence(list(antecedent), consequent, transactions) # gets the confidence
                if confidence >= min_confidence: # check the thershoold
                    rules.append((list(antecedent), consequent, support, confidence)) # save it to list
    return rules

# Function for apriori library
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
    print("\n This is APRIORI LIBRARY\n")
    print(rules_mlxtend)

# Function to call the frequent itmeset, and assocaiton rule. I used to minimize the calls. This function also prints the rules in the format
def execute_brute_force(items_data, min_support_value, min_confidence_value):
    frequent_itemsets = frequent_itemset_generator(items_data, min_support_value) # calling frequent_itemset_generator
    association_rules_ = association_rule_generator(frequent_itemsets, items_data, min_confidence_value) # calling association_rule_generator

    count = 0
    print("\n This is BRUTE FORCE\n")
    print("count Antecedent => Consequent\t support:, confidence:\n")
    for each_rule in association_rules_:
        print(f"{count}: {each_rule[0]} => {each_rule[1]} \t support: {each_rule[2]}, confidence: {each_rule[3]}")
        count += 1

#-------------------------------------------------------
# Time for executing
# below is the parameter to play with 
min_support = 0.1
min_confidence = 0.5
items_generate_per_trans = 7
# Table 1
print("-----------------------------------------------------------------------------")
print("Table 1")
electronic_file_path = "electronics_items.txt"
electronics_items = ['Digital Camera', 'Desktop', 'Printer', 'Xbox', 'Scanner', 'PS5', 'Nintendo Switch', 'Gaming Mouse', 'SDD', 'HDD']
electronics_items_data = generate_transactions_and_write(electronics_items, items_generate_per_trans, electronic_file_path)
print_transactions(electronics_items_data)
start_time_b = time.time()
execute_brute_force(electronics_items_data, min_support, min_confidence)
end_time_b = time.time()
start_time = time.time()
apriori_library(electronics_items_data, min_support, min_confidence)
end_time = time.time()
print("RUNTIME OF BRUTE FORCE: ", end_time_b - start_time_b)
print("RUNTIME OF APRIORI LIBRARY: ", end_time - start_time)

# Table 2
print("-----------------------------------------------------------------------------")
print("Table 2")
grocery_items = ['Milk', 'Bread', 'Eggs', 'Butter', 'Cheese','Tomatoes', 'Onions', 'Rice', 'Pasta', 'Chicken']
grocery_file_path = "grocery_items.txt"
grocery_items_data = generate_transactions_and_write(grocery_items, items_generate_per_trans, grocery_file_path)
print_transactions(grocery_items_data)
start_time_b = time.time()
execute_brute_force(grocery_items_data, min_support, min_confidence)
end_time_b = time.time()
start_time = time.time()
apriori_library(grocery_items_data, min_support, min_confidence)
end_time = time.time()
print("RUNTIME OF BRUTE FORCE: ", end_time_b - start_time_b)
print("RUNTIME OF APRIORI LIBRARY: ", end_time - start_time)

# Table 3
print("-----------------------------------------------------------------------------")
print("Table 3")
kmart_items = ['T-shirt', 'Cookware Set', 'Shoes', 'Toys', 'Bath Towels','Desk Lamp', 'Cushion', 'Curtains', 'Coffee Maker', 'Blanket']
kmart_items_file_path = "kmart_items.txt"
kmart_items_data = generate_transactions_and_write(kmart_items, items_generate_per_trans, kmart_items_file_path)
print_transactions(kmart_items_data)
start_time_b = time.time()
execute_brute_force(kmart_items_data, min_support, min_confidence)
end_time_b = time.time()
start_time = time.time()
apriori_library(kmart_items_data, min_support, min_confidence)
end_time = time.time()
print("RUNTIME OF BRUTE FORCE: ", end_time_b - start_time_b)
print("RUNTIME OF APRIORI LIBRARY: ", end_time - start_time)

# Table 4
print("-----------------------------------------------------------------------------")
print("Table 4")
flowers_items = ['Roses', 'Tulips', 'Daisies', 'Lilies', 'Sunflowers','Orchids', 'Carnations', 'Lavender', 'Chrysanthemums', 'Daffodils']
grocery_file_path = "flowers_items.txt"
flowers_items_data = generate_transactions_and_write(grocery_items, items_generate_per_trans, grocery_file_path)
print_transactions(flowers_items_data)
start_time_b = time.time()
execute_brute_force(flowers_items_data, min_support, min_confidence)
end_time_b = time.time()
start_time = time.time()
apriori_library(flowers_items_data, min_support, min_confidence)
end_time = time.time()
print("RUNTIME OF BRUTE FORCE: ", end_time_b - start_time_b)
print("RUNTIME OF APRIORI LIBRARY: ", end_time - start_time)

# Table 5
print("-----------------------------------------------------------------------------")
print("Table 5")
pets_items = ['Dog Food', 'Cat Litter', 'Bird Cage', 'Fish Tank', 'Pet Toys','Dog Leash', 'Cat Tree', 'Bird Seed', 'Aquarium Filter', 'Pet Bed']
pets_items_file_path = "pets_items.txt"
pets_items_data = generate_transactions_and_write(pets_items, items_generate_per_trans, pets_items_file_path)
print_transactions(pets_items_data)
start_time_b = time.time()
execute_brute_force(pets_items_data, min_support, min_confidence)
end_time_b = time.time()
start_time = time.time()
apriori_library(pets_items_data, min_support, min_confidence)
end_time = time.time()
print("RUNTIME OF BRUTE FORCE: ", end_time_b - start_time_b)
print("RUNTIME OF APRIORI LIBRARY: ", end_time - start_time)




