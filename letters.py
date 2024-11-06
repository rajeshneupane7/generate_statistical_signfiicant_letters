import string
import pandas as pd

def get_letters(df):
    df_True = df[df['reject'] == True]
    letters = list(string.ascii_lowercase)
    n = 0

    # Get unique groups from the True dataframe
    group1_list = df_True['group1'].tolist()
    group2_list = df_True['group2'].tolist()
    unique_groups = sorted(set(group1_list + group2_list))
    
    # Initialize dictionary with default values
    dictionary = {group: '' for group in unique_groups}
    
    # Generate all unique pairs of groups
    all_pairs = [(unique_groups[i], unique_groups[j]) for i in range(len(unique_groups)) for j in range(i+1, len(unique_groups))]
    
    for pair in all_pairs:
        group1, group2 = pair
        # Check if the pair exists in df_True
        pair_exists = not df_True[(df_True['group1'] == group1) & (df_True['group2'] == group2)].empty

        # Handle "equal" case where pair does not exist in df_True
        if not pair_exists:
            if dictionary[group1] and not dictionary[group2]:
                dictionary[group2] = dictionary[group1]
            elif dictionary[group1] and dictionary[group2]:
                if any(char in dictionary[group2] for char in dictionary[group1]):
                    continue  # No need to change if they share a character
                dictionary[group2] += dictionary[group1][0]
            else:
                dictionary[group1] = letters[n]
                dictionary[group2] = letters[n]
                n += 1
        else:
            # Handle "not equal" case where pair exists in df_True
            if dictionary[group1]:
                if dictionary[group2] and not any(char in dictionary[group2] for char in dictionary[group1]):
                    continue  # No need to change if they already have different labels
                elif not dictionary[group2]:
                    dictionary[group2] = letters[n]
                    n += 1
            else:
                dictionary[group1] = letters[n]
                dictionary[group2] = letters[n + 1]
                n += 2

    # Remove duplicate characters for each group and return sorted dictionary
    for key in dictionary:
        dictionary[key] = ''.join(sorted(set(dictionary[key])))

    return dict(sorted(dictionary.items()))

# Example usage (assuming df_tukey_speed is a DataFrame with 'group1', 'group2', and 'reject' columns):
# result = get_letters(df_tukey_speed)
