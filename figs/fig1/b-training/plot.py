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
models = ["60M", "150M", "300M", "700M", "1B (3T)"]
carbon = [0.4, 1.0, 2.0, 3.0, 10.0]
water = [1.8, 3.9, 6.2, 12.0, 42.0]
size_scale = 80
sizes = [(c + w) * size_scale for c, w in zip(carbon, water)]

fig, ax = plt.subplots(figsize=(_mm(60), _mm(55)))

vals = np.linspace(0, 1, len(models))
cmap = plt.get_cmap("Spectral")
colors = [cmap(v) for v in vals]

ax.scatter(
    carbon,
    water,
    s=sizes,
    alpha=0.85,
    c=vals,
    cmap=cmap,
    edgecolors="black",
    linewidth=0.7,
    marker="o",
    zorder=2,
)
ax.set_xlabel("Carbon Emissions (tCO2e)")
ax.set_ylabel("Water Consumption (kL)")
ax.set_title("Training Phase", pad=2)
ax.grid(True, linestyle="--", alpha=0.35)
ax.set_xlim(0, max(carbon) * 1.05)
set_y_headroom(ax, values=water, bottom=0.0, headroom=0.18)

legend_elements = [
    Line2D([0], [0], marker="o", color="w", label=label,
           markerfacecolor=c, markeredgecolor="black", markersize=6.5)
    for label, c in zip(models, colors)
]
ax.legend(handles=legend_elements, title="Models", frameon=False, loc="upper left")

ax.text(-0.10, 1.03, "(b)", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=8, fontweight="bold")

plt.tight_layout()
out = "fig_b_training.png"
fig.savefig(out, dpi=600, transparent=True, bbox_inches="tight")
print(f"Saved {out}")
