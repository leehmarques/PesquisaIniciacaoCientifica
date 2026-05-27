"""
Module for Data Enrichment with MedDRA Hierarchy.

This module takes the filtered FDA adverse reactions dataset and merges it 
with MedDRA mapping files (HLT, HLGT) to add hierarchical codes and names,
reordering the columns for better readability.
"""

import pandas as pd
import os

def standardize_columns(df):
    """
    Strips whitespace and converts column names to uppercase 
    to prevent merge errors due to inconsistent formatting.
    """
    df.columns = df.columns.str.strip().str.upper()
    return df

def enrich_with_meddra(df_fda, data_dir="data"):
    """
    Merges HLT and HLGT codes and names into the FDA dataset,
    and reorders the columns to group MedDRA terminology together.
    """
    df_hlt_pt = pd.read_csv(os.path.join(data_dir, 'hlt_pt.csv'))
    df_hlt_name = pd.read_csv(os.path.join(data_dir, 'hlt_name.csv'))
    df_hlgt_hlt = pd.read_csv(os.path.join(data_dir, 'hlgt_hlt.csv'))
    df_hlgt_name = pd.read_csv(os.path.join(data_dir, 'hlgt_name.csv'))

    df_fda = standardize_columns(df_fda)
    df_hlt_pt = standardize_columns(df_hlt_pt)
    df_hlt_name = standardize_columns(df_hlt_name)
    
    df_hlgt_hlt = standardize_columns(df_hlgt_hlt)
    df_hlgt_hlt.columns = ['HLGT CODE', 'HLT CODE']
    
    df_hlgt_name = standardize_columns(df_hlgt_name)
    df_hlgt_name.columns = ['HLGT CODE', 'HLGT NAME']

    df_merged = pd.merge(df_fda, df_hlt_pt[['PT CODE', 'HLT CODE']], on='PT CODE', how='left')

    df_merged = pd.merge(df_merged, df_hlt_name[['HLT CODE', 'HLT NAME']], on='HLT CODE', how='left')

    df_merged = pd.merge(df_merged, df_hlgt_hlt[['HLT CODE', 'HLGT CODE']], on='HLT CODE', how='left')

    df_merged = pd.merge(df_merged, df_hlgt_name[['HLGT CODE', 'HLGT NAME']], on='HLGT CODE', how='left')

    
    meddra_group = ['PT', 'PT CODE', 'HLT NAME', 'HLT CODE', 'HLGT NAME', 'HLGT CODE']
    
    all_cols = df_merged.columns.tolist()
    
    other_cols = [col for col in all_cols if col not in meddra_group]
    
    if 'LLT CODE' in other_cols:
        insert_idx = other_cols.index('LLT CODE') + 1
    else:
        insert_idx = len(other_cols) 
        
    final_column_order = other_cols[:insert_idx] + meddra_group + other_cols[insert_idx:]
    
    df_final = df_merged[final_column_order]
    
    return df_final

def save_data(df, output_folder, filename):
    """
    Saves the enriched dataframe as a CSV file in the specified folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, filename)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"File '{file_path}' saved successfully!")

# Main execution block
if __name__ == "__main__":
    print("Starting MedDRA data enrichment process...")
    
    data_directory = "data"
    input_fda_file = os.path.join(data_directory, 'fdalabel.csv') 
    output_file = 'fdalabel_with_meddra_hierarchy.csv' 
    
    try:
        print("Loading filtered FDA data...")
        df_base = pd.read_csv(input_fda_file)
        
        print("Enriching dataset with HLT and HLGT hierarchies and names...")
        df_enriched = enrich_with_meddra(df_base, data_dir=data_directory)
        
        print("Saving the enriched dataset...")
        save_data(df_enriched, output_folder=data_directory, filename=output_file)
        
        print("Enrichment completed successfully! The dataset is ready for the NMF model.")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file. Details: {e}")
        print("Make sure 'fdalabel.csv' and all MedDRA CSVs are inside the 'data/' folder.")