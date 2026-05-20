import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


def plot_accuracy_comparison(top_k_list,
                             results_by_lambda,
                             lambda_values,
                             latent_k):

    """
    Plots Top-K accuracy curves for different lambda values
    and displays the value of each point on the graph.
    """

    plt.figure(figsize=(10, 6))

    colors = ['red', 'blue', 'green', 'purple', 'orange']

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

        for x, y in zip(top_k_list, means):

            plt.annotate(
                f'{y:.2f}%',          
                (x, y),              
                textcoords="offset points",
                xytext=(0, 8 + idx*3), 
                ha='center',
                fontsize=8
            )

    plt.title(
        rf'Regularization Comparison ($K$={latent_k})',
        fontsize=14
    )

    plt.xlabel('Top-K', fontsize=12)
    plt.ylabel('Hit Rate (%)', fontsize=12)

    plt.xscale('log')

    plt.xticks(top_k_list, top_k_list)

    plt.ylim(0, 100)

    plt.yticks(np.arange(0, 101, 10))

    plt.grid(True, linestyle='--', alpha=0.6)

    plt.gca().yaxis.set_major_formatter(
        mticker.PercentFormatter()
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        'accuracy_comparison.png',
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()


def plot_error_convergence(error_curves_by_lambda,
                           lambda_values):

    """
    Plots Frobenius error convergence curves
    and displays the value of each point.
    """

    plt.figure(figsize=(10, 6))

    plt.title(
        r'Impact of $\lambda$ on Frobenius Error Convergence',
        fontsize=14
    )

    colors = ['red', 'blue', 'green', 'purple', 'orange']

    for idx, lmbd in enumerate(lambda_values):

        mean_error = error_curves_by_lambda[lmbd]

        plt.plot(
            mean_error,
            linewidth=2,
            color=colors[idx % len(colors)],
            label=rf'$\lambda$={lmbd}'
        )

        for x, y in enumerate(mean_error):

            plt.annotate(
                f'{y:.2f}',
                (x, y),
                textcoords="offset points",
                xytext=(0, 8 + idx*3),
                ha='center',
                fontsize=7
            )

    plt.xlabel('Iteration', fontsize=12)

    plt.ylabel('Frobenius Error', fontsize=12)

    plt.grid(True, linestyle='--', alpha=0.6)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        'error_convergence.png',
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()