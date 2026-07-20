"""
Main Module for Non-Negative Matrix Factorization (NMF) Evaluation.

This script acts as the orchestrator for the NMF experiment, applying 
regularization and evaluating performance through a 
Leave-One-Out cross-validation approach. 

It imports the mathematical logic from `nmf_model` and the plotting 
functions from `graphics_nmf_model`.
"""

import numpy as np
import pandas as pd
import os
from collections import defaultdict

from model import nmf_model as nmf
from visualization import graphics_nmf_model as viz
from processing import processing_fda_data as proc

def main():
    """
    Main execution pipeline for the NMF experiment.
    
    Workflow:
    1. Loads the FDA adverse reactions dataset.
    2. Constructs the binary interaction matrix A (Trade Name x PT) 
       and the guidance matrix Y (HLGT Name x PT).
    3. Iterates over predefined lambda regularization values and 
       evaluates the model's Top-K accuracy using Leave-One-Out validation.
    4. Compiles the metrics and generates visual performance reports.
    """
    csv_path = "data/fdalabel_with_meddra_hierarchy.csv"

    if not os.path.exists(csv_path):

        print("\nDatabase not found.")
        print("Generating FDA database automatically...")

        df_raw = proc.download_fda_data()

        if df_raw.empty:
            print("Error: Failed to download FDA data.")
            return

        df_cleaned = proc.filter_adverse_reactions(df_raw)

        proc.save_data(df_cleaned, csv_path)

        print("Database generated successfully.\n")

    df = pd.read_csv(csv_path)

    print("CSV file loaded successfully.")

    # Matrix A: Interaction between Trade Names and Preferred Terms (PT)
    matrix_A = pd.crosstab(df['TRADE NAME'], df['PT']) 
    A = (matrix_A > 0).astype(float).values 
    m, n = A.shape

    # Matrix Y: MedDRA hierarchy guidance (HLGT Name x PT)
    matrix_Y = pd.crosstab(df['HLGT NAME'], df['PT']) 
    Y = (matrix_Y > 0).astype(float).values 
    r, _ = Y.shape

    print(f"Generated Dimensions -> Matrix A: {A.shape} | Matrix Y: {Y.shape}")

    latent_k_list = [10]
    max_iter = 100
    evaluate_top_k = [1, 3, 5, 10, 20, 50, 100]
    num_tests = 100
    experiment_repetitions = 100
    # lambda_test_values = [0.0, 0.001, 0.01, 0.1, 1.0]
    
    alpha_val = 1.0
    lambda_test_values = [0.0]

    results_by_lambda = {}
    error_curves_by_lambda = {}

    for lmbd in lambda_test_values:
        print(f"\n--- Evaluating model with Lambda = {lmbd} ---")
        
        results_lmbd = defaultdict(list)
        errors_lmbd = []

        for k in latent_k_list:
            for rep in range(experiment_repetitions):
                print(f"  Progress: Repetition {rep+1}/{experiment_repetitions}", end="\r")

                rates, loo_errors = nmf.leave_one_out_topk(
                    A, Y, k,
                    max_iter,
                    evaluate_top_k,
                    num_tests_desired=num_tests,
                    alpha=alpha_val,
                    lambda_reg=lmbd
                )

                for tk in evaluate_top_k:
                    results_lmbd[tk].append(rates[tk])
                
                errors_lmbd.extend(loo_errors)

        mean_lambda_results = {tk: np.mean(results_lmbd[tk]) for tk in evaluate_top_k}
        results_by_lambda[lmbd] = mean_lambda_results
        
        error_curves_by_lambda[lmbd] = np.mean(errors_lmbd, axis=0)

        console_summary = " | ".join([f"Top-{tk}: {mean_lambda_results[tk]:.1f}%" for tk in evaluate_top_k])
        print(f"\n  Mean Results -> {console_summary}")


    print("\nGenerating evaluation plots with detailed annotations...")
    
    viz.plot_accuracy_comparison(
        top_k_list=evaluate_top_k, 
        results_by_lambda=results_by_lambda, 
        lambda_values=lambda_test_values, 
        latent_k=latent_k_list[0]
    )
    
    viz.plot_error_convergence(
        error_curves_by_lambda=error_curves_by_lambda, 
        lambda_values=lambda_test_values
    )
    
    print("Process finished! High-resolution plots have been saved to the current directory.")

    # EXPORTING DATA FOR STREAMLIT
    os.makedirs("results", exist_ok=True)
    
    reference_lambda = 0.0 
    
    if reference_lambda in results_by_lambda:
        topk_results = results_by_lambda[reference_lambda]
        df_topk = pd.DataFrame({
            'Top_K': evaluate_top_k,
            'Accuracy_Percentage': [topk_results[tk] * 100 for tk in evaluate_top_k]
        })
        df_topk.to_csv("results/topk_accuracy.csv", index=False)
        
        convergence_errors = error_curves_by_lambda[reference_lambda]
        df_error = pd.DataFrame({
            'Iteration': range(1, len(convergence_errors) + 1),
            'MSE_Error': convergence_errors
        })
        df_error.to_csv("results/convergence_error.csv", index=False)
        
        print(" -> 'results/topk_accuracy.csv' saved successfully!")
        print(" -> 'results/convergence_error.csv' saved successfully!")

if __name__ == "__main__":
    main()