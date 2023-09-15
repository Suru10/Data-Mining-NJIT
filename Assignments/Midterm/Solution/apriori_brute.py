def read_txt(file_name):
    content_file = []
    # Open the file for reading
    with open(file_name, 'r') as file:
        for line in file:
            # Split each line into two parts: the number and iPhone models
            parts = line.strip().split(' ', 1)
            
            # Extract the number and iPhone models
            number = int(parts[0])
            models = parts[1].split(', ')
            
            # Create a dictionary for the current line and append it to the content list
            content_file.append({number: models})
    return content_file

# def get_combinations(dictionary_data, combination_size):
#     keys = list(dictionary_data.keys())

#     # Check if combination_size is valid
#     if combination_size <= 0 or combination_size > len(keys):
#         return []

#     # Initialize an empty list to store combinations
#     combinations_list = []

#     # Helper function to generate combinations recursively
#     def generate_combinations(current_combination, remaining_keys, size):
#         if size == 0:
#             combinations_list.append(tuple(current_combination))
#             return

#         for i in range(len(remaining_keys)):
#             new_combination = current_combination + [remaining_keys[i]]
#             generate_combinations(new_combination, remaining_keys[i + 1:], size - 1)

#     generate_combinations([], keys, combination_size)

#     return combinations_list

def get_combinations(dictionary_data, combination_size):
    keys = list(dictionary_data.keys())

    # Check if combination_size is valid
    if combination_size <= 0 or combination_size > len(keys):
        return []

    # Initialize an empty list to store combinations
    combinations_list = []

    # Helper function to generate combinations recursively
    def generate_combinations(current_combination, start_index, size):
        if size == 0:
            combinations_list.append(tuple(current_combination))
            return

        for i in range(start_index, len(keys)):
            new_combination = current_combination + [keys[i]]
            generate_combinations(new_combination, i + 1, size - 1)

    generate_combinations([], 0, combination_size)

    return combinations_list



def brute_force(data):
    i = 0
    flag = True
    tables = []
    while flag:
        current_trans = 1
        tables.append({})
        if i == 0:
            for trans in data:
                # Check if the current transaction number exists in the dictionary
                if current_trans in trans:
                    number = tuple(trans[current_trans])  # Convert the list to a tuple
                    # Increment the count for the current number in the current table
                    for item in number:
                        if item in tables[i]:
                            tables[i][item] += 1
                        else:
                            tables[i][item] = 1

                current_trans += 1
        comb = get_combinations(tables[0], i + 1)
        

        if i > 0:
            
            tables.append({})
            for each_comb in comb:
                
                current_trans = 1
                for trans in data:
                    previous_item_tracker = True
                    
                    transaction_numbers = trans.keys()  # Get the keys (transaction numbers) in the current trans
                    if current_trans not in transaction_numbers:
                        continue  # Skip this transaction if current_trans doesn't exist in the keys
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
        print(i)
        print("\nTables", tables[i-1])
        print('\n')
        
      

    

# Print the content list
content = read_txt("transaction1.txt")
print(content)
brute_force(content)

