import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl


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
models = ["<1B", "7B", "13B"]
carbon = [8, 55, 76]    # tCO2e
water = [24, 252, 402]  # kL
x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(_mm(60), _mm(55)))

color_carbon = "#F9C7B8"
color_water = "#CFE7F3"

bar1 = ax.bar(
    x - width / 2,
    carbon,
    width,
    label="Carbon Emissions (tCO2e)",
    color=color_carbon,
    edgecolor="black",
    linewidth=0.6,
    zorder=2,
)
bar2 = ax.bar(
    x + width / 2,
    water,
    width,
    label="Water Consumption (kL)",
    color=color_water,
    edgecolor="black",
    linewidth=0.6,
    zorder=2,
)

for bars in (bar1, bar2):
    for b in bars:
        h = b.get_height()
        ax.annotate(
            f"{h}",
            (b.get_x() + b.get_width() / 2, h),
            xytext=(0, 1.5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=SMALL_FONTSIZE,
            clip_on=True,
        )

ax.set_xlabel("Model Scale")
ax.set_ylabel("Environmental Impact")
ax.set_title("Development Phase", pad=2)
ax.set_xticks(x, models)
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.legend(frameon=False, loc="upper left")

set_y_headroom(ax, values=np.r_[carbon, water], bottom=0.0, headroom=0.18)

ax.text(-0.10, 1.03, "(a)", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=8, fontweight="bold")

plt.tight_layout()
out = "fig_a_development.png"
fig.savefig(out, dpi=600, transparent=True, bbox_inches="tight")
print(f"Saved {out}")
