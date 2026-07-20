from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


def set_plot_style():
    """
    Set a consistent plotting style for the project.
    """

    sns.set_theme(
        style="whitegrid",
        palette="Set2",
        font_scale=1.1,
    )

    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["figure.dpi"] = 120


def save_plot(output_dir: Path, filename: str):
    """
    Save the current matplotlib figure.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()

    plt.savefig(
        output_dir / filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def print_heading(title: str):
    """
    Print formatted console headings.
    """

    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)