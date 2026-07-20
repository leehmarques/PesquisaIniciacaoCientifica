"""
Module for Generating NMF Predictions.

This script trains the NMF model and generates two final reports:
1. A complete spreadsheet with ALL combinations (Known and Unknown).
2. A filtered spreadsheet with ONLY UNKNOWN (new) associations.
It also includes the HLGT NAME category for each adverse reaction.
"""

import os
import numpy as np
import pandas as pd

from model import nmf_model as nmf

def generate_predictions_reports():
    """
    Loads data, trains the NMF model, calculates scores, and exports 
    two CSV files (All associations and Unknown only), adding the 
    HLGT NAME column and printing distinct reaction metrics.
    """
    
    csv_path = "data/fdalabel_with_meddra_hierarchy.csv"

    # 1. Data Loading
    try:
        df = pd.read_csv(csv_path)
        print("Dataset loaded successfully.")
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        return

    print("Constructing matrices and mappings...")

    # 2. Mapping PT to HLGT NAME
    pt_to_hlgt_df = df.drop_duplicates(subset=['PT'])[['PT', 'HLGT NAME']]
    pt_to_hlgt_map = dict(zip(pt_to_hlgt_df['PT'], pt_to_hlgt_df['HLGT NAME']))

    # 3. Matrix Construction
    matrix_A = pd.crosstab(df['TRADE NAME'], df['PT'])
    A = (matrix_A > 0).astype(float).values

    trade_names = np.array(matrix_A.index.tolist())
    pt_names = np.array(matrix_A.columns.tolist())

    matrix_Y = pd.crosstab(df['HLGT NAME'], df['PT'])
    Y = (matrix_Y > 0).astype(float).values

    print(f"Matrix A shape: {A.shape}")
    print(f"Matrix Y shape: {Y.shape}")

    # 4. Model Hyperparameters
    best_k = 10
    best_lambda = 0.0
    best_alpha = 1.0
    max_iter = 100

    # 5. NMF Model Training
    print("Training NMF model...")
    W, H, T, error_history = nmf.fit_nmf_with_y_reg(
        A, Y, best_k, max_iter, best_alpha, best_lambda
    )

    # Matrix P: The reconstructed prediction matrix (Raw Scores)
    P = W @ H

    # 6. Vectorization for ALL combinations
    m, n = A.shape
    
    all_trade_names = np.repeat(trade_names, n)
    all_pts = np.tile(pt_names, m)
    
    # Map the HLGT Names using our previously created dictionary
    all_hlgts = [pt_to_hlgt_map.get(pt, "UNKNOWN_HLGT") for pt in all_pts]

    all_raw_scores = P.flatten()
    is_known_by_fda = (A.flatten() > 0)

    # 7. Global Normalization
    score_min = all_raw_scores.min()
    score_max = all_raw_scores.max()
    
    if score_max > score_min:
        normalized_scores = 100 * (all_raw_scores - score_min) / (score_max - score_min)
    else:
        normalized_scores = np.zeros_like(all_raw_scores)

    # 8. Result DataFrame Construction
    print("Building DataFrames...")
    all_predictions_df = pd.DataFrame({
        "TRADE_NAME": all_trade_names,
        "ADVERSE_REACTION_PT": all_pts,
        "HLGT_NAME": all_hlgts,
        "KNOWN_BY_FDA": is_known_by_fda,
        "RAW_SCORE": all_raw_scores,
        "NORMALIZED_SCORE_0_100": np.round(normalized_scores, 2)
    })

    # Sort from strongest to weakest
    all_predictions_df = all_predictions_df.sort_values(by="RAW_SCORE", ascending=False)

    # Filter to create the UNKNOWN ONLY dataframe
    unknown_predictions_df = all_predictions_df[~all_predictions_df["KNOWN_BY_FDA"]]

    # 9. Results Export
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    all_output_path = os.path.join(output_dir, "all_associations_predictions.csv")
    unknown_output_path = os.path.join(output_dir, "unknown_associations_predictions.csv")

    print("Saving files...")
    all_predictions_df.to_csv(all_output_path, index=False, encoding="utf-8-sig")
    unknown_predictions_df.to_csv(unknown_output_path, index=False, encoding="utf-8-sig")

    # 10. Metrics Calculation and Console Report
    total_combinations = len(all_predictions_df)
    unknown_combinations = len(unknown_predictions_df)
    known_combinations = total_combinations - unknown_combinations

    # Distinct reactions metrics
    distinct_pts_total = all_predictions_df['ADVERSE_REACTION_PT'].nunique()

    print("\n" + "="*40)
    print("FINAL PREDICTION REPORT")
    print("="*40)
    print("\nFiles generated: ")
    print(f"1. {all_output_path}")
    print(f"2. {unknown_output_path}")

    print("\n--- METRICS ---")
    print(f"Total combinations analyzed: {total_combinations:,}")
    print(f"Total KNOWN associations:    {known_combinations:,}")
    print(f"Total UNKNOWN associations:  {unknown_combinations:,}")
    
    print(f"\nDistinct adverse reactions (Total):   {distinct_pts_total:,}")
    print("="*40 + "\n")

if __name__ == "__main__":
    generate_predictions_reports()