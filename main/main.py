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
from collections import defaultdict

from model import nmf_model as nmf
from visualization import graphics_nmf_model as viz

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
    print("Starting data processing and NMF pipeline...")

    try:
        df = pd.read_csv('fdalabel_base_completa.csv')
        print("CSV file loaded successfully.")
    except FileNotFoundError:
        print("Error: File 'fdalabel_base_completa.csv' not found. Please check the path.")
        return

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
    alpha_val = 1.0

    lambda_test_values = [0.0, 0.001, 0.01, 0.1, 1.0]

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

if __name__ == "__main__":
    main()