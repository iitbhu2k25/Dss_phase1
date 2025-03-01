import pandas as pd
import numpy as np

def normalize_columns(list_of_dicts):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(list_of_dicts)
    print("Original DataFrame:")
    print(df)
    # Create a copy for normalization
    normalized_df = df.copy()
    # Process each column
    for column in df.columns:
        # Check if column contains non-numeric values
        if df[column].dtype == 'object' or not pd.to_numeric(df[column], errors='ignore').dtype.kind in 'if':
            print(f"\nWarning: Column '{column}' contains non-numeric values. Skipping normalization for this column.")
            normalized_df[column] = df[column]  # Keep original values
        else:
            # Normalize numeric columns
            min_val = df[column].min()
            max_val = df[column].max()
            if min_val == max_val:
                print(f"\nWarning: Column '{column}' has constant values. Setting normalized values to 1.")
                normalized_df[column] = 1
            else:
                normalized_df[column] = (df[column] - min_val) / (max_val - min_val)
    
    # Convert back to list of dictionaries
    normalized_list = normalized_df.to_dict('records')

    print(normalized_df)

    print(normalized_list)
    
    return normalized_list, normalized_df