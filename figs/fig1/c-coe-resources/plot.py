import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.lines import Line2D


def _mm(x):
    return x / 25.4


BASE_FONTSIZE = 7.0
SMALL_FONTSIZE = 6.5

NATURE_RC = {
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
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    "grid.alpha": 0.25,
    "savefig.dpi": 600,
    "figure.dpi": 200,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.unicode_minus": False,
}

mpl.rcParams.update(NATURE_RC)


def set_y_headroom(ax, values, bottom=0.0, headroom=0.18):
    vmax = float(np.max(values)) if len(values) else 1.0
    ax.set_ylim(bottom, vmax * (1.0 + headroom))


# Data
models = ["ESM-C (600M)", "PGLM (1B)", "ProteinSage(650M)"]
tokens = [5.2, 1.0, 0.5]   # Training Tokens (T)
size = [2.4, 0.64, 0.14]   # Data Size (B sequences)
size_scale = 600
bubble_sizes = [(t + d) * size_scale for t, d in zip(tokens, size)]

fig, ax = plt.subplots(figsize=(_mm(60), _mm(55)))

cmap = plt.get_cmap("viridis")
vals = np.linspace(0, 1, len(models))
colors = [cmap(v) for v in vals]

ax.scatter(
    size,
    tokens,
    s=bubble_sizes,
    alpha=0.85,
    c=vals,
    cmap=cmap,
    edgecolors="black",
    linewidth=0.7,
    marker="o",
    zorder=2,
)
ax.set_xlabel("Data Size (B sequences)")
ax.set_ylabel("Training Tokens (T)")
ax.set_title("Reduction in Training Resources", pad=2)
ax.grid(True, linestyle="--", alpha=0.35)
ax.set_xlim(0, max(size) * 1.10)
set_y_headroom(ax, values=tokens, bottom=0.0, headroom=0.18)

legend_elements = [
    Line2D([0], [0], marker="o", color="w", label=label,
           markerfacecolor=c, markeredgecolor="black", markersize=6.5)
    for label, c in zip(models, colors)
]

lg = ax.legend(
    handles=legend_elements,
    title="Models",
    frameon=False,
    loc="upper left",
    bbox_to_anchor=(0.01, 0.97),
    borderaxespad=0.0,
    handlelength=1.4,
    handletextpad=0.6,
    columnspacing=0.8,
)
try:
    lg._legend_box.align = "left"
except Exception:
    pass

ax.text(-0.10, 1.03, "(c)", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=8, fontweight="bold")

plt.tight_layout()
out = "fig_c_coe_resources.png"
fig.savefig(out, dpi=600, transparent=True, bbox_inches="tight")
print(f"Saved {out}")
