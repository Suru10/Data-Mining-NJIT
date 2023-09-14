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

def get_combinations(dictionary_data, combination_size):
    keys = list(dictionary_data.keys())

    # Check if combination_size is valid
    if combination_size <= 0 or combination_size > len(keys):
        return []

    # Initialize an empty list to store combinations
    combinations_list = []

    # Helper function to generate combinations recursively
    def generate_combinations(current_combination, remaining_keys, size):
        if size == 0:
            combinations_list.append(tuple(current_combination))
            return

        for i in range(len(remaining_keys)):
            new_combination = current_combination + [remaining_keys[i]]
            generate_combinations(new_combination, remaining_keys[i + 1:], size - 1)

    generate_combinations([], keys, combination_size)

    return combinations_list



def brute_force(data):
    i = 0
    flag = True
    tables = []
    while flag:
        current_trans = 1
        tables.append({})
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
        i += 1 
        if i == 1:
            flag = False
        
        print(tables[i-1])
        comb = get_combinations(tables[i-1], 2)
        print(comb)

    

# Print the content list
content = read_txt("transaction1.txt")
print(content)
brute_force(content)

