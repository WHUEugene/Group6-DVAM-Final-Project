import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


BASE_FONTSIZE = 12.0
SMALL_FONTSIZE = 10.0

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "font.size": BASE_FONTSIZE,
    "axes.labelsize": BASE_FONTSIZE,
    "axes.titlesize": BASE_FONTSIZE,
    "legend.fontsize": SMALL_FONTSIZE,
    "xtick.labelsize": SMALL_FONTSIZE,
    "ytick.labelsize": SMALL_FONTSIZE,
    "axes.linewidth": 0.6,
    "lines.linewidth": 1.0,
    "patch.linewidth": 0.6,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    "grid.alpha": 0.25,
    "savefig.dpi": 600,
    "figure.dpi": 200,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.unicode_minus": False,
})

palette = {
    "ProteinSage": "#F7C98B",
    "ESM-2": "#9FBAD5",
    "cnn": "#F5B8B5",
    "transformer": "#B7D5C0",
    "attention": "#C7DCA7",
    "LSTM": "#9C73A7",
}


def soft_grid(ax):
    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.28)
    ax.set_axisbelow(True)


def set_adaptive_ylim(ax, values):
    vmin, vmax = min(values), max(values)
    span = vmax - vmin if vmax > vmin else 0.01
    ax.set_ylim(max(0.88, vmin - span * 0.15), 1.00)


def add_bar_labels(ax, xs, heights, fontsize=7.1):
    for x, v in zip(xs, heights):
        ax.text(x, v + 0.002, f"{v:.4f}",
                ha="center", va="bottom",
                fontsize=fontsize, clip_on=False)


models = ["ProteinSage", "ESM-2", "cnn", "transformer", "attention", "LSTM"]
f1 = [
    0.9286473510926831,
    0.9635827410956382,
    0.9172654390874615,
    0.9736541829076543,
    0.9481726539084715,
    0.9681726539084715,
]

fig, ax = plt.subplots(figsize=(80 / 25.4, 60 / 25.4))
xs = np.arange(len(models))
colors = [palette[m] for m in models]

ax.bar(xs, f1, width=0.72, color=colors, edgecolor="black", linewidth=0.9)
set_adaptive_ylim(ax, f1)
add_bar_labels(ax, xs, f1)
ax.set_xticks(xs, models, rotation=35, ha="right")
ax.set_title("F1-score")
ax.set_ylabel("F1-score")
soft_grid(ax)

plt.tight_layout()
out = "fig5_b_f1score.png"
fig.savefig(out, dpi=600, transparent=True)
print(f"Saved {out}")
