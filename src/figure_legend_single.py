# coding: UTF-8
import os
import sys


def build_legend_text(abulk_color, window_size, step_size):
    legend_text = (
        "Figure legend\n"
        f"{abulk_color} dots represent the SNP-index values for the Abulk from QTL-seq "
        f"analysis. The red line indicates the sliding window average calculated using a "
        f"{window_size} bp window with a {step_size} bp step interval. Light green and "
        f"orange lines represent the 95% and 99% confidence intervals, respectively, derived "
        f"from simulation under the null hypothesis of random bulk sampling.\n"
    )
    return legend_text


def main(output_folder, abulk_color, window_size, step_size):
    legend_text = build_legend_text(abulk_color, window_size, step_size)

    output_path = os.path.join(output_folder, "figure_legend.txt")
    with open(output_path, "w") as f:
        f.write(legend_text)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python figure_legend.py <output_folder> <abulk_color> "
            "<window_size> <step_size>"
        )
        sys.exit(1)

    main(
        sys.argv[1], sys.argv[2], sys.argv[3],
        sys.argv[4]
    )