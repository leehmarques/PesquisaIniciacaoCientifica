import numpy as np

def initialize_w_h_t(A, m, n, r, k):
    """
    Initializes W, H, and T matrices using a uniform distribution scaled by 
    the mean value of the matrix A to prevent absolute zeros.
    """
    avg = np.sqrt(A.mean() / k) if A.mean() > 0 else 0.001
    W = np.random.uniform(0, avg, (m, k))
    H = np.random.uniform(0, avg, (k, n))
    T = np.random.uniform(0, avg, (r, k))
    return W, H, T

def fit_nmf_with_y_reg(A_bin, Y, k, max_iter, alpha=1.0, lambda_reg=0.01):
    """
    Performs Non-negative Matrix Factorization with joint learning on Y 
    and regularization.
    """
    m, n = A_bin.shape
    r, n = Y.shape
    W, H, T = initialize_w_h_t(A_bin, m, n, r, k)
    eps = 1e-9

    error_history = []

    for i in range(max_iter):
        # Multiplicative update for H (including Y guidance and regularization)
        numerator_H = (W.T @ A_bin) + alpha * (T.T @ Y) + eps
        denominator_H = (W.T @ W @ H) + alpha * (T.T @ T @ H) + (lambda_reg * H) + eps
        H *= numerator_H / denominator_H

        # Multiplicative update for W (with regularization)
        numerator_W = A_bin @ H.T + eps
        denominator_W = W @ (H @ H.T) + (lambda_reg * W) + eps
        W *= numerator_W / denominator_W

        # Multiplicative update for T (with regularization)
        numerator_T = alpha * (Y @ H.T) + eps
        denominator_T = alpha * (T @ (H @ H.T)) + (lambda_reg * T) + eps
        T *= numerator_T / denominator_T

        # Calculate the Frobenius error of the reconstruction of matrix A
        current_error = np.linalg.norm(A_bin - (W @ H), 'fro')
        error_history.append(current_error)

    return W, H, T, error_history

def leave_one_out_topk(A, Y, k, max_iter, top_k_list, num_tests_desired, alpha, lambda_reg):
    """
    Evaluates the model using Leave-One-Out cross-validation on true positive interactions.
    """
    m, n = A.shape
    results = {topk: 0 for topk in top_k_list}
    test_errors = []
    
    # Identify positions where interactions exist (A == 1)
    positive_positions = list(zip(*np.where(A == 1)))
    total_available = len(positive_positions)
    num_tests = min(num_tests_desired, total_available)

    # Randomly select positions to leave out
    chosen_indices = np.random.choice(total_available, num_tests, replace=False)
    test_positions = [positive_positions[i] for i in chosen_indices]

    for idx, (i, j) in enumerate(test_positions):
        # Hide the true positive link
        A_mod = A.copy()
        A_mod[i, j] = 0

        # Fit the model on the modified matrix
        W, H, T, errors = fit_nmf_with_y_reg(A_mod, Y, k, max_iter, alpha, lambda_reg)
        test_errors.append(errors)

        # Compute predictions
        pred = W @ H
        pred_row = pred[i, :].copy()

        # Penalize other known positives to focus on evaluating the hidden item
        other_positives = np.where(A[i, :] == 1)[0]
        true_other_positives = other_positives[other_positives != j]
        pred_row[true_other_positives] = -np.inf

        # Rank predictions in descending order
        ranking = np.argsort(-pred_row)

        # Check hit rate for each top-K threshold
        for tk in top_k_list:
            if j in ranking[:tk]:
                results[tk] += 1

    results_percentage = {tk: (count / num_tests) * 100 for tk, count in results.items()}

    return results_percentage, test_errors