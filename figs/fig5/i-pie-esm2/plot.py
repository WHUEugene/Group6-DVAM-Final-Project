import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.patches import Patch


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


def lighten_color(hex_color, amount=0.62):
    rgb = np.array(mcolors.to_rgb(hex_color))
    white = np.array([1, 1, 1])
    return mcolors.to_hex(rgb + (white - rgb) * amount)


c_b = "#9FBAD5"  # ESM-2
pie = {
    "BR": 2984 - (79 + 258 + 71 + 83 + 102 + 443 + 152),
    "AU": 79,
    "BaxI_1": 258,
    "NrfD": 71,
    "Rcel-like": 83,
    "HeR": 102,
    "Other": 443,
    "Unknown": 152,
}

fig, ax = plt.subplots(figsize=(90 / 25.4, 90 / 25.4))

keys = list(pie.keys())
vals = np.array([pie[k] for k in keys], dtype=float)

cmap = {"BR": c_b}
other_keys = [k for k in keys if k != "BR"]
tab = list(mcolors.TABLEAU_COLORS.values())
for i, k in enumerate(other_keys):
    cmap[k] = lighten_color(tab[i % len(tab)], 0.35)

colors = [cmap[k] for k in keys]
explode = [0.06 if k == "BR" else 0.00 for k in keys]

ax.pie(
    vals,
    startangle=90,
    counterclock=False,
    colors=colors,
    explode=explode,
    wedgeprops=dict(linewidth=0.8, edgecolor="white"),
)
ax.set_title("ESM-2 (n=2984)", pad=6)

br = pie.get("BR", 0)
br_pct = br / vals.sum() * 100.0 if vals.sum() > 0 else 0.0
ax.text(0.0, -1.15, f"BR: {int(br)} ({br_pct:.1f}%)",
        ha="center", va="top", fontsize=10.2, fontweight="bold")

handles = [Patch(facecolor=cmap[k], edgecolor="white", label=f"{k}: {int(pie[k])}") for k in keys]
ax.legend(handles=handles, frameon=False, loc="center left",
          bbox_to_anchor=(1.02, 0.50), handletextpad=0.6, labelspacing=0.55)
ax.set_aspect("equal")

plt.tight_layout()
out = "fig5_i_pie_esm2.png"
fig.savefig(out, dpi=600, transparent=True)
print(f"Saved {out}")
