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

c_a = "#F7C98B"  # ProteinSage
c_b = "#9FBAD5"  # ESM-2

thr = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.95])
ps = np.array([0.5575920, 0.6851580, 0.7877230, 0.8544970, 0.8958770, 0.9181000])
esm = np.array([0.4675650, 0.5950760, 0.6894710, 0.7989300, 0.8185020, 0.8744510])

fig, ax = plt.subplots(figsize=(90 / 25.4, 70 / 25.4))
LINE_W = 2.0
MARKER_S = 4.8
MEW = 0.8

ax.plot(thr, ps, marker="o", markersize=MARKER_S, linewidth=LINE_W,
        color=c_a, markerfacecolor=c_a,
        markeredgecolor="white", markeredgewidth=MEW, label="ProteinSage")
ax.plot(thr, esm, marker="o", markersize=MARKER_S, linewidth=LINE_W,
        color=c_b, markerfacecolor=c_b,
        markeredgecolor="white", markeredgewidth=MEW, label="ESM-2")

ax.set_ylabel("ratio of 7tm")
ax.set_xlabel("Prediction threshold")
ax.set_xticks(thr)
ax.set_xticklabels([f"{t:g}" for t in thr])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.25)
ax.set_axisbelow(True)
ax.legend(loc="best", frameon=False)

# value labels
_, y1 = ax.get_ylim()
dy = (y1 - ax.get_ylim()[0]) * 0.04
for xi, yi in zip(thr, ps):
    ax.text(xi, yi + dy, f"{yi:.3f}", ha="center", va="bottom", fontsize=7.2)
for xi, yi in zip(thr, esm):
    ax.text(xi, yi + dy, f"{yi:.3f}", ha="center", va="bottom", fontsize=7.2)

plt.tight_layout()
out = "fig5_g_7tm_ratio.png"
fig.savefig(out, dpi=600, transparent=True)
print(f"Saved {out}")
