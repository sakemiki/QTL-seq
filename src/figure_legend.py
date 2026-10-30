# coding: UTF-8
import os
import sys


def build_legend_text(abulk_color, bbulk_color, delta_color, window_size, step_size):
    legend_text = (
        "Figure legend\n"
        f"{abulk_color} and {bbulk_color} dots represent the SNP-index values for the Abulk and "
        f"Bbulk bulks, respectively, and {delta_color} dots represent the ΔSNP-index "
        f"(Abulk − Bbulk) values from QTL-seq analysis. The red line indicates the sliding "
        f"window average calculated using a {window_size} bp window with a {step_size} bp step "
        f"interval. Light green and orange lines represent the 95% and 99% confidence intervals, "
        f"respectively, derived from simulation under the null hypothesis of random bulk sampling.\n"
    )
    return legend_text


def main(output_folder, abulk_color, bbulk_color, delta_color, window_size, step_size):
    legend_text = build_legend_text(abulk_color, bbulk_color, delta_color, window_size, step_size)

    output_path = os.path.join(output_folder, "figure_legend.txt")
    with open(output_path, "w") as f:
        f.write(legend_text)


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(
            "Usage: python figure_legend.py <output_folder> <abulk_color> <bbulk_color> "
            "<delta_color> <window_size> <step_size>"
        )
        sys.exit(1)

    main(
        sys.argv[1], sys.argv[2], sys.argv[3],
        sys.argv[4], sys.argv[5], sys.argv[6],
    )