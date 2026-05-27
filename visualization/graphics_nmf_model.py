import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

def plot_accuracy_comparison(top_k_list,
                             results_by_lambda,
                             lambda_values,
                             latent_k,
                             output_dir="data"):
    """
    Plots Top-K accuracy curves for different lambda values
    and generates a clean data table below the graph.
    """
    
    plt.figure(figsize=(10, 7))

    colors = ['red', 'blue', 'green', 'purple', 'orange']
    
    cell_text = []
    row_labels = []

    for idx, lmbd in enumerate(lambda_values):
        means = [results_by_lambda[lmbd][tk] for tk in top_k_list]

        plt.plot(
            top_k_list,
            means,
            marker='o',
            linestyle='-',
            linewidth=2,
            color=colors[idx % len(colors)],
            label=rf'$\lambda$={lmbd}'
        )

        row_labels.append(rf'$\lambda$={lmbd}')
        cell_text.append([f'{y:.2f}%' for y in means])

    plt.title(rf'Regularization Comparison ($K$={latent_k})', fontsize=14)
    plt.xlabel('Top-K', fontsize=12)
    plt.ylabel('Hit Rate (%)', fontsize=12)
    plt.xscale('log')
    plt.xticks(top_k_list, top_k_list)
    plt.ylim(0, 100)
    plt.yticks(np.arange(0, 101, 10))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter())
    plt.legend()

    plt.subplots_adjust(bottom=0.35)

    tabela = plt.table(
        cellText=cell_text,
        rowLabels=row_labels,
        colLabels=[f'Top-{tk}' for tk in top_k_list],
        cellLoc='center',
        loc='bottom',
        bbox=[0.0, -0.45, 1.0, 0.3]
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'accuracy_comparison.png')
    
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_error_convergence(error_curves_by_lambda,
                           lambda_values,
                           output_dir="data"):
    """
    Plots Frobenius error convergence curves.
    Text annotations are removed to prevent visual clutter across 100+ iterations.
    """
    plt.figure(figsize=(10, 6))
    plt.title(r'Impact of $\lambda$ on Frobenius Error Convergence', fontsize=14)

    colors = ['red', 'blue', 'green', 'purple', 'orange']

    for idx, lmbd in enumerate(lambda_values):
        mean_error = error_curves_by_lambda[lmbd]

        plt.plot(
            mean_error,
            linewidth=2,
            color=colors[idx % len(colors)],
            label=rf'$\lambda$={lmbd}'
        )

    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Frobenius Error', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'error_convergence.png')
    
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.show()